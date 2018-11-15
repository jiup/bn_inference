import copy
from test import *

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

def tp_sort(vars, bn):
    result = list()
    while vars:
        var = vars.pop(0)
        parents = get_parents(var.lower(), bn)
        if len(parents) > 0:
            flg = 0
            for parent in parents:
                if parent.strip('!').upper() not in result:
                    vars.append(var)
                    flg = 1
                    break
            if flg == 0:
                result.append(var)
        else:
            result.append(var)
    result.reverse()
    return result

def enumeration_ask(X, e, bn):
    variables = set()
    for k in bn.keys():
        variables.add(k.fore.strip('!').upper())
    e_x = copy.copy(e)
    e_x.add(X.lower())
    e_not_x = copy.copy(e)
    e_not_x.add('!' + X.lower())
    result = dict()
    result[X.lower()] = enumerate_all(copy.copy(tp_sort(list(variables), bn)), e_x, bn)
    result['!' + X.lower()] = enumerate_all(copy.copy(tp_sort(list(variables), bn)), e_not_x, bn)
    normalize(result)
    return result

def normalize(result):
    total = 0
    for v in result.values():
        total += v
    for k in result.keys():
        result[k] = result[k] / total

def check(keys, e):
    flg = True
    for given in keys.given:
        if in_e(given, e) == 3:
            flg = False
    return flg

def enumerate_all(variables, e, data):
    if len(variables) < 1:
        return 1.0
    y = variables.pop()
    sum_p = 0
    if in_e(y, e) == 1:
        e_y = copy.copy(e)
        e_y.add(y.lower())
        e_not_y = copy.copy(e)
        e_not_y.add('!' + y.lower())
        for keys, val in data.items():
            if keys.fore == y.lower() and check(keys, e):
                    sum_p += (float(val) * enumerate_all(copy.copy(variables), e_y, data))
            elif ((keys.fore == '!' + y.lower()) or (keys.fore == y.lower().strip('!'))) and (keys.fore != y.lower()) and check(keys, e):
                    sum_p += (float(val) * enumerate_all(copy.copy(variables), e_not_y, data))
    else:
        if in_e(y, e) == 2:
            for keys, val in data.items():
                if keys.fore == y.lower() and check(keys, e):
                        sum_p += (float(val) * enumerate_all(variables, copy.copy(e), data))
        else:
            for keys, val in data.items():
                if ((keys.fore == '!' + y.lower()) or (keys.fore == y.lower().strip('!'))) and (keys.fore != y.lower()) and check(keys, e):
                        sum_p += (float(val) * enumerate_all(variables, copy.copy(e), data))
    return sum_p


data = readdata('aima-alarm.xml')
# print(enumeration_ask("B", {"j", 'm'}, data))
