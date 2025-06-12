from jwcrypto import jwk, jws
from datetime import datetime, timezone
import json
import os
import functools

def _ts():
    return datetime.now(tz=timezone.utc).isoformat(timespec="seconds")

@functools.lru_cache
def _load_keys() -> tuple[jwk.JWK, jwk.JWK]:
    """
    Lazily load the EC key‑pair from the environment (FMCPEX_JWS_PRIV_KEY).

    The value must be a PEM‑encoded ECDSA P‑256 private key.  
    A public key is derived automatically for verification.
    """
    pem = os.getenv("FMCPEX_JWS_PRIV_KEY")
    if not pem:
        raise RuntimeError(
            "JWS signing requires the FMCPEX_JWS_PRIV_KEY environment variable "
            "to contain a PEM‑encoded ES256 private key."
        )
    priv = jwk.JWK.from_pem(pem.encode())
    pub = jwk.JWK.from_pem(priv.export_to_pem(private_key=False, compress=True))
    return priv, pub

def sign_response(data: dict) -> dict:
    priv, _ = _load_keys()
    payload = json.dumps(data).encode()
    token = jws.JWS(payload)
    token.add_signature(priv, alg="ES256", protected={"iat": _ts()})
    return {"jws": token.serialize(compact=True), "ts": _ts()}

def verify(jws_token: str) -> dict:
    _, pub = _load_keys()
    obj = jws.JWS()
    obj.deserialize(jws_token)
    obj.verify(pub)
    return json.loads(obj.payload)