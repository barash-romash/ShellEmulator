import tarfile
import xml.etree.ElementTree as ET
from pprint import pprint


class ShellEmulator:
    def __init__(self, config_file):
        self.file_system_path = self.get_file_path(config_file)
        self.users = ["root", "User1"]
        self.users_files = {self.users[0]: [],
                            self.users[1]: []}
        self.user_name = self.users[0]
        self.fill_files_owner()
        self.prefix = self.user_name + ":~"
        self.cur_dir = []
        self.sfl = self.get_sys_file_list()

    def fill_files_owner(self):
        for i in tarfile.open(self.file_system_path, 'r').getnames():
            self.users_files[self.user_name] += [i]

    def get_file_path(self, config_file):
        tree = ET.parse(config_file)
        root = tree.getroot()
        return root.find('file_system_path').text

    def ls(self, arg=''):
        files = {}
        if arg == '-l':
            for [file] in self.get_dir_file_list():
                path_of_file = self.get_cur_dir_str() + file
                for owner in self.users:
                    if path_of_file in self.users_files[owner]:
                        files[file] = owner
            for file, owner in files.items():
                print(owner, file)
        elif arg != '':
            cur_dir = "/" + self.get_cur_dir_str()[:-1]
            if(self.cd(arg)):
                self.ls()
                self.cd(cur_dir)
        else:
            for [file] in self.get_dir_file_list():
                print(file, end='  ')
            print()

    def get_dir_file_list(self):
        fl = [f for f in self.sfl if len(f) == len(self.cur_dir) + 1]
        fl = [f for f in fl if all(f[i] == self.cur_dir[i] for i in range(len(self.cur_dir)))]
        fl = [f[len(self.cur_dir):] for f in fl]
        return fl

    def get_sys_file_list(self):
        with tarfile.open("system.tar") as tar:
            fl = [f.split('/') for f in tar.getnames()]
            return fl

    def cd(self, path):
        if path == "":
            return False
        elif path == '..':
            if len(self.cur_dir) != 0:
                self.cur_dir.pop()
                return True
        elif path == '/':
            self.cur_dir = []
            return True
        elif path[0] == '/':
            path = path[1:].split('/')
            if path in self.get_sys_file_list():
                self.cur_dir = path
                return True
            else:
                print("Не удаётся найти путь")
                return False
        else:
            path_split = path.split('/')
            with tarfile.open(self.file_system_path, 'r') as tar:
                if [path_split[0]] in self.get_dir_file_list() and \
                        (self.cur_dir + path_split) in self.get_sys_file_list() \
                        and tar.getmember(self.get_cur_dir_str() + path).isdir():
                    self.cur_dir.extend(path_split)
                    return True
                else:
                    print("Не удаётся найти путь")
                    return False

    def get_cur_dir_str(self):
        cur_dir_str = ''
        for i in self.cur_dir:
            cur_dir_str += i + '/'
        return cur_dir_str

    def pwd(self):
        print('/', end='')
        for i in self.cur_dir:
            print(i, end='/')
        print()

    def chown(self, arg):
        owner, filename = arg.split()
        if owner in self.users_files:
            path = self.get_cur_dir_str() + filename
            if path in tarfile.open(self.file_system_path).getnames():
                if path not in self.users_files[owner]:
                    for user in self.users:
                        try:
                            self.users_files[user].remove(path)
                        except ValueError:
                            pass
                    self.users_files[owner] += [path]
            else:
                print('Директория или файл не найдены')
        else:
            print("Пользователь не найден")

    def uniq(self, path):
        if len(path) == 0:
            return
        if path[0] != '/':
            path = self.get_cur_dir_str() + path
        with tarfile.open(self.file_system_path, 'r') as tar:
            try:
                file = tar.getmember(path)
            except KeyError:
                print("Файл не найден")
                return
            if not file.isfile():
                print("Невозможно обработать файл")
                return
            unique_lines = []
            previous_line = None

            for line in tar.extractfile(path):
                line = line.decode().strip()
                if line != previous_line:
                    unique_lines.append(line)
                    previous_line = line
            for i in unique_lines:
                print(i)

    def run(self):
        while True:
            line_start = f"{self.user_name}/{self.get_cur_dir_str()}:~ $"
            command = input(line_start).split(' ', 1)
            if len(command) == 0:
                continue
            elif command[0] == 'exit':
                break
            elif command[0] == 'ls':
                if len(command) == 2:
                    self.ls(command[1])
                else:
                    self.ls()
            elif command[0] == 'pwd':
                self.pwd()
            elif command[0] == 'cd':
                if len(command) > 1:
                    self.cd(command[1])
            elif command[0] == 'uniq':
                if len(command) > 1:
                    self.uniq(command[1])
            elif command[0] == 'chown':
                if len(command) > 1:
                    self.chown(command[1])
            elif command[0] == "sufl":
                pprint(self.users_files)
            else:
                print("Команда не найдена:", command[0])


if __name__ == '__main__':
    emulator = ShellEmulator('config.xml')
    emulator.run()
