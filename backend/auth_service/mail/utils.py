from uuid import uuid4


def generate_token_for_email() -> str:
    return str(uuid4())