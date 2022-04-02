# научные константы: https://docs.scipy.org/doc/scipy/reference/constants.html
# цвета в pygame: https://pygame-zero.readthedocs.io/en/latest/colors_ref.html#id2
# пример создания платформера: https://habr.com/ru/post/193888/
# визуализация гравитациооного поля: https://habr.com/ru/post/467803/ и https://habr.com/ru/post/470742/
# создать модуль Vector для расчета силовых полей: https://www.youtube.com/watch?v=PRPDt1ryhOk


"""
Используемая система измерени: https://metrob.ru/html/ed_izmer/Sist_SI.html
расстояния:         м - метры
весс:               кг - килограммы
время:              с - секунды
"""


import pygame
from objects import SpaceObjects
from space import Space
from gui import GUI
from settings import Settings


def run():
    """
    Функция run() запускает программу

    Данная функция:
    - считывает настройки по умолчанию
    - запускает математическое пространство Space()
    - формирует начальные космические объекты SpaceObjects()
    - добавляет SpaceObjects() в Space()
    - запускает процесс визуализации
    """

    # запускаем математическую среду
    space = Space()

    # создаем объекты
    # Солнце
    mass_of_sun = 1.9891 * 10**30
    sun = SpaceObjects('Sun', mass_of_sun,  695990000 * 10**1)
    sun.set_color(pygame.Color('gold'))
    sun.set_coord(0, 0)
    # Солнце стоит неподвижно и никуда в дальнейшем не сдвинется
    sun.StaticCoord = True

    # Земля
    mass_of_earth = 5.9722 * 10 ** 24
    earth = SpaceObjects('Earth', mass_of_earth, 6371302 * 10**3)
    earth.set_color(pygame.Color('blue'))
    earth.set_coord(149.6 * 10 ** 9, 0, 0, 29765)

    # # Марс
    # # mass_of_mars = ...
    # mass_of_mars = 45000000
    # mars = SpaceObjects('Mars', mass_of_mars, 25)
    # mars.set_color(pygame.Color('red'))
    # mars.set_coord(x0, y0 - 250, -0.35)

    # добавляем объекты в математической пространство
    space.add_obj(sun, earth)

    # запуск визуализации
    GUI(Settings.w, Settings.h, space, Settings.t, Settings.fps, Settings.m)

    # после закрытия окна визуализации, программа останавливается и не производит никаких действий


if __name__ == "__main__":

    run()
