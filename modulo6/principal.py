#import datetime #para el tiemstamp de cada block
import hashlib # para usar SHA256
from flask import Flask, jsonify , request


#Esta clase representa a un bloque de blockChain
class Block:
    def __init__(self, data, previous_hash, hash="", nonce=0):
        self.nonce= nonce
        self.data=data
        self.previous_hash=previous_hash
        self.hash=hash
        
    def __dict__(self) -> dict:
        return {
            "nonce":self.nonce,
            "data":self.data,
            "previous_hash":self.previous_hash,
            "hash":self.hash
        }

#Clase para crear el BlockChain
class Blockchain:
    def __init__(self):
        self.chain=[] #aquí se almacenan las cadenas de bloques
        self.create_block(Block(data="genesis", previous_hash="0"*64))
    
    #Metodo usado para crear el Bloque
    def create_block(self, block:Block)->Block:
        res=self.proof_of_work(block=block)
        if res!=None and  res:
            self.chain.append(block)
        else:
            raise Exception("Error al añadir Bloque")
        return block
    
    def get_previous_hash(self):
        return self.chain[-1].hash
    
    #proof of work para 4 ceros este se implementa
    #cada vez que agregas un nuevo bloque
    def proof_of_work(self, block:Block)->bool:
        nonce=0
        while True:
            hash=hashlib.sha256((block.data+block.previous_hash+str(nonce)).encode()).hexdigest()
            if hash[:4] == '0000':
                block.nonce=nonce
                block.hash=hash
                return True
            nonce+=1
    
    #Método para validar si el blockchain es válido 
    def is_chain_valid(self, chain):
        previous_block=chain[0]
        block_index=1
        while block_index< len(chain):
            previous_hash=previous_block.hash
            block_hash=chain[block_index].previous_hash
            if not ((previous_hash==block_hash) and  (block_hash[:4]=='0000' and previous_hash[:4]=="0000")):
                return False
            previous_block=chain[block_index]
            block_index+=1
        return True
            
                
                
            
            
        
#Crear Servicio web         
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Crear Blockchain
blockchain= Blockchain()

#Metodo para crear Bloque
@app.route('/block', methods = ['GET'])
def  crear_bloque():
    parameters=request.args
    data=parameters.get("data", default="", type=str)
    previous_hash=blockchain.get_previous_hash()
    response={}
    block=None
    try:
        block=blockchain.create_block(Block(data=data, previous_hash=previous_hash))
    except Exception as ex:
        response["Error"]=ex.__str__()
    if block!=None:
        response['block']=block.__dict__()
    
    return jsonify(response), 200

@app.route('/chain', methods = ['GET'])
def get_chain():
    lista=[]
    for tmp in blockchain.chain:
        lista.append(tmp.__dict__())
    response={'chain':lista}
    return jsonify(response), 200
    
        
    

    
    
    
    
       
if __name__=="__main__":
    app.run(host='0.0.0.0', port = 5000)
    
    '''
    blockchain=Blockchain()
    previous_hash=blockchain.get_previous_hash()
    block=Block("mis datos", previous_hash=previous_hash)
    blockchain.create_block(block)
    previous_hash=blockchain.get_previous_hash()
    block=Block("Otros", previous_hash=previous_hash)
    blockchain.create_block(block)
    for tmp in blockchain.chain:
        print(tmp.__dict__())
    
    print(blockchain.is_chain_valid(blockchain.chain))'''
    
    
    
    
        
        
        







