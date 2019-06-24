import os
import subprocess

def compileFiles():
    outputstring = ''
    lastProtocol = ''
    for dirName, subDirs, fileNames in os.walk('compiled/'):
        for filename in fileNames:
            if filename.endswith(".pi"):
                path = dirName+'/'+filename
                proverifResult = subprocess.Popen(['proverif',path],
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE).communicate()[0]
                #print(str(proverifResult[-8:]))
                splits = filename.split('-')
                protocolName = splits[0]
                if lastProtocol != protocolName:
                    print('-----------------------------------')
                lastProtocol = protocolName
                attackName = splits[-2]
                if "true" in str(proverifResult[-8:]):
                    print("Protocol:", protocolName, ". Attack: ", attackName, "SECURE")
                elif "false" in str(proverifResult[-8:]):
                    print("Protocol:", protocolName, ". Attack: ", attackName, "ATTACK")
                else:
                    print("Input failed for file: ", filename,"!")
    
    return True

if __name__ == '__main__':      
    compileFiles()