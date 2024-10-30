from typing import Any
from uuid import UUID
from adapters.pos_integration_call_adapters import PosIntegrationCallDataAdapter
from models.pos_integration_call_model import (
    PosIntegrationCallCreateModel,
    PosIntegrationCallDatabaseModel,
    PosIntegrationCallModel,
    PosIntegrationCallSearchModel, 
)
from models.common_model import ItemList
from util.configuration import get_global_configuration
from util.database import PagingModel, SearchTerm
from util.db_connection import SelectQueryResults
 
class PosIntegrationCallDataAccessor:
    adapter: PosIntegrationCallDataAdapter = PosIntegrationCallDataAdapter()

    def insert(self, model: PosIntegrationCallCreateModel):
        connection = get_global_configuration().pg_connection

        db_model: dict[
            str,
            Any] = self.adapter.convert_from_create_model_to_database_model(
                model)

        db_result: dict[str, Any] = connection.insert('pos_integration_calls',
                                                      db_model)

        result_model = self.adapter.convert_from_database_model_to_model(
            db_result)

        return result_model

    def select_by_id(self, id: UUID):

        connection = get_global_configuration().pg_connection

        db_result = connection.select_by_id('pos_integration_calls', id)

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(
            db_result)

        return result_model

    def select(
        self,
        model: PosIntegrationCallSearchModel,
        paging_model: PagingModel | None = None,
    ) -> ItemList[PosIntegrationCallModel]:

        connection = get_global_configuration().pg_connection

        search_terms: list[
            SearchTerm] = self.adapter.convert_from_search_model_to_search_terms(
                model)
        db_result: SelectQueryResults = connection.select(
            'pos_integration_calls', search_terms, paging_model)

        results: ItemList[PosIntegrationCallModel] = ItemList[PosIntegrationCallModel](
            db_result.paging)

        if db_result is None:
            return results

        for item in db_result.items:
            result_model = self.adapter.convert_from_database_model_to_model(
                item)
            results.items.append(result_model)

        return results 

    def delete(self, id: UUID):

        connection = get_global_configuration().pg_connection

        db_result = connection.delete('pos_integration_calls', id)

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(
            db_result)

        return result_model
