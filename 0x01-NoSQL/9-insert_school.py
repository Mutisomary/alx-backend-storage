#!/usr/bin/env python3
"""Using the pymongo module"""


def insert_school(mongo_collection, **kwargs):
    """"insert a new document"""
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
