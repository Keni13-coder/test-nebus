from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Optional, Union
import re

class PhoneI(BaseModel):
    phone: str = Field(..., description="Телефон")
    
class CategoryI(BaseModel):
    title: str = Field(..., description="Название категории")
    path: str = Field(
        ..., 
        description="Иерархический путь категории, максимум 3 уровня",
        json_schema_extra={
            "examples": [
                "/category1",
                "/category1/subcategory1",
                "/category1/subcategory1/subsubcategory1"
            ]
        },
        pattern=r"^/[a-zA-Zа-яА-Я0-9-_]+(/[a-zA-Zа-яА-Я0-9-_]+){0,2}$"
    )

    @field_validator('path')
    def validate_path(cls, v: str) -> str:
        if not v.startswith('/'):
            raise ValueError('Path must start with "/"')
        
        parts = [p for p in v.split('/') if p]
        if len(parts) > 3:
            raise ValueError('Path hierarchy cannot be deeper than 3 levels')
            
        return v

class GeoI(BaseModel):
    lon: float = Field(..., description="Долгота")
    lat: float = Field(..., description="Широта")
    
class OfficeI(BaseModel):
    address: str = Field(..., description="Адрес офиса")
    geo: GeoI = Field(..., description="Гео-данные офиса")

class OrganizationI(BaseModel):
    title: str = Field(..., description="Название организации")
    office: OfficeI = Field(..., description="Офис организации")
    phones: list[PhoneI] = Field(..., description="Телефоны организации")
    categories: list[CategoryI] = Field(..., description="Категории организации")

class OrgIdQuery(BaseModel):
    org_id: int = Field(..., description="Идентификатор организации")

class OrgTitleQuery(BaseModel):
    org_title: str = Field(..., description="Название организации")

class CategoryPathQuery(BaseModel):
    category_path: str = Field(..., description="Иерархический путь категории")

class CategoryTitleQuery(BaseModel):
    category_title: str = Field(..., description="Название категории")

class OfficeAddressQuery(BaseModel):
    office_address: str = Field(..., description="Адрес офиса")

class GeoRadiusQuery(BaseModel):
    geo: GeoI = Field(..., description="Гео-данные для поиска")
    radius: float = Field(..., description="Радиус поиска")
    
class GeoBoxQuery(BaseModel):
    min_lon: float = Field(..., description="Минимальная долгота")
    min_lat: float = Field(..., description="Минимальная широта")
    max_lon: Optional[float] = Field(None, description="Максимальная долгота")
    max_lat: Optional[float] = Field(None, description="Максимальная широта")

    @model_validator(mode='after')
    def set_max_coordinates(self) -> 'GeoBoxQuery':
        """Если max координаты не указаны, инвертируем min координаты"""
        if self.max_lon is None:
            self.max_lon = -self.min_lon
        if self.max_lat is None:
            self.max_lat = -self.min_lat
            
        # Проверяем, что min действительно меньше max
        if self.min_lon > self.max_lon:
            self.min_lon, self.max_lon = self.max_lon, self.min_lon
        if self.min_lat > self.max_lat:
            self.min_lat, self.max_lat = self.max_lat, self.min_lat
            
        return self

class OrganizationQueryO(BaseModel):
    org_title: str = Field(..., description="Название организации")
    phones: list[str] = Field(..., description="Телефоны организации")
    office_address: str = Field(..., description="Адрес офиса")
    categories_titles: list[str] = Field(..., description="Названия категорий")

OrganizationQueryI = Union[
    OrgIdQuery,
    OrgTitleQuery,
    CategoryPathQuery,
    CategoryTitleQuery,
    OfficeAddressQuery,
    GeoRadiusQuery,
    GeoBoxQuery
]
    
if __name__ == "__main__":
    query = OrganizationQueryI(org_id=1)