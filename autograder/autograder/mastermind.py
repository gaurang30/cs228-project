#!/usr/bin/python3

from z3 import *
import time
import random

num_pegs 	= 0 	# number of pegs a.k.a. positions
num_colors 	= 0		# number of colors
vs 		= []
l 		= []

# solver
s = Optimize()

def min2( vs, l ):
	min_list = []
	for c in range(num_colors):
		x = Sum([If(vs[i][c],1,0) for i in range(num_pegs)])
		y = Int('y')
		y = f(l,c)
		z = If(x<y, x, y)
		min_list.append(z)
	return min_list

def f( l, c ):
	count = 0
	for i in range(num_pegs):
		if l[i]==c:
			count = count + 1
	return count

def initialize ( n, k ):

	global l

	global num_colors
	num_colors = n

	global num_pegs
	num_pegs = k

	# x_{i}_{j} represents ith position has the jth color
	global vs
	vs = [ [ Bool("x_{}_{}".format(i,j)) for j in range(num_colors) ] for i in range(num_pegs) ]

	# every position can have exactly one color
	s.add( [ PbEq( [ (vs[i][j], 1) for j in range(num_colors) ], 1 ) for i in range(num_pegs) ] )

	for i in range(num_pegs):
		l.append( random.randint(0, n-1) )

def get_second_player_move():
	
	global l
	return l

def put_first_player_response( r, w ):

	global vs, l

	# number of correct colors in correct positions
	F1 = PbEq( [ (vs[i][l[i]], 1) for i in range(num_pegs) ], r )

	# number of correct colors (not necessarily in the correct positions)
	min_list = min2( vs, l )
	F2 = Sum( [ e for e in min_list ] ) == r + w
	
	s.add_soft( And(F1, F2) )

	r = s.check()
	m = s.model()

	l*=0
	for i in range(num_pegs):
		for j in range(num_colors):
			if is_true(m[vs[i][j]]):
				l.append(j)
