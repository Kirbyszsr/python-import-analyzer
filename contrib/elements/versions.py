# Versions.py
# 定义版本号
import re


__all__ = 'Version'


# 为版本截取的部分比较大小
def compare_version_part(part1, part2):
    assert(isinstance(part1, str))
    assert(isinstance(part2, str))
    try:
        part1_number = int(part1)
        part2_number = int(part2)
        return 0 if part1_number == part2_number else int(
            (part1_number - part2_number) / abs(part1_number - part2_number))
    except ValueError:
        return 0 if part1 == part2 else -1 if part1 < part2 else 1


class Version:
    def __init__(self, version_str):
        assert(isinstance(version_str, str))
        self.version_str = version_str
        self.version = version_str.split(".")

    def compare(self, other):
        assert(isinstance(other, Version))
        len_a = len(self.version)
        len_b = len(other.version)
        i = 0
        while i < len_a and i < len_b:
            if compare_version_part(self.version[i], other.version[i]):
                return compare_version_part(self.version[i], other.version[i])
            i += 1
        return len_a < len_b

    @staticmethod
    def check_clear(version_list):
        cleared_list = []
        # todo: 错误列表暂时先不使用
        error_list = []

        for element in version_list:
            assert(isinstance(element, str))
        # 先清理 *
        for version_str in version_list:
            if version_str != '*':
                cleared_list.append(version_str)

        symbols = ['<','<=','>','>=','==','!=']
        versions = [[], [], [], [], [], []]
        version_dict = dict(zip(symbols,versions))
        for version_str in cleared_list:
            elements = re.findall("([!><=]+)([0-9].*)",string=version_str)[0]
            for symbol in symbols:
                if elements[0] == symbol:
                    version_dict[symbol].append(Version(elements[1]))
        version_dict['<'] = [min(version_dict['<'])] if version_dict['<'] else []
        version_dict['<='] = [min(version_dict['<='])] if version_dict['<='] else []
        version_dict['>'] = [max(version_dict['>'])] if version_dict['>'] else []
        version_dict['>='] = [max(version_dict['>='])] if version_dict['>='] else []

        if version_dict['<'] and version_dict['<=']:
            if version_dict['<'][0] <= version_dict['<='][0]:
                version_dict['<='] = []
            else:
                version_dict['<'] = []
        if version_dict['>'] and version_dict['>=']:
            if version_dict['>'][0] <= version_dict['>='][0]:
                version_dict['>='] = []
            else:
                version_dict['>'] = []

        result_list = []
        for key, values in version_dict.items():
            for version in values:
                result_str = key + version.version_str
                result_list.append(result_str)

        return (['*'] if not cleared_list else result_list), error_list

    def __cmp__(self, other):
        if isinstance(other, Version):
            return self.compare(other)
        elif isinstance(other, str):
            return self.__cmp__(Version(other))
        else:
            return NotImplemented

    def __lt__(self, other):
        return self.compare(other) == -1

    def __le__(self, other):
        return self.compare(other) <= 0

    def __gt__(self, other):
        return self.compare(other) == 1

    def __ge__(self, other):
        return self.compare(other) >= 0

    def __eq__(self, other):
        return self.compare(other) == 0

    def __str__(self):
        return "<version %s>" % self.version_str


if __name__ == "__main__":
    version_a = Version("3.1a.5a")
    version_b = Version("3.1a.6a")
    print(compare_version_part("3", '3a'))
    print(version_a == version_b)
    print(max(version_a,version_b))
