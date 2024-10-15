from typing import Any
from models.vendor_model import (
    VendorCreateModel,
    VendorDatabaseModel,
    VendorInboundCreateModel,
    VendorInboundSearchModel,
    VendorInboundUpdateModel,
    VendorModel,
    VendorOutboundModel,
    VendorSearchModel,
    VendorUpdateModel,
)
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm,
    LikeComparatorModes,
    LikeSearchTerm,
    SearchTerm,
)


class VendorDataAdapter:
    common_utilities: CommonUtilities = CommonUtilities()

    def convert_from_inbound_create_model_to_create_model(
        self,
        inbound_create_model: VendorInboundCreateModel,
    ) -> VendorCreateModel:
        model = VendorCreateModel(
            name=inbound_create_model.name,
            is_registered=inbound_create_model.is_registered,
            unregistered_vendor_retailer_id=inbound_create_model.
            unregistered_vendor_retailer_id,
            registered_replacement_vendor_id=inbound_create_model.
            registered_replacement_vendor_id,
            hq_state=inbound_create_model.hq_state,
            hq_city=inbound_create_model.hq_city,
            hq_country=inbound_create_model.hq_country,
            contact_email=inbound_create_model.contact_email,
            contact_phone=inbound_create_model.contact_phone,
        )

        return model

    def convert_from_inbound_update_model_to_create_model(
        self,
        inbound_update_model: VendorInboundUpdateModel,
    ) -> VendorUpdateModel:
        model = VendorUpdateModel(
            name=inbound_update_model.name,
            is_registered=inbound_update_model.is_registered,
            hq_state=inbound_update_model.hq_state,
            hq_city=inbound_update_model.hq_city,
            hq_country=inbound_update_model.hq_country,
            contact_email=inbound_update_model.contact_email,
            contact_phone=inbound_update_model.contact_phone,
        )

        return model

    def convert_from_inbound_search_model_to_search_model(
            self, inbound_search_model: VendorInboundSearchModel
    ) -> VendorSearchModel:
        model = VendorSearchModel(
            ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.ids)
                if inbound_search_model.ids is not None else None),
            unregistered_vendor_retailer_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.unregistered_vendor_retailer_ids)
                if inbound_search_model.unregistered_vendor_retailer_ids
                is not None else None),
            registered_replacement_vendor_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.registered_replacement_vendor_ids)
                if inbound_search_model.registered_replacement_vendor_ids
                is not None else None),
            is_registered=inbound_search_model.is_registered,
            name=inbound_search_model.name,
            name_like=inbound_search_model.name_like,
            hq_state=inbound_search_model.hq_state,
            hq_city=inbound_search_model.hq_city,
            hq_country=inbound_search_model.hq_country,
        )

        return model

    def convert_from_search_model_to_search_terms(
            self, model: VendorSearchModel) -> list[SearchTerm]:
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(InListSearchTerm('id', model.ids))

        if model.registered_replacement_vendor_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    'registered_replacement_vendor_id',
                    model.registered_replacement_vendor_ids,
                ))

        if model.unregistered_vendor_retailer_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    'unregistered_vendor_retailer_id',
                    model.unregistered_vendor_retailer_ids,
                ))

        if model.name is not None:
            search_terms.append(ExactMatchSearchTerm('name', model.name, True))

        if model.name_like is not None:
            search_terms.append(
                LikeSearchTerm('name', model.name_like,
                               LikeComparatorModes.Like, True))

        if model.hq_state is not None:
            search_terms.append(
                ExactMatchSearchTerm('hq_state', model.hq_state, True))

        if model.hq_city is not None:
            search_terms.append(
                ExactMatchSearchTerm('hq_city', model.hq_city, True))

        if model.hq_country is not None:
            search_terms.append(
                ExactMatchSearchTerm('hq_country', model.hq_country, True))

        return search_terms

    def convert_from_create_model_to_database_model(
            self, model: VendorCreateModel) -> dict[str, Any]:
        database_model: dict[str, Any] = {
            'name': model.name,
            'registered_replacement_vendor_id':
            model.registered_replacement_vendor_id,
            'unregistered_vendor_retailer_id':
            model.unregistered_vendor_retailer_id,
            'is_registered': model.is_registered,
            'hq_state': model.hq_state,
            'hq_city': model.hq_city,
            'hq_country': model.hq_country,
            'contact_email': model.contact_email,
            'contact_phone': model.contact_phone,
        }

        return database_model

    def convert_from_update_model_to_database_model(
            self, model: VendorUpdateModel) -> dict[str, Any]:
        database_model: dict[str, Any] = {
            'name': model.name,
            'is_registered': model.is_registered,
            'hq_state': model.hq_state,
            'hq_city': model.hq_city,
            'hq_country': model.hq_country,
            'contact_email': model.contact_email,
            'contact_phone': model.contact_phone,
        }

        return database_model

    def convert_from_database_model_to_model(
            self, database_model: dict[str, Any]) -> VendorModel:
        model = VendorModel(
            id=database_model['id'],
            name=database_model['name'],
            registered_replacement_vendor_id=database_model[
                'registered_replacement_vendor_id'],
            unregistered_vendor_retailer_id=database_model[
                'unregistered_vendor_retailer_id'],
            is_registered=database_model['is_registered'],
            hq_state=database_model['hq_state'],
            hq_city=database_model['hq_city'],
            hq_country=database_model['hq_country'],
            contact_email=database_model['contact_email'],
            contact_phone=database_model['contact_phone'],
            created_at=database_model['created_at'],
            updated_at=database_model['updated_at'],
        )

        return model

    def convert_from_model_to_outbound_model(
            self, model: VendorModel) -> VendorOutboundModel:
        outbound_model = VendorOutboundModel(
            id=model.id,
            name=model.name,
            registered_replacement_vendor_id=model.
            registered_replacement_vendor_id,
            unregistered_vendor_retailer_id=model.
            unregistered_vendor_retailer_id,
            is_registered=model.is_registered,
            hq_state=model.hq_state,
            hq_city=model.hq_city,
            hq_country=model.hq_country,
            contact_email=model.contact_email,
            contact_phone=model.contact_phone,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

        return outbound_model
