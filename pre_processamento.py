import pandas as pd
import glob
import csv

def read_csv(args):
    return pd.read_csv(args, encoding='latin1', on_bad_lines='skip')

infantilPath = glob.glob("./dados_brutos/infantil/*.csv")
df = pd.concat(map(read_csv, infantilPath))
df = df.reset_index()  

adultoPath = glob.glob("./dados_brutos/geral/*.csv")
adultoDf = pd.concat(map(read_csv, adultoPath))
adultoDf = adultoDf.reset_index()

dfByCid = pd.DataFrame({})

statesByIndex = {
    1: "RO", 2: "AC", 3: "AM", 4: "RR", 5: "PA", 6: "AP", 7: "TO", 8: "MA", 9: "PI", 10: "CE", 11: "RN", 12: "PB", 13: "PE", 14: "AL", 15: "SE", 16: "BA", 17: "MG", 18: "ES", 19: "RJ", 20: "SP", 21: "PR", 22: "SC", 23: "RS", 24: "MS", 25: "MT", 26: "GO", 27: "DF"
}

def breakItem(row):
    return str(row[1]).split(";")

def getCid(item):
    return item[0].split(" ")[0]

def removeUnnecessaryCids(df):
    for index, row in df.iterrows():
         breakedItem = breakItem(row)
         cid = getCid(breakedItem)
         # cids de cancer começam com C, alem do D46
         if "C" not in cid and "D46" not in cid:
             df.drop(index, inplace=True)

def separateDataByCid(df):
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
    mutedItem = item.split(";")
    correctedItem = [mutedItem[0]]

    correctedItem.append({ "ESTADOS": {}, "TOTAL": int(mutedItem[28])  })

    for index, row in enumerate(mutedItem[1:28]):
        correctedRow = row
   
        if row == "-":
            correctedRow = 0 

        correctedItem[1]["ESTADOS"][statesByIndex[index + 1]] = int(correctedRow)

    return correctedItem 

def organizeEachIndividualState(data):
    dict = {
        data[0][0]: { "ESTADOS": data[0][1]["ESTADOS"], "TOTAL": data[0][1]["TOTAL"] }
    }
    
    for _, cid in enumerate(data[1:]):
        for key, item in cid[1].items():
            if key == "ESTADOS":
                for stateKey, value in item.items():
                    dict[data[0][0]]["ESTADOS"][stateKey] += int(value)
            else:
                dict[data[0][0]]["TOTAL"] += int(item)

    return dict

def organizeDataByState(df):
    dataWithState = []

    for _, row in df.iterrows():
        for cid in row:
            mutableCid = cid

            for index, row in enumerate(cid):
                mutableCid[index] = correctStateInItem(row)    

            dataWithState.append(organizeEachIndividualState(mutableCid))

    return dataWithState

def exportProcessedCSV(data, outputName):
    fields = ["CID","RO","AC","AM","RR","PA","AP","TO","MA","PI","CE","RN","PB","PE","AL","SE","BA","MG","ES","RJ","SP","PR","SC","RS","MS", "MT", "GO", "DF", "TOTAL" ]
    
    with open(outputName, "w", newline='') as output:
        header = ",".join(fields) + "\n"
        output.write(header)
        w = csv.DictWriter(output, fields)
        for item in data:
            for key, val in sorted(item.items()):
                row = {'CID': key }

                for keyState, state in val["ESTADOS"].items():
                    row.update({ keyState: state })

                row.update({ "TOTAL": val["TOTAL"]  })
                w.writerow(row)

def processDataAndExport(df, exportFileName):
    removeUnnecessaryCids(df)
    dfByCid = separateDataByCid(df)
    stateDict = organizeDataByState(dfByCid)
    exportProcessedCSV(stateDict, exportFileName)


if __name__ == '__main__':
    print("------------------------------------------")
    print("---- Realizando o pré-processamento dos dados brutos -------")
    print("----------- Aguarde um momento -----------")
    print("------------------------------------------")
    
    print("")
    print("Processando os dados infantis...")
    print("")

    processDataAndExport(df, "dados_infantis.csv")

    print("")
    print("Processando os dados de adultos...")
    print("")

    processDataAndExport(adultoDf, "dados_adultos.csv")

    print("------------------------------------------")
    print("---- Processamento finalizado com sucesso! -------")
    print("----------- Para ver os dados, acesse os arquivos: 'dados_infantis.csv' e; 'dados_adultos.csv' -----------")
    print("------------------------------------------")