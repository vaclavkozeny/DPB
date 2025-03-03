import time
MyPath = "/home/vaclav/Stažené/data.txt"
MyOutPath = "./out.txt"
MyDecryptedPath = "./decrypted.txt"
MyKey = 69
def cypher(inPath, outPath):
    f = open(outPath,"w")
    with open(inPath) as fileobj:
        for line in fileobj:  
            for ch in line: 
                f.write(chr(ord(ch)^MyKey))
    f.close()

def decrypt(inPath, decryptedPath):
    cypher(inPath, decryptedPath)

start = time.time()
cypher(MyPath,MyOutPath)
end = time.time()
cas = end - start
print(f'Sifrovani: {cas}')

start = time.time()
decrypt(MyOutPath,MyDecryptedPath)
end = time.time()
cas = end - start
print(f'Desifrovani {cas}')