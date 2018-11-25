from matplotlib import pyplot as plt
import numpy as np
from gibbs_sampling import *
from likelihood_weighting import *
from rejection_sampling import *
from time import *
x = np.arange(100, 100000, 10000)
y_gibbs_sampling = list()
y_likelihood_weighting = list()
y_rejection_sampling = list()
y_rejection = list()
y_likelihood_weighting_time = list()
y_rejection_sampling_time = list()
y_gibbs_sampling_time = list()
_data, _parents = xmlparser.readdata('aima-wet-grass.xml')
_query = 'R'
_evidences = {'s'}
variables = set()
for k in _data.keys():
    variables.add(k.fore.strip('!').upper())
real = Enumeration_Ask(_query, list(_evidences), get_variables(_query, list(_evidences), _data), _data, _parents)

for i in x:
    time1 = time()
    y_gibbs_sampling.append(gibbs_sampling(_query, _evidences, _data, _parents, i)[0])
    time2 = time()
    y_likelihood_weighting.append(likelihood_weighting(_query, list(_evidences), list(variables), i, _data, _parents)[0])
    time3 = time()
    y_rejection_sampling.append(rejection_sample(_query, list(_evidences), list(variables), i, _data, _parents)[0])
    time4 = time()
    y_gibbs_sampling_time.append(time4-time3)
    y_likelihood_weighting_time.append(time3-time2)
    y_rejection_sampling_time.append(time2-time1)
    # y_rejection.append(rejection_sampling(_query,_evidences,_data,i)[0])

plt.plot(x, y_gibbs_sampling_time, color='green', label='gibbs_sampling ')
plt.plot(x, y_likelihood_weighting_time, color='red', label='likelihood_weighting ')
plt.plot(x, y_rejection_sampling_time,  color='skyblue', label='rejection_sample ')
# plt.plot(x, [real[0]]*len(x),  color='blue', label=' Exact Inference')
plt.xlim((100,100000))
# plt.ylim((0, 0.5))
# plt.title('error between Approximate Inference and Exact Inference')
# plt.title(' Approximate Inference performance')
plt.title('run time')
# plt.plot(x, y_rejection, color='blue', label='my rejection')
plt.legend() # 显示图例
plt.xlabel('sample number')
plt.ylabel('time')
plt.show()
