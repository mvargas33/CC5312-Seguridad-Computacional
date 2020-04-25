from utils import *
from decimal import *

getcontext().prec = 4096

def get_p_q(N):
    sqrt_N = int(Decimal(N).sqrt().to_integral_exact())
    p = next_prime(sqrt_N)
    q = Decimal(N)/Decimal(p)
    return (int(p), int(q))