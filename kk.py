### HUIDS: 90978217 and 90949705 ###

#!/usr/bin/env python

from random import randint
from random import uniform
from heapq import *
import math
import time
import sys

MAX_ITER = 25000 # number of iterations to run our 3 randomized algorithms
SIZE = 100 # size of problem
MAX_INT = 10 ** 12 # maximum integer size in problems

# Common class contains the functions specific to either the pre-partitioning or standard representation 
# solution form. Common is used to dynamically call these specific functions in our later implementation
# of the three randomized algorithms.
class Common(object):
  # Returns random solution of length SIZE for prepartitioning.
  def rsol_pp(self):
    return [randint(0, SIZE - 1) for i in xrange(SIZE)]

  # Returns random solution of length SIZE for standard representation.
  def rsol_ss(self):
    S = []
    for i in xrange(SIZE):
      rand = randint(0, 1)
      if rand == 0: 
        rand = -1
      S.append(rand)
    return S

  # Converts pre-partitioned solution into standard form solution.
  # Returns residue obtained by running KK on this solution.
  def residue_pp(self, P, A):
    A_prime = [0] * len(A)
    for i in range(0,len(A)):
      A_prime[P[i]] += A[i]
    return kk(A_prime)

  # Returns residue of list A given standard-representation of solution S.
  def residue_ss(self, S, A):
    return abs(sum([x * y for x, y in zip(S, A)]))

  # Returns random neighbor (defined as a solution differing in one spot) for pre-partitioned solution.
  def rneighbor_pp(self, P):
    P_prime = P[:]
    i = randint(0, len(P_prime) - 1)
    j = P_prime[i]
    while (P_prime[i] == j):
      j = randint(0, len(P) - 1)
    P_prime[i] = j
    return P_prime

  # Returns random neighbor (defined as a solution differing in one or two spots) for standard rep. solution.
  def rneighbor_ss(self, S):
    S_prime = S[:]
    i = randint(0, len(S) - 1)
    j = randint(0, len(S) - 1)
    while (i == j):
      j = randint(0, len(S) - 1)
    S_prime[i] *= -1
    if (uniform(0,1) < 0.5):
      S_prime[j] *= -1
    return S_prime

# Returns random problem i.e. list of length SIZE.
def rprob():
  return [randint(1, MAX_INT) for i in xrange(SIZE)]

# Runs Karmankar-Karp algorithm on problem A. Returns the residue obtained. 
def kk(A):
  A_prime = [-elt for elt in A]
  
  heapify(A_prime)
  first = heappop(A_prime)
  for i in range(0,SIZE - 1):
    second = heappop(A_prime)
    first = heappushpop(A_prime, first - second)
  res = -first
  return res

# Cooling function, defined in specs of the problem set.
def cooling(iter):
  expo = math.floor(iter / 300)
  return (10 ** 10) * (.8 ** expo)

# Repeated random: given partitioning problem A, randomly generates solutions to A. 
# Returns the best solution over all iterations. 
def rr(A, method):
  common = Common()
  rsol = getattr(common, "rsol_%s" % method)
  residue = getattr(common, "residue_%s" % method)

  S = rsol()
  for i in range(0,MAX_ITER):
    S_prime = rsol()
    if residue(S_prime, A) < residue(S, A):
      S = S_prime
  return S

# Hill climbing: given partitioning problem A, randomly generates solution and steps to find better neighbors.
# Returns the final solution that is reached.
def hc(A, method):
  common = Common()
  rsol = getattr(common, "rsol_%s" % method)
  residue = getattr(common, "residue_%s" % method)
  rneighbor = getattr(common, "rneighbor_%s" % method)

  S = rsol()
  for i in range(0,MAX_ITER):
    S_prime = rneighbor(S)
    if residue(S_prime,A) < residue(S,A):
      S = S_prime
  return S

# Simulated annealing: given partitioning problem A, randomly generates solution and steps to find neighbors (not always better).
# Returns the best neighbor found across all iterations.
def sa(A, method):
  common = Common()
  rsol = getattr(common, "rsol_%s" % method)
  residue = getattr(common, "residue_%s" % method)
  rneighbor = getattr(common, "rneighbor_%s" % method)

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

# Given a randomized algorithm func, list A, file output, and method "pp" or "ss".
# Computes solution to A using func and representation method, writes time and residue to output.
# Returns time taken and the residue of the solution.
def time_func(func, A, output, method):
  common = Common()
  residue = getattr(common, "residue_%s" % method)

  t0 = time.time()
  solution = func(A, method)
  t1 = time.time()
  output.write(str(t1 - t0) + " " + str(residue(solution, A)) + " // ") 
  return ((t1 - t0), residue(solution, A))

# TESTING FUNCTION: Generates random file of 100 ints, each on a new line.
def random_input():
  random = open("random.txt", "w")
  for i in range(SIZE):
    random.write(str(randint(1, MAX_INT)) + "\n")
  random.close()
  return random


"""
----- PART ONE: Given input file of 100 integers, outputs residue -----
"""
# FOR TESTING: writes random file of 100 integers.
# inputfile = random_input().name

# Gets command line's inputfile.
try:
  inputfile = sys.argv[1]
except:
  print "Usage: ./kk.py <inputfile>"
  sys.exit(1)

# Stores problem A as the problem given by the input file.
with open(inputfile) as f:
  A = f.readlines() 
  A = [int(x.strip()) for x in A] 

# Prints residue obtained by running KK on A.
print "Residue for given input file:", kk(A) 



"""
----- PART TWO: Generates 100 random instances of the problem, runs three algorithms on each -----
Uncomment below to run.
"""

# # Number of problems to generate.
# niter = 100

# # Output file to write data to.
# output = open("output.txt", "w")
# output.write("FORMAT: Iteration: KK residue // RR SS time, RR SS residue // HC SS time, HC SS residue // SA SS time, SA SS residue // \
#   RR PP time, RR PP residue // HC PP time, HC PP residue // SA PP time, SA PP residue \n") 

# t = time.time()

# for i in range(0, niter):
#   A = rprob()

#   print "This is iteration", i  

#   output.write(str(i) + ": ") 
#   output.write(str(kk(A)) + " // ")
#   time_func(rr, A, output, "ss")
#   time_func(hc, A, output, "ss")
#   time_func(sa, A, output, "ss")

#   time_func(rr, A, output, "pp")
#   time_func(hc, A, output, "pp")
#   time_func(sa, A, output, "pp")
#   output.write("\n")

# tz = time.time()

# print "Total time taken: ", (tz - t)
# output.write("Total time taken: " + str(tz - t) + "\n")

# output.close() 




