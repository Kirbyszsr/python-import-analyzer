# Versions.py
# 定义版本号

__all__ = 'Version'


# 为版本截取的部分比较大小
def compare_version_part(part1, part2):
    assert(isinstance(part1,str))
    assert(isinstance(part2,str))
    try:
        part1_number = int(part1)
        part2_number = int(part2)
        return 0 if part1_number == part2_number else \
            int((part1_number - part2_number) / abs(part1_number - part2_number))
    except ValueError:
        return 0 if part1 == part2 else -1 if part1 < part2 else 1


class Version:
    def __init__(self,version_str):
        assert(isinstance(version_str,str))
        self.version_str = version_str
        self.version = version_str.split(".")

    def compare(self, other):
        assert(isinstance(other,Version))
        len_a = len(self.version)
        len_b = len(other.version)
        i = 0
        while i < len_a and i < len_b:
            if compare_version_part(self.version[i],other.version[i]):
                return compare_version_part(self.version[i], other.version[i])
            i += 1
        return len_a < len_b

    def __cmp__(self, other):
        if isinstance(other,Version):
            return self.compare(other)
        elif isinstance(other,str):
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
    version_b = Version("3.1a.5a")
    print(compare_version_part("3", '3a'))
    print(version_a == version_b)
