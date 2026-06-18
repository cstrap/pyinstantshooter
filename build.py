#!/usr/bin/env python3
"""
Build script for pyInstantShooter (Python3Tk).

Usage:
    python3 build.py            # builds both targets
    python3 build.py zipapp     # only zipapp
    python3 build.py pyinstaller # only PyInstaller
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import zipapp

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "Python3Tk")
PLUGINS = os.path.join(ROOT, "plugins")
DIST = os.path.join(ROOT, "dist")


def build_zipapp():
    out_dir = os.path.join(DIST, "zipapp")
    os.makedirs(out_dir, exist_ok=True)

    old_plugins = os.path.join(out_dir, "plugins")
    if os.path.exists(old_plugins):
        shutil.rmtree(old_plugins)

    pyz = os.path.join(out_dir, "pyinstantshooter.pyz")
    with tempfile.TemporaryDirectory() as staging:
        shutil.copytree(
            SRC,
            staging,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        shutil.copytree(PLUGINS, os.path.join(staging, "plugins"))
        zipapp.create_archive(staging, pyz, interpreter="/usr/bin/env python3")

    print(f"[zipapp] done → {out_dir}/")
    print(f"         run : python3 {os.path.relpath(pyz)}")


def build_pyinstaller():
    out_dir = os.path.join(DIST, "pyinstaller")
    build_dir = os.path.join(DIST, "_pyi_build")
    spec_dir = os.path.join(DIST, "_pyi_build")

    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(build_dir, exist_ok=True)

    sep = os.pathsep
    add_data = f"{PLUGINS}{sep}plugins"

    subprocess.run(
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",
            "--windowed",
            f"--add-data={add_data}",
            f"--distpath={out_dir}",
            f"--workpath={build_dir}",
            f"--specpath={spec_dir}",
            "--name=pyinstantshooter",
            os.path.join(SRC, "pyinstantshooter.py"),
        ],
        check=True,
        cwd=ROOT,
    )

    print(f"[pyinstaller] done → {out_dir}/")


def main():
    parser = argparse.ArgumentParser(
        description="Build pyInstantShooter distributables."
    )
    parser.add_argument(
        "target",
        nargs="?",
        choices=["zipapp", "pyinstaller", "all"],
        default="all",
        help="What to build (default: all)",
    )
    args = parser.parse_args()

    if args.target in ("zipapp", "all"):
        build_zipapp()

    if args.target in ("pyinstaller", "all"):
        build_pyinstaller()


if __name__ == "__main__":
    main()
