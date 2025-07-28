# main.py
import sys
from Device_Analysis import check_device
from App_Analysis import apk_permission_analysis, apk_hashing

DEBUG = False

def print_header():
    print("-" * 50)
    print(" Stonehaven - Static Android Security Toolkit ")
    print("-" * 50)

def main_menu():
    while True:
        print_header()
        print("[1] Check connected device")
        print("[2] APK Permission Analysis")
        print("[3] APK Hashing")
        print("[0] Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            check_device.run(DEBUG)
        elif choice == "2":
            apk_permission_analysis.run(DEBUG)
        elif choice == "3":
            apk_hashing.run(DEBUG)
        elif choice == "0":
            print("Exiting Stonehaven...")
            break
        else:
            print("[!] Invalid selection. Please try again.")

def parse_args():
    global DEBUG
    if "--debug" in sys.argv:
        DEBUG = True
        print("[DEBUG] Debug mode enabled.")

if __name__ == "__main__":
    parse_args()
    main_menu()
