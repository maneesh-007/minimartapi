from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()

def hash_password(password:str):
    return password_hasher.hash(password)

def verify_pasword(plain_password:str,hash_password:str):
    return password_hasher.verify(plain_password,hash_password)

