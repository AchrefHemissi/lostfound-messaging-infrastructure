from http.client import HTTPException


def validate_api_key(api_key: str | None, allowed_keys: set):
    if not api_key or api_key not in allowed_keys:
        raise HTTPException(status_code=401, detail="Unauthorized")
