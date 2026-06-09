import typer
import uvicorn
from carrot.shared import get_shared_state

cli = typer.Typer()


@cli.command()
def batch(
    file: str = typer.Option(..., help="File path"),
    max: int = typer.Option(..., help="Maximum value"),
    stats: bool = typer.Option(False, help="Show stats"),
):
    # Placeholder logic for batch command
    typer.echo(f"Batch processing file: {file}, max: {max}, stats: {stats}")


@cli.command()
def run(
    max: int = typer.Option(..., help="Maximum value"),
    render: bool = typer.Option(False, help="Render output"),
):
    state = get_shared_state()
    state["max_value"] = max
    state["render_value"] = render
    typer.echo(f"Context: {state}\n")
    uvicorn.run("carrot.web:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    cli()
