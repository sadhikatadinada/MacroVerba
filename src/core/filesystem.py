from pathlib import Path

def ensure_directories(directories: list[Path]) -> None:
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)