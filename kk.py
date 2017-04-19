#!/usr/bin/env python

from random import randint
from random import uniform
from heapq import *
import math
import time
import sys

MAX_ITER = 500
SIZE = 100
MAX_INT = 10 ** 12

# generates random problem i.e. list of length SIZE
def rprob():
  return [randint(1, MAX_INT) for i in xrange(SIZE)]

# runs Karmankar-Karp algorithm on list A of integers 
# returns residue
# note heapq is min heap
def kk(A):
  A_prime = [-elt for elt in A]
  
  heapify(A_prime)
  first = heappop(A_prime)
  for i in range(0,SIZE - 1):
    second = heappop(A_prime)
    first = heappushpop(A_prime, first - second)
  res = -first
  return res

# generates random solution of length SIZE
def rsol():
  return [randint(0, SIZE - 1) for i in xrange(SIZE)]

# turns pre-partitioned solution into standard form solution
# returns residue
def residue(P, A):
  A_prime = [0] * len(A)
  for i in range(0,len(A)):
    A_prime[P[i]] += A[i]
  return kk(A_prime)

# generates random neighbor (list differing in one spot)
def rneighbor(P):
  P_prime = P[:]
  i = randint(0, len(P_prime) - 1)
  j = P_prime[i]
  while (P_prime[i] == j):
    j = randint(0, len(P) - 1)
  P_prime[i] = j
  return P_prime

# cooling function given in problem set
def cooling(iter):
  expo = math.floor(iter / 300)
  return (10 ** 10) * (.8 ** expo)

# repeated random
def rr(A):
  S = rsol()
  for i in range(0,MAX_ITER):
    S_prime = rsol()
    if residue(S_prime,A) < residue(S,A):
      S = S_prime
  return S

# hill climbing
def hc(A):
  S = rsol()
  for i in range(0,MAX_ITER):
    S_prime = rneighbor(S)
    if residue(S_prime,A) < residue(S,A):
      S = S_prime
  return S

# simulated annealing
def sa(A):
  S = rsol()
  S_2prime = S[:]
  prime2_res = residue(S_2prime, A)
  for i in range(0, MAX_ITER):
    S_prime = rneighbor(S)
    prime_res = residue(S_prime,A)
    res = residue(S,A)
    if prime_res < res:
      S = S_prime
    elif (uniform(0,1) < math.exp(-1*(prime_res - res) / cooling(i))):
      S = S_prime
    if (prime_res < prime2_res):
      S_2prime = S[:]
      prime2_res = prime_res
  return S_2prime

# given an algorithm func, list A, and file output, computes solution to A using func
# writes time and residue to output file
# returns time taken and solution residue
def time_func(func, A, output):
  t0 = time.time()
  solution = func(A)
  t1 = time.time()
  output.write(str(t1 - t0) + " " + str(residue(solution, A)) + " // ") 
  return ((t1 - t0), residue(solution, A))

def random_input():
  random = open("random.txt", "w")
  for i in range(SIZE):
    random.write(str(randint(1, MAX_INT)) + "\n")
  random.close()
  return random


"""----- PART ONE: Given input file of 100 integers, outputs residue -----"""
# FOR TESTING: writes random file of 100 integers
# inputfile = random_input().name

# gets command line argument input file
inputfile = sys.argv[1]

# stores problem A as problem given by input file
with open(inputfile) as f:
  A = f.readlines() 
  A = [int(x.strip()) for x in A] 

# outputs residue obtained by running KK
print "Residue for given input file:", kk(A) 



"""----- PART TWO: Generates 100 random instances of the problem, runs three algorithms on each -----"""
niter = 5

# opens file to write data to
output = open("output.txt", "w")
output.write("FORMAT: Iteration: RR time, RR residue, HC time, HC residue, SA time, SA residue \n") 

# runs code for niter iterations
t = time.time()

for i in range(0, niter):
  # generates random problem A
  A = rprob()
  
  output.write(str(i) + ": ") 
  print "This is iteration", i  
  time_func(rr, A, output)
  time_func(hc, A, output)
  time_func(sa, A, output)
  output.write("\n")

tz = time.time()

print "Total time taken: ", (tz - t)
output.write("Total time taken: " + str(tz - t) + "\n")

output.close() 




