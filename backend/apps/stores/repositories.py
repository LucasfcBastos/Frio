from apps.stores.models import Organization, Store
from core.entities import StoreEntity
from core.interfaces import StoreRepository


def _to_entity(store: Store) -> StoreEntity:
    return StoreEntity(
        id=store.id,
        organization_id=store.organization_id,
        organization_name=store.organization.name,
        name=store.name,
        city=store.city,
        state=store.state,
    )


class DjangoStoreRepository(StoreRepository):
    def list(self) -> list[StoreEntity]:
        return [_to_entity(store) for store in Store.objects.select_related("organization")]

    def exists(self, store_id: int) -> bool:
        return Store.objects.filter(pk=store_id).exists()

    def create_organization(self, name: str) -> int:
        return Organization.objects.create(name=name).id

    def create(self, organization_id: int, name: str, city: str, state: str) -> StoreEntity:
        store = Store.objects.create(
            organization_id=organization_id, name=name, city=city, state=state
        )
        return _to_entity(Store.objects.select_related("organization").get(pk=store.pk))

    def reset(self) -> None:
        Organization.objects.all().delete()
