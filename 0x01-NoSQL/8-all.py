#!/usr/bin/env python3
"""List documents
"""
from bson.raw_bson import RawBSONDocument
from pymongo.collection import Collection


# def list_all(mongo_collection: Collection) -> RawBSONDocument:
def list_all(mongo_collection):
    """List all documents in the collection

    Args:
        mongo_collection (Collection): collection

    Returns:
        RawBSONDocument: list of all collection documents
    """
    output = mongo_collection.find()
    if len(output) == 0:
        return []
    else:
        return output
    
if __name__ == "__main__":
    pass