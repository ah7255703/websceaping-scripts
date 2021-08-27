from anime4up import Anime4UP
from fire import Fire
import time
from colorama import Style, Fore

if __name__ == '__main__':
    time_start = time.time()
    Fire(Anime4UP)
    time_end = time.time()
    print(
        f"{Fore.GREEN}[-]{Style.RESET_ALL} Executed in {int(time_end-time_start)} Seconds")
