from fastapi import HTTPException


class BaseException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class ServerException(BaseException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail)
