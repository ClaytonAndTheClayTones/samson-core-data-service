

from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Generic, TypeVar
from uuid import UUID  

T = TypeVar("T")
TRangeSearchable = TypeVar("TRangeSearchable", str, int, float, datetime) 
TListSearchable = TypeVar("TListSearchable", str, int, float, UUID)

class PagingModel: 
    def __init__(self, 
                 page: int | None = None,
                 page_length: int | None = None,
                 sort_by: str | None = None,
                 is_sort_descending: bool | None = None) -> None:
        
        self.page = page
        self.page_length = page_length
        self.sort_by = sort_by
        self.is_sort_descending = is_sort_descending

class ResultantPagingModel: 
    def __init__(self, 
                 page: int,
                 page_length: int,
                 sort_by: str,
                 is_sort_descending: bool,
                 total_record_count: int | None = None) -> None:
        
        self.page = page
        self.page_length = page_length
        self.sort_by = sort_by
        self.is_sort_descending = is_sort_descending
        self.total_record_count = total_record_count

class LikeComparatorModes(Enum):
    Like = "Like",
    StartsWith = "StartsWith",
    EndsWith = "EndsWith"

class SearchTerm:
    @abstractmethod 
    def generate_sql():
        raise NotImplementedError()

    def __init__(self, column_name) -> None:
        self.column_name = column_name
    
class ExactMatchSearchTerm(SearchTerm, Generic[T]):
        
    def __init__(self, column_name, value, ignore_case = False) -> None:
        super().__init__(column_name)

        self.value = value
        self.ignore_case = ignore_case

    def generate_sql(self):
        sqlstring: str = ""
        
        if(self.ignore_case):
            sqlstring = f"LOWER({self.column_name}) = LOWER('{self.value}')"
        else:
            sqlstring = f"{self.column_name} = '{self.value}'"

        return sqlstring


class LikeSearchTerm(SearchTerm):
    def __init__(self, column_name, value, comparator_mode: LikeComparatorModes = LikeComparatorModes.Like, ignore_case = True) -> None:
        super().__init__(column_name)

        self.value = value
        self.ignore_case = ignore_case
        self.comparator_mode = comparator_mode

    def generate_sql(self):
        sqlstring: str = ""
        sql_value_string = ""
        sql_command_string = ""

        # value
        if(self.comparator_mode == LikeComparatorModes.Like):
            sql_value_string = f"%{self.value}%"
        if(self.comparator_mode == LikeComparatorModes.StartsWith):
            sql_value_string = f"{self.value}%"
        if(self.comparator_mode == LikeComparatorModes.EndsWith):
            sql_value_string = f"%{self.value}"
        
        # command
        sql_command_string = "ILIKE" if self.ignore_case else "LIKE"

        sqlstring = f"{self.column_name} {sql_command_string} '{sql_value_string}'"

        return sqlstring
    
class InListSearchTerm(SearchTerm, Generic[TListSearchable]):

    def __init__(self, column_name, value_list : list[TListSearchable]= [], ignore_case = False) -> None:
        super().__init__(column_name)

        self.value_list = value_list
        self.ignore_case = ignore_case 

    def generate_sql(self): 
        sqlstring =  f"LOWER({self.column_name}) IN (\n" if self.ignore_case else f"{self.column_name} IN (\n"

        for i, value in enumerate(self.value_list):
            sqlstring += f"\tLOWER('{value}')" if self.ignore_case else f"\t'{value}'"
            sqlstring += "," if i < len(self.value_list) - 1 else ""
            sqlstring += "\n"
 
        sqlstring += ")"

        return sqlstring
    
class RangeSearchTerm(SearchTerm, Generic[TRangeSearchable]):
 
    def __init__(self, column_name, value_min : TRangeSearchable | None = None, value_max : TRangeSearchable | None = None, ignore_case = False) -> None:
        super().__init__(column_name)

        self.value_min: TRangeSearchable | None = value_min
        self.value_max: TRangeSearchable | None = value_max 
        self.ignore_case: bool = ignore_case

    def generate_sql(self):
        column_sql: str = f"LOWER({self.column_name})" if self.ignore_case else f"{self.column_name}"
        value_min_sql: str | None = (f"LOWER('{self.value_min}')" if self.ignore_case else f"'{self.value_min}'") if self.value_min is not None else None
        value_max_sql: str | None = (f"LOWER('{self.value_max}')" if self.ignore_case else f"'{self.value_max}'") if self.value_max is not None else None

        sqlstring: str = ""

        if(value_min_sql is None and value_max_sql is None):
            sqlstring += f"{column_sql} = {column_sql} OR {column_sql} IS NULL"
        elif(value_min_sql is not None and value_max_sql is not None):
            sqlstring += f"{column_sql} >= {value_min_sql} AND {column_sql} <= {value_max_sql}"
        elif(value_min_sql is not None):
            sqlstring += f"{column_sql} >= {value_min_sql}"
        elif(value_max_sql is not None):
            sqlstring += f"{column_sql} <= {value_max_sql}"
 
        return sqlstring