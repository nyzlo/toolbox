import argparse
import logging
from modules.misc import logger_config, load_usernames, load_passwords
from arakaali.arakaali import run_spoder
from chen.chen import run_chen
from aiur.aiur import run_aiur


def main():
    # Toolbox
    parser = argparse.ArgumentParser(description="Toolbox for various scripts")
    subparsers = parser.add_subparsers(dest="command")

    # Arakaali
    arakaali_parser = subparsers.add_parser("arakaali", help="Run Arakaali")
    arakaali_parser.add_argument("start_url", help="The starting URL for the web crawler")

    # Chen
    chen_parser = subparsers.add_parser("chen", help="Run Chen")
    chen_parser.add_argument("domain", help="The domain to run Chen against")

    # Aiur
    aiur_parser = subparsers.add_parser("aiur", help="Run Aiur")
    aiur_parser.add_argument("-H", required=True, help="The target host")
    aiur_parser.add_argument("-s", required=True, choices=["ssh", "ftp"], help="Pick a service to bruteforce")
    aiur_parser.add_argument("-l", help="Target username")
    aiur_parser.add_argument("-L", help="Username wordlist")
    aiur_parser.add_argument("-p", help="Target password")
    aiur_parser.add_argument("-P", help="Password wordlist")
    aiur_parser.add_argument("-t", type=int, help="The port to connect to (default: SSH 22, FTP 21)")

    args = parser.parse_args()

    if args.command == "arakaali":
        logger_config("arakaali")
        run_spoder(args.start_url)

    elif args.command == "chen":
        logger_config("chen")
        print(f"Scanning for subdomains...\n")
        run_chen(args.domain)

    elif args.command == "aiur":
        logger_config("aiur")
        usernames = load_usernames(args.l, args.L)
        passwords = load_passwords(args.p, args.P)
        port = args.t

        if not usernames or not passwords:
            print("Incorrect username or password syntax --Help for commands")
            return

        run_aiur(args.H, args.s, usernames, passwords, port)

if __name__ == "__main__":
    main()
