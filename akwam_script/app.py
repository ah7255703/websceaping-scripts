from colorama.ansi import Style
from akwam import Akwam
import time
from fire import Fire
from colorama import Fore

try:
    if __name__ == '__main__':
        t1 = time.time()
        Fire(Akwam)
        t2 = time.time()
        print(
            f'{Fore.GREEN}[*]{Style.RESET_ALL} Executed in {Fore.RED}{int(t2-t1)} {Style.RESET_ALL}Second(s) \n')
except KeyboardInterrupt:
    print(f'\n{Fore.RED}[*] {Fore.BLUE}Terminated By The User')
