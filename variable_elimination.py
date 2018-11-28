import xmlparser
from exact_inference import *


def normalize(dist):
    result = []
    s = sum(dist)
    for i in range(len(dist)):
        result.append(dist[i] / s)
    return result


def to_observed_pair(x):
    return [x.lower(), '!' + x.lower()]


def parent_es(variable, data):
    result = []
    for prob in data.keys():
        if variable == prob.fore:
            result.append(prob.given)
    return result


def valid_query(data, var):
    for prob in data.keys():
        if prob.fore == var.lower() and not var.startswith('!'):
            return True
    return False


# B     E
#    A
# j     m
#
# A -> B -> E -> j -> m
def elimination_ask(query, variables, evidences, data, parents):
    factors = []
    rest_variables = variables
    while len(rest_variables) > 0:
        var = rest_variables[0]
        print('->', var, rest_variables)
        rest_variables, factor = make_factor(var, rest_variables, evidences, data, parents)
        if var != query and var.lower() not in evidences and '!' + var.lower() not in evidences:
            factors.append(factor)
            print('before sum_out', factors)
            factors = sum_out(var, factors, rest_variables)
            print('after  sum_out', factors)
    query_pos = query.lower()
    query_neg = '!' + query.lower()
    # print(factors)
    return normalize([factors[0][1][frozenset(set(query_pos))], factors[0][1][frozenset({query_neg})]])


def make_factor(var, variables, evidences, data, parents):
    related = related_vars(var, variables + evidences, data)
    # rest_variables = [i for i in variables if i not in related]
    rest_variables = variables[1:]
    tag = set([i for i in related if i.isupper()])
    for r in related:
        tag |= {i for i in given_vars(r, variables, data) if i.isupper()}
    tag.remove(var)
    cp_table = {}
    cpt(var, tag, related, variables, evidences, data, parents, cp_table)
    # print('𝜓(' + ', '.join(tag) + ')', '=', cp_table)
    return rest_variables, ({var} | tag, cp_table)


# B     E
#    A
# j     m
def cpt(var, tag, related_fores, variables, evidences, data, parents, result):
    for t in tag:
        if t.isupper():
            tmp_tag = tag.copy()
            tmp_tag.remove(t)
            cpt(var, tmp_tag | {t.lower()}, related_fores, variables, evidences, data, parents, result)
            cpt(var, tmp_tag | {'!' + t.lower()}, related_fores, variables, evidences, data, parents, result)
            return
    if var.isupper():
        cpt(var.lower(), tag, related_fores, variables, evidences, data, parents, result)
        cpt('!' + var.lower(), tag, related_fores, variables, evidences, data, parents, result)
    else:
        p = 1
        for fore in related_fores:
            if fore.lower() == var.strip('!'):
                fore = var
            elif fore.isupper():
                new_related = set(related_fores)
                new_related.remove(fore)
                cpt(var, tag, list(new_related) + [fore.lower()], variables, evidences, data, parents, result)
                cpt(var, tag, list(new_related) + ['!' + fore.lower()], variables, evidences, data, parents, result)
                return
            # print(fore, '|', [var] + list(tag) + evidences, '=', xmlparser.Prob(fore, parents, data, [var] + list(tag) + evidences))
            p *= xmlparser.Prob(fore, parents, data, [var] + list(tag) + evidences)
        result[frozenset({var} | tag)] = p
        # print('result[', frozenset({var} | tag), '] = ', p)
    return


def sum_out(var, factors, variables):
    result = []
    focused_factors = []
    for factor in factors:
        tag, cp_table = factor
        if var in tag:
            focused_factors.append(factor)
        else:
            result.append(factor)
    for factor in pointwise_product(focused_factors, variables):
        tag, cp_table = factor
        new_tag = tag
        new_tag.remove(var)
        events = []
        all_events(list(new_tag), events)
        table = {}
        for e in events:
            table[frozenset(e)] = cp_table[frozenset(set(e) | {var.lower()})] + cp_table[frozenset(set(e) | {'!' + var.lower()})]
        result.append((new_tag, table))
    return result


def all_events(variables, result):
    for v in variables:
        if v.isupper():
            tmp_variables = variables.copy()
            tmp_variables.remove(v)
            all_events(tmp_variables + [v.lower()], result)
            all_events(tmp_variables + ['!' + v.lower()], result)
            return
    result.append(variables)


def pointwise_product(factors, variables):
    table = {}
    vars = set()
    for factor in factors:
        vars |= factor[0]
    events = []
    all_events(list(vars), events)
    for event in events:
        p = 1
        for factor in factors:
            tag, cp_table = factor
            es = set()
            for e in event:
                if e.strip('!').upper() in tag:
                    es.add(e)
            p *= cp_table[frozenset(es)]
        table[frozenset(set(event))] = p
    return [(vars, table)]


def get_variables(query, evidences, data):
    variables = set()
    for prob in data.keys():
        v = prob.fore
        if not v.startswith('!') and v != query.lower():
            if v in evidences:
                variables.add(v)
            else:
                variables.add(v.upper())
    return list(variables)


def related_vars(variable, variables, data):
    related = set()
    var = variable.lower()
    for prob in data.keys():
        if var == prob.fore or var in prob.given:
            # data structure should be improved
            for v in variables:
                if v.lower() == prob.fore:
                    related.add(v)
    return list(related)


def given_vars(variable, variables, data):
    variables_set = set(variables)
    given = set()
    for prob in data.keys():
        if variable.lower() in prob.fore:
            for g in prob.given:
                if g in variables_set:
                    given.add(g)
                elif g.upper() in variables_set:
                    given.add(g.upper())
    return given


_data, _parents = xmlparser.readdata('aima-alarm.xml')
_query = 'B'
_evidences = ['j', 'm']
print(elimination_ask(_query, ['E', 'A', _query], _evidences, _data, _parents))
# print(related_vars('A', ['A', 'E', 'B', 'j', 'm'], _data))
