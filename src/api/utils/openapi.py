from typing import Type, Union, get_args, Any
from pydantic import BaseModel

def generate_union_openapi_schema(union_type: Any) -> dict:
    """
    Генерирует OpenAPI схему для Union типа, используя
    встроенные схемы Pydantic моделей
    """
    schemas = get_args(union_type)
    
    return {
        'parameters': [{
            'in': 'query',
            'name': 'query',
            'required': True,
            'schema': {
                'anyOf': [
                    schema.model_json_schema()
                    for schema in schemas
                    if issubclass(schema, BaseModel)
                ]
            },
            'examples': {
                f"example_{schema.__name__.lower()}": {
                    'summary': schema.__doc__ or f'Пример {schema.__name__}',
                    'value': schema.model_json_schema().get('example', {})
                }
                for schema in schemas
                if issubclass(schema, BaseModel)
            }
        }]
    } 