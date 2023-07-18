#!/usr/bin/env python3
"""Insert operation
"""


def insert_school(mongo_collection, **kwargs):
    """insert a new document

    Args:
        mongo_collection (Collection): collection object

    Returns:
        _id (int): id of the new document
    """
    return mongo_collection.insert(kwargs)