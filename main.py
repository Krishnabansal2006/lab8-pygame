from sim.game import run_game


def main() -> None:
    """Thin entry point: keeps startup separate from simulation internals."""
    run_game()


if __name__ == "__main__":
    main()
