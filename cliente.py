import os
import hashlib
import string
import socket
import pickle
import time
from phe import paillier
import string

start = time.time()
os.system('hashcat.exe -m 0 -a 1 --force --outfile-format=2 -o outfile_1.txt archivo_1 diccionario_1.dic diccionario_2.dic')
time1 = time.time() - start

start = time.time()
os.system('hashcat.exe -m 10 -a 1 --force --outfile-format=2 -o outfile_2.txt archivo_2 diccionario_1.dic diccionario_2.dic')
time2 = time.time() - start

start = time.time()
os.system('hashcat.exe -m 10 -a 1 --force --outfile-format=2 -o outfile_3.txt archivo_3 diccionario_1.dic diccionario_2.dic')
time3 = time.time() - start

start = time.time()
os.system('hashcat.exe -m 1000 -a 1 --force --outfile-format=2 -o outfile_4.txt archivo_4 diccionario_1.dic diccionario_2.dic')
time4 = time.time() - start

start = time.time()
os.system('hashcat.exe -m 1800 -a 1 --force --outfile-format=2 -o outfile_5.txt archivo_5 diccionario_1.dic diccionario_2.dic')
time5 = time.time() - start

print('Tiempo archivo 1: ',time1,'\n')
print('Tiempo archivo 2: ',time2,'\n')
print('Tiempo archivo 3: ',time3,'\n')
print('Tiempo archivo 4: ',time4,'\n')
print('Tiempo archivo 5: ',time5,'\n')


x = open ('hash_file.txt','w')
for i in range(5):
    f = open ("outfile_"+str(i+1)+".txt","r")
    while True: 
        palabra = f.readline() 
        if not palabra: 
            break

        palabra = hashlib.sha3_256(palabra.encode('utf-8')).hexdigest()   
        x.write(palabra)
        x.write('\n')
    f.close()

x.close()

count = 0
file1 = open('hash_cifrado.txt','w')
file2 = open('hash_file.txt','r')
host = "localhost"
port = 5000
cli = socket.socket()
cli.connect((host, port))
print("Conectado al servidor")
 
while True:
    public_key = cli.recv(2048)
    public_key = pickle.loads(public_key)
    lista = []
    while True:
        hash = file2.readline()

        if not hash:
            break

        hash_utf = hash.encode('utf-8')

        hash_hex = hash_utf.hex()

        hash_int = int(hash_hex,16) 

        e_hash = public_key.encrypt(hash_int)

        file1.write(str(e_hash))
        file1.write('\n')
        lista.append(e_hash)

    file1.close()
    file2.close()
    size = pickle.dumps(len(lista)) 
    cli.send(size)    
    for i in range(len(lista)):
        enviar = pickle.dumps(lista[i])
        cli.send(enviar)    
        time.sleep(1)
    break
cli.close()
