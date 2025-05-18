import json
import base64
import hashlib


def pubkey_to_service_id(pubkey: bytes) -> str:
    """
    Returns service id (onion addr) for the specified v3 onion addr (PUBKEY).

    CHECKSUM = SHA3_256(".onion checksum" | PUBKEY | VERSION)[:2]
    service_id = base32(PUBKEY | CHECKSUM | VERSION)
    onion_address = service_id + ".onion"

    See https://spec.torproject.org/rend-spec/encoding-onion-addresses.html
    """
    version = b"\x03"
    checksum = hashlib.sha3_256(b".onion checksum" + pubkey + version).digest()[:2]
    return base64.b32encode(pubkey + checksum + version).decode().lower()


def get_keys_from_onionshare(config = {}) -> tuple[bytes, bytes]:
    """
    Extract onion v3 key files from onionshare config
    """
    service_id = config.get("general", {}).get("service_id", "")
    public_key = bytearray(b"== ed25519v1-public: type0 ==\x00\x00\x00")
    public_key.extend(base64.b32decode(service_id)[:-3])

    private_key = config.get("onion", {}).get("private_key", "").encode('ascii')
    secret_key = bytearray(b"== ed25519v1-secret: type0 ==\x00\x00\x00")
    secret_key.extend(base64.b64decode(private_key))

    return (bytes(public_key), bytes(secret_key))


def add_keys_to_onionshare(config = {}, public_key = b'', secret_key = b'') -> dict:
    """
    Add onion v3 key files to onionshare config
    """

    if public_key.startswith(b"== ed25519v1-public: type0 ==\x00\x00\x00"):
        service_id = pubkey_to_service_id(
            public_key.removeprefix(b"== ed25519v1-secret: type0 ==\x00\x00\x00")
        )
        config.setdefault("general", {})
        config["general"]["service_id"] = service_id

    if secret_key.startswith(b"== ed25519v1-secret: type0 ==\x00\x00\x00"):
        private_key = base64.b64encode(
            secret_key.removeprefix(b"== ed25519v1-secret: type0 ==\x00\x00\x00")
        ).decode('ascii')
        config.setdefault("onion", {})
        config["onion"]["private_key"] = private_key

    return config


def main():
    config = {}

    # Get Keys from Config
    with open('onionshare.json', 'r') as f:
        config = json.load(f)
    public_key, secret_key = get_keys_from_onionshare(config)
    with open('hs_ed25519_secret_key', 'wb') as f:
        f.write(secret_key)
    with open('hs_ed25519_public_key', 'wb') as f:
        f.write(public_key)

    # Add Keys to Config
    public_key = b''
    with open('hs_ed25519_public_key', 'rb') as f:
        public_key = f.read().strip()
    secret_key = b''
    with open('hs_ed25519_secret_key', 'rb') as f:
        secret_key = f.read().strip()
    config = add_keys_to_onionshare(config, public_key, secret_key)
    with open('onionshare.json', 'w') as f:
        json.dump(config, f, indent=2)

if __name__ == "__main__":
    main()
