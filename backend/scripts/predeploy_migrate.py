import subprocess
import sys
import time


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
                f"Running pre-deploy migrations (attempt {attempt}/{DB_RETRY_ATTEMPTS})...",
                flush=True,
            )
            run_command(migrate_command)
            print("Pre-deploy migrations complete.", flush=True)
            return
        except subprocess.CalledProcessError as exc:
            if attempt == DB_RETRY_ATTEMPTS:
                print("Pre-deploy migrations failed after all retries.", flush=True)
                raise exc

            print(
                "Database is not ready yet. "
                f"Retrying in {DB_RETRY_DELAY_SECONDS} seconds...",
                flush=True,
            )
            time.sleep(DB_RETRY_DELAY_SECONDS)


def seed_admin_from_env() -> None:
    seed_command = [sys.executable, "manage.py", "seed_admin_from_env"]
    print("Running admin seed command...", flush=True)
    run_command(seed_command)
    print("Admin seed command complete.", flush=True)


if __name__ == "__main__":
    migrate_with_retries()
    seed_admin_from_env()
