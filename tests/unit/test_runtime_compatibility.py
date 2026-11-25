"""Exercise the Lambda imports and key serialization without contacting AWS."""

from unittest.mock import MagicMock

import boto3
import pytest
from cryptography.hazmat.primitives import serialization


@pytest.fixture
def entrypoint(monkeypatch):
    client = MagicMock()
    client.get_caller_identity.return_value = {"Account": "123456789012"}
    monkeypatch.setenv("AWS_DEFAULT_REGION", "eu-central-1")
    monkeypatch.setattr(boto3, "client", MagicMock(return_value=client))
    import cfn_secret_handler as module

    return module


def test_lambda_imports(entrypoint):
    assert callable(entrypoint.handler)


def set_properties(provider, **properties):
    provider.set_request(
        {
            "StackId": "test-stack",
            "RequestId": "test-request",
            "LogicalResourceId": "TestKey",
            "ResourceProperties": {"Name": "/test/key", **properties},
        },
        {},
    )


@pytest.mark.parametrize("key_size", [1024, 2048, 3072])
def test_dsa_serialization(entrypoint, key_size):
    provider = entrypoint.cfn_dsakey_provider.DSAKeyProvider()
    set_properties(provider, KeySize=key_size)
    private, public = provider.create_key()
    key = serialization.load_pem_private_key(private.encode("ascii"), password=None)
    assert key.key_size == key_size
    if key_size == 1024:
        assert public.startswith("ssh-dss ")
    else:
        loaded = serialization.load_pem_public_key(public.encode("ascii"))
        assert loaded.public_numbers() == key.public_key().public_numbers()


@pytest.mark.parametrize("key_format", ["PKCS8", "TraditionalOpenSSL"])
def test_rsa_serialization(entrypoint, key_format):
    provider = entrypoint.cfn_rsakey_provider.RSAKeyProvider()
    set_properties(provider, KeySize=2048, KeyFormat=key_format)
    private, public = provider.create_key()
    key = serialization.load_pem_private_key(private.encode("ascii"), password=None)
    loaded = serialization.load_ssh_public_key(public.encode("ascii"))
    assert loaded.public_numbers() == key.public_key().public_numbers()
