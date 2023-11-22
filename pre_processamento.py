import pandas as pd
import glob

cancerCidsNumber = (00, 97)

def read_csv(args):
    return pd.read_csv(args, encoding='latin1', on_bad_lines='skip')

dfUpdated = pd.DataFrame({})
path = glob.glob("./dados_brutos/*.csv")
df = pd.concat(map(read_csv, path))
df = df.reset_index()  

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
            dataByCids[cid] = [breakedItem]
        else:
            dataByCids[cid] = dataByCids[cid] + breakedItem

    df.drop(df.index, inplace=True)

    return pd.DataFrame({
        'Categoria_CID;RO;AC;AM;RR;PA;AP;TO;MA;PI;CE;RN;PB;PE;AL;SE;BA;MG;ES;RJ;SP;PR;SC;RS;MS;MT;GO;DF;Total': dataByCids 
    })


if __name__ == '__main__':
    print("------------------------------------------")
    print("---- Começando o pré-processamento -------")
    print("----------- Aguarde um momento -----------")
    print("------------------------------------------")

    removeUnnecessaryCids()

    dfUpdated = separateDataByCid()
