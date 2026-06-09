from pydantic_settings import BaseSettings
import typer
from typing import Annotated

app = typer.Typer()


# Step 1: Define a settings model that reads from env vars
class Config(BaseSettings):
    foo: str = "default_foo value"
    bar: int = 42
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
    # foo: str = typer.Option(..., help="Value for foo"),
    foo: Annotated[str, typer.Option(help="Value for foo")],
    bar: int = typer.Option(..., help="Value for bar"),
    baz: bool = typer.Option(..., help="Value for baz"),
):
    typer.echo(f"foo={foo}, bar={bar}, baz={baz}")


if __name__ == "__main__":
    app()


# To run:# 1. Create a .env file with:
#    FOO=hello
#    BAR=123
#    BAZ=true
# 2. Run the script without args:
#    python app.py
#    It should print: foo=hello, bar=123, baz=True
# 3. Override with command-line args:
#    python app.py --foo world --bar 456
#    It should print: foo=world, bar=456, baz=True

# Step 2[alternate]: Typer command using config as defaults
# @app.command()
# def main(
#     foo: str = typer.Option(None, help="Value for foo"),
#     bar: int = typer.Option(None, help="Value for bar"),
#     baz: bool = typer.Option(None, help="Value for baz"),
# ):
#     # Load from env vars first
#     config = Config()
#
#     # CLI args override env vars if provided
#     foo_value = foo if foo is not None else config.foo
#     bar_value = bar if bar is not None else config.bar
#     baz_value = baz if baz is not None else config.baz
#
#     typer.echo(f"foo={foo_value}, bar={bar_value}, baz={baz_value}")
