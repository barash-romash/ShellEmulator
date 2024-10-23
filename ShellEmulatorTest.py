import io
import unittest
from ShellEmulator import ShellEmulator
from unittest.mock import patch


class ShellEmulatorTest(unittest.TestCase):
    def setUp(self):
        # Инициализация ShellEmulator перед каждым тестом
        self.se = ShellEmulator("config.xml")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ls_1(self, mock_stdout):
        self.se.ls()  # Вызов функции ls
        output = mock_stdout.getvalue().strip()  # Получение захваченного вывода
        self.assertEqual(output, "d  t.txt")  # Проверка на соответствие ожидаемому выводу

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ls_2(self, mock_stdout):
        self.se.ls('-l')
        output = mock_stdout.getvalue().strip()  # Получение захваченного вывода
        self.assertEqual(output, 'root d\nroot t.txt')  # Проверка на соответствие ожидаемому выводу

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ls_3(self, mock_stdout):
        self.se.chown('User1 d')
        self.se.ls('-l')
        output = mock_stdout.getvalue().strip()  # Получение захваченного вывода
        self.assertEqual(output, 'User1 d\nroot t.txt')  # Проверка на соответствие ожидаемому выводу

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_ls_4(self, mock_stdout):
        self.se.ls('-lkjfl')
        output = mock_stdout.getvalue().strip()  # Получение захваченного вывода
        self.assertEqual(output, 'Не удаётся найти путь')  # Проверка на соответствие ожидаемому выводу

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cd_1(self, mock_stdout):
        self.se.cd('d')
        self.se.pwd()
        output = mock_stdout.getvalue().strip()  # Получение захваченного вывода
        self.assertEqual(output, '/d/')  # Проверка на соответствие ожидаемому выводу

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cd_2(self, mock_stdout):
        self.se.cd('d/a')
        self.se.pwd()
        output = mock_stdout.getvalue().strip()  # Получение захваченного вывода
        self.assertEqual(output, '/d/a/')  # Проверка на соответствие ожидаемому выводу

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cd_3(self, mock_stdout):
        self.se.cd('d/a')
        self.se.cd('..')
        self.se.pwd()
        output = mock_stdout.getvalue().strip()  # Получение захваченного вывода
        self.assertEqual(output, '/d/')  # Проверка на соответствие ожидаемому выводу

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cd_4(self, mock_stdout):
        self.se.cd('t.txt')
        self.se.pwd()
        output = mock_stdout.getvalue().strip()  # Получение захваченного вывода
        self.assertEqual(output, 'Не удаётся найти путь\n/')  # Проверка на соответствие ожидаемому выводу

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_pwd_1(self, mock_stdout):
        self.se.pwd()
        output = mock_stdout.getvalue().strip()  # Получение захваченного вывода
        self.assertEqual(output, '/')  # Проверка на соответствие ожидаемому выводу

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_pwd_2(self, mock_stdout):
        self.se.cd('d')
        self.se.pwd()
        output = mock_stdout.getvalue().strip()  # Получение захваченного вывода
        self.assertEqual(output, '/d/')  # Проверка на соответствие ожидаемому выводу

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_pwd_3(self, mock_stdout):
        self.se.cd('d/a')
        self.se.pwd()
        output = mock_stdout.getvalue().strip()  # Получение захваченного вывода
        self.assertEqual(output, '/d/a/')  # Проверка на соответствие ожидаемому выводу

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_chown_1(self, mock_stdout):
        self.se.chown('User1 d')
        self.se.ls('-l')
        output = mock_stdout.getvalue().strip()  # Получение захваченного вывода
        self.assertEqual(output, 'User1 d\nroot t.txt')  # Проверка на соответствие ожидаемому выводу

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_chown_2(self, mock_stdout):
        self.se.chown('User2 d')
        output = mock_stdout.getvalue().strip()  # Получение захваченного вывода
        self.assertEqual(output, 'Пользователь не найден')  # Проверка на соответствие ожидаемому выводу

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_chown_3(self, mock_stdout):
        self.se.chown('User1 d')
        self.se.chown('root d')
        self.se.ls('-l')
        output = mock_stdout.getvalue().strip()  # Получение захваченного вывода
        self.assertEqual(output, 'root d\nroot t.txt')  # Проверка на соответствие ожидаемому выводу

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_uniq_1(self, mock_stdout):
        self.se.uniq('t.txt')
        output = mock_stdout.getvalue().strip()  # Получение захваченного вывода
        self.assertEqual(output, 'Apple\nPear\nApple\nPear\nCow')  # Проверка на соответствие ожидаемому выводу

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_uniq_2(self, mock_stdout):
        self.se.uniq('t')
        output = mock_stdout.getvalue().strip()  # Получение захваченного вывода
        self.assertEqual(output, 'Файл не найден')  # Проверка на соответствие ожидаемому выводу

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_uniq_3(self, mock_stdout):
        self.se.uniq('d')
        output = mock_stdout.getvalue().strip()  # Получение захваченного вывода
        self.assertEqual(output, 'Невозможно обработать файл')  # Проверка на соответствие ожидаемому выводу


if __name__ == '__main__':
    unittest.main()
