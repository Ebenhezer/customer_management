import secrets
import hashlib

class Utilities:
    
    def getToken(self):
        token = secrets.token_hex(20)
        return token
    
    def getApiKey(self):
        token = secrets.token_hex(25)
        return token
    
    def hash_password(self, password):
        return hashlib.sha256(str.encode(password)).hexdigest()

    def check_hash(self, password, hash):
        if self.hash_password(password) == hash:
            #Password matches
            return True
        # Password don't match
        return False