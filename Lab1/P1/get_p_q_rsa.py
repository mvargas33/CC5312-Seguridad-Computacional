from utils import *
from decimal import *

getcontext().prec = 4096

def get_p_q(N):
    """
    Return p and q from consecutives primes p, q vulnerability

    :param N : Integer which corresponds to p*q
    :type N : Int
    
    :returns: A tuple with p and q
    :rtype: Tuple

    """
    sqrt_N = int(Decimal(N).sqrt().to_integral_exact())
    p = next_prime(sqrt_N)
    q = Decimal(N)/Decimal(p)
    return (int(p), int(q))