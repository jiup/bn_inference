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
        print([tmp_bn, tmp_e])
        dis = Enumeration_ALL(tmp_bn, tmp_e, data)
        distribution.append(dis)
    return Normalize(distribution)


def match(s=set(), e=[]):
    if (s.__len__() == 0): return True
    for i in s:
        if i not in e:
            # print([s, e])
            return False
    return True


def Enumeration_ALL(bn, e, data):
    if bn.__len__() == 0:
        return 1

    if bn[0] in e:
        parents = []
        for key in data.keys():
            if key.fore == bn[0]:
                parents.append(key)
        for parent in parents:
            given = parent.given
            if match(given, e):
                rest = bn[1:]
                return data[parent] * Enumeration_ALL(rest, e, data)

    else:
        variable_true = bn[0].lower()
        variable_false = '!' + bn[0].lower()
        e_true = e.copy()
        e_true.append(variable_true)
        e_false = e.copy()
        e_false.append(variable_false)
        parents = []
        given = set()
        rest = []
        for key in data.keys():
            if key.fore == variable_true:
                parents.append(key)
        for parent in parents:
            tmp_given = parent.given
            if match(tmp_given, e):
                rest = bn[1:]
                given = tmp_given
        p_true = Probability(variable_true, given)
        p_false = Probability(variable_false, given)
        return data[p_true] * Enumeration_ALL(rest, e_true, data) + data[p_false] * Enumeration_ALL(rest, e_false, data)


data = test.readdata('aima-alarm.xml')
l = Enumeration_Ask('B', ['j', 'm'], ['E', 'A', 'j', 'm'], data)
print(l)
