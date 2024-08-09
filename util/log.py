from prompt_toolkit import prompt
from termcolor import colored

class logger:

    def log(text):
        print(colored(f"[+] {text}", "light_blue"))
    
    def warn(text):
        print(colored(f"[!] {text}", "light_yellow"))

    def error(text):
        print(colored(f"[!] {text}", "red"))
