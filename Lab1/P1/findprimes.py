from utils import *
import constants
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization.base import Encoding, PublicFormat, NoEncryption
import time


if __name__ == '__main__':
    start = time.time()
    A = 1 # Next prime de 2
    B = 2**860 - 1
    N = 831677144048211101826106378525395849642437600911548240408051478026348423287759281146588736896229892448714738199299739927904680347414422068035842874423011267641499302808777460602659600095379967012412865393606374656175490561022979622257999806193675319996819687
    e = 65537
    d = 0
    # p = 911963345781074197788086250371769804887067889359350261355514227218930922528828667463921558189570967769024858500782098386636596773
    # q = 911963345781074197788086250371769804887067889359350261355514227218930922528828667463921558189570967769024858500782098386636597019

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
    print("Time elapsed: " + str((end-start)/60) + " minutos")
