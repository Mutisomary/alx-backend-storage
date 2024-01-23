#!/usr/bin/env python3
"""Using the pymongo module"""


def update_topics(mongo_collection, name, topics):
    """Update the document with the specified name
    and set the new topics"""
    result = mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
