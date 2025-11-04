import uuid

"""
Генерация уникального id в форме PREFIX-UUID4 короткий
"""
def gen_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"
