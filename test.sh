#!/bin/sh
clear
echo "\033[49;32m exact_inference test: \033[0m "

python3 exact_inference.py aima-alarm.xml B J true M true
python3 exact_inference.py aima-alarm.xml E J true M true
python3 exact_inference.py aima-wet-grass.xml C W true
python3 exact_inference.py aima-wet-grass.xml R W true
python3 exact_inference.py dog-problem.xml LIGHT-ON HEAR-BARK false
python3 exact_inference.py dog-problem.xml BOWEL-PROBLEM HEAR-BARK false

echo "\033[49;32m rejection_sampling test: \033[0m "

python3 rejection_sampling.py 100000 aima-alarm.xml  B J true M true
python3 rejection_sampling.py 100000 aima-alarm.xml E J true M true
python3 rejection_sampling.py 100000 aima-wet-grass.xml C W true
python3 rejection_sampling.py 100000 aima-wet-grass.xml R W true
python3 rejection_sampling.py 100000 dog-problem.xml LIGHT-ON HEAR-BARK false
python3 rejection_sampling.py 100000 dog-problem.xml BOWEL-PROBLEM HEAR-BARK false

echo "\033[49;32m likelihood_sampling test: \033[0m "

python3 likelihood_weighting.py 100000 aima-alarm.xml  B J true M true
python3 likelihood_weighting.py 100000 aima-alarm.xml E J true M true
python3 likelihood_weighting.py 100000 aima-wet-grass.xml C W true
python3 likelihood_weighting.py 100000 aima-wet-grass.xml R W true
python3 likelihood_weighting.py 100000 dog-problem.xml LIGHT-ON HEAR-BARK false
python3 likelihood_weighting.py 100000 dog-problem.xml BOWEL-PROBLEM HEAR-BARK false

echo "\033[49;32m gibbs_sampling test: \033[0m "
python3 gibbs_sampling.py 100000 aima-alarm.xml  B J true M true
python3 gibbs_sampling.py 100000 aima-alarm.xml E J true M true
python3 gibbs_sampling.py 100000 aima-wet-grass.xml C W true
python3 gibbs_sampling.py 100000 aima-wet-grass.xml R W true
python3 gibbs_sampling.py 100000 dog-problem.xml LIGHT-ON HEAR-BARK false
python3 gibbs_sampling.py 100000 dog-problem.xml BOWEL-PROBLEM HEAR-BARK false



