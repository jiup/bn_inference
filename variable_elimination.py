import test
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


def make_factor(var, variables, evidences, data):
    related = related_vars(var, variables, data)
    rest_variables = [i for i in variables if i not in related]
    tag = set(related)
    for r in related:
        tag |= {i for i in given_vars(r, variables, data) if i.isupper()}
    tag.remove(var)
    cp_table = []
    cpt((tag | {var}), related, variables, data, cp_table)
    print('𝜓' + tag.__str__(), '=', cp_table)
    return rest_variables, (tag, cp_table)


# {{a, b} => 0.71,...}
def cpt(tag, related_fores, variables, data, result):
    for t in tag:
        if t.isupper():
            tmp_tag = tag.copy()
            tmp_tag.remove(t)
            cpt(tmp_tag | {t.lower()}, related_fores, variables, data, result)
            cpt(tmp_tag | {'!' + t.lower()}, related_fores, variables, data, result)
            return
    p = 1
    for fore in related_fores:
        given = set()
        given_v = given_vars(fore, variables, data)
        for t in tag:
            gs = given_v
            if t.startswith('!') and t[1:] in gs or t[1:].upper() in gs:
                given.add(t)
            elif t in gs or t.upper() in gs:
                given.add(t)
        if fore.isupper():
            if fore.lower() in tag:
                p *= data[Probability(fore.lower(), given)]
            elif '!' + fore.lower() in tag:
                p *= data[Probability('!' + fore.lower(), given)]
        else:
            p *= data[Probability(fore, given)]
    result.append({frozenset(tag): p})
    return


def sum_out(var, variables, factors, data):
    pass


def pointwise_product(factors, variables):
    pass


def elimination_ask(query, variables, evidences, data):
    factors = []
    rest_variables = variables.copy()
    while len(rest_variables) > 0:
        print('->', rest_variables)
        # related = related_vars(var, variables, data)
        # rest_variables = [i for i in variables if i not in related]
        # if var.lower() != query and var.lower() not in evidences:

        rest_variables, factor = make_factor(rest_variables[0], rest_variables, evidences, data)
        factors.append(factor)
        #     factors.add(sum_out(var, variables, factors, data))
    return
    # return normalize(pointwise_product(factors, variables))


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
            # TODO: this search can be improved
            # print(prob)
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


_data = test.readdata('aima-alarm.xml')
_query = 'B'
_evidences = ['j', 'm']
# print(enumerate_ask(_query, get_variables(_query, _evidences, _data), _evidences, _data))
# print(get_variables(_query, _evidences, _data))
# for var in get_variables(_query, _evidences, _data):
#     print(parent_es(var, _data))
# for key in _data.keys():
#     print(key)
# print(related_vars('a', get_variables(_query, _evidences, _data), _data))
elimination_ask(_query, ['E', 'A', _query], _evidences, _data)
