# научные константы: https://docs.scipy.org/doc/scipy/reference/constants.html
# цвета в pygame: https://pygame-zero.readthedocs.io/en/latest/colors_ref.html#id2
# пример создания платформера: https://habr.com/ru/post/193888/


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

    w - Ширина экрана.
    h - Высота экрана.
    sm - Объект класса SpaceMath, отвечающего за математику.
    t - Время.

    """

    def __init__(self, w, h, sm, t):
        pygame.init()

        # название окна
        pygame.display.set_caption('OSN')

        # ширина и высота окна
        self.Wscreen, self.Hscreen = 1600, 900

        # ширина и высота расчетной области
        self.Wbg, self.Hbg = w, h

        # стартовые смещение камеры (середина области)
        self.offset_x = -self.Wbg // 2 + self.Wscreen // 2
        self.offset_y = -self.Hbg // 2 + self.Hscreen // 2

        # количество кадров в секунду
        self.fps = 30

        # создание окна
        self.sc = pygame.display.set_mode((self.Wscreen, self.Hscreen), pygame.FULLSCREEN)

        # создание области отрисовки (может быть больше окна прогарммы)
        self.bg = pygame.Surface((self.Wbg, self.Hbg))

        # обработка событий
        self.event_loop(sm, t)

    def camera_motion_limiter(self):
        """
        Метод, который ограничивает движение камеры, границами области отрисовки.

        """

        if self.offset_x >= 0:
            self.offset_x = 0
        elif self.offset_x <= -self.Wbg + self.Wscreen:
            self.offset_x = -self.Wbg + self.Wscreen

        if self.offset_y >= 0:
            self.offset_y = 0
        elif self.offset_y <= -self.Hbg + self.Hscreen:
            self.offset_y = -self.Hbg + self.Hscreen

    def event_loop(self, sm, t):

        # скорость смещения камеры (пикселей за кадр)
        key_move = 20
        # флаги направлений смещения камеры
        offset_up = False
        offset_down = False
        offset_left = False
        offset_right = False

        # Ввод процесса (события)
        while True:

            # обновление фона
            self.bg.fill("#000022")

            # цикл обработки событий
            for event in pygame.event.get():
                # проверить закрытие окна
                if event.type == pygame.QUIT:
                    exit()
                # обработка нажатий клавиш
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        exit()
                    if event.key == pygame.K_UP:
                        offset_up = True
                    elif event.key == pygame.K_DOWN:
                        offset_down = True
                    if event.key == pygame.K_LEFT:
                        offset_left = True
                    elif event.key == pygame.K_RIGHT:
                        offset_right = True
                # обработка отжатий клавиш
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        offset_up = False
                    elif event.key == pygame.K_DOWN:
                        offset_down = False
                    if event.key == pygame.K_LEFT:
                        offset_left = False
                    elif event.key == pygame.K_RIGHT:
                        offset_right = False
                # анализ нажатия кнопок мыши
                if event.type == pygame.MOUSEBUTTONDOWN and event.button in [1]:  # ЛКМ
                    print(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button in [3]:  # ПКМ
                    pass

            # смещение камеры
            if offset_up:
                self.offset_y += key_move
            elif offset_down:
                self.offset_y -= key_move
            if offset_left:
                self.offset_x += key_move
            elif offset_right:
                self.offset_x -= key_move

            # Обновление данных
            # sm.tic_tac()
            sm.gravity_interactions(t)

            # Визуализация (сборка)
            for sp in sm.Objects:
                sp.draw(self.bg)
            # ограничитель движения камеры - проверка границ
            self.camera_motion_limiter()
            # отрисовка видимой области
            self.sc.blit(self.bg, (self.offset_x, self.offset_y))

            # после отрисовки всего, переворачиваем экран
            # pygame.display.flip()
            pygame.display.update()

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
        Все объекты из списка args добавлены в среду self.Objects для вычисления их взаимодействий.
        Если хотя бы один из объектов не содержит параметра self.Mass возвращае исключение.

        """

        # сначала проверим объекты
        for i in args:
            assert i.Mass

        # добавить объекты в общий список объектов взаимодействий
        self.Objects += args

    def tic_tac(self):
        """
        Метод создан для тестов - изменяет внутреннее состояние объектов в self.Objects с течением времени.

        """

        self.Time += 1/60
        for obj in self.Objects:
            obj.change_coord(self.Time)

    @staticmethod
    def distance(obj1, obj2, to_orient=False):
        """
        Метод измеряет дистанцию между двумя объектами obj1 и obj2 (модуль вектора между ними).

        obj1: Объект класса SpaceObjects.
        obj2: Объект класса SpaceObjects.
        to_orient: Логический флаг, по умолчанию имеет значение False. Если True, метод возвращает ортогональный вектор.

        """

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
        """
        Метод возвращает модуль силы между двумя объектами obj1 и obj2.

        obj1: Объект класса SpaceObjects.
        obj2: Объект класса SpaceObjects.

        """

        return G * obj1.Mass * obj2.Mass / SpaceMath.distance(obj1, obj2)**2

    @staticmethod
    def orientation_from_obj(obj1, obj2):
        """
        Метод возвращает ортогональный вектор между двумя объектами obj1 и obj2.

        obj1: Объект класса SpaceObjects.
        obj2: Объект класса SpaceObjects.

        """

        return SpaceMath.distance(obj1, obj2, True)

    def gravity_interactions(self, t):
        """
        Метод анализирует гравитационное взаимодействие между всеми обектами в self.Objects.
        Результатом работы метода является изменение состаяний всех объектов в self.Objects
        по результатам их совместных взаимотействий.

        """

        # Сравниваем каждый объект с каждым (только один раз)
        for n, obj1 in enumerate(self.Objects):
            for j in range(n+1, len(self.Objects)):
                obj2 = self.Objects[j]
                # вычисляем силу взаимодействия между двумя объектами
                force = SpaceMath.gravity_force(obj1, obj2)
                # выисляем ускорение
                a1 = force / obj1.Mass
                a2 = force / obj2.Mass
                # вычисляем направление действия силы (ускорения)
                ort_vector = SpaceMath.orientation_from_obj(obj1, obj2)
                # умножаем модуль ускорения на направление и обновляем состояния объектов
                obj1.change_coord(t, ax=a1 * ort_vector[0], ay=a1 * ort_vector[1])
                obj2.change_coord(t, ax=-a2 * ort_vector[0], ay=-a2 * ort_vector[1])


class SpaceObjects:
    """
    Класс космических объектов

    self.Name: Имя объекта.
    self.Mass: Масса объекта.
    self.R: Радиус объекта.
    self.X: Координата Х объекта.
    self.Y: Координата Y объекта.
    self.Vх: Проекция скорости по оси Х объекта.
    self.Vy: Проекция скорости по оси У объекта.
    self.Ax: Проекция ускорения по оси Х объекта.
    self.Ay: Проекция ускорения по оси У объекта.
    self.StaticCoord: Логический флаг.
    По умолчанию имеет значение False - координаты объекта можно менять.
    True - координаты объекта статичны, их не изменить методом change_coord().
    self.Color: Цвет объекта.

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

    def set_coord(self, x=0.0, y=0.0, vx=0.0, vy=0.0, ax=0.0, ay=0.0, t=1.0):
        """
        Метод устанавливает значение координат объекта.

        """

        self.X = x + vx * t + ax * t**2
        self.Y = y + vy * t + ay * t**2
        self.Vx = vx + ax * t
        self.Vy = vy + ay * t
        self.Ax = ax
        self.Ay = ay

    def get_coord(self):
        """
        Метод возвращает пару координат объекта.

        """

        return self.X, self.Y

    def change_coord(self, t=1, x=None, y=None, vx=None, vy=None, ax=None, ay=None):
        """
        Метод предназначен для изменения координат, скорости и ускорения объекта.

        """

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
        """
        Метод позволяет изменить цвет объекта.

        color: Цвет объекта.

        """

        self.Color = color

    def draw(self, sc):
        """
        Метод отрисовки объекта на плоскости sc.

        sc: плоскость для отрсовки объекта.

        """

        pygame.draw.circle(sc, self.Color, (self.X, self.Y), self.R)

#====================================================================================================


def run():
    """
    Метод run() запускает программу

    Данный метод:
    - считывает настройки по умолчанию
    - запускает математическое пространство SpaceMath()
    - формирует начальные космические объекты SpaceObjects()
    - добавляет SpaceObjects() в SpaceMath()
    - запускает процесс визуализации
    """

    # Настройки
    # Размеры расчетной области
    w, h = 3000, 3000

    # запускаем математическую среду
    sm = SpaceMath()

    # Начальные координаты
    x0 = w // 2
    y0 = h // 2

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
    earth.set_coord(x0 - 100, y0 + 150, 0.35)

    # Марс
    # mass_of_mars = ...
    mass_of_mars = 45000000
    mars = SpaceObjects('Earth', mass_of_mars, 25)
    mars.set_color(pygame.Color('red'))
    mars.set_coord(x0, y0 - 250, -0.35)

    # Небиру
    mass_of_nebyru = 75000000
    nebyru = SpaceObjects('Nebyru', mass_of_nebyru, 25)
    nebyru.set_color(pygame.Color('violet'))
    nebyru.set_coord(x0, y0 - 350, -0.15)

    # добавляем объекты в математической пространство
    sm.add_obj(sun, earth, mars, nebyru)

    # ускорение
    t = 10

    # запуск визуализации
    GUI(w, h, sm, t)

    # после закрытия окна визуализации, программа останавливается и не производит никаких действий

#====================================================================================================


if __name__ == "__main__":

    run()
