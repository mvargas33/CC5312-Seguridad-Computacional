import secrets

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import rsa_crt_iqmp, rsa_crt_dmp1, rsa_crt_dmq1, RSAPrivateNumbers, \
    RSAPublicNumbers

from constants import MILLER_RABIN_ROUNDS


def random_prime(bits):
    """
    Returns a secure random prime of n bits
    :param bits: number of bits
    :return: a secure random prime of n bits
    """
    while True:
        x = secrets.randbits(bits)
        if miller_rabin(x, MILLER_RABIN_ROUNDS):
            return x


def next_prime(n):
    """
    Returns the next prime, searching from n
    :param n: number where to start searching
    :return: the lowest number greater than n that is prime
    """
    while True:
        n += 1
        if miller_rabin(n, MILLER_RABIN_ROUNDS):
            return n


def miller_rabin(n, k):
    """
    Performs a Miller-Rabin primality test k times over n,
    Using the pseudo code from Wikipedia.
    We need this function to check if our big random numbers are primes or not.
    (A classic sieve is too slow for our magnitudes (~2048 bits)
    :param n: number to check
    :param k: number of times to make the check
    :return true if number is probably prime, false otherwise:
    """
    if n % 2 == 0:
        return n == 2  # return true only if n is pair and 2, if it is pair and not 2 return false
    d = n - 1
    r = 0
    while d % 2 == 0:
        r += 1
        d >>= 1
    # now n = 2^r * d
    for i in range(k):
        x = 1
        a = secrets.randbelow(n - 4) + 2  # a \in [2, n-2]
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for j in range(r - 1):
            x = (x << 1) % n
            if x == n - 1:
                continue
        return False
    return True


def mod_inv(e, phi):
    """
    Computes the inverse of e mod phi.
    If the number is not invertible, return -1.
    We use this function to calculate d.
    From Wikipeida
    :param e: number
    :param phi: modulus used
    :return: inverse of e mod phi, or -1 if e is not invertible in mod phi
    """
    t, r, newt, newr = 0, phi, 1, e

    while newr != 0:
        quotient = r // newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
    if r > 1:
        return -1
    elif t < 0:
        return t + phi
    return t

def new_fixed_rsa_key(p, q):
    """
    new_fixed_rsa_key creates a new Cryptography-lib-compatible RSA private key
    using p and q as factors of N.
    :param p: first prime
    :param q: second prime
    :return: RSA private key
    """
    # We calculate n
    n = p * q
    # phi is phi(n) = (p - 1) * (q - 1)
    phi = (p - 1) * (q - 1)
    # e is usually used as pow(2,16) + 1 = 65537
    e = 65537
    # d is the inverse of e mod phi
    d = mod_inv(e, phi)
    # some useful precalculations required by Cryptography library (here is not what you are looking for)
    iqmp = rsa_crt_iqmp(p, q)
    dmp1 = rsa_crt_dmp1(d, p)
    dmq1 = rsa_crt_dmq1(d, q)
    public_numbers = RSAPublicNumbers(e, n)
    return RSAPrivateNumbers(p, q, d, dmp1, dmq1, iqmp, public_numbers).private_key(default_backend())


def new_rsa_key(bitsize):
    """
    Generates a random Cryptography-lib-compatible RSA key,
    using our superoptimized prime generation function.
    I created a new function for doing this because
    Cryptography was too slow on our legacy hardware.
    You can thank me later for my improvement.
    :param bitsize: key size
    :return:
    """
    # First we get a prime of size bitsize / 2
    p = random_prime(bitsize // 2)
    # Then we use a smart hack I invented to speed up the process!
    q = next_prime(p)
    return new_fixed_rsa_key(p, q)


def load_public_key_file(path):
    """
    allows to load a public key in a file, returning a Cryptography Public RSA key object.
    :param path: key path (default is ./public_key.pem)
    :return:  Cryptography Public RSA Key object.
    """
    with open(path, 'rb') as f:
        b = f.read()
        return serialization.load_pem_public_key(b, default_backend())

def get_n(public_key):
    """
    Returns N from a public key
    :param public_key: Cryptography Public RSA Key Object
    :return: N as int
    """
    return public_key.public_numbers().n

def get_e(public_key):
    """
    Returns E from a public key
    :param public_key: Cryptography Public RSA Key Object
    :return: E as int
    """
    return public_key.public_numbers().e