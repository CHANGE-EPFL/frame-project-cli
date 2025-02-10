import typer

app = typer.Typer()


@app.command()
def list():
    print("Listing")


if __name__ == "__main__":
    app()
