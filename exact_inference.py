import test
from test import Probability


def normalize(dist):
    result = []
    s = sum(dist)
    if s == 0:
        return [0] * len(dist)
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


def enumerate_ask(query, variables, evidences, data):
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
                return data[Probability(true_var, parent_e)] * enumerate_all(variables[1:], evidences + [true_var], data) + \
                       data[Probability(false_var, parent_e)] * enumerate_all(variables[1:], evidences + [false_var], data)
    return 0


path = 'aima-alarm.xml'
data = test.readdata(path)
print(enumerate_ask('B', ['E', 'A', 'j', 'm'], ['j', 'm'], data))
