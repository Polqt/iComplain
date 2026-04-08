import os
import sys
import time
import subprocess
import threading


DEFAULT_PORT = "8000"
DB_RETRY_ATTEMPTS = 20
DB_RETRY_DELAY_SECONDS = 5


def run_command(command: list[str]) -> None:
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, command)


def migrate_with_retries() -> None:
    migrate_command = [sys.executable, "manage.py", "migrate", "--noinput"]

    for attempt in range(1, DB_RETRY_ATTEMPTS + 1):
        try:
            print(
                f"Running migrations (attempt {attempt}/{DB_RETRY_ATTEMPTS})...",
                flush=True,
            )
            run_command(migrate_command)
            print("Migrations complete.", flush=True)
            return
        except subprocess.CalledProcessError as exc:
            if attempt == DB_RETRY_ATTEMPTS:
                print("Migrations failed after all retries. Exiting.", flush=True)
                raise exc

            print(
                "Database is not ready yet. "
                f"Retrying in {DB_RETRY_DELAY_SECONDS} seconds...",
                flush=True,
            )
            time.sleep(DB_RETRY_DELAY_SECONDS)


def migrate_in_background() -> None:
    thread = threading.Thread(target=migrate_with_retries, daemon=True)
    thread.start()


def start_daphne() -> None:
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


def main() -> None:
    migrate_in_background()
    start_daphne()


if __name__ == "__main__":
    main()
