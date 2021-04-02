import requests
import json


class PyPIWebCrawler:
    pass


if __name__ == "__main__":
    package_name = "pip"
    res = requests.get("https://pypi.org/pypi/%s/json" % package_name)
    response = res.json()
    print(json.dumps(response,sort_keys=True, indent=2))
    print(__file__)
    f = open('./output/%s/requirement.json' % package_name,'a+')
    f.write(str(res.json()))
    f.close()