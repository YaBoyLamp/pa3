from random import randint
from random import uniform
from heapq import *
import math
import time

MAX_ITER = 1000
SIZE = 100
MAX_INT = 10 ** 12

# generates random problem i.e. list of length size
def rprob(size):
  A = []
  for i in range(0,size):
    A.append(randint(1,MAX_INT))
  return A

# runs Karmankar-Karp algorithm on list A of integers 
# returns residue
def kk(A):
  A_prime = [-elt for elt in A]
  for i in range(0,len(A)):
    heapify(A_prime) # note heapq is min heap
    first = heapreplace(A_prime,0)
    second = heappop(A_prime)
    heappush(A_prime, first - second)
  res = -1 * heappop(A_prime)
  return res

# generates random solution 
def rsol(A):
  P = []
  for i in range(0,len(A)):
    P.append(randint(0, len(A) - 1))
  return P

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
  S = rsol(A)
  for i in range(0,MAX_ITER):
    S_prime = rsol(A)
    if residue(S_prime,A) < residue(S,A):
      S = S_prime
  return S

# hill climbing
def hc(A):
  S = rsol(A)
  for i in range(0,MAX_ITER):
    S_prime = rneighbor(S)
    if residue(S_prime,A) < residue(S,A):
      S = S_prime
  return S

# simulated annealing
def sa(A):
  S = rsol(A)
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



t0 = time.time()
for i in range(0,1):
  A = rprob(SIZE)
  
  t0 = time.time()
  S_rr = rr(A)
  t1 = time.time()
  print('rr')
  print(t1-t0)
  t0 = time.time()
  S_hc = hc(A)
  t1 = time.time()
  print('hc')
  print(t1-t0)  
  t0 = time.time()
  S_sa = sa(A)
  t1 = time.time()
  print('sa')
  print(t1-t0)
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
t1 = time.time()

#print(t1-t0)