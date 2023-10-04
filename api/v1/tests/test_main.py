#!/usr/bin/python3
"""Test EstateTrust entry point route."""


def test_index(client):
    """Test entry route."""
    res = client.get('/')
    assert res.json().get("message") == "Welcome to Estate Trust."
    assert res.status_code == 200
