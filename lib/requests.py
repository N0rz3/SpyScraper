import requests

class Requests:
    def __init__(self, 
                url: str,
                headers=None,
                timeout: int=5):
        self.url = url
        self.head = headers
        self.time = timeout

    async def sender(self):
        try:
            return requests.get(url=self.url, headers=self.head, timeout=self.time)

        except requests.HTTPError as h:
            print(f"[-] HTTP Error! : {h}")
            exit()