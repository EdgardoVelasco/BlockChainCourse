import hashlib

def proofOfWork(data:str):
    hash_resultado=""
    nonce=0
    while True:
        if hash_resultado[:4] !="0000":
            cadena=(data+str(nonce)).encode()
            hash_resultado=hashlib.sha256(cadena).hexdigest()
            nonce+=1
        else:
            break
    return {"hash":hash_resultado, "nonce":nonce}
            


if __name__=="__main__":
    print("Proof of Work".center(40,"•"))
    data="mis datos" #cambiar con tus datos
    resultado=proofOfWork(data)
    print("Salida de la prueba de trabajo")
    print(resultado)