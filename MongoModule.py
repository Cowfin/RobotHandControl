def get_database():
    import pymongo

    CONNECTION_STRING = 'Mongo URL here'

    try:
        client = pymongo.MongoClient(CONNECTION_STRING,
                                     connectTimeoutMS=30000,
                                     socketTimeoutMS=None)
        print("Connection successful")
    except:
        print("Unsuccessful")

    return client


if __name__ == "__main__":

    dbname = get_database()
