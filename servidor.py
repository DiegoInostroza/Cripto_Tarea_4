from phe import paillier
import socket 
import pickle
import time
import codecs
import sqlite3
from sqlite3 import Error




def connection():
    try:
        connection = sqlite3.connect('cripto.bd')
        return connection
    except Error:
        print(Error)

def table(connection):
    cursorObj = connection.cursor()
    cursorObj.execute("DROP table IF EXISTS HashSHA3_256")
    cursorObj.execute("CREATE TABLE HashSHA3_256(id integer PRIMARY KEY, Archivo_n°, Data)")
    connection.commit()

def insert(connection, obj):
    cursorObj = connection.cursor()
    cursorObj.execute('INSERT INTO HashSHA3_256(id,Archivo_n°,Data) VALUES(?, ?, ?)', obj)
    connection.commit()

def fetch(connection):
    cursorObj = connection.cursor()
    cursorObj.execute('SELECT * FROM HashSHA3_256')
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)


connection = connection()
table(connection)
public_key, private_key = paillier.generate_paillier_keypair()

pb = pickle.dumps(public_key)

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("localhost", 5000))
servidor.listen(1)
cliente, addr = servidor.accept()


 
while True:
    cliente.send(pb)
    print("Enviado")
    size = cliente.recv(2048)
    size = pickle.loads(size)
    print(size)
    count = 1 
    lista = []
    for i in range(size):
        lista.append(cliente.recv(2048))

    for i in range(size):

        hash_enc = pickle.loads(lista[i])

        hash_dec = private_key.decrypt(hash_enc)

        hash_hex = hex(hash_dec)

        aux = hash_hex[2:len(hash_hex)]

        hash = codecs.decode(aux, "hex").decode('utf-8') 

        if(i>=102 and i<204):
            count = 2

        if (i>=204 and i<1204):
            count = 3
        
        if(i>=1204 and i<1310):
            count = 4
        
        if (i>=1310):
            count = 5

        obj = (i ,"Hash Archivo N° "+str(count),hash)

        
        insert(connection, obj)


    break
cliente.close()

fetch(connection)
