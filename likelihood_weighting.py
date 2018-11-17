import test
import random


def likelihood_weighting(X='', e=[], bn=[], N=1000, data={}, parents={}):
    x_true = X.lower()
    x_false = '!' + X.lower()
    x_true_weight = 0.0
    x_false_weight = 0.0
    for i in range(N):
        event, w = weighted_sample(bn, e, data, parents)
        if x_true in event:
            x_true_weight += w
        if x_false in event:
            x_false_weight += w
    x_total_weight = x_true_weight + x_false_weight
    return [x_true_weight / x_total_weight, x_false_weight / x_total_weight]


def weighted_sample(bn=[], e=[], data={}, parents={}):
    bn = test.sort(bn, parents)
    event = bn.copy()
    w = 1.0
    for i in range(bn.__len__()):
        Variable = bn[i]
        if Variable.lower() in e:
            event[i] = Variable.lower()
        if '!' + Variable.lower() in e:
            event[i] = '!' + Variable.lower()
    for i in range(event.__len__()):
        Variable = event[i]
        if Variable == Variable.lower():
            w *= test.Prob(Variable, parents, data, event)
        else:
            variable = Variable.lower()
            prob = test.Prob(variable, parents, data, event)
            if random.random() > prob:
                variable = '!' + variable
            event[i] = variable
    return event, w


data, parents = test.readdata('aima-alarm.xml')
print(likelihood_weighting('B', ['j', 'm'], ['A', 'E', 'J', 'M', 'B'], 100000, data, parents))
