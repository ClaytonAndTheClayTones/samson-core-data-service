from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Generic, TypeVar
from uuid import UUID
import uuid

T_in = TypeVar('T_in')
T_out = TypeVar('T_out')
TRangeSearchable = TypeVar('TRangeSearchable', str, int, float, datetime)
TListSearchable = TypeVar('TListSearchable', str, int, float)


class CommonUtilities:

    def convert_comma_delimited_ids_to_uuid_list(self, string: str):
        returnlist: list[UUID] = []

        str_list = string.split(',')

        for x in str_list:
            returnlist.append(uuid.UUID(x))

        return returnlist

    def validate_comma_delimited_ids(self, ids_string: str):

        if ids_string is None:
            return None

        errors: dict[int, str] = {}

        ids = ids_string.split(',')

        for index, x in enumerate(ids):
            try:
                UUID(x, version=4)
            except ValueError:
                errors[index] = x

        if len(errors.keys()) > 0:
            return errors
        else:
            return None

    def generate_invalid_comma_delimited_ids_message(self, errors):
        message = f'Property must be a valid list of v4 uuids. Invalid values received: ['

        for i, key in enumerate(errors.keys()):

            message += f'\n\t{key}: {errors[key]}'

            if i != len(errors.keys()) - 1:
                message += f','

        message += '\n].'

        return message

    def convert_uuid_list_to_string_list(self, uuids: list[UUID]):
        resultlist = [str(x) for x in uuids]
        return resultlist