from pydantic import BaseModel, Field

class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Описание ошибки")