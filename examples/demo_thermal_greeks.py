"""Run the synthetic Cal/Val thermal-Greeks demo."""

from pathlib import Path

from hytes_calval.cli import run_demo

if __name__ == "__main__":
    print(run_demo(Path("outputs"), n=2500, seed=42).to_string(index=False))
