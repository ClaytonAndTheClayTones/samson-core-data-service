from typing import Any
from uuid import UUID
from adapters.product_adapters import ProductDataAdapter
from models.product_model import (
    ProductCreateModel,
    ProductDatabaseModel,
    ProductModel,
    ProductSearchModel,
    ProductUpdateModel,
)
from models.common_model import ItemList
from util.configuration import get_global_configuration
from util.database import PagingModel, SearchTerm
from util.db_connection import SelectQueryResults
 
class ProductDataAccessor:
    adapter: ProductDataAdapter = ProductDataAdapter()

    def insert(self, model: ProductCreateModel):
        connection = get_global_configuration().pg_connection

        db_model: dict[
            str,
            Any] = self.adapter.convert_from_create_model_to_database_model(
                model)

        db_result: dict[str, Any] = connection.insert('products',
                                                      db_model)

        result_model = self.adapter.convert_from_database_model_to_model(
            db_result)

        return result_model

    def select_by_id(self, id: UUID):

        connection = get_global_configuration().pg_connection

        db_result = connection.select_by_id('products', id)

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(
            db_result)

        return result_model

    def select(
        self,
        model: ProductSearchModel,
        paging_model: PagingModel | None = None,
    ) -> ItemList[ProductModel]:

        connection = get_global_configuration().pg_connection

        search_terms: list[
            SearchTerm] = self.adapter.convert_from_search_model_to_search_terms(
                model)
        db_result: SelectQueryResults = connection.select(
            'products', search_terms, paging_model)

        results: ItemList[ProductModel] = ItemList[
            ProductModel](db_result.paging)

        if db_result is None:
            return results

        for item in db_result.items:
            result_model = self.adapter.convert_from_database_model_to_model(
                item)
            results.items.append(result_model)

        return results

    def update(
        self,
        id: UUID,
        model: ProductUpdateModel,
        explicitNullSet: list[str] | None = None,
    ):

        explicitNullSet = explicitNullSet or []

        connection = get_global_configuration().pg_connection

        db_model: dict[
            str,
            Any] = self.adapter.convert_from_update_model_to_database_model(
                model)

        db_result = connection.update('products', id, db_model)

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(
            db_result)

        return result_model

    def delete(self, id: UUID):

        connection = get_global_configuration().pg_connection

        db_result = connection.delete('products', id)

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(
            db_result)

        return result_model
