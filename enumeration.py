import test
from test import Probability


def Normalize(l=[]):
    res = [0] * l.__len__()
    s = 0.0
    for num in l:
        s += num
    for i in range(l.__len__()):
        res[i] = l[i] / s
    return res


def Enumeration_Ask(X='', e=[], bn=[], data={}):
    distribution = []
    query_variable = [X.lower(), '!' + X.lower()]

    for x in query_variable:
        tmp_e = e.copy()
        tmp_bn = bn.copy()
        tmp_e.append(x)
        tmp_bn = [x] + tmp_bn
        # print(tmp_bn, tmp_e)
        dis = Enumeration_ALL(tmp_bn, tmp_e, data)
        distribution.append(dis)
    return Normalize(distribution)


def all_in(s=set(), e=[]):
    if s.__len__() == 0:
        return True
    for i in s:
        if i not in e:
            # print([s, e])
            return False
    return True


def parents(variable, data):
    ps = []
    for key in data.keys():
        if key.fore == variable:
            ps.append(key)
    return ps


def Enumeration_ALL(bn, e, data):
    if bn.__len__() == 0:
        return 1

    if bn[0] in e:
        for parent in parents(bn[0], data):
            if all_in(parent.given, e):
                rest_bn = bn[1:]
                return data[parent] * Enumeration_ALL(rest_bn, e, data)

    else:
        variable_true = bn[0].lower()
        variable_false = '!' + bn[0].lower()
        given = set()
        rest_bn = []
        # variable_true and variable_false both represents the same node
        for parent in parents(variable_true, data):
            if all_in(parent.given, e):
                rest_bn = bn[1:]
                given = parent.given
                break
        return data[Probability(variable_true, given)] * Enumeration_ALL(rest_bn, e.copy() + [variable_true], data) + \
            data[Probability(variable_false, given)] * Enumeration_ALL(rest_bn, e.copy() + [variable_false], data)


print(Enumeration_Ask('B', ['j', 'm'], ['E', 'A', 'j', 'm'], test.readdata('aima-alarm.xml')))
