from myenumeration import *
import random


def given_in(givens, e):
    if len(givens) == 0:
        return True
    flg = True
    for given in givens:
        if given not in e:
            flg = False
            break
    return flg


def proior_simple(bn):
    e = set()
    variables = set()
    for k in bn.keys():
        variables.add(k.fore.strip('!').upper())
    variables = tp_sort(list(variables), bn).reverse()
    for variable in variables:
        rand_p = random.uniform(0, 1)
        for keys, val in bn.items():
            if keys.fore == variable.lower() and given_in(keys.given, e):
                p = float(val)
        if rand_p < p:
            e.add(variable.lower())
        else:
            e.add('!' + variable.lower())
    return e


def rejection_sampling(X, e, bn, N):
    result = {X.lower():0,'!'+X.lower():0}
    for i in range(N):
        flg = True
        sample_es = proior_simple(bn)
        for sample_e in sample_es:
            if in_e(sample_e,e) == 3:
                flg = False
                break
        if flg and X.lower() in sample_es:
            result[X.lower()] += 1
        elif flg and '!' + X.lower() in sample_es:
            result['!' + X.lower()] += 1
    normalize(result)
    return result


data = readdata('aima-alarm.xml')
# print(rejection_sampling('B', {'j', 'm'}, data, 100000))
