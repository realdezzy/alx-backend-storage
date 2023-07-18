#!/usr/bin/env python3
"""List documents
"""
from bson.raw_bson import RawBSONDocument
from pymongo.collection import Collection


def list_all(mongo_collection: Collection) -> RawBSONDocument:
    """List all documents in the collection

    Args:
        mongo_collection (Collection): collection

    Returns:
        RawBSONDocument: list of all collection documents
    """
    return mongo_collection.find()