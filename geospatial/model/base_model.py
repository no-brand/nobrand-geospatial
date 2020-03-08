# -*- coding: utf-8 -*-

from boto3.dynamodb.types import *
from abc import ABC, abstractmethod


class BaseModel(ABC):

    @abstractmethod
    def __dict__(self):
        pass

    def serialize_to_ddb(self, type_nested=False):
        """
        get dict, representing a dynamodb data type.
        :param type_nested: boolean, to determine between original dict and dynamodb's type defined type.

            type_nested = False (Python)            type_nested = True (DynamoDB)
            ------                                  --------
            None                                    {'NULL': True}
            True/False                              {'BOOL': True/False}
            int/Decimal                             {'N': str(value)}
            string                                  {'S': string}
            Binary/bytearray/bytes (py3 only)       {'B': bytes}
            set([int/Decimal])                      {'NS': [str(value)]}
            set([string])                           {'SS': [string])
            set([Binary/bytearray/bytes])           {'BS': [bytes]}
            list                                    {'L': list}
            dict                                    {'M': dict}

        :rtype: dict
        :return: a dictionary that can be directly passed to dynamodb.
        """
        def __serialize(x):
            if isinstance(x, list):
                return [__serialize(sub_x) for sub_x in x]
            elif isinstance(x, BaseModel):
                return x.serialize_to_ddb(type_nested=type_nested)
            elif isinstance(x, float):
                x = round(Decimal(x), 10)
            return TypeSerializer().serialize(x) if type_nested else x

        params = self.__dict__()
        return {k: __serialize(v) for k, v in params.items()}

    def serialize_to_elastic(self):
        """
        get dict the represents a elasticsearch data type.
        :rtype: dict
        :returns: a dictionary that can be directly passed to index into elasticsearch.
        """
        params = self.__dict__()
        return params
