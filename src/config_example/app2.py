from pydantic_settings import BaseSettings
import typer
from inspect import signature

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

    # Capture env_prefix from Pydantic config
    env_prefix = getattr(settings_cls.Config, "env_prefix", "") or ""

    def decorator(func):
        sig = signature(func)
        new_params = []

        for name, param in sig.parameters.items():
            env_val = getattr(settings, name, None)
            env_name = f"{env_prefix}{name}".upper()

            # Determine default: env_val if set, else keep required/defined
            if env_val is not None:
                new_default = env_val
            else:
                new_default = param.default if param.default is not param.empty else ...

            # If it's a Typer Option, add envvar if not already set
            if isinstance(param.default, typer.models.OptionInfo):
                # Merge existing OptionInfo kwargs with envvar + new default
                opt_info = param.default
                opt_kwargs = opt_info.__dict__.copy()

                # Avoid overriding if user manually set envvar
                if "envvar" not in opt_kwargs or not opt_kwargs["envvar"]:
                    opt_kwargs["envvar"] = env_name

                opt_kwargs["default"] = new_default
                param = param.replace(default=typer.models.OptionInfo(**opt_kwargs))
            else:
                param = param.replace(default=new_default)

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
