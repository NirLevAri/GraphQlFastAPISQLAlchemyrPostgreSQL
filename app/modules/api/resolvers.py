# app/contexts/api/resolvers.py
import strawberry
from typing import List, Optional
from strawberry.types import Info

from app.core.db import SessionLocal
from app.graphql.types import APIType
from app.contexts.api.services import APIService

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@strawberry.type
class APIQuery:
    @strawberry.field
    def api(self, info: Info, api_id: int) -> Optional[APIType]:
        db = next(get_db())
        service = APIService(db)
        api_obj = service.get_api(api_id)
        if api_obj:
            return APIType(
                id=api_obj.id,
                path=api_obj.path,
                host=api_obj.host,
                method=api_obj.method
            )
        return None

    @strawberry.field
    def apis(self, info: Info) -> List[APIType]:
        db = next(get_db())
        service = APIService(db)
        api_list = service.list_apis()
        return [
            APIType(
                id=a.id,
                path=a.path,
                host=a.host,
                method=a.method
            )
            for a in api_list
        ]

@strawberry.type
class APIMutation:
    @strawberry.mutation
    def create_api(self, info: Info, path: str, host: str, method: str) -> APIType:
        db = next(get_db())
        service = APIService(db)
        created = service.create_api(path, host, method)
        return APIType(
            id=created.id,
            path=created.path,
            host=created.host,
            method=created.method
        )

    @strawberry.mutation
    def update_api(
        self,
        info: Info,
        api_id: int,
        path: Optional[str] = None,
        host: Optional[str] = None,
        method: Optional[str] = None
    ) -> Optional[APIType]:
        db = next(get_db())
        service = APIService(db)
        updated = service.update_api(api_id, path=path, host=host, method=method)
        if updated:
            return APIType(
                id=updated.id,
                path=updated.path,
                host=updated.host,
                method=updated.method
            )
        return None

    @strawberry.mutation
    def delete_api(self, info: Info, api_id: int) -> bool:
        db = next(get_db())
        service = APIService(db)
        return service.delete_api(api_id)
