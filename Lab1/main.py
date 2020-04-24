import lorem
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization.base import Encoding, PublicFormat, NoEncryption

import constants
import utils

if __name__ == "__main__":
    print("Creating a random document...")
    # creating a new 2048 bit rsa key
    print("Creating a new 2048 bit RSA key...")
    sk = utils.new_rsa_key(2048)
    pk = sk.public_key()
    print("the key has N = {} and e = {}".format(utils.get_n(pk), utils.get_e(pk)))
    print("Creating a random latin-like sentence...")
    doc = lorem.sentence()
    print("Encrypting sentence...")
    cipheredDoc = sk.public_key().encrypt(doc.encode(), padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    ))
    with open(constants.PLAINTEXT_PATH, 'w') as f:
        print("Saving plain text version of text...")
        f.write(doc)
    with open(constants.PUBLIC_KEY_PATH, 'wb') as f:
        print("Saving public key...")
        f.write(sk.public_key().public_bytes(Encoding.PEM, PublicFormat.PKCS1))
    with open(constants.CIPHERED_PATH, 'wb') as f:
        print("Saving ciphered version of text...")
        f.write(cipheredDoc)
    decipheredDoc = sk.decrypt(cipheredDoc, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    ))
    with open(constants.DECIPHERED_PATH, 'wb') as f:
        print("Saving deciphered version of text...")
        f.write(decipheredDoc)
    print("Done!")
