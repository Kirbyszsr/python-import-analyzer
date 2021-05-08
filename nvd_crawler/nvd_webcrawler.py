import requests
import json
import os


class NVDWebCrawler:
    def __init__(self, packages, force_updating=False):
        """
        PYPI WebCrawler
        :param packages: list[str]
        a list of name of packages
        """
        assert (isinstance(packages, list))
        for element in packages:
            assert (isinstance(element, str))
        self.packages = packages
        self.result = {}
        self.force_updating = force_updating

    def parse(self):
        for package_name in self.packages:
            try:
                path = './output/%s/' % package_name
                if not self.force_updating:
                    if os.path.exists(path + 'nvd-simple.json'):
                        print(
                            "[NVDWebCrawler]parsing package %s found nvd-simple.json" %
                            package_name)
                        is_succeed = False
                        f = None
                        try:
                            f = open(path + 'nvd-simple.json', 'r')
                            basic_info = json.load(f)
                            self.result[package_name] = basic_info
                            print(
                                "[parse succeed]package_name: %s" %
                                package_name)
                            is_succeed = True
                        except Exception as e:
                            print(
                                "[NVDWebCrawler]Error when parsing nvd-simple.json:%s" %
                                e.__str__())
                            print("[NVDWebCrawler]now downloading data")
                        finally:
                            if f:
                                f.close()
                        if is_succeed:
                            continue
                res = requests.get(
                    "https://services.nvd.nist.gov/rest/json/cves/1.0",
                    {"keyword": package_name,
                     "isExactlyMatch": True})

                if res.status_code != 200:
                    raise RuntimeError("Internet Error, status code=%d" % res.status_code)

                response = res.json()
                # print(json.dumps(response,sort_keys=True, indent=2))

                if not os.path.exists(path):
                    # make dirs for packages that have not been parsed
                    os.makedirs(path)
                f = open(path + 'cve.json', 'w+')
                json.dump(response, f, indent=2)
                f.close()

                if "error" in response.keys():
                    basic_info = []
                else:
                    # parse nvd.json to nvd-simple.json
                    cves = response['result']['CVE_Items']
                    basic_info = [{
                        "cveID": cve["cve"]["CVE_data_meta"]["ID"],
                        "cveASSIGNER": cve["cve"]["CVE_data_meta"]["ASSIGNER"],
                        "publishedDate": cve["publishedDate"],
                        "lastModifiedDate": cve["lastModifiedDate"],
                        "description": cve["cve"]["description"]["description_data"],
                        "references": cve["cve"]["references"]["reference_data"]
                        }
                        for cve in cves]
                f = open(path + 'nvd-simple.json', 'w+')
                json.dump(basic_info, f, indent=2)
                f.close()
                self.result[package_name] = basic_info
                print('[parse succeed]package_name: %s' % package_name)
            except Exception as e:
                print('[exception]Exception occurred: %s' % e.__str__())
                print('[parse failed]package_name: %s' % package_name)
                self.result[package_name] = {"Exception": e.__str__()}
                continue
        return self.result


if __name__ == "__main__":
    package_names = ["hnya123", "pip", "requests", "django"]
    wrapper = NVDWebCrawler(package_names, True)
    print(wrapper.parse())
