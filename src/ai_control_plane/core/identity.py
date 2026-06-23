"""JWT validation stub — Milestone B. Full JWKS in Milestone C."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
from typing import Any

from ai_control_plane.core.exceptions import ControlPlaneError

_DEFAULT_DEV_SECRET = "acp-dev-secret"


class JWTValidationError(ControlPlaneError):
    """Raised when JWT is invalid, expired, or untrusted."""

    def __init__(self, message: str, *, code: str = "JWT_INVALID") -> None:
        super().__init__(message)
        self.code = code


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def encode_hs256_token(claims: dict[str, Any], *, secret: str = _DEFAULT_DEV_SECRET) -> str:
    """Encode HS256 JWT for dev/smoke tests."""
    header = _b64url_encode(b'{"alg":"HS256","typ":"JWT"}')
    payload = _b64url_encode(json.dumps(claims, separators=(",", ":")).encode())
    signature = _b64url_encode(
        hmac.new(secret.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest(),
    )
    return f"{header}.{payload}.{signature}"


class JWTValidator:
    """HS256 stub validator. Replace with RS256 + JWKS in production."""

    def __init__(self, secret: str = _DEFAULT_DEV_SECRET) -> None:
        self._secret = secret.encode()

    def validate(self, token: str) -> dict[str, Any]:
        """Validate HS256 token, return claims dict. Raise JWTValidationError if invalid."""
        parts = token.split(".")
        if len(parts) != 3:
            raise JWTValidationError("invalid JWT structure", code="JWT_INVALID")

        try:
            header_b64, payload_b64, sig_b64 = parts
            expected_sig = hmac.new(
                self._secret,
                f"{header_b64}.{payload_b64}".encode(),
                hashlib.sha256,
            ).digest()
            sig = _b64url_decode(sig_b64)
            if not hmac.compare_digest(expected_sig, sig):
                raise JWTValidationError("invalid signature", code="JWT_SIG_INVALID")
            claims_raw = _b64url_decode(payload_b64)
            claims = json.loads(claims_raw)
            if not isinstance(claims, dict):
                msg = "JWT payload must be a JSON object"
                raise JWTValidationError(msg, code="JWT_PARSE_ERROR")
            return claims
        except JWTValidationError:
            raise
        except Exception as exc:
            raise JWTValidationError(f"JWT parse error: {exc}", code="JWT_PARSE_ERROR") from exc


__all__ = [
    "JWTValidationError",
    "JWTValidator",
    "encode_hs256_token",
]
