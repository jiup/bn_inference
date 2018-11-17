import random
from exact_inference import *
import sys
import test


def in_e(a, evidence):
    a = a.lower()
    for e in evidence:
        if a == e:
            return 2
        elif ('!' + a == e or a.strip('!') == e) and (a != e):
            return 3
    return 1


def get_parents(var, bn):
    result = set()
    for key in bn.keys():
        if key.fore == var:
            for given in key.given:
                result.add(given)
    return result


def gibbs_sampling(X, e, bn, parents, N):
    result = {X.lower(): 0, '!' + X.lower(): 0}
    sample = set()
    for k in bn.keys():
        if in_e(k.fore, e) == 1:
            sample.add(k.fore.strip('!').upper())
    sample = list(sample)
    for i in range(len(sample)):
        rand_p = random.uniform(0, 1)
        if rand_p > 0.5:
            sample[i] = sample[i].lower()
        else:
            sample[i] = '!' + sample[i].lower()
    tmp = sample + list(e)
    for j in range(N):
        for i in range(len(sample)):
            rand_p = random.uniform(0, 1)
            children = set()
            for keys in bn.keys():
                if sample[i] in keys.given:
                    children.add(keys.fore)
            children = children & set(tmp)
            parent = get_parents(sample[i], bn) & set(tmp)
            children_parent = set()
            for child in children:
                children_parent = children_parent | (get_parents(child, bn) & set(tmp))
            enumerate_e = (parent | children | children_parent) - {sample[i]}
            p = enumerate_ask(sample[i].strip('!').upper(),
                              get_variables(sample[i].strip('!').upper(), list(enumerate_e), bn), list(enumerate_e), bn)
            if rand_p < p[0]:
                sample[i] = sample[i].strip('!')
            else:
                sample[i] = sample[i].strip('!')
                sample[i] = '!' + sample[i]
            tmp = sample + list(e)
        if X.lower() in sample:
            result[X.lower()] += 1
        elif '!' + X.lower() in sample:
            result['!' + X.lower()] += 1

    result = normalize([result[X.lower()], result['!' + X.lower()]])
    return result


# data, parents = readdata('aima-alarm.xml')
# print(gibbs_sampling('B', {'j', 'm'}, data, parents, 10000))


if __name__ == '__main__':
    sys.argv.pop(0)
    print(sys.argv)
    _data, _parents = test.readdata(sys.argv[0])
    _query = sys.argv[1]
    _evidences = set()
    for i in range(2, len(sys.argv)):
        if i % 2 == 0:
            e = sys.argv[i]
            if sys.argv[i + 1] == 'true':
                _evidences.add(e.lower())
            elif sys.argv[i + 1] == 'false':
                _evidences.add('!' + e.lower())
            else:
                exit('invalid input')
    variables = set()
    for k in _data.keys():
        variables.add(k.fore.strip('!').upper())
    print(gibbs_sampling(_query, _evidences, _data, _parents, 100000))
