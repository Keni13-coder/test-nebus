from hashlib import sha256
import hmac
from src.api.config.settings import settings
def generate_signature() -> str:
    """
    Генерирует API ключ для пользователя на основе нашего SECRET_KEY.
    Этот ключ выдается пользователю для доступа к API.
    """
    return hmac.new(
        settings.SECRET_KEY.encode(),
        settings.SECRET_KEY.encode(),
        sha256
    ).hexdigest()


def verify_signature(signature: str) -> bool:
    """
    Проверяет, что присланный в заголовке ключ был сгенерирован нами
    """
    expected_signature = generate_signature()
    return hmac.compare_digest(signature, expected_signature)
