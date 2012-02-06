#!/usr/bin/env python
# -*- encoding: utf-8 -*-

try:
    import simplejson as json
except ImportError:
    import json


class Resource(object):

    _dates = ()
    _maps = {}
    _collection_maps = {}

    def __init__(self, attrs):
        """ """
        self._attrs = attrs
        self.__set_attrs()

    def __set_attrs(self):
        for attr in self._attrs:
            setattr(self, attr, self._attrs[attr])

    @classmethod
    def loads(self, json_content):
        resource_chunk = json.loads(json_content)
        if not hasattr(resource_chunk, 'items'):
            return [self.__load(raw_resource)
                    for raw_resource in resource_chunk]
        else:
            return self.__load(resource_chunk)

    @classmethod
    def __load(self, raw_resource):
        def parse_date(string_date):
            from datetime import datetime
            try:
                date = datetime.strptime(string_date, '%Y-%m-%dT%H:%M:%SZ')
            except TypeError:
                date = None
            return date

        def parse_map(resource, raw_resource):
            if hasattr(raw_resource, 'items'):
                return resource.__load(raw_resource)

        def parse_collection_map(resource, raw_resources):
            # Dict of resources (Ex: Gist file)
            if hasattr(raw_resources, 'items'):
                dict_map = {}
                for key, raw_resource in raw_resources.items():
                    dict_map[key] = resource.__load(raw_resource)
                return dict_map
            # list of resources
            elif hasattr(raw_resources, '__iter__'):
                return [resource.__load(raw_resource)
                        for raw_resource in raw_resources]
        raw_resource.update(
            {attr: parse_date(raw_resource[attr])
             for attr in self._dates if attr in raw_resource})
        raw_resource.update(
            {attr: parse_map(resource, raw_resource[attr])
             for attr, resource in self._maps.items()
             if attr in raw_resource})
        raw_resource.update(
            {attr: parse_collection_map(resource, raw_resource[attr])
             for attr, resource in self._collection_maps.items()
             if attr in raw_resource})

        return self(raw_resource)


class Raw(Resource):

    @classmethod
    def loads(self, json_content):
        return json.loads(json_content)