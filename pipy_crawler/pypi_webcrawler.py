import requests
import json


class PyPIWebCrawler:
    pass


if __name__ == "__main__":
    res = requests.get("https://pypi.org/pypi/pip/json")
    response = res.json()
    print(response)