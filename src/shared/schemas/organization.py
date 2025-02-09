from pydantic import BaseModel, Field

class PhoneI(BaseModel):
    phone: str = Field(..., description="Телефон")
    
class CategoryI(BaseModel):
    title: str = Field(..., description="Название категории")
    path: str = Field(..., description="Иерархический путь категории")
    
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
