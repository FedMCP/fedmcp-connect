"""fmcpx CLI – FedMCP connector generator"""
from __future__ import annotations

import json
import pathlib
import shutil
import sys
from typing import Final

import typer

# ─────────────────────────────────────────────
# Typer application setup
# ─────────────────────────────────────────────
app = typer.Typer(
    help="FedMCP connector toolkit",
    context_settings={"help_option_names": ["-h", "--help"]},
)

TEMPLATE_DIR: Final[pathlib.Path] = pathlib.Path(__file__).parent / "templates" / "basic"

@app.command("init", help="Scaffold a new FedMCP connector project.")
def init(name: str):
    """Scaffold a new FedMCP connector project."""
    dst = pathlib.Path(name).resolve()
    if dst.exists():
        typer.secho(f"❌ Directory '{dst}' already exists", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    shutil.copytree(TEMPLATE_DIR, dst)
    schema = {
        "name": f"{dst.name}_action",
        "description": "Generated FedMCP connector",
        "inputSchema": {
            "type": "object",
            "properties": {
                "example": {"type": "string", "description": "Example string input"}
            },
            "required": ["example"],
        },
        "compliance": {
            "pii_handling": True,
            "audit_log": True,
            "fedramp_level": "high",
        },
    }
    (dst / "tool.schema.json").write_text(json.dumps(schema, indent=2))
    typer.secho(f"✅  Connector scaffold created at {dst}", fg=typer.colors.GREEN)

@app.command("version", help="Show fmcpx version")
def show_version():
    typer.echo("fmcpx version 0.0.0-dev")

if __name__ == "__main__":  # pragma: no cover
    sys.exit(app())