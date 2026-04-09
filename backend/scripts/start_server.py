import os
import sys


DEFAULT_PORT = "8000"


def main() -> None:
    port = os.getenv("PORT", DEFAULT_PORT)
    daphne_command = [
        sys.executable,
        "-m",
        "daphne",
        "-b",
        "0.0.0.0",
        "-p",
        port,
        "config.asgi:application",
    ]
    os.execvp(daphne_command[0], daphne_command)


if __name__ == "__main__":
    main()
