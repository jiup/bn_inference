from matplotlib import pyplot as plt
import numpy as np
from Gibbs_sampling import *
from likelihood_weighting import *
from Rejection_sampling import *
import scipy.optimize as opt

x = [10, 50, 250] + list(np.arange(1000, 10000, 250)) + [20000]
# x = [200, 1000, 5000, 10000]
# x = [10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120, 10240, 20480, 40960]#
y_gibbs_sampling = list()
y_likelihood_weighting = list()
y_rejection_sampling = list()
y_rejection_sampling2 = list()
standard_list = list()
_data, _parents = xmlparser.readdata('aima-alarm.xml')
# for i in _data.keys():
#     print(i)
_query = 'B'
_evidences = {'j', 'm'}
variables = set()
for k in _data.keys():
    variables.add(k.fore.strip('!').upper())

time = 0
while time < 10:
    time = time + 1
    print('time: ', time)
    c = 0
    for i in x:
        if i > 0 and i % 1000 == 0:
            print(i)
        # print(_query.strip('!').upper(), list(_evidences), get_variables(_query.strip('!').upper(), list(_evidences), _data))
        std = enumerate_ask(_query.strip('!').upper(), get_variables(_query.strip('!').upper(), list(_evidences), _data), list(_evidences), _data)[0]
        standard_list.append(0)
        if time == 1:
            y_likelihood_weighting.append(abs(likelihood_weighting(_query, list(_evidences), list(variables), i, _data, _parents)[0] - std))
            y_gibbs_sampling.append(abs(gibbs_sampling(_query, _evidences, _data, _parents, i)[0] - std))
            y_rejection_sampling.append(abs(rejection_sample(_query, list(_evidences), list(variables), i, _data, _parents)[0] - std))
            # y_rejection_sampling2.append(abs(rejection_sample2(_query, list(_evidences), list(variables), i, _data, _parents)[0] - std))
        else:
            y_likelihood_weighting[c] = y_likelihood_weighting[c] + abs(likelihood_weighting(_query, list(_evidences), list(variables), i, _data, _parents)[0] - std)
            y_gibbs_sampling[c] = y_gibbs_sampling[c] + abs(gibbs_sampling(_query, _evidences, _data, _parents, i)[0] - std)
            y_rejection_sampling[c] = y_rejection_sampling[c] + abs(rejection_sample(_query, list(_evidences), list(variables), i, _data, _parents)[0] - std)
        c = c + 1
for i, v in enumerate(y_rejection_sampling):
    y_likelihood_weighting[i] /= 10.0
    y_gibbs_sampling[i] /= 10.0
    y_rejection_sampling[i] /= 10.0

# optimizedParameters, pcov = opt.curve_fit(func, xdata, ydata);
plt.plot(x, y_rejection_sampling,  color='orange', label='Rejection Sampling')
# plt.plot(x, y_rejection_sampling2,  color='orange', label='Rejection Sampling (N Adopted Sample)')
plt.plot(x, y_likelihood_weighting, color='red', label='Likelihood Weighting')
plt.plot(x, y_gibbs_sampling, color='green', label='Gibbs Sampling')
# plt.plot(x, standard_list,  color='blue', label='PN distance')#skyblue
# plt.plot(x, thresholds, color='blue', label='threshold')
plt.title("Error Comparision [aima-alarm: P(B|j, m)]")
plt.legend()
plt.xlabel('N')
plt.ylabel('Average Error (n=10)')
plt.ylim(bottom=0)
# plt.ylim(0, .5)
plt.xlim(0, 10000)
# plt.autoscale(False)
plt.show()
