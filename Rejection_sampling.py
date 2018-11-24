import random
import xmlparser
import sys
import exact_inference


def prior_sample(bn=[], data={}, parents={}):
    bn = xmlparser.sort(bn, parents)
    for index in range(bn.__len__()):
        Variable = bn[index]
        variable = Variable.lower()
        given = set(parents[variable])
        for g in given:
            if ('!' + g) in bn:
                given.discard(g)
                given.add('!' + g)

        p = xmlparser.Probability(variable, given)
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


# data, parents = test.readdata('aima-alarm.xml')
# print(rejection_sample('B', ['j', 'm'], ['A', 'E', 'J', 'M', 'B'], 100000, data, parents))

if __name__ == '__main__':
    sys.argv.pop(0)
    N = sys.argv.pop(0)
    _data, _parents = xmlparser.readdata(sys.argv[0])
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
    variables = set()
    for k in _data.keys():
        variables.add(k.fore.strip('!').upper())
    print(rejection_sample(_query, _evidences, list(variables), int(N), _data, _parents))
