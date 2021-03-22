# File.py
# 用于定义项目中所需要的文件系统

__all__ = 'File'


class File(object):
    """
    定义项目中所需要的文件类
    """
    def __init__(self, filename, file_type="file", owned_by=None):
        self.__filename = filename
        self.__file_type = file_type
        self.owned_by = owned_by
        self.owns = []
        return

    def __copy__(self):
        return File(self.__filename,self.__file_type,self.owned_by)

    def __str__(self):
        return self.filename

    #def __repr__(self):
    #    return self.filename

    #文件名
    @property
    def filename(self):
        return self.__filename

    @property
    def get_suffix(self):
        return self.__filename.split(".")[-1].lower()
    #文件种类:
    #
    # file:文件
    # folder:文件夹
    @property
    def file_type(self):
        return self.__file_type

    def is_type(self, file_type):
        return file_type == self.file_type

    # 上一级文件夹
    def owned_by(self):
        # self.owned_by是一个文件
        return self.owned_by

    # 如果文件是一个文件夹,返回其拥有的文件夹列表
    def owns(self):
        if self.file_type != "folder":
            return None
        return self.owns

    def add(self,file):
        if isinstance(file,list):
            for file in list:
                self.add(file)
            return
        else:
            if isinstance(file,File):
                self.owns = self.owns + [file]
                file.owned_by = self
                return
            # 如果不是File则略过

    # 为文件删除关联关系
    def delete(self,file):
        if isinstance(file,File):
            if file not in self.owns:
                return
            else:
                self.owns.remove(file)
                file.owned_by = None
                return

    # 寻找文件夹下所属文件
    def find(self,name=''):
        if self.is_type('folder'):
            if name == '':
                return self.owns
            for file in self.owns:
                if file.filename.lower() == name.lower():
                    return file
        return None

    def find_all(self):
        return self.find()

    # 绘制树的关系图
    def print_tree(self,root=0):
        for i in range(1,root):
            print('       ',end='')
        if root != 0:
            print('|———', end='')
        print('['+self.filename+ ' type:'+ self.__file_type + ']')
        for file in self.owns:
            file.print_tree(root + 1)
        return


    #为文件返回文件url
    def get_concrete_url(self,base_url = ''):
        url = self.filename
        file = self
        while file.owned_by:
            file = file.owned_by
            url = file.filename + '\\' + url
        return base_url + url


if __name__ == "__main__":
    file_a = File("main","folder")
    print('file_a.filename=', file_a.filename)
    file_b = File("sub","folder")
    print('file_b.filename=', file_b.filename)

    file_a.add(file_b)
    print('file_a.owns=', file_a.owns)
    print('file_b.owned_by', file_b.owned_by)
    print('tree 1:')
    file_a.print_tree()

    file_a.delete(file_b)
    print('file_a.owns=', file_a.owns)
    print('file_b.owned_by', file_b.owned_by)
    print('tree 2:')
    file_a.print_tree()

    file_c = File("sub1","folder")
    file_a.add(file_b)
    file_a.add(file_c)
    print('tree 3:')
    file_a.print_tree()

    file_d = File("sub2")
    file_b.add(file_d)
    print('tree 4:')
    file_a.print_tree()

    print(file_d.get_concrete_url())
    file_copy = file_a.__copy__()
    print('tree 5:')
    file_copy.print_tree()