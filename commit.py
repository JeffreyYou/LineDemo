import os
import subprocess

if __name__ == '__main__':
    subprocess.call("git pull origin main", shell=True)
    message = input("Please enter your git commit message:\n")
    subprocess.call("git add -A", shell=True)
    subprocess.call("git commit -m \"" + message + "\"", shell=True)
    subprocess.call("git push origin main", shell=True)
