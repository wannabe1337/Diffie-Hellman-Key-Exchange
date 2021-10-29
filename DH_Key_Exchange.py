# Algorithm
'''
                            Sender                  Receiver
                            \--------{a,n} --------/         Both agrees upon {a,n} | 'n' is prime and 'a' is primitive root of 'n'

Generate Random #              p                        q

Computes                 S=(a^p) mod n            R=(a^q) mod n 


Interchange (S,R)              R                        S

Compute Key               (R^p) mod n              (S^q) mod n
                               |                        |
                               |                        |
                               V                        V
                    =>  ((a^q)^p) mod n       =>  ((a^p)^q) mod n
                
                    =>  (a^pq) mod n          =>  (a^pq) mod n          // Symmetric key got exchanged

'''
# Implementation
import random,time
from tqdm.auto import tqdm

# progressive bar
bar=tqdm(total=2,position=0,leave=False)
#-----------------------------------------------------------------#
def GeneratePrime():
	n=random.randint(10,90)
	#print(n)
	#Generating nth row of pascal's triangle
	line = [1]
	for j in range(n):             
		line.append(int(line[j]*(n-j)//(j+1)))             
	#print(line)
	
	# AKS Primality test 
	l=int(n/2)+1
	l=n-l+1
	for k in line[1:-l]:
		if(k%n!=0):
			return 0
	return n
#-----------------------------------------------------------------#
#Program to verify co-prime
def gcd(p,q):
# find the gcd of two positive integers. | Euclid's Algorithm
    while(q!=0):
        p,q = q,p%q
    return p
def is_coprime(x,y):
    return gcd(x,y)==1

def find_primitive_root_of_n (n,Phi):
    # 'm' is a primitive root of n; iff the multiplicative order of 'm mod n' is Phi(n) 
    # [i.e. Phi(n) is the smallest integer | gcd(m,n)=1 and m^Phi(n) is congruent to 1 mod n]
    a=0
    while(a==0):
        bar.set_description("Finding primitive root of modulo 'n' ...")
        # m=random.randint(1,1000)
        for m in range(1,1000):
            if(is_coprime(m,n)):
                for i in range(1,Phi+1):    # searches multiplicative order between [1,Phi]
                    if (((m**i)%n)==1):
                        if(i==Phi):
                            a=m
                        else:
                            break
            if(a!=0):
                break
    return a

#-----------------------------------------------------------------#
#-----------------------------------------------------------------#
def dh_key_exchange():
    # generate prime 'n'
    n=0
    while(n==0):
        bar.set_description("Generating Large Prime 'n' ...")
        n=GeneratePrime()
        bar.update()
        time.sleep(0.2)

    print('\nLarge primes n : ',n)
    # no. of coprime with n under n (i.e. Euler's Totient Function [Phi])
    Phi=(n-1)

    #find_primitive_root_of_n(n)
    a=find_primitive_root_of_n(n,Phi)
    print(f"\nPrimitive root a={a}")

    return a,n

# dh_key_exchange()