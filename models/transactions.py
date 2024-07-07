from extensions import mongo


class DatabaseError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def get_collection(db_name, collection_name):
    try:
        return mongo.cx[db_name][collection_name]
    except Exception as error:
        raise DatabaseError(f"Error retrieving {collection_name} collection: {str(error)}")


def get_by_id(db_name, collection_name, user_id):
    try:
        return get_collection(db_name, collection_name).find_one({"_id": user_id})
    except Exception as error:
        raise DatabaseError(
            f"Error retrieving record from collection {collection_name} in {db_name}: {str(error)}")


def find_one(db_name, collection_name, filter_dict):
    try:
        return get_collection(db_name, collection_name).find_one(filter_dict)
    except Exception as error:
        raise DatabaseError(
            f"Error retrieving record from collection {collection_name} in {db_name}: {str(error)}")


def insert_one(db_name, collection_name, document):
    try:
        get_collection(db_name, collection_name).insert_one(document)
    except Exception as error:
        raise DatabaseError(
            f"Error inserting record into collection {collection_name}: {str(error)}")


def delete_one(db_name, collection_name, filter_dict):
    try:
        get_collection(db_name, collection_name).delete_one(filter_dict)
    except Exception as error:
        raise DatabaseError(f"Error deleting record from {collection_name}: {str(error)}")


def update_one(db_name, collection_name, filter_dict, update):
    try:
        get_collection(db_name, collection_name).update_one(filter_dict, update)
    except Exception as error:
        raise DatabaseError(f"Error updating record from {collection_name}: {str(error)}")
