import random

from rejection_sampling import *
import enumeration

def Gibbs_sampling(X, e, bn, N):
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
            p = enumeration.enumeration_ask(sample[i].strip('!'), enumerate_e, bn)
            if rand_p < p[sample[i].strip('!')]:
                sample[i] = sample[i].strip('!')
            else:
                sample[i] = sample[i].strip('!')
                sample[i] = '!' + sample[i]
            if X.lower() in sample:
                result[X.lower()] += 1
            elif '!' + X.lower() in sample:
                result['!' + X.lower()] += 1
            tmp = sample + list(e)
    normalize(result)
    return result


data = readdata('aima-alarm.xml')
print(Gibbs_sampling('B', {'j', 'm'}, data, 10000))
