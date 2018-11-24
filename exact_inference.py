from xmlparser import *
import sys

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


def enumerate_ask(query, variables, evidences, data):
    if valid_query(data, query):
        query_true, query_false = to_observed_pair(query)
        return normalize([enumerate_all(variables + [query_true], evidences + [query_true], data),
                          enumerate_all(variables + [query_false], evidences + [query_false], data)])


def enumerate_all(variables, evidences, data):
    if len(variables) == 0:
        return 1

    first = variables[0]
    if first in evidences:
        for parent_e in parent_es(first, data):
            if parent_e.issubset(evidences):
                return data[Probability(first, parent_e)] * enumerate_all(variables[1:], evidences, data)
    else:
        true_var, false_var = to_observed_pair(first)
        # parent_es on true_var and false_var always return same result
        for parent_e in parent_es(true_var, data):
            if parent_e.issubset(evidences):
                return data[Probability(true_var, parent_e)] * enumerate_all(variables[1:], evidences + [true_var],
                                                                             data) + \
                       data[Probability(false_var, parent_e)] * enumerate_all(variables[1:], evidences + [false_var],
                                                                              data)

    return enumerate_all(variables[1:] + [variables[0]], evidences, data)


def get_variables(query, evidences, data):
    variables = set()
    for prob in data.keys():
        v = prob.fore
        if not v.startswith('!') and v != query.lower():
            if v in evidences:
                variables.add(v)
            elif '!' + v in evidences:
                variables.add('!' + v)
            else:
                variables.add(v.upper())
    return list(variables)


# _data, _parents = readdata('aima-alarm.xml')
# _query = 'A'
# _evidences = ['!e', 'j', '!b', 'm']
# print(enumerate_ask(_query, get_variables(_query, _evidences, _data), _evidences, _data))
if __name__ == '__main__':
    sys.argv.pop(0)
    _data, _parents = readdata(sys.argv[0])
    _query = sys.argv[1]
    _evidences = []
    for i in range(2, len(sys.argv)):
        if i % 2 == 0:
            e = sys.argv[i]
            if sys.argv[i + 1] == 'true':
                _evidences.append(e.lower())
            elif sys.argv[i + 1] == 'fasle':
                _evidences.append('!' + e.lower())
            else:
                exit('invalid input')
    print(enumerate_ask(_query, get_variables(_query, _evidences, _data), _evidences, _data))
