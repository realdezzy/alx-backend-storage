#!/usr/bin/env python3
"""Find school by topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school having a specific topic

    Args:
        mongo_collection (Collection): pymongo collection object
        topic (str): topic searched
    """
    query = {"topics": topic}
    return mongo_collection.find(query)
