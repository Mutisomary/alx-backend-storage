#!/usr/bin/env python3
"""Using the Pymongo module"""


def list_all(mongo_collection):
    """return documents in a collection"""
    documents = mongo_collection.find({})
    if documents == 0:
        return []
    else:
        return documents
