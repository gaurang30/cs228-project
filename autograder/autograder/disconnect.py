#!/usr/bin/python3

from z3 import *
import argparse
import itertools
import time

def invert_dict(V):

	inverse = dict()

	N = len(V)
	for i in range(N):
		inverse[V[i]] = i

	return inverse

def find_minimal( graph, s, t ):

	# M : number of edges
	M = len(graph)

	# V : vertex set
	V = []
	for e in graph:
		V.append(e[0])
		V.append(e[1])
	V = list(set(V))

	# N : number of vertices
	N = len(V)

	# V_in : mapping from key value to vertex index
	V_in = invert_dict(V)

	# p_{i}_{j} denotes the edge (v_i,v_j) is picked in the final graph
	P = [ [ Bool ("p_{}_{}".format(i,j)) for j in range(N) ] for i in range(N) ]

	# maximize sum of p_{i}_{j}s over all edges
	G = Sum([If(P[V_in[e[0]]][V_in[e[1]]],1,0) for e in graph])

	# c_{i} denotes the node s is connected to the node i
	C = [ Bool ("c_{}".format(i)) for i in range(N) ]

	F1 = [ Or(Not(C[V_in[e[0]]]), Not(P[V_in[e[0]]][V_in[e[1]]]), C[V_in[e[1]]]) for e in graph ]

	F2 = [ Or(Not(C[V_in[e[1]]]), Not(P[V_in[e[0]]][V_in[e[1]]]), C[V_in[e[0]]]) for e in graph ]

	F3 = Not(C[V_in[t]])

	# F4 = []
	# for e in graph:
	# 	if e[0] == s:
	# 		F4.append(C[V_in[e[1]]])
	# 	elif e[1] == s:
	# 		F4.append(C[V_in[e[0]]])
	F4 = C[V_in[s]]

	# solver
	s = Optimize()

	# add the "constraints"
	s.add(F1)
	s.add(F2)
	s.add(F3)
	s.add(F4)

	# maximize the satisfying assignment
	s.maximize(G)

	# check for SAT
	r = s.check()

	# num : num stores the deleted edges
	num = []

	if r == sat:		
		m = s.model()
		# print(m)
		for e in graph:
			if not is_true(m[P[V_in[e[0]]][V_in[e[1]]]]):
				num.append(e)

	return num
