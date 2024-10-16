from datetime import datetime
from typing import Any, cast
from uuid import UUID
import psycopg2

from util.database import PagingModel, ResultantPagingModel, SearchTerm


class BuildSelectQueryResults:

    def __init__(self, sqlstring: str, paging: ResultantPagingModel) -> None:
        self.sqlstring = sqlstring
        self.paging = paging


class SelectQueryResults:

    def __init__(
        self,
        paging: ResultantPagingModel,
        items: list[dict[str, Any]] | None = None,
    ) -> None:

        self.paging = paging
        self.items = items or []


class PGConnection:

    connection: psycopg2.extensions.connection
    cursor: psycopg2.extensions.cursor

    def create_connection(self, host: str, port: str, database: str,
                          username: str, password: str):

        self.connection = psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=host,
            port=port,
        )

        self.cursor = self.connection.cursor()

    def map_result_columns_to_values(self, column_names: list[str],
                                     record: tuple[Any, ...]):

        returndict: dict[str, Any] = {}

        for i, column_name in enumerate(column_names):
            returndict[column_name] = record[i]

        return returndict

    def execute_command(self, sqlstring: str):

        self.cursor.execute(sqlstring)
        self.connection.commit()

    def execute_command_with_results(self, sqlstring: str):
        self.cursor.execute(sqlstring)

        self.connection.commit()

        records = self.cursor.fetchall()

        return records

    def insert(self, table_name: str, model: dict[str, Any]):
        sqlstring = self.build_insert_query(table_name, model)

        try:
            self.cursor.execute(sqlstring)
        except Exception as e:
            self.connection.rollback()
            raise e

        self.connection.commit()

        rows = self.cursor.fetchall()

        columns = self.cursor.description

        if columns is None or rows is None or len(rows) != 1:
            raise

        colnames: list[str] = [desc[0] for desc in columns]

        returndict = self.map_result_columns_to_values(colnames, rows[0])

        return returndict

    def select_by_id(self, table_name: str, id: UUID) -> dict[str, Any] | None:
        sqlstring = self.build_select_by_id_query(table_name, id)

        try:
            self.cursor.execute(sqlstring)
        except Exception as e:
            self.connection.rollback()
            raise e

        rows = self.cursor.fetchall()

        columns = self.cursor.description

        if columns is None:
            raise

        if len(rows) == 0:
            return None

        colnames: list[str] = [desc[0] for desc in columns]

        returndict = self.map_result_columns_to_values(colnames, rows[0])

        return returndict

    def select(
        self,
        tablename: str,
        search_terms: list[SearchTerm],
        paging_model: PagingModel | None = None,
    ):
        buildqueryresults = self.build_select_query(tablename, search_terms,
                                                    paging_model)

        try:
            self.cursor.execute(buildqueryresults.sqlstring)
        except Exception as e:
            self.connection.rollback()
            raise e

        rows = self.cursor.fetchall()

        columns = self.cursor.description

        if columns is None:
            raise

        colnames: list[str] = [desc[0] for desc in columns]

        returnitemlist: SelectQueryResults = SelectQueryResults(
            buildqueryresults.paging)

        for row in rows:
            returnitemlist.items.append(
                self.map_result_columns_to_values(colnames, row))

        return returnitemlist

    def update(self, table_name: str, id: UUID, model: dict[str, Any]):
        # Eliminate nulls
        refined_model = dict[str, Any]()

        for x in model.keys():
            if model[x] is not None:
                refined_model[x] = model[x]

        # if nothing to update, just select by id
        if len(refined_model) == 0:
            returndict = self.select_by_id(table_name, id)
            return returndict

        else:
            refined_model['updated_at'] = datetime.utcnow()

        sqlstring = self.build_update_query(table_name, id, refined_model)

        try:
            self.cursor.execute(sqlstring)
        except Exception as e:
            self.connection.rollback()
            raise e

        self.connection.commit()

        rows = self.cursor.fetchall()

        columns = self.cursor.description

        if columns is None:
            raise

        if len(rows) == 0:
            return None

        colnames: list[str] = [desc[0] for desc in columns]

        returndict = self.map_result_columns_to_values(colnames, rows[0])

        return returndict

    def delete(self, table_name: str, id: UUID) -> dict[str, Any] | None:
        sqlstring = self.build_delete_query(table_name, id)

        try:
            self.cursor.execute(sqlstring)
        except Exception as e:
            self.connection.rollback()
            raise e

        self.connection.commit()

        rows = self.cursor.fetchall()

        columns = self.cursor.description

        if columns is None:
            raise

        if len(rows) == 0:
            return None

        colnames: list[str] = [desc[0] for desc in columns]

        returndict = self.map_result_columns_to_values(colnames, rows[0])

        return returndict

    def build_insert_query(self, table_name: str, model: dict[str, Any]):
        sqlstring: str = f'INSERT INTO {table_name}\n' f'(\n'

        keys = model.keys()

        # Columns
        values = model.values()
        valid_count = 0
        for key in keys:
            if model[key] is not None:
                valid_count += 1

        for i, key in enumerate(keys):
            if model[key] is not None:
                sqlstring += f'\t{key}'
                if i < (valid_count - 1):
                    sqlstring += ','
                sqlstring += '\n'

        sqlstring += f')\n' f'VALUES\n' f'(\n'

        # Values

        for i, value in enumerate(values):
            if value is not None:
                sqlstring += '\tNULL' if value is None else f"\t'{value}'"

                if i < (valid_count - 1):
                    sqlstring += ','
                sqlstring += '\n'

        sqlstring += f')\n' f'RETURNING *;'

        return sqlstring

    def build_select_query(
        self,
        table_name: str,
        search_terms: list[SearchTerm],
        paging_model: PagingModel | None = None,
        skip_paging: bool = False,
    ):

        if paging_model is None:
            paging_model = PagingModel(
                is_sort_descending=False,
                page=1,
                page_length=25,
                sort_by='created_at',
            )

        page = (1 if paging_model.page is None or paging_model.page < 1 else
                paging_model.page)

        page_length = 25
        if paging_model.page_length is None:
            page_length = 25
        elif paging_model.page_length < 0:
            page_length = 1
        elif paging_model.page_length > 1000:
            page_length = 1000
        else:
            page_length = paging_model.page_length

        offset = page_length * (page - 1)

        sort_by = paging_model.sort_by or 'created_at'
        is_sort_descending = (True if paging_model.is_sort_descending == True
                              else False)

        resultant_paging_model = ResultantPagingModel(
            page=page,
            page_length=page_length,
            sort_by=sort_by,
            is_sort_descending=is_sort_descending,
        )

        sqlstring: str = f'SELECT * FROM {table_name}\n'

        if len(search_terms) > 0:
            sqlstring += f'WHERE\n' f'(\n'

            for i, search_term in enumerate(search_terms):
                sqlstring += f'\t({search_term.generate_sql()})\n'
                sqlstring += '\tAND\n' if (i < len(search_terms) - 1) else ''

            sqlstring += f')\n'

        sqlstring += f'ORDER BY {sort_by}'

        if is_sort_descending:
            sqlstring += ' DESC'

        if not skip_paging:

            sqlstring += f'\nOFFSET {offset} LIMIT {page_length}'

        sqlstring += ';'

        return_object = BuildSelectQueryResults(sqlstring=sqlstring,
                                                paging=resultant_paging_model)

        return return_object

    def build_select_by_id_query(self, table_name: str, id: UUID):
        sqlstring: str = f'SELECT * FROM {table_name}\n' f"WHERE id = '{id}';"

        return sqlstring

    def build_update_query(self, table_name: str, id: UUID, model: dict[str,
                                                                        Any]):
        sqlstring: str = f'UPDATE {table_name}\n' f'SET\n'
        keys = model.keys()

        for i, key in enumerate(keys):
            sqlstring += f"\t{key} = '{model[key]}'"
            if i < len(keys) - 1:
                sqlstring += ','
            sqlstring += '\n'

        sqlstring += f"WHERE id = '{id}'\n" f'RETURNING *;'

        return sqlstring

    def build_delete_query(self, table_name: str, id: UUID):
        sqlstring: str = (f'DELETE FROM {table_name}\n'
                          f"WHERE id = '{id}'\n"
                          f'RETURNING *;')

        return sqlstring
