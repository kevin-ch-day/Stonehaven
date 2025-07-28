# main.py
import sys

DEBUG = False

def print_header():
    print("-" * 50)
    print(" Stonehaven - Static Android Security Toolkit ")
    print("-" * 50)

def main_menu():
    pass

def parse_args():
    global DEBUG
    if "--debug" in sys.argv:
        DEBUG = True
        print("[DEBUG] Debug mode enabled.")

if __name__ == "__main__":
    parse_args()
    main_menu()
