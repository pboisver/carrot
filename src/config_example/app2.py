from inspect import signature

import typer
from pydantic_settings import BaseSettings

app = typer.Typer()


class Config(BaseSettings):
    foo: str = "default_foo value"
    bar: int = 42
    baz: bool = False

    class Config:
        env_prefix = ""  # could be "MYAPP_" if desired
        case_sensitive = False


def settings_defaults(settings_cls):
    """
    Reads values from a Pydantic settings class and injects them into
    Typer command defaults. Also sets envvar=FIELDNAME (or with prefix)
    so CLI help shows which env vars are accepted.
    """
    settings = settings_cls()

    env_prefix = getattr(settings_cls.Config, "env_prefix", "") or ""

    def _compute_default(name, param):
        env_val = getattr(settings, name, None)
        if env_val is not None:
            return env_val
        if param.default is not param.empty:
            return param.default
        return ...

    def _apply_option_default(param, env_name, new_default):
        if not isinstance(param.default, typer.models.OptionInfo):
            return param.replace(default=new_default)

        opt_info = param.default
        opt_kwargs = opt_info.__dict__.copy()
        if not opt_kwargs.get("envvar"):
            opt_kwargs["envvar"] = env_name
        opt_kwargs["default"] = new_default
        return param.replace(default=typer.models.OptionInfo(**opt_kwargs))

    def decorator(func):
        sig = signature(func)
        new_params = []

        for name, param in sig.parameters.items():
            env_name = f"{env_prefix}{name}".upper()
            new_default = _compute_default(name, param)
            param = _apply_option_default(param, env_name, new_default)
            new_params.append((name, param))

        func.__signature__ = sig.replace(parameters=[p for _, p in new_params])
        return func

    return decorator


@app.command()
@settings_defaults(Config)
def main(
    foo: str = typer.Option(..., help="Value for foo"),
    bar: int = typer.Option(..., help="Value for bar"),
    baz: bool = typer.Option(..., help="Value for baz", show_default=True),
):
    typer.echo(f"foo={foo}, bar={bar}, baz={baz}")


if __name__ == "__main__":
    app()
