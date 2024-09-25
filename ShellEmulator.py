import os
import tarfile
import xml.etree.ElementTree as ET


class ShellEmulator:
    def __init__(self, config_file):
        self.file_system_path = self.get_file_path(config_file)
        self.users = ["User1", "User2"]
        self.user_name = self.users[0]
        self.prefix = self.user_name + ":~"
        self.cur_dir = []
        self.sfl = self.get_sys_file_list()

    def get_file_path(self, config_file):
        tree = ET.parse(config_file)
        root = tree.getroot()
        return root.find('file_system_path').text

    def ls(self):
        for i in self.get_dir_file_list():
            print(*i, end='  ')
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
        if path == '..':
            self.cur_dir.pop()
        elif path == '/':
            self.cur_dir = []
        elif path[0] == '/':
            path = path[1:].split('/')
            if path in self.get_sys_file_list():
                self.cur_dir = path
            else:
                print("Не удаётся найти путь")
        else:
            path = path.split('/')
            if path in self.get_dir_file_list():
                self.cur_dir.extend(path)
            else:
                print("Не удаётся найти путь")

    def pwd(self):
        print('/', end='')
        for i in self.cur_dir:
            print(i, end='/')
        print()

    def chown(self, owner, path):
        # Реализация изменения владельца
        pass

    def uniq(self, file_name):
        if [file_name] in self.get_dir_file_list():
            print(1)

    def run(self):
        while True:
            command = input(f"{self.prefix} $ ")
            if command == 'exit':
                break
            elif command == 'ls':
                self.ls()
            elif command[:2] == 'cd':
                if len(command) >= 4:
                    self.cd(command[3:])
            elif command == 'pwd':
                self.pwd()
            elif command == 'uniq':
                self.uniq()
            # Обработка других команд


emulator = ShellEmulator('config.xml')
emulator.run()
