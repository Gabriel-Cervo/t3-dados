import pandas as pd
import glob
import csv
import itertools
import sys

cancerCidsNumber = (00, 97)

def read_csv(args):
    return pd.read_csv(args, encoding='latin1', on_bad_lines='skip')

path = glob.glob("./dados_brutos/*.csv")
df = pd.concat(map(read_csv, path))
df = df.reset_index()  

dfByCid = pd.DataFrame({})

statesByIndex = {
    1: "RO", 2: "AC", 3: "AM", 4: "RR", 5: "PA", 6: "AP", 7: "TO", 8: "MA", 9: "PI", 10: "CE", 11: "RN", 12: "PB", 13: "PE", 14: "AL", 15: "SE", 16: "BA", 17: "MG", 18: "ES", 19: "RJ", 20: "SP", 21: "PR", 22: "SC", 23: "RS", 24: "MS", 25: "MT", 26: "GO", 27: "DF"
}

def breakItem(row):
    return str(row[1]).split(";")

def getCid(item):
    return item[0].split(" ")[0]

def removeUnnecessaryCids():
    for index, row in df.iterrows():
         breakedItem = breakItem(row)
         cid = getCid(breakedItem)
         # cids de cancer começam com C, alem do D46
         if "C" not in cid and "D46" not in cid:
             df.drop(index, inplace=True)

def separateDataByCid():
    dataByCids = {}

    for _, row in df.iterrows():
        breakedItem = breakItem(row)
        cid = getCid(breakedItem)
        
        if cid not in dataByCids:
            dataByCids[cid] = [str(row[1])]
        else:
            dataByCids[cid] = dataByCids[cid] + [str(row[1])]

    return pd.DataFrame({
        'Categoria_CID;RO;AC;AM;RR;PA;AP;TO;MA;PI;CE;RN;PB;PE;AL;SE;BA;MG;ES;RJ;SP;PR;SC;RS;MS;MT;GO;DF;Total': dataByCids 
    })

def correctStateInItem(item):
    print(item)
    print("::::::")
    mutedItem = item.split(";")
    correctedItem = [mutedItem[0]]

    for index, row in enumerate(mutedItem[1:27]):
        if row is not "-":
            correctedItem.append(statesByIndex[index + 1])

    correctedItem.append(mutedItem[28])
    return correctedItem 

def organizeByIndividualState(cids):
    total = 0

    cidWithAttr = {
        cids[0][0]: {}
    }

    for cid in cids:
        for key, state in statesByIndex.items():
            cidWithAttr[cid[0]][state] = 0

        for attr in cid[1:-1]:
            cidWithAttr[cid[0]][attr] = int(cidWithAttr[cid[0]][attr]) + int(cid[-1])

    cidWithAttr[cid[0]]["TOTAL"] = 0
    return cidWithAttr

def organizeDataByState():
    dataWithState = []

    for _, row in dfByCid.iterrows():
        for cid in row:
            mutableCid = cid

            for index, row in enumerate(cid):
                mutableCid[index] = correctStateInItem(row)    
            
            dataWithState.append(organizeByIndividualState(mutableCid))

    return dataWithState

def exportProcessedCSV(data):
    fields = ["CID","RO","AC","AM","RR","PA","AP","TO","MA","PI","CE","RN","PB","PE","AL","SE","BA","MG","ES","RJ","SP","PR","SC","RS","MS", "MT", "GO", "DF", "TOTAL" ]

    with open("test_output.csv", "w") as output:
        w = csv.DictWriter(output, fields)
        for item in data:
            for key, val in sorted(item.items()):
                row = {'CID': key }
                row.update(val)
                w.writerow(row)

if __name__ == '__main__':
    print("------------------------------------------")
    print("---- Realizando o pré-processamento dos dados brutos -------")
    print("----------- Aguarde um momento -----------")
    print("------------------------------------------")

    removeUnnecessaryCids()

    dfByCid = separateDataByCid()

    stateDict = organizeDataByState()
    exportProcessedCSV(stateDict)