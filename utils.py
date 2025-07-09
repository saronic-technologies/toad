import subprocess

def send_imx8_command(boat: str, command) -> subprocess.Popen:
    user_at_host = f"saronic@{boat}"
    timeout = 10
    
    try:
        result = subprocess.run(
            ["ssh", user_at_host, command],
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout  
        )

        return result.stdout
    except:
        return "Error: Command execution failed"

import subprocess

def send_crystal_command(boat: str, command) -> subprocess.Popen:
    user_at_host = f"saronic@{boat}-crystal"
    timeout = 10
    
    try:
        result = subprocess.run(
            ["ssh", user_at_host, command],
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout  
        )

        return result.stdout

    except:
        return "Error: Command execution failed"

def send_local_command(command: str) -> subprocess.Popen:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout

    except:
        return "Error: Command execution failed"