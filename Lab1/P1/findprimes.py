from utils import *
import constants
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization.base import Encoding, PublicFormat, NoEncryption
import time
import math
from decimal import Decimal


if __name__ == '__main__':
    start = time.time()
    N =16324242263806929338883691464847939386268272559910745234713482522596883346252671436566260758046042481669745073201307352699391152423741076884860766505705736127747258311463192230866785690542989565215810046683451920587467082692796607938964583205775437240501995117687660359719031987312915277897474397675560756932974705602707659872100871276143977129847971884850971993846558594756000453492744218560883863033384617929627947035740659946069206228443476870736350393045951697130372215782247120135281155412070673811997741431516441261686409896076876776010943787753695553484733709186657296369141671091670961809161833228347698563161
    sqrt_N = int(Decimal(N).sqrt().to_integral_exact())
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
