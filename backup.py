#!/usr/bin/python3
import subprocess
from pathlib import Path
import os
import argparse

def parse_args():
    # Setting up parser and subparsers
    parser = argparse.ArgumentParser(prog="backup.py", description="Simple Linux backup script")
    subparsers = parser.add_subparsers(dest="command")

    # Create the 'path' argument
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        help="Path of the file or directory to back up"
    )
    parser.add_argument(
        "-d", "--destination", 
        type=Path, 
        help="Destination file/directory to back up to"
    )

    # Create the 'db' command and '--user' flag
    parser.add_argument(
        "--db", 
        action="store_true",
        help="Backup all MySQL databases"
    )
    parser.add_argument("-u", "--user", help="MySQL user")

    args = parser.parse_args()

    return args, parser


def main(args, parser):
    
    if args.db:
        if not args.user:
            parser.error("--db requires --user")
        if args.path:
            parser.error("--db cannot be used with a file path")
        backup_sql_db(Path.cwd(), args.user)

    elif args.path:
        backup_file(args.path, args.destination or Path.cwd() / args.path.name)

    else:
        backup_predefined()


def backup_sql_db(backup_dir: Path, db_user: str) -> None:
    backup_file = backup_dir / f"db.sql.bak"

    cmd = [
        "mysqldump",
        "--all-databases",
        "--single-transaction",
        "--routines",
        "--events",
        "--triggers",
        "-u", f"{db_user}",
        "-p"
    ]

    try:
        with backup_file.open("w") as f:
            subprocess.run(cmd, stdout=f, check=True)

    except subprocess.CalledProcessError:
        print("Database backup failed. Check user/password.")
        
    
def backup_file(path, destination=Path.cwd()):
    
    backed_dest = destination.with_name(destination.name + ".bak")
    print(backed_dest)

    cmd = [
        "cp",
        "-ar",
        f"{path}",
        f"{backed_dest}"
    ]

    try:
        subprocess.run(cmd, stdout=None, check=True)

    except subprocess.CalledProcessError:
        print("File backup failed")


def backup_predefined():
    print("Defualt behavior hasn't been implemented yet. Please run with the -h to get help!")


if __name__ == "__main__":
    args, parser = parse_args()
    main(args, parser)
