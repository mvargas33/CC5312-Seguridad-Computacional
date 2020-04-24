# Lab1-P1

_(This repository makes sense in CC5312 - Computer Security course)_

Behold! The best RSA key generation algorithm of the world!

This is an example of how to use my excellent key generation function.

### How to use

```bash
pip install requirements.txt
python main.py
```

The previous command will create three files:
* `plaintext.txt`: A random latin-like sentence (thanks to `lorem` library)
* `ciphered.txt`: The previous latin-like sentence, ciphered with a random Public RSA key.
* `deciphered.txt`:  The previous ciphered text, deciphered with the correspondent Private RSA Key (This is to show you that my keys work!)
* `public_key.pem`: Public Key that encrypted the message.

Given the private key is lost, I guarantee that you will never be able to decipher the ciphered text!
