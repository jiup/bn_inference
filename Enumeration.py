import copy
from test import *


class Node:
    pass


# evidence:set()
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
            # else:
            #     result.append(var)
        else:
            result.append(var)
    result.reverse()
    return result


def enumeration_ask(X, e, bn):
    variables = set()
    for k in bn.keys():
        variables.add(k.fore.strip('!').upper())
    e_x = copy.deepcopy(e)
    e_x.add(X.lower())
    e_not_x = copy.deepcopy(e)
    e_not_x.add('!' + X.lower())
    result = dict()
    bnx = copy.deepcopy(bn)
    bnnotx = copy.deepcopy(bn)
    for sentence, v in bn.items():
        flg1 = 0
        flg2 = 0
        for given in sentence.given:
            if in_e(given, e_x) == 3:
                flg1 = 1
            if in_e(given, e_not_x) == 3:
                flg2 = 2
        if flg1 == 1:
            bnx.pop(sentence)
        if flg2 == 2:
            bnnotx.pop(sentence)
    a = ["E", "B", "A", "J", "M"]
    b = ["E", "B", "A", "J", "M"]
    a.reverse()
    b.reverse()
    print(tp_sort(list(variables), bnx))
    result[X.lower()] = enumerate_all(copy.deepcopy(tp_sort(list(variables), bnx)), e_x, bnx, '')
    print('___________________')
    result['!' + X.lower()] = enumerate_all(copy.deepcopy(tp_sort(list(variables), bnnotx)), e_not_x, bnnotx, '')
    normalize(result)
    return result


def normalize(result):
    total = 0
    for v in result.values():
        total += v
    for k in result.keys():
        result[k] = result[k] / total


def enumerate_all(variables, e, data, str):
    # print(e)

    if len(variables) < 1:
        print(str)
        return 1.0
    y = variables.pop()
    if in_e(y, e) == 1:
        sum_p = 0
        e_y = copy.deepcopy(e)
        e_y.add(y.lower())
        e_not_y = copy.deepcopy(e)
        e_not_y.add('!' + y.lower())
        for keys, val in data.items():
            if keys.fore == y.lower():
                # print(keys.fore, y.lower(), e)
                flg = True
                for given in keys.given:
                    print(given, e)
                    if in_e(given, e) == 3:
                        flg = False
                if flg:
                    sum_p += (float(val) * enumerate_all(copy.deepcopy(variables), e_y, data,
                                                         str + keys.tostring() + val))
                else:
                    print('==========')
            elif ((keys.fore == '!' + y.lower()) or (keys.fore == y.lower().strip('!'))) and (keys.fore != y.lower()):
                # else:
                # print(keys.fore, y.lower(), e)
                flg = True
                for given in keys.given:
                    print(given, e)
                    if in_e(given, e) == 3:
                        flg = False
                if flg:
                    sum_p += (float(val) * enumerate_all(copy.deepcopy(variables), e_not_y, data,
                                                         str + keys.tostring() + val))
                else:
                    print('==========')
        return sum_p
    else:
        if in_e(y, e) == 2:
            sum_p = 0
            for keys, val in data.items():
                if keys.fore == y.lower():
                    # print(keys.fore, y.lower(), e,2)
                    flg = True
                    for given in keys.given:
                        print(given, e)
                        if in_e(given, e) == 3:
                            flg = False
                    if flg:
                        sum_p += (float(val) * enumerate_all(copy.deepcopy(variables), copy.deepcopy(e), data,
                                                             str + keys.tostring() + val))
                    else:
                        print('==========')
            return sum_p
        else:
            sum_p = 0
            for keys, val in data.items():
                if ((keys.fore == '!' + y.lower()) or (keys.fore == y.lower().strip('!'))) and (keys.fore != y.lower()):
                    # print(keys.fore,y.lower(),e,3)
                    flg = True
                    for given in keys.given:
                        print(given, e)
                        if in_e(given, e) == 3:
                            flg = False
                    if flg:
                        sum_p += (float(val) * enumerate_all(copy.deepcopy(variables), copy.deepcopy(e), data,
                                                             str + keys.tostring() + val))
                    else:
                        print('==========')
            return sum_p

    #
    #
    #
    #
    # if y in list(e.keys()):
    #     if y.lower() in e:
    #         sum_p = 0
    #         for keys, val in data.items():
    #             if keys.fore == y.lower():
    #                 sum_p += float(val) * enumerate_all(variables, e, data)
    #                 print(keys.tostring(), 'e')
    #     else:
    #         sum_p = 0
    #         for keys, val in data.items():
    #             if keys.fore == '!' + y.lower():
    #                 sum_p += float(val) * enumerate_all(variables, e, data)
    #                 print(keys.tostring(), '!e')
    #     return sum_p
    # else:
    #     sum_p = 0
    #     noty = '!' + y.lower()
    #     e_noty = copy.deepcopy(e)
    #     e_y = copy.deepcopy(e)
    #     e_y[y] = y.lower()
    #     e_noty[y] = noty
    #     for keys, val in data.items():
    #         if keys.fore == y.lower():
    #             sum_p += float(val) * enumerate_all(variables, e_y, data)
    #             print(keys.tostring(), 2)
    #         elif keys.fore == noty:
    #             sum_p += float(val) * enumerate_all(variables, e_noty, data)
    #             print(keys.tostring(), 3)
    #     return sum_p


data = readdata('dog-problem.xml')
print(enumeration_ask("BOWEL-PROBLEM", {"dog-out", 'hear-bark'}, data))

