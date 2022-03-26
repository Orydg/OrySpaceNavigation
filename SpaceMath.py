import datetime
from scipy.constants import G


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
                # выисляем ускорение для каждого из двух объектов
                a1 = force / obj1.Mass
                a2 = -force / obj2.Mass  # сила противодействия (знак "-")
                # вычисляем направление действия силы (ускорения) для каждого из двух объектов
                ort_vector = SpaceMath.orientation_from_obj(obj1, obj2)
                # умножаем модуль ускорения на направление и обновляем состояния каждого из двух объектов
                obj1.change_coord(t, ax=a1 * ort_vector[0], ay=a1 * ort_vector[1])
                obj2.change_coord(t, ax=a2 * ort_vector[0], ay=a2 * ort_vector[1])