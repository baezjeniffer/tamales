import numpy as np
import sys
import pandas as pd
from os import walk, listdir, path

def crecimiento(x,y):
    if x is None or y is None:
        return None
    elif y==0:
        return 1
    elif x==0 and y==0:
        return 0
    else:
        return (x-y)/abs(y)

def getDataByListDates(listDates:list, pathArg,file_name):
    listDataFolders = [ path.join(pathArg,x) for x in listdir(pathArg) if x in listDates]
    listDataFrames = []
    for dataFolder in listDataFolders:
        for (root,dirs,files) in walk(dataFolder):
            if len(files)>0:
                listTmpDF = [ pd.read_csv(path.join(root,file),header=None) for file in files if file.startswith(file_name)]
                listDataFrames.extend(listTmpDF)
    
    return pd.concat(listDataFrames).reset_index(drop=True)