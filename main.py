import asyncio 
import sys
from lib.banner import bann

def version():
    version = sys.version_info
    
    if (version > (3, 10)):
        print("SpyScraper only works with Python 3.10+.")
        print("[+] Go install the most recent version of python -> https://www.python.org/downloads/")


    from lib.launcher import launch
    print(bann)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(launch())
