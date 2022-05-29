import json


def StoreUserData(data,FileName):
    if (data):
        with open(FileName, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        print(data)

def ReadUserData(FileName):
    ReadData = {}
    try:
        with open(FileName, 'r', encoding='utf-8') as f:
            ReadData = json.load(f)
    except:
            print (FileName, "Bad File Format")

    return ReadData