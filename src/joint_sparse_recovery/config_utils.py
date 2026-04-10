"""Config and path helpers for experiment scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def resolve_project_path(path: str | Path) -> Path:
    """Resolve a relative path against the project root."""

    path_obj = Path(path)
    if path_obj.is_absolute():
        return path_obj
    return PROJECT_ROOT / path_obj


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a JSON object stored in a .yaml file."""

    config_path = resolve_project_path(path)
    return json.loads(config_path.read_text(encoding="utf-8"))


def merge_dicts(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge two dictionaries without mutating either input."""

    merged: dict[str, Any] = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged


def _namespace_output_paths(run_cfg: dict[str, Any], profile_name: str, default_profile: str) -> dict[str, Any]:
    """Reroot output paths under outputs/profiles/<profile>/ for non-default profiles."""

    if profile_name == default_profile:
        return dict(run_cfg)

    namespaced: dict[str, Any] = {}
    for key, value in run_cfg.items():
        if isinstance(value, str) and value.startswith("outputs/"):
            relative = value.removeprefix("outputs/")
            namespaced[key] = f"outputs/profiles/{profile_name}/{relative}"
        else:
            namespaced[key] = value
    return namespaced


def resolve_run_config(config: dict[str, Any], profile: str | None = None) -> dict[str, Any]:
    """Resolve the active run config, optionally applying a named profile override."""

    base_run = dict(config["run"])
    profiles = config.get("profiles", {})
    default_profile = str(config.get("default_profile", "quick"))
    selected_profile = str(profile or default_profile)
    if selected_profile not in profiles and selected_profile != default_profile:
        raise ValueError(f"unknown config profile={selected_profile}")

    override = profiles.get(selected_profile, {})
    resolved = merge_dicts(base_run, override)
    resolved = _namespace_output_paths(
        run_cfg=resolved,
        profile_name=selected_profile,
        default_profile=default_profile,
    )
    resolved["profile_name"] = selected_profile
    resolved["default_profile"] = default_profile
    return resolved


def ensure_parent_dir(path: str | Path) -> Path:
    """Create the parent directory of a project path and return the path."""

    resolved = resolve_project_path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


__all__ = [
    "PROJECT_ROOT",
    "ensure_parent_dir",
    "load_config",
    "merge_dicts",
    "resolve_project_path",
    "resolve_run_config",
]
