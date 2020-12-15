import sys
import pandas as pd
from os import walk, listdir, path

def getDataByListDates(listDates:list, pathArg):
    listDataFolders = [ path.join(pathArg,x) for x in listdir(pathArg) if x in listDates]
    listDataFrames = []
    for dataFolder in listDataFolders:
        for (root,dirs,files) in walk(dataFolder):
            if len(files)>0:
                print(files)
                listTmpDF = [ pd.read_csv(path.join(root,file),header=None) for file in files]
                listDataFrames.extend(listTmpDF)
    
    return pd.concat(listDataFrames).reset_index(False)
            

def main():
    pathArg = ""
    if len(sys.argv) >= 2:
        pathArg = str(sys.argv[1])
        print("path: "+ pathArg)
    else:
        print ('Argument List:'+ str(sys.argv) )
        print ("Se requiere como argumento el path raíz donde se encuentran los datos")
        exit()

    print("path: " + pathArg)

    print(getDataByListDates(['20200101','20200107', '20200104'],pathArg).head())


if __name__ == "__main__":
    main()