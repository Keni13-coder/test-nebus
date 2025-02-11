from typing import TypeVar, Type, get_args, Any
from fastapi import Query, HTTPException
from pydantic import BaseModel, ValidationError
import json
from functools import wraps

T = TypeVar('T')

class UnionQueryParser:
    """
    Универсальный парсер для Union типов в GET запросах.
    
    Класс предназначен для обработки Union типов в FastAPI GET запросах.
    Позволяет валидировать входящие параметры на соответствие одной из схем Union.
    
    Особенности:
    - Строгая проверка соответствия полей только одной схеме
    - Автоматическая генерация документации и примеров
    - Подробные сообщения об ошибках
    - Поддержка вложенных Pydantic моделей
    
    Пример использования:
    ```python
    @router.get("/endpoint")
    async def endpoint(
        query: Annotated[UnionType, Depends(UnionQueryParser.parse(UnionType))]
    ):
        return {"result": query}
    ```
    """

    @staticmethod
    def get_schema_examples(schema: Type[BaseModel]) -> dict:
        """
        Получает примеры и схему из Pydantic модели.
        
        Args:
            schema: Pydantic модель для извлечения информации
            
        Returns:
            dict: Словарь содержащий:
                - example: Пример данных из схемы
                - properties: Описание полей схемы
                - title: Название схемы
                - description: Описание схемы
                
        Используется для генерации документации в Swagger UI.
        """
        json_schema = schema.model_json_schema()
        return {
            'example': json_schema.get('example', {}),
            'properties': json_schema.get('properties', {}),
            'title': json_schema.get('title', schema.__name__),
            'description': json_schema.get('description', '')
        }

    @staticmethod
    def parse(union_type: Type[T]) -> Any:
        """
        Создает зависимость FastAPI для парсинга Union типов из query параметров.
        
        Args:
            union_type: Union тип для парсинга (например, Union[ModelA, ModelB])
            
        Returns:
            Callable: FastAPI зависимость для парсинга и валидации
            
        Особенности:
        - Проверяет точное соответствие полей одной из схем
        - Генерирует подробную документацию для Swagger
        - Предоставляет информативные сообщения об ошибках
        
        Возможные ошибки:
        - 400: Неверный формат JSON
        - 400: Поля не соответствуют ни одной схеме
        - 400: Поля соответствуют нескольким схемам
        - 400: Ошибка валидации значений полей
        
        Пример запроса:
        GET /endpoint?query={"field1": "value1"}
        """
        schemas = get_args(union_type)
        
        schema_fields = {}
        for schema in schemas:
            if not issubclass(schema, BaseModel):
                continue
            schema_info = UnionQueryParser.get_schema_examples(schema)
            schema_fields[schema.__name__] = set(schema_info['properties'].keys())

        examples = {}
        query_formats = []
        for schema in schemas:
            if not issubclass(schema, BaseModel):
                continue
                
            schema_info = UnionQueryParser.get_schema_examples(schema)
            properties = schema_info['properties']
            
            format_desc = {
                'name': schema.__name__,
                'fields': {
                    name: {
                        'type': prop.get('type', 'any'),
                        'description': prop.get('description', '')
                    }
                    for name, prop in properties.items()
                }
            }
            query_formats.append(format_desc)
            
            if schema_info.get('example'):
                examples[f"example_{schema.__name__.lower()}"] = {
                    "summary": f"Example for {schema.__name__}",
                    "description": "\n".join(
                        f"{name}: {prop.get('description', '')}"
                        for name, prop in properties.items()
                    ),
                    "value": json.dumps(schema_info['example'])
                }

        formats_description = "\n\nPossible formats:\n" + "\n".join(
            f"- {fmt['name']}:\n" + "\n".join(
                f"  * {field}: {details['type']} - {details['description']}"
                for field, details in fmt['fields'].items()
            )
            for fmt in query_formats
        )

        async def parser(
            query: str = Query(
                ...,
                description=f"JSON-encoded query parameters. Must match exactly one schema format:{formats_description}",
                examples=examples
            )
        ) -> T:
            try:
                data = json.loads(query)
                if not isinstance(data, dict):
                    raise HTTPException(
                        status_code=400,
                        detail="Query parameter must be a JSON object"
                    )

                request_fields = set(data.keys())
                matching_schemas = []
                
                for schema_name, fields in schema_fields.items():
                    if request_fields == fields:
                        matching_schemas.append(schema_name)

                if len(matching_schemas) == 0:
                    raise HTTPException(
                        status_code=400,
                        detail={
                            "message": "Query fields don't match any schema exactly",
                            "your_fields": list(request_fields),
                            "available_schemas": {
                                name: list(fields)
                                for name, fields in schema_fields.items()
                            }
                        }
                    )
                elif len(matching_schemas) > 1:
                    raise HTTPException(
                        status_code=400,
                        detail={
                            "message": "Query fields match multiple schemas",
                            "matching_schemas": matching_schemas
                        }
                    )

                for schema in schemas:
                    if schema.__name__ == matching_schemas[0]:
                        try:
                            return schema(**data)
                        except ValidationError as e:
                            raise HTTPException(
                                status_code=400,
                                detail={
                                    "message": f"Validation failed for {schema.__name__}",
                                    "errors": str(e)
                                }
                            )

            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid JSON format in query parameter"
                )

        return parser 