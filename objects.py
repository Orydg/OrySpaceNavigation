import pygame
from scipy.constants import G


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
    self.CoordFromTime: Логический флаг.
    По умолчанию имеет значение False - координаты объекта не зависят от времени.
    True - координаты объекта зависят только от времени, а не от гравитации.
    self.Color: Цвет объекта.

    """
    def __init__(self, name='', mass=0, r=0):
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
        self.CoordFromTime = False
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
            # self.set_coord(self.X, self.Y)
            # ничего не происходит - при этом флаге координаты объекта статичны (не изменяются)
            return
        if self.CoordFromTime:
            # координаты зависят только от времени
            # TODO метод перестроения координат по времени (время передается в закон движения по орбите)
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

    def draw(self, sc, shift=(0, 0), m=1):
        """
        Метод отрисовки объекта на плоскости sc.

        sc: плоскость для отрсовки объекта.
        shift: смещение отрисовки
        m: коэффициент масштабирования

        """

        pygame.draw.circle(sc, self.Color, (self.X * m + shift[0], self.Y * m + shift[1]), self.R * m)

    def distance_to(self, obj, to_orient=False):
        """
        Метод измеряет дистанцию до объекта obj (модуль вектора).

        obj: Объект класса SpaceObjects.
        to_orient: Логический флаг, по умолчанию имеет значение False. Если True, метод возвращает ортогональный вектор.

        """

        dist = ((obj.X - self.X)**2 + (obj.Y - self.Y)**2)**0.5
        if to_orient:
            return [(obj.X - self.X) / dist, (obj.Y - self.Y) / dist]
        return dist

    def orientation_to_obj(self, obj):
        """
        Метод возвращает ортогональный вектор в направлении obj.

        obj: Объект класса SpaceObjects.

        return: проекции вектора на оси Х, У

        """

        return self.distance_to(obj, True)

    def gravity_force(self, obj):
        """
        Метод возвращает модуль силы притяжения с объектом obj.

        obj: Объект класса SpaceObjects.

        """

        return G * self.Mass * obj.Mass / self.distance_to(obj)**2

    def law_of_orbit(self):  # TODO закон движения по орбите для этого небесного объекта
        """
        Метод описывает траекторию движения объекта

        """

        # (G * obj.Mass / self.distance_to(obj)) ** 0.5 - скорость у поверхность гравитирующего тела (от v1 до v2)

        pass

    def draw_orbit(self):
        """
        Метод визуализации траектории движения

        """

        pass

    def first_cosmic_velocity(self):
        """
        Пе́рвая косми́ческая ско́рость (кругова́я ско́рость) — минимальная (для заданной высоты над поверхностью планеты)
        горизонтальная скорость, которую необходимо придать объекту,
        чтобы он совершал движение по круговой орбите вокруг планеты.

        return: v1 - первая космическая скорость данного гравитирующего объекта

        """

        # v1 = (G*M/R+h)**0.5
        # v1 - первая космическая скорость
        # G - гравитационная константа
        # M - масса гравитирующего тела (планеты)
        # R - радиус гравитирующего тела (планеты)
        # h - высота над поверхностью гравитирующего тела (планеты)
        # h = 0, потому что исследуем минимальную необходимую скорость для выхода на орбиту

        assert self.R > 0, "Радиус гравитирующего объекта не может быть меньше или равен нулю"

        return (G * self.Mass / self.R)**0.5

    def second_cosmic_velocity(self):
        """
        Втора́я косми́ческая ско́рость (параболи́ческая ско́рость) — наименьшая скорость, которую необходимо придать
        стартующему с поверхности небесного тела объекту (например, космическому аппарату),
        масса которого пренебрежимо мала по сравнению с массой небесного тела (например, планеты),
        для преодоления гравитационного притяжения этого небесного тела и покидания замкнутой орбиты вокруг него.

        """

        pass
