import subprocess
import sys


def run_command(user_input):
    subprocess.run(user_input, shell=True, check=False)


if __name__ == "__main__":
    run_command(sys.argv[1])