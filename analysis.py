from matplotlib import pyplot as plt
# from sklearn.datasets import load_iris
import numpy as np
import itertools
from gibbs_sampling import *
from likelihood_weighting import *
from rejection_sampling import *

x = np.arange(10000, 100000, 10)
y_gibbs_sampling = list()
y_likelihood_weighting = list()
y_rejection_sampling = list()
_data, _parents = xmlparser.readdata('aima-alarm.xml')
_query = 'B'
_evidences = {'j','m'}
variables = set()
for k in _data.keys():
    variables.add(k.fore.strip('!').upper())

for i in x:
    y_gibbs_sampling.append(gibbs_sampling(_query, _evidences, _data, _parents, i))
    y_likelihood_weighting.append(likelihood_weighting(_query, list(_evidences), list(variables), i, _data, _parents))
    y_rejection_sampling.append(rejection_sample(_query, list(_evidences), list(variables), i, _data, _parents))


plt.plot(x, y_gibbs_sampling, color='green', label='training accuracy')
plt.plot(x, y_likelihood_weighting, color='red', label='testing accuracy')
plt.plot(x, y_rejection_sampling,  color='skyblue', label='PN distance')
# plt.plot(x, thresholds, color='blue', label='threshold')
plt.legend() # 显示图例

plt.xlabel('Porbability')
plt.ylabel('sample number')
plt.show()
