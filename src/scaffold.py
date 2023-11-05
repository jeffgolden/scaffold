import pathlib
import os
import json
import argparse
from typing import Dict, Any

def parse_arguments() -> str:
    """Parses the CLI arguments and returns the scaffold file"""
    parser = argparse.ArgumentParser(
        description="Creates files and folders based on a structure specified in a supplied JSON file.")
    parser.add_argument("--scaffold-file", required=True)
    ns = parser.parse_args()
    return ns.scaffold_file


def read_scaffold_file(scaffold_file: str) -> Dict[str, Any]:
    """Reads the scaffold file and returns it as a dictionary"""
    try:
        with open(scaffold_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{scaffold_file} not found.")
        return None
    except Exception:
        print(f"Unexcpected Error.")
        return None


def create_folders(scaffold: Dict[str, Any]) -> None:
    """Creates the folders in scaffold['folers']"""
    try:
        if "folders" in scaffold:
            for folder in scaffold["folders"]:
                pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    except Exception as ex:
        print(f"Error creating {folder} - {ex}")


def create_files(scaffold: Dict[str, Any]) -> None:
    """Creates and populates the files in scaffold['files']"""
    last_file = None
    if "files" in scaffold:
        try:
            for file, contents in scaffold["files"].items():
                last_file =file
                contents = [f"{l}\n" for l in contents]
                pathlib.Path(os.path.dirname(os.path.abspath(file))).mkdir(parents=True, exist_ok=True)
                with open(file, "w") as f:
                    f.writelines(contents)
        except Exception as ex:
            print(f"Error creating {last_file} - {ex}")


def main():
    """Entrypoint of program"""
    scaffold_file = parse_arguments()

    if scaffold_file is None:
        exit()

    scaffold = read_scaffold_file(scaffold_file)
    if scaffold is None:
        exit()

    create_folders(scaffold)
    create_files(scaffold)


if __name__ == "__main__":
    main()
