"""
Скрипт для быстрого тестирования сновного функционала

"""

from space import Space
from objects import SpaceObjects


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

        # создали объект класса для тестов
        object_test = SpaceObjects('Earth', 5.9722 * 10 ** 24, 6371302)

        # проверка v1 на корректность
        assert round(object_test.first_cosmic_velocity() / 1000, 1) == 7.9

        # проверка v1 при неправильном радиусе
        try:
            object_test_v1 = SpaceObjects('Earth', 5.9722 * 10 ** 24, 0)
            object_test_v1.first_cosmic_velocity()
            raise Exception(f"SpaceObjects.first_cosmic_velocity() прочитал объект с некорретным радиусом")
        except AssertionError:
            pass


if __name__ == "__main__":

    Test().test_gui()
    Test().test_space()
    Test().test_objects()

    print('''
    
    Все тесты пройдены! Вы великолепны!
    ''')
