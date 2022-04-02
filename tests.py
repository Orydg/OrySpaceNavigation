"""
Скрипт для быстрого тестирования сновного функционала

"""

from space import Space
from objects import SpaceObjects
from gui import GUI
from settings import Settings


class Test:
    """
    Класс для тестирования основного функционала

    """

    def test_gui(self):
        """
        Метод для тестирования GUI.

        """

        pass

    def test_space(self):
        """
        Метод для тестирования space.

        """

        # создали объект класса для тестов
        space = Space()

        # ввод стороннего объекта
        try:
            space.add_obj(1)
            raise Exception(f"Space.add_obj() прочитал объект, отличный от <class 'SpaceObjects'>")
        except AssertionError:
            pass

        # ввод некорретной массы
        try:
            space.add_obj(SpaceObjects('name', -100))
            raise Exception(f"Space.add_obj() прочитал объект с некорретной массой")
        except AssertionError:
            pass

    def test_objects(self):
        """
        Метод для тестирования objects.

        """

        pass


if __name__ == "__main__":

    Test().test_gui()
    Test().test_space()
    Test().test_objects()

    print('''
    Все тесты пройдены! Вы великолепны!
    ''')
