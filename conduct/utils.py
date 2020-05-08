from os import path


def macaroon_to_hex(macaroon_path: str) -> str:
    with open(path.expanduser(macaroon_path), "rb") as f:
        macaroon_bytes: bytes = f.read()

    return macaroon_bytes.hex().upper()
