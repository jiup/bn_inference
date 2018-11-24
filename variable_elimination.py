import test
from exact_inference import *
from test import Probability


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


def elimination_ask(query, variables, evidences, data, parents):
    factors = []
    rest_variables = variables
    while len(rest_variables) > 0:
        var = rest_variables[0]
        print('->', rest_variables)
        rest_variables, factor = make_factor(var, rest_variables, evidences, data, parents)
        if len(factor[0]) > 0:
            factors.append(factor)
        # if var != query and var.lower() not in evidences:
        #     factors = sum_out(var, factors)
    # print(factors)
    return
    # return normalize(pointwise_product(factors, variables))


def make_factor(var, variables, evidences, data, parents):
    related = related_vars(var, variables + evidences, data)
    rest_variables = [i for i in variables if i not in related]
    tag = set([i for i in related if i.isupper()])
    for r in related:
        tag |= {i for i in given_vars(r, variables, data) if i.isupper()}
    tag.remove(var)
    cp_table = {}
    cpt(var, tag, related, variables, evidences, data, parents, cp_table)
    print('𝜓(' + ', '.join(tag) + ')', '=', cp_table)
    return rest_variables, (tag, cp_table)


def cpt(var, tag, related_fores, variables, evidences,  data, parents, result):
    for t in tag:
        if t.isupper():
            tmp_tag = tag.copy()
            tmp_tag.remove(t)
            cpt(var, tmp_tag | {t.lower()}, related_fores, variables, evidences, data, parents, result)
            cpt(var, tmp_tag | {'!' + t.lower()}, related_fores, variables, evidences, data, parents, result)
            return
    if var.isupper():
        obs_var = [var.lower(), '!' + var.lower()]
    else:
        obs_var = [var]
    prob = 0
    # print(var, tag, related_fores, variables, evidences)
    for v in obs_var:
        p = 1
        for fore in related_fores:
            if fore == var:
                fore = v
            p *= test.Prob(fore, parents, data, [v] + list(tag) + evidences)
            #print([v] + list(tag) + evidences, fore, '|', parents[fore], '=', test.Prob(fore, parents, data, [v] + list(tag) + evidences))
        # print('multiplied =', p)
        prob += p
    result[frozenset(tag)] = prob
    return


def sum_out(var, factors):
    result = []
    var_true = var.lower()
    var_false = '!' + var.lower()
    print(factors)
    for factor in factors:
        tag, cp_table = factor
        if var in tag:
            print(var, tag)
            new_tag = tag
            new_tag.remove(var)
            events = []
            all_events(list(new_tag), events)
            table = {}
            for e in events:
                print(set(e) | {var_true}, cp_table)
                table[frozenset(e)] = cp_table[frozenset(set(e) | {var_true})] + cp_table[frozenset(set(e) | {var_false})]
            result.append((new_tag, table))
        else:
            result.append(factor)
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
    pass


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


_data, _parents = test.readdata('aima-alarm.xml')
_query = 'B'
_evidences = ['j', 'm']
# print(enumerate_ask(_query, get_variables(_query, _evidences, _data), _evidences, _data))
# print(get_variables(_query, _evidences, _data))
# for var in get_variables(_query, _evidences, _data):
#     print(parent_es(var, _data))
# for key in _data.keys():
#     print(key)
# print(related_vars('a', get_variables(_query, _evidences, _data), _data))
elimination_ask(_query, ['A', 'E', _query], _evidences, _data, _parents)
# print(related_vars('A', ['A', 'E', 'B', 'j', 'm'], _data))
