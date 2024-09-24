import os
import tarfile
import xml.etree.ElementTree as ET


class ShellEmulator:
    def __init__(self, config_file):
        self.file_system_path = self.get_file_path(config_file)
        self.users = ["User1", "User2"]
        self.user_name = self.users[0]
        self.prefix = self.user_name + ":~"
        self.current_directory = ""

    def get_file_path(self, config_file):
        tree = ET.parse(config_file)
        root = tree.getroot()
        return root.find('file_system_path').text

    def ls(self):
        print(*self.get_directory_file_names(), sep='  ')

    def cut(self, str, substr):
        f = str.find(substr)
        if f == 0:
            return str[len(substr)+1:]
        return str

    def get_directory_file_names(self):
        with tarfile.open(self.file_system_path) as tar:
            all_files = [self.cut(f, self.current_directory) for f in tar.getnames()]
            files_here = [f for f in all_files if "/" not in f]
            return files_here

    def cd(self, path):
        print(path)
        path_list = path.split("/")
        print(path_list)
        with tarfile.open(self.file_system_path) as tar:
            old_directory = self.current_directory
            for i in path_list:
                if i in self.get_directory_file_names():
                    self.current_directory += "/" + i
                else:
                    self.current_directory = old_directory
                    print(f"Директория {i} не найдена")
                    break


    def pwd(self):
        return "/home/" + self.user_name + '/' + self.current_directory

    def chown(self, owner, path):
        # Реализация изменения владельца
        pass

    def uniq(self, filename):
        # Реализация фильтрации уникальных строк
        pass

    def run(self):
        while True:
            command = input(f"{self.prefix} $ ")
            if command == 'exit':
                break
            elif command == 'ls':
                self.ls()
            elif command[:2] == 'cd':
                self.cd(command[3:])
            elif command == 'pwd':
                print(self.pwd())
            # Обработка других команд


# Пример запуска
emulator = ShellEmulator('config.xml')
emulator.run()
