from core.entities import StoreEntity
from core.exceptions import NotFoundError
from core.interfaces import StoreRepository


def ensure_store_exists(stores: StoreRepository, store_id: int | None) -> None:
    """Shared guard: a filter by a store that does not exist is a 404, not an empty list."""
    if store_id is not None and not stores.exists(store_id):
        raise NotFoundError(f"Store {store_id} not found.", details={"store_id": store_id})


class StoreService:
    def __init__(self, stores: StoreRepository) -> None:
        self._stores = stores

    def list_stores(self) -> list[StoreEntity]:
        return self._stores.list()
