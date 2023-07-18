#!/usr/bin/env python3
"""
Update topics
"""


def update_topics(mongo_collection, name, topics):
    """Update topics based on name

    Args:
        mongo_collection (Collection): collection object
        name (str): name for filtering topics
        topics (str): topics to update
    """
    filter = {"name": name}
    values =  {"$set": {"topics": topics}}

    mongo_collection.update_many(filter, values)
