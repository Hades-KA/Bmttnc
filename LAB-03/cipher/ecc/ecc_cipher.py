import ecdsa, os
if not os.path.exists('LAB-03/cipher/ecc/keys'): 
    os.makedirs('LAB-03/cipher/ecc/keys')
class ECCCipher:
    def _init__(self):
        pass
    def generate_keys(self):
        sk = ecdsa.SigningKey.generate()
        vk  = sk.get_verifying_key()
        with open('LAB-03/cipher/ecc/keys/privateKey.pem', 'wb') as p:
            p.write(sk.to_pem())
        with open('LAB-03/cipher/ecc/keys/publickey.pem', 'wb') as p:
            p.write(vk.to_pem())
    def load_keys(self):
        with open('LAB-03/cipher/ecc/keys/privateKey.pem', 'rb') as p:
            sk = ecdsa.SigningKey.from_pem(p.read())
        with open('LAB-03/cipher/ecc/keys/publickey.pem', 'rb') as p:
            vk = ecdsa.VerifyingKey.from_pem(p.read())
        return sk, vk
    def sign(self, message, key):
        # Sign data with private key
        return key.sign(message.encode('ascii'))
    def verify(self, message, signature, key): 
        _, vk = self.load_keys()
        try: 
            return vk.verify(signature, message.encode('ascii'))
        except ecdsa.BadSignatureError:
            return False