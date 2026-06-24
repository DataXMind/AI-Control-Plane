"""JWKS RS256 JWT validation tests."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

pytest.importorskip("jwt")
pytest.importorskip("cryptography")

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from ai_control_plane.core.identity import JWKSValidator, JWTValidationError, create_jwt_validator


def _rsa_token() -> tuple[bytes, bytes, str]:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    token = jwt.encode(
        {"agent_id": "agent2", "project_id": "rust-gateway", "role": "backend"},
        private_pem,
        algorithm="RS256",
        headers={"kid": "test-key"},
    )
    return private_pem, public_pem, token


def test_jwks_validator_accepts_rs256_token() -> None:
    _private_pem, public_pem, token = _rsa_token()
    mock_signing = MagicMock()
    mock_signing.key = public_pem

    with patch("jwt.PyJWKClient") as mock_client_cls:
        mock_client_cls.return_value.get_signing_key_from_jwt.return_value = mock_signing
        validator = JWKSValidator("https://idp.test/.well-known/jwks.json")
        claims = validator.validate(token)

    assert claims["agent_id"] == "agent2"
    assert claims["project_id"] == "rust-gateway"


def test_jwks_validator_rejects_invalid_token() -> None:
    _private_pem, public_pem, _token = _rsa_token()
    mock_signing = MagicMock()
    mock_signing.key = public_pem

    with patch("jwt.PyJWKClient") as mock_client_cls:
        mock_client_cls.return_value.get_signing_key_from_jwt.return_value = mock_signing
        validator = JWKSValidator("https://idp.test/.well-known/jwks.json")
        with pytest.raises(JWTValidationError):
            validator.validate("not.a.jwt")


def test_create_jwt_validator_uses_jwks_when_env_set(monkeypatch) -> None:
    monkeypatch.setenv("ACP_JWKS_URL", "https://idp.test/jwks")
    validator = create_jwt_validator()
    assert isinstance(validator, JWKSValidator)
