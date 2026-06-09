# Note

Alright — here’s the **fully automatic** version where Typer will take defaults directly from a `Pydantic BaseSettings` config, so you don’t have to manually check `None` for each argument.

---

## Automatic Pydantic + Typer integration

```python
from pydantic import BaseSettings
import typer

app = typer.Typer()

# Step 1: Define a settings model that reads from env vars
class Config(BaseSettings):
    foo: str
    bar: int
    baz: bool = False

    class Config:
        env_prefix = ""  # e.g. "MYAPP_" if you want MYAPP_FOO
        case_sensitive = False


# Step 2: Helper to inject defaults into Typer from Pydantic settings
def settings_defaults(settings_cls):
    """
    Reads values from a Pydantic settings class and returns a decorator
    that sets Typer defaults from those values.
    """
    settings = settings_cls()

    def decorator(func):
        from inspect import signature
        sig = signature(func)
        new_params = []

        for name, param in sig.parameters.items():
            default = getattr(settings, name, param.default)
            if isinstance(param.default, typer.models.OptionInfo):
                # Clone the OptionInfo with a new default
                param = param.replace(default=default)
            else:
                param = param.replace(default=default)
            new_params.append((name, param))

        # Build a new function signature
        func.__signature__ = sig.replace(parameters=[p for _, p in new_params])
        return func

    return decorator


# Step 3: Use the decorator to auto-fill Typer defaults from env
@app.command()
@settings_defaults(Config)
def main(
    foo: str = typer.Option(..., help="Value for foo"),
    bar: int = typer.Option(..., help="Value for bar"),
    baz: bool = typer.Option(..., help="Value for baz"),
):
    typer.echo(f"foo={foo}, bar={bar}, baz={baz}")


if __name__ == "__main__":
    app()
```

---

### How this works

1. **`Config`** is a `BaseSettings` model, so it automatically loads from environment variables (and `.env` files if configured).
2. **`settings_defaults` decorator**:

   * Instantiates `Config()` to get env-based defaults.
   * Uses `inspect.signature()` to modify the defaults of your Typer command parameters.
   * Works even if you later add more CLI parameters — no manual changes needed.
3. **CLI behavior**:

   * If you set `FOO`, `BAR`, `BAZ` in the environment, those become defaults.
   * CLI arguments override environment defaults.
   * If neither is given, Pydantic raises a validation error for required fields.

---

**Example:**

```bash
export FOO=apple
export BAR=42
python app.py main
# Output: foo=apple, bar=42, baz=False

python app.py main --foo banana --baz
# Output: foo=banana, bar=42, baz=True
```

---

This approach means:

* You write **env var logic once** in your `Config`.
* Typer automatically picks up those defaults.
* No repetitive `None`-checking code.

---

Do you want me to also make this work so that **nested Pydantic models** (like `DatabaseSettings` inside `Config`) can also be automatically injected into Typer parameters? That’s a common pattern for large apps.
