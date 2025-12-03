import platform
import subprocess
import sys

def clear_screen():
    """Clear terminal screen"""
    os_name = platform.system()
    if os_name == "Windows":
        subprocess.run('cls', shell=True)
    else:
        subprocess.run('clear', shell=True)

def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        sys.exit(1)
    return True

def get_os_info():
    """Get operating system information"""
    return {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine()
    }
