import os
from utils import *
from boats import AVAILABLE_BOATS

# Skipped steps:
# - Building the .#camera-position and .#metrical packages

def main():
    user = "saronic"
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
    
    

if __name__ == "__main__":
    main()