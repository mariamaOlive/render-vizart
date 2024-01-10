import os
from os.path import isfile, join
import pandas as pd

def leituraDados():
    
    folderName = 'static/rescaled_dataset_artistas'
    fileList = []
    for paths, dirs, files in os.walk(folderName):
        for file in files:
            if file.endswith(".jpg"):
                    id = os.path.splitext(file)[0]
                    fileList.append((os.path.join(paths, file), id))

    #Load all dataframes
    dfList = []
    d = 'data/artistas'
    #Json list with all works of the artists
    artistasFiles = [os.path.join(d,o) for o in os.listdir(d) if os.path.isfile(os.path.join(d,o))]

    for artista in artistasFiles:
        dfList.append(pd.read_json(artista, orient='records'))

    dfAll = pd.concat(dfList, ignore_index=True)
    dfAll['contentId'] = dfAll['contentId'].astype(str)

    #Add path to dataframe
    dfFiles = pd.DataFrame(fileList, columns =['path', 'contentId'])
    dfAll = pd.merge(dfAll, dfFiles, on=["contentId"])

    #Remover "sketch and study" e NA
    dfAll = pd.DataFrame(dfAll[dfAll['genre']!="sketch and study"])
    dfAll = dfAll[dfAll['completitionYear'].notna()]

    return dfAll 

def getPaths(artista, ano):
    df = leituraDados()
    df = df[df['artistName']==artista]

    df = df[df['completitionYear']==int(ano)]
    return df[['title', 'genre', 'style', 'path']]
