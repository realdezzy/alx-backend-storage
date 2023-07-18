#!/usr/bin/env python3
"""List documents
"""


def list_all(mongo_collection):
    """List all documents in the collection

    Args:
        mongo_collection (Collection): collection

    Returns:
        RawBSONDocument: list of all collection documents
    """
    output = mongo_collection.find()
    if output.count() == 0:
        return []
    return output
    