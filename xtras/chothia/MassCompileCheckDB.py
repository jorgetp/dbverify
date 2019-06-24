import os

def compileFiles():
    for dirName, subDirs, fileNames in os.walk('uncompiled/'):
        for filename in fileNames:
            if filename.endswith(".pi"):
                path = dirName+'/'+filename
                outDir = 'compiled'+'/' + '/'.join(dirName.split('/')[1:])
                outFile = filename[:-3]+"-out.pi"
                outPath = outDir+"/"+outFile
                df = ("-df" in filename)
                if not os.path.exists(outDir):
                    os.mkdir(outDir)
                bashCommand = "./checkdb "
                if df:
                    bashCommand = bashCommand + "-nolocal "
                    #print("Protocol was df!")
                bashCommand = bashCommand + path +" > "+outPath
                #print("bashCommand is: "+bashCommand)
                os.system(bashCommand)
    
    return True

if __name__ == '__main__':      
    compileFiles()