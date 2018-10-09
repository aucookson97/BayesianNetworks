# BayesianNetworks

This is an implementation of a Bayesian Network in python using networkx for its direct acyclic graph structure
Given input node information and query information, it builds a Bayesian Network, and performs rejection sampling 
as well as likelihood weighting sampling

Please refer to requirements.txt for the required libraries for this project 

To run our program use the following format in a terminal window:

python bayesian_network_acml.py network.txt query.txt sample_size

example:  
python bayesian_network_acml.py network_option_a.txt query2.txt 10000

