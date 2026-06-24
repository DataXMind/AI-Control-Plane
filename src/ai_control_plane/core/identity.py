"""JWT validation — HS256 dev stub and RS256 JWKS (Milestone B/C)."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
from typing import Any, Protocol, runtime_checkable

from ai_control_plane.core.exceptions import ControlPlaneError

_DEFAULT_DEV_SECRET = "acp-dev-secret"


class JWTValidationError(ControlPlaneError):
    """Raised when JWT is invalid, expired, or untrusted."""

    def __init__(self, message: str, *, code: str = "JWT_INVALID") -> None:
        super().__init__(message)
        self.code = code


@runtime_checkable
class TokenValidator(Protocol):
    def validate(self, token: str) -> dict[str, Any]:
        ...


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
    """HS256 validator for dev/smoke (SMK-06)."""

    def __init__(self, secret: str = _DEFAULT_DEV_SECRET) -> None:
        self._secret = secret.encode()

    def validate(self, token: str) -> dict[str, Any]:
        """Validate HS256 token, return claims dict. Raise JWTValidationError if invalid."""
        parts = token.split(".")
        if len(parts) != 3:
            raise JWTValidationError("invalid JWT structure", code="JWT_INVALID")

        try:
            header_b64, payload_b64, sig_b64 = parts
            header_raw = _b64url_decode(header_b64)
            header = json.loads(header_raw)
            if not isinstance(header, dict):
                raise JWTValidationError("invalid JWT header", code="JWT_INVALID")
            alg = header.get("alg")
            if alg not in (None, "HS256"):
                raise JWTValidationError(f"unsupported alg '{alg}'", code="JWT_ALG_UNSUPPORTED")

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


class JWKSValidator:
    """RS256 validator using a remote JWKS document (``ACP_JWKS_URL``)."""

    def __init__(self, jwks_url: str) -> None:
        self._jwks_url = jwks_url

    def validate(self, token: str) -> dict[str, Any]:
        try:
            import jwt
            from jwt import PyJWKClient
        except ImportError as exc:
            msg = "PyJWT required for JWKS validation (pip install ai-control-plane[jwt])"
            raise RuntimeError(msg) from exc

        try:
            client = PyJWKClient(self._jwks_url)
            signing_key = client.get_signing_key_from_jwt(token)
            decoded = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                options={"verify_aud": False},
            )
            if not isinstance(decoded, dict):
                msg = "JWT payload must be a JSON object"
                raise JWTValidationError(msg, code="JWT_PARSE_ERROR")
            return decoded
        except JWTValidationError:
            raise
        except Exception as exc:
            raise JWTValidationError(f"JWKS validation failed: {exc}", code="JWT_INVALID") from exc


def create_jwt_validator() -> TokenValidator:
    """JWKS when ``ACP_JWKS_URL`` set; else HS256 stub."""
    jwks_url = os.environ.get("ACP_JWKS_URL")
    if jwks_url:
        return JWKSValidator(jwks_url)
    secret = os.environ.get("ACP_JWT_HS256_SECRET", _DEFAULT_DEV_SECRET)
    return JWTValidator(secret=secret)


__all__ = [
    "JWKSValidator",
    "JWTValidationError",
    "JWTValidator",
    "TokenValidator",
    "create_jwt_validator",
    "encode_hs256_token",
]
