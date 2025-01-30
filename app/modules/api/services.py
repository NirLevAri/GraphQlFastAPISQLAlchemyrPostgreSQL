# app/contexts/api/services.py
from sqlalchemy.orm import Session
from .repositories import APIRepository

class APIService:
    def __init__(self, db: Session):
        self.repo = APIRepository(db)

    def create_api(self, path: str, host: str, method: str):
        # Potential extra business logic/validation goes here
        return self.repo.create_api(path, host, method)

    def get_api(self, api_id: int):
        return self.repo.get_api(api_id)

    def list_apis(self):
        return self.repo.list_apis()

    def update_api(self, api_id: int, path=None, host=None, method=None):
        return self.repo.update_api(api_id, path=path, host=host, method=method)

    def delete_api(self, api_id: int):
        return self.repo.delete_api(api_id)
