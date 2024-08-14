from fastapi import HTTPException, status

def http_exception(status_code: int, detail: str):
    raise HTTPException(status_code=status_code, detail={"error": detail, "status_code": status_code})

def not_found_exception(entity: str):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"{entity} not found", "status_code": status.HTTP_404_NOT_FOUND})

def unauthorized_exception():
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Unauthorized", "status_code": status.HTTP_401_UNAUTHORIZED})
