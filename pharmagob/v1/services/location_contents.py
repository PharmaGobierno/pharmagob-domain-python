from dataclasses import asdict
from time import time
from typing import Dict, Iterator, List, Optional, Tuple

from pharmagob.v1.models.location_content import LocationContentModel
from pharmagob.v1.models.minified.min_models import UserMin
from pharmagob.v1.repository_interfaces.location_contents import (
    LocationContentRepositoryInterface,
)

from ._base import BaseService


class LocationContentService(
    BaseService[LocationContentModel, LocationContentRepositoryInterface]
):
    __model__ = LocationContentModel

    # Quantities move only through increase_quantity / decrease_quantity /
    # upsert_increase_quantity (atomic $inc). Do NOT use `update` / `set` to
    # change `quantity`: they rewrite the whole document and can erase a
    # concurrent increment (H-11).

    def search_by_item(
        self,
        search_str: str,
        *,
        umu_id: str,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[Dict[str, int]] = None,
        quantity_gt: Optional[int] = None,
        quantity_lt: Optional[int] = None,
        expiration_date_gt: Optional[int] = None,
        expiration_date_lt: Optional[int] = None,
        lot: Optional[str] = None,
        location_id: Optional[str] = None,
        location_label_code: Optional[str] = None,
        location_label_code_not_in: Optional[List[str]] = None
    ) -> Tuple[int, Iterator[LocationContentModel]]:
        count, result = self.repository.search_by_item(
            search_str,
            expiration_date_gt=expiration_date_gt,
            expiration_date_lt=expiration_date_lt,
            umu_id=umu_id,
            quantity_gt=quantity_gt,
            quantity_lt=quantity_lt,
            lot=lot,
            location_id=location_id,
            location_label_code=location_label_code,
            location_label_code_not_in=location_label_code_not_in,
            page=page,
            limit=limit,
            sort=sort,
        )
        return count, map(lambda r: LocationContentModel(**r), result)

    def search_by_item_global(
        self,
        search_str: str,
        *,
        page: int,
        limit: int,
        sort: Optional[Dict[str, int]] = None,
        umu_id_not_in: Optional[List[str]] = None,
        umu_id_in: Optional[List[str]] = None,
        quantity_gt: Optional[int] = None,
        quantity_lt: Optional[int] = None,
        expiration_date_gt: Optional[int] = None,
        expiration_date_lt: Optional[int] = None,
        lot: Optional[str] = None,
        location_id: Optional[str] = None,
        location_label_code: Optional[str] = None
    ) -> Tuple[int, Iterator[LocationContentModel]]:
        count, result = self.repository.search_by_item_global(
            search_str,
            expiration_date_gt=expiration_date_gt,
            expiration_date_lt=expiration_date_lt,
            umu_id_in=umu_id_in,
            umu_id_not_in=umu_id_not_in,
            quantity_gt=quantity_gt,
            quantity_lt=quantity_lt,
            lot=lot,
            location_id=location_id,
            location_label_code=location_label_code,
            page=page,
            limit=limit,
            sort=sort,
        )
        return count, map(lambda r: LocationContentModel(**r), result)

    def get_by_ids(
        self,
        entity_ids: List[str],
        umu_id: str,
    ) -> Iterator[LocationContentModel]:

        result = self.repository.get_by_ids(
            entity_ids=entity_ids,
            umu_id=umu_id,
        )

        return map(
            lambda r: LocationContentModel(**r),
            result,
        )

    def get_batch_after(
        self,
        umu_id: str,
        *,
        after_id: Optional[str] = None,
        limit: int = 1000,
        location_label_code: Optional[str] = None,
        location_label_code_not_in: Optional[List[str]] = None,
        quantity_gt: Optional[int] = None,
        item_ids: Optional[List[str]] = None,
    ) -> List[LocationContentModel]:
        result = self.repository.get_batch_after(
            umu_id,
            after_id=after_id,
            limit=limit,
            location_label_code=location_label_code,
            location_label_code_not_in=location_label_code_not_in,
            quantity_gt=quantity_gt,
            item_ids=item_ids,
        )
        return [LocationContentModel(**r) for r in result]

    def increase_quantity(
        self,
        location_content_id: str,
        quantity: int,
        *,
        author: UserMin,
        umu_id: Optional[str] = None,
    ) -> Optional[LocationContentModel]:
        """Adds `quantity` atomically. Returns the document after the change,
        or None when the location content does not exist (or is not of
        `umu_id`)."""
        self._validate_quantity(quantity)
        document = self.repository.increment_quantity(
            location_content_id,
            quantity,
            last_author=asdict(author),
            updated_at=round(time() * 1000),
            umu_id=umu_id,
        )
        return LocationContentModel(**document) if document else None

    def decrease_quantity(
        self,
        location_content_id: str,
        quantity: int,
        *,
        author: UserMin,
        umu_id: Optional[str] = None,
    ) -> Optional[LocationContentModel]:
        """Subtracts `quantity` atomically, only if the stock covers it.
        Returns the document after the change, or None when it does not exist
        or has less than `quantity` (the caller `get`s to tell which)."""
        self._validate_quantity(quantity)
        document = self.repository.increment_quantity(
            location_content_id,
            -quantity,
            min_quantity=quantity,
            last_author=asdict(author),
            updated_at=round(time() * 1000),
            umu_id=umu_id,
        )
        return LocationContentModel(**document) if document else None

    def upsert_increase_quantity(
        self,
        entity: LocationContentModel,
        quantity: int,
        *,
        author: UserMin,
    ) -> LocationContentModel:
        """Creates the location content or adds `quantity` to the existing
        one. `entity` provides the fields written only on insert (its own
        `quantity` is ignored). Returns the document after the change."""
        self._validate_quantity(quantity)
        document = self.repository.upsert_increment_quantity(
            entity._id,
            quantity,
            insert_data=entity.dict(),
            last_author=asdict(author),
            updated_at=round(time() * 1000),
        )
        return LocationContentModel(**document)

    @staticmethod
    def _validate_quantity(quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("quantity must be greater than 0")
