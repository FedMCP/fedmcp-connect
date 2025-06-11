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
app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})

TEMPLATE_DIR: Final[pathlib.Path] = pathlib.Path(__file__).parent / "templates" / "basic"

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def _copy_template(dst: pathlib.Path) -> None:
    """Copy basic template + create tool.schema.json."""
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

@app.command("init", help="Scaffold a new FedMCP connector project.")
def init_cmd(name: str):
    dst = pathlib.Path(name).resolve()
    if dst.exists():
        typer.secho(f"❌ Directory '{dst}' already exists", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    _copy_template(dst)
    typer.secho(f"✅  Connector scaffold created at {dst}", fg=typer.colors.GREEN)

# default behaviour when no sub‑command provided
@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    name: str | None = typer.Argument(None, help="Folder name for the new connector"),
):
    """Fallback so `python -m fmcpx <NAME>` works."""
    if ctx.invoked_subcommand is None:
        if name:
            # Re‑use the same logic as explicit command
            ctx.invoke(init_cmd, name=name)
        else:
            typer.echo(ctx.get_help())
            raise typer.Exit()

if __name__ == "__main__":  # pragma: no cover
    sys.exit(app())