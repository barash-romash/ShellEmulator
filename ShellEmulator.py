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
        print(*self.get_list_of_files(), sep='  ')
        print()

    def get_list_of_files(self):
        with tarfile.open(self.file_system_path) as tar:
            all_files = tar.getnames()
            files_here = [f for f in all_files if "/" not in f]
            return files_here
            # TODO(Сделать проверку на директорию)

    def cd(self, path):
        with tarfile.open(self.file_system_path) as tar:
            slash_pos = path.find("/")
            file_list = self.get_list_of_files()
            while len(path) != 0:
                if path[:slash_pos + 1] in file_list:
                    path = path[slash_pos + 1:]
                    self.current_directory += path[:slash_pos]
                    # TODO(Завершить обновление переменных)

    def pwd(self):
        return self.current_directory

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
            # Обработка других команд


# Пример запуска
emulator = ShellEmulator('config.xml')
emulator.run()
