from utils import *
from Cryptodome.PublicKey import RSA
import constants
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization.base import Encoding, PublicFormat, NoEncryption
import time
import math
from decimal import Decimal
from get_p_q_rsa import *


if __name__ == '__main__':
    start = time.time()
    f = open(constants.PUBLIC_KEY_PATH, "r")
    key = RSA.importKey(f.read())
    f.close()
    N = key.n
    sqrt_N = int(Decimal(N).sqrt().to_integral_exact())
    """
    # print(sqrt_N*sqrt_N/N)
    tolerancia = 2**256 # Peor caso
    print(sqrt_N)
    A = sqrt_N - tolerancia # 1 # Next prime de 2
    print(A)
    B = sqrt_N + tolerancia # 2**1024 - 1
    print(B)
    if(B > N):
        B = N
    e = 65537
    d = 0

    while(A < B):
        print("A: " + str(A) + "\nB: " + str(B) + "\nDELTA: " + str(B-A))
        mid = (B-A)//2 + A
        #print(mid)
        p = next_prime(mid)
        q = next_prime(p)

        # print("p: " + str(p) + " q:  " + str(q) + " p*q: " + str(p*q) + " N: " + str(7043*7079))
        if(p*q == N):
            break
        elif(p*q > N):
            B = mid
        else:
            A = mid + 1
    """

    p,q = get_p_q(N)
    
    print("p: " + str(p) + " q:  " + str(q))

    if( p*q == N):
        print("p % q FOUND!")
        # phi is phi(n) = (p - 1) * (q - 1)
        phi = (p - 1) * (q - 1)
        # e is usually used as pow(2,16) + 1 = 65537
        e = 65537
        # d is the inverse of e mod phi
        d = mod_inv(e, phi)

        print("d: " + str(d))

        # some useful precalculations required by Cryptography library (here is not what you are looking for)
        iqmp = rsa_crt_iqmp(p, q)
        dmp1 = rsa_crt_dmp1(d, p)
        dmq1 = rsa_crt_dmq1(d, q)
        public_numbers = RSAPublicNumbers(e, N)
        secret_key = RSAPrivateNumbers(p, q, d, dmp1, dmq1, iqmp, public_numbers).private_key(default_backend())


        with open(constants.CIPHERED_PATH, 'rb') as f:
            print("Reading ciphered version of text...")
            cipheredDoc = f.read()
        
        decipheredDoc = secret_key.decrypt(cipheredDoc, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ))
        with open("./deciphered-MANUAL.txt", 'wb') as f:
            print("Saving deciphered version of text...")
            f.write(decipheredDoc)

        end = time.time()
        print("h4cK C0mP1et3D !")
    else:
        print("ERROR: p & q not found :(")
    print("Time elapsed: " + str((end-start)/60) + " minutos")
