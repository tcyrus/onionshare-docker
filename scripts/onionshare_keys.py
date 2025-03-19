import json
import base64
import hashlib

def parse_conf():
    config = {}
    with open('onionshare.json', 'r') as f:
        config = json.load(f)

    private_key = config.get("onion", {}).get("private_key", "").encode('ascii')

    with open('hs_ed25519_secret_key', 'wb') as f:
        f.write(b"== ed25519v1-secret: type0 ==\x00\x00\x00")
        f.write(base64.b64decode(private_key))

    service_id = config.get("general", {}).get("service_id", "")

    with open('hs_ed25519_public_key', 'wb') as f:
        f.write(b"== ed25519v1-public: type0 ==\x00\x00\x00")
        f.write(base64.b32decode(service_id)[:-3])

def gen_conf():
    config = {}

    secret_key = b''
    with open('hs_ed25519_secret_key', 'rb') as f:
        secret_key = f.read().strip()

    assert secret_key.startswith(b"== ed25519v1-secret: type0 ==\x00\x00\x00")

    private_key = base64.b64encode(
        secret_key.removeprefix(b"== ed25519v1-secret: type0 ==\x00\x00\x00")
    ).decode('ascii')

    config["onion"] = {"private_key": private_key}

    public_key = b''
    with open('hs_ed25519_public_key', 'rb') as f:
        public_key = f.read().strip()

    assert public_key.startswith(b"== ed25519v1-public: type0 ==\x00\x00\x00")

    def _service_id_from_public_key(public_key: bytes) -> str:
        version = b"\x03"
        checksum = hashlib.sha3_256(b".onion checksum" + public_key + version).digest()[:2]
        return base64.b32encode(public_key + checksum + version).decode().lower()

    service_id = _service_id_from_public_key(
        public_key.removeprefix(b"== ed25519v1-secret: type0 ==\x00\x00\x00")
    )

    config["general"] = {"service_id": service_id}

    with open('onionshare.json', 'w') as f:
        json.dump(f)
