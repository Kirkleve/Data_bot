import json


def OpenDataBase():
    try:
        with open(r"Data.json", "r", encoding="utf-8") as fh:
            db = json.load(fh)
            db["persons"] = {int(k): v for k, v in db["persons"].items()}
            db["city"] = {int(k): v for k, v in db["city"].items()}
            return db
    except:
        return {"persons": {}, "city": {}}


def SaveDataBase(directory):
    with open(r"Data.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(directory, ensure_ascii=False))


def GetCityID(database, city):
    if city in [n[0] for n in database["city"].values()]:
        for k, v in database["city"].items():
            if city == v[0]:
                return k
    else:
        return None

def AddCity(database, city):
    cityID = GetCityID(database, city)
    if cityID is None:
        if len(database["city"]) == 0:
            cityID = 1
        else:
            cityID = max(database["city"].keys()) + 1
        database["city"][cityID] = [city]
    return cityID

def GetAllCity(database):
    return [(id, node[0]) for id, node in database["city"].items()]

def AddPerson(database, name, tel, city):

    if len(database["persons"]) == 0:
        personID = 1
        database["persons"][personID] = [personID]
    else:
        personID = max(database["persons"].keys()) + 1
    database["persons"][personID] = [name, tel, city]


def GetPerson(database, id):
    if id in database["persons"]:
        return (
            id,
            database["persons"][id][0],
            database["persons"][id][1],
            database["city"][database["persons"][id][2]][0],
        )
    else:
        return None


def GetAllPersons(database):
    return [GetPerson(database, key) for key in database["persons"].keys()]


def GetFilterPersonID(database, search):
    return [k for k, v in database["persons"].items() if search.lower() in v[0].lower()]


def GetFilterPerson(database, search):
    return [GetPerson(database, k) for k, v in database["persons"].items() if search.lower() in v[0].lower()]


def RemovePerson(database, id):
    database["persons"].pop(id, None)