import typer
from rich import print
from rich.console import Console
from logic.process_alpaca import is_candidate


def main(symbol):
    print(symbol)

if __name__ == "__main__":
    typer.run(main)