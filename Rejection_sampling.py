import random
import test


def prior_sample(bn=[], data={}, parents={}):
    bn = test.sort(bn, parents)
    for index in range(bn.__len__()):
        Variable = bn[index]
        variable = Variable.lower()
        given = set(parents[variable])
        for g in given:
            if ('!' + g) in bn:
                given.discard(g)
                given.add('!' + g)

        p = test.Probability(variable, given)
        probability = data[p]
        if probability < random.random():
            variable = '!' + variable
        bn[index] = variable
    return bn


def rejection_sample(X='', e=[], bn=[], N=0, data={}, parents={}):
    x_true = X.lower()
    x_false = '!' + X.lower()
    x_true_count = 0
    x_false_count = 0
    for i in range(N):
        event = prior_sample(bn, data, parents)
        if event.__len__() != (set(event).union(set(e))).__len__():
            continue
        else:
            if x_true in event:
                x_true_count += 1
            if x_false in event:
                x_false_count += 1
    x_count = x_true_count + x_false_count
    return [x_true_count / x_count, x_false_count / x_count]


data, parents = test.readdata('aima-alarm.xml')
print(rejection_sample('B', ['j', 'm'], ['A', 'E', 'J', 'M', 'B'], 100000, data, parents))
