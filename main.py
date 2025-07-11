import os
import threading
import time
from utils import *
from boats import AVAILABLE_BOATS
from doomper_gui import PauseUnpauseGUI
import tkinter as tk

def doomper_thread(boat:str):
    result = send_crystal_command(boat=boat, command="cd ~/data && sudo -E doomper --config doomper.json")

def main():
    valid_boat = False
    while not valid_boat:
        boat = input("Which Boat are you trying to calibrate? (Enter the name of the boat): ")
        if boat not in AVAILABLE_BOATS:
            print(f"Boat '{boat}' is not available. Please choose from the following list:")
            print(", ".join(AVAILABLE_BOATS))
            continue
        valid_boat = True

    print(f"Calibrating boat: {boat}")
    crystal = boat + "-crystal"
    crystal_version = send_crystal_command(boat=boat, command="grep '^IMAGE_VERSION=' /etc/os-release | cut -d'=' -f2")
    print(f"Commit Hash for {crystal}: {crystal_version}")

    # Skipped steps:
    # - Building the .#camera-position and .#metrical packages
    
    print("please make sure that the .#camera-position and .#metrical packages are built and copied to the crystal before proceeding.")

    input("Press Enter to continue with the calibration process...")

    send_crystal_command(boat=boat, command="mkdir ~/data")

    valid_location = False
    while not valid_location:
        location = input("is the boat inside or outside? (Enter 'inside' or 'outside'): ")
        if location not in ['inside', 'outside']:
            print("Invalid input. Please enter 'inside' or 'outside'.")
            continue
        valid_location = True

    print(f"Location: {location}")
    board_copy_result = send_local_command(command=f"scp {os.getcwd()}/assets/board-0.json saronic@cr10-crystal:/home/saronic/board-0.json")
    if location == 'inside':
        print("Using inside doomper.json for calibration.")
        doomper_copy_result = send_local_command(command=f"scp {os.getcwd()}/assets/doomper_indoors.json saronic@{crystal}:/home/saronic/data/doomper.json")
    else:
        print("Using outside doomper.json for calibration.")
        doomper_copy_result = send_local_command(command=f"scp {os.getcwd()}/assets/doomper.json saronic@{crystal}:/home/saronic/data/doomper.json")
    
    input("Press Enter to verify that all cameras are listed using arv-tool-0.8 ... ")

    result = send_crystal_command(boat=boat, command="arv-tool-0.8")
    print(result)
    arv_check = False
    while not arv_check:
        arv_tool_valid = input("Does the output look correct? ('yes' or 'no'): ")
        if arv_tool_valid == 'yes':
            print("arv-tool-0.8 output is valid.")
            arv_check = True
        elif arv_tool_valid == 'no':
            print("arv-tool-0.8 output is not valid. Please check the camera connections and try again.")
            continue
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
            continue
    
    # open_foxglove_result = send_local_command(command='open -a "Foxglove Studio"')
    print("Please check the output for torchyd2 to ensure it is running correctly...")
    result = send_crystal_command(boat=boat, command="jfu torchyd2")
    torchy_check = False
    while not torchy_check:
        torchy_valid = input("Does the output look correct? ('yes' or 'no'): ")
        if torchy_valid == 'yes':
            print("jfu torchyd2 output is valid.")
            torchy_check = True
        elif torchy_valid == 'no':
            print("jfu torchyd2 output is not valid. Please check the camera connections and try again.")
            continue
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
            continue

    result = send_crystal_command(boat=boat, command="sudo systemctl stop torchyd2")

    print("Torchyd2 service stopped. Please check the output for any errors...")

    result = send_crystal_command(boat=boat, command="sup torchyd2")
    torchy_check = False
    while not torchy_check:
        torchy_valid = input("Is torchyd2 stopped? ('yes' or 'no'): ")
        if torchy_valid == 'yes':
            print("jfu torchyd2 output is valid.")
            torchy_check = True
        elif torchy_valid == 'no':
            print("jfu torchyd2 output is not valid. Please check the camera connections and try again.")
            continue
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
            continue

    input(f"Press Enter to start doomper on {crystal}...")
    doomper_thread_instance = threading.Thread(target=doomper_thread, args=(boat,))
    doomper_thread_instance.start()
    print(f"Doomper thread starting, waiting for 15 seconds to ensure it is running...")
    time.sleep(15)

    gui = PauseUnpauseGUI(boat=boat)
    gui.run()

    doomper_thread_instance.join()

    # steps left: 
    # post processing the calibration.mcap file
    # deploying the json data to the /etc/calibration folder

if __name__ == "__main__":
    main()