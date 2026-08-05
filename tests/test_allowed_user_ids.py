"""Tests for standalone human authorization configuration."""

from __future__ import annotations

import pytest

from claude_discord.main import resolve_allowed_user_ids


def test_allow_all_users_disables_the_user_allowlist() -> None:
    assert resolve_allowed_user_ids(42, "7,8", "true") is None


def test_explicit_users_are_unioned_with_the_owner() -> None:
    assert resolve_allowed_user_ids(42, "7,8", "false") == {7, 8, 42}


def test_owner_only_remains_the_backward_compatible_default() -> None:
    assert resolve_allowed_user_ids(42, "", "") == {42}


def test_missing_owner_and_allowlist_denies_everyone() -> None:
    assert resolve_allowed_user_ids(None, "", "") == set()


def test_invalid_explicit_user_id_fails_closed() -> None:
    with pytest.raises(RuntimeError, match="CCDB_ALLOWED_USER_IDS"):
        resolve_allowed_user_ids(42, "7,not-an-id", "false")
