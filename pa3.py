from random import randint
from random import uniform
from heapq import *
import math
import time

MAX_ITER = 1000
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



t = time.time()
# testing 
niter = 1
for i in range(0,niter):
  A = rprob()
    
  t0 = time.time()
  S_rr = rr(A)
  t1 = time.time()
  print 'Repeated random sampling time:', (t1 - t0), "seconds / residue of", residue(S_rr, A)
  t0 = time.time()
  S_hc = hc(A)
  t1 = time.time()
  print 'Hill climbing sampling time: ', (t1 - t0), " seconds / residue of", residue(S_hc, A)
  t0 = time.time()
  S_sa = sa(A)
  t1 = time.time()
  print 'Simulated annealing sampling time: ', (t1 - t0), " seconds / residue of", residue(S_sa, A)
'''
  print('kk')
  print(kk(A))
  print("rr")
  print(residue(S_rr, A))
# print(S_rr)
  print("hc")
  print(residue(S_hc, A))
# print(S_hc)
  print("sa")
  print(residue(S_sa, A))
# print(S_sa)
  print()
'''
tz = time.time()

print(tz-t)
