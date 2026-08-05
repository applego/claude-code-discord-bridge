"""Tests for Discord bot startup configuration."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from claude_discord.bot import guild_commands_are_missing, sync_commands_on_ready_enabled


@pytest.mark.parametrize("value", ["0", "false", "FALSE", "no", "off"])
def test_sync_commands_on_ready_can_be_disabled(
    monkeypatch: pytest.MonkeyPatch, value: str
) -> None:
    monkeypatch.setenv("CCDB_SYNC_COMMANDS_ON_READY", value)
    assert sync_commands_on_ready_enabled() is False


def test_sync_commands_on_ready_defaults_to_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CCDB_SYNC_COMMANDS_ON_READY", raising=False)
    assert sync_commands_on_ready_enabled() is True


@pytest.mark.asyncio
async def test_registered_guild_commands_skip_mutating_sync() -> None:
    tree = MagicMock()
    tree.fetch_commands = AsyncMock(return_value=[MagicMock()])
    assert await guild_commands_are_missing(tree, MagicMock()) is False


@pytest.mark.asyncio
async def test_empty_guild_registry_allows_initial_sync() -> None:
    tree = MagicMock()
    tree.fetch_commands = AsyncMock(return_value=[])
    assert await guild_commands_are_missing(tree, MagicMock()) is True
