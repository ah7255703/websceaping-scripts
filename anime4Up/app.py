from anime4up import Anime4UP
from fire import Fire
import time
from colorama import Style, Fore

import time
from tqdm import tqdm


def main():

    time_start = time.time()
    Fire(Anime4UP)

    time_end = time.time()
    print(
        f"{Fore.GREEN}[-]{Style.RESET_ALL} Executed in {round(time_end-time_start,2)} Seconds")


if __name__ == '__main__':
    main()
