from pymongo import MongoClient

"""
WILL LIKELY NEED TO CHANGE CLIENT FOR HEROKU USE
"""
client = MongoClient("mongodb+srv://heroku:herokupass@footballpicker-cluster.yqjdz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
col = client.football_picks
db = col.data

# insert object into database
def ins(dict0):
    dict1 = {
        "week": dict0["week"],
        "name": dict0["name"]
    }
    
    # checks if object already exists
    dup = db.count_documents(dict1)
    
    # if it does not exist create new object
    if dup <= 0:
        result = db.insert_one(dict0)
        print(f'Added to database with id {result.inserted_id}')
    # if it does exist replace data with updated data
    else:
        try:
            dataId = db.find_one(dict0)['_id']
            db.replace_one({'_id': dataId}, dict0)
            print(f"Replaced duplicate at id {dataId}")
        except:
            print("No duplicates present")

def find(week, name):
    dict0 = {
        "week": week,
        "name": name
    }
    fnd = db.find_one(dict0, {'_id': False})
    return fnd

def find_all(week):
    arr = []

    cursor = db.find({"week": week}, {'_id': False})
    for document in cursor:
        arr.append(document)
    return arr
