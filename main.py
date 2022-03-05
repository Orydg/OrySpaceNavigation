# научные константы: https://docs.scipy.org/doc/scipy/reference/constants.html
# цвета в pygame: https://pygame-zero.readthedocs.io/en/latest/colors_ref.html#id2

"""
Используемая система измерени: https://metrob.ru/html/ed_izmer/Sist_SI.html
расстояния:         м - метры
весс:               кг - килограммы
время:              с - секунды
"""


from scipy.constants import G
import pygame
import datetime


class GUI:
    """
    Класс, отвечающий за визуализацию
    """

    def __init__(self, w, h, t):
        pygame.init()

        # название окна
        pygame.display.set_caption('OSN')

        self.W, self.H = w, h
        self.fps = 30

        self.sc = pygame.display.set_mode((self.W, self.H))

        self.EventLoop(t)

    def Update_screen(self):
        # после отрисовки всего, переворачиваем экран
        pygame.display.update()
        # pygame.display.flip()

    def EventLoop(self, t):

        # Ввод процесса (события)
        while True:

            # обновление фона
            self.sc.fill("#000022")

            # цикл обработки событий
            for event in pygame.event.get():
                # проверить закрытие окна
                if event.type == pygame.QUIT:
                    exit()

            # Обновление данных
            # sm.tic_tac()
            sm.gravity_interactions(t)

            # Визуализация (сборка)
            for sp in sm.Objects:
                sp.draw(self.sc)

            # после отрисовки всего, переворачиваем экран
            pygame.display.flip()

            # держим цикл на правильной скорости
            pygame.time.Clock().tick(self.fps)


class SpaceMath:
    """
    Класс, описывающий математику взаимодействий обектов.

    Objects - список объектов для обработки в математическом пространстве данного класса
    Time - время

    """
    def __init__(self):
        self.Objects = []
        self.StartTime = datetime.datetime(2000, 1, 1)
        self.Time = 0

    def add_obj(self, *args):
        """

        Parameters
        ----------
        args: Объекты для обработки в математическом пространстве.

        Returns
        -------

        """

        # сначала проверим объекты
        for i in args:
            assert i.Mass

        # добавить объекты в общий список объектов взаимодействий
        self.Objects += args

    def tic_tac(self):
        self.Time += 1/60
        for obj in self.Objects:
            obj.change_coord(self.Time)

    @staticmethod
    def distance(obj1, obj2, to_orient=False):
        x1, y1 = obj1.get_coord()
        x2, y2 = obj2.get_coord()
        dist = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        if to_orient:
            x = x2 - x1
            y = y2 - y1
            return [x / dist, y / dist]
        return dist

    @staticmethod
    def gravity_force(obj1, obj2):
        return G * obj1.Mass * obj2.Mass / SpaceMath.distance(obj1, obj2)**2

    @staticmethod
    def orientation_form_obj(obj1, obj2):
        return SpaceMath.distance(obj1, obj2, True)

    def gravity_interactions(self, t):
        for n, obj1 in enumerate(self.Objects):
            for j in range(n+1, len(self.Objects)):
                obj2 = self.Objects[j]
                force = SpaceMath.gravity_force(obj1, obj2)
                a1 = force / obj1.Mass
                a2 = force / obj2.Mass
                ort_vect = SpaceMath.orientation_form_obj(obj1, obj2)
                obj1.change_coord(t, ax=a1 * ort_vect[0], ay=a1 * ort_vect[1])
                obj2.change_coord(t, ax=-a2 * ort_vect[0], ay=-a2 * ort_vect[1])


class SpaceObjects:
    """
    Класс космических объектов
    """
    def __init__(self, name, mass, r):
        self.Name = name
        self.Mass = mass
        self.R = r
        self.X = None
        self.Y = None
        self.Vx = None
        self.Vy = None
        self.Ax = None
        self.Ay = None
        self.StaticCoord = False
        self.Color = pygame.Color('green')

    def set_coord(self, x=0, y=0, vx=0, vy=0, ax=0, ay=0, t=1):
        self.X = x + vx * t + ax * t**2
        self.Y = y + vy * t + ay * t**2
        self.Vx = vx + ax * t
        self.Vy = vy + ay * t
        self.Ax = ax
        self.Ay = ay

    def get_coord(self):
        return self.X, self.Y

    def change_coord(self, t=1, x=None, y=None, vx=None, vy=None, ax=None, ay=None):
        if self.StaticCoord:
            self.set_coord(self.X, self.Y)
            return
        if not x:
            x = self.X
        if not y:
            y = self.Y
        if not vx:
            vx = self.Vx
        if not vy:
            vy = self.Vy
        if not ax:
            ax = self.Ax
        if not ay:
            ay = self.Ay
        self.set_coord(x, y, vx, vy, ax, ay, t)

    def set_color(self, color):
        self.Color = color

    def draw(self, sc):
        pygame.draw.circle(sc, self.Color, (self.X, self.Y), self.R)


if __name__ == "__main__":

    # Настройки
    # Размеры окна
    w, h = 1200, 800

    # запускаем математическую среду
    sm = SpaceMath()

    # Начальные координаты
    x0 = w//2
    y0 = h//2

    # создаем объекты
    # Солнце
    # mass_of_sun = 1.9891 * 10**30
    mass_of_sun = 1000000000000
    sun = SpaceObjects('Sun', mass_of_sun, 40)
    sun.set_color(pygame.Color('gold'))
    sun.set_coord(x0, y0)
    # Солнце стоит неподвижно и никуда в дальнейшем не сдвинется
    sun.StaticCoord = True

    # Земля
    # mass_of_earth = 5.9722 * 10 ** 24
    mass_of_earth = 50000000
    earth = SpaceObjects('Earth', mass_of_earth, 25)
    earth.set_color(pygame.Color('blue'))
    earth.set_coord(x0-100, y0+150, 0.5)

    # Марс
    # mass_of_mars = ...
    mass_of_mars = 45000000
    mars = SpaceObjects('Earth', mass_of_mars, 25)
    mars.set_color(pygame.Color('red'))
    mars.set_coord(x0, y0 - 250, -0.35)

    # добавляем объекты в математической пространство
    sm.add_obj(sun, earth, mars)

    # ускорение
    t = 10

    # запуск визуализации
    GUI(w, h, t)

    # после закрытия окна визуализации, программа останавливается и не производит никаких действий
