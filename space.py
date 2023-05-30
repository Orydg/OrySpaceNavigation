import datetime
import csv
from objects import SpaceObjects
from settings import Settings


class Space:
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
            assert type(i) is SpaceObjects, f"Передаваемый объект: '{i}' является объектом {type(i)}, " \
                                            f"а должент быть объектом <class 'SpaceObjects'>."
            assert i.Mass > 0, f"Объект {i} обладает некорректной массой: {i.Mass}."

        # добавить объекты в общий список объектов взаимодействий
        self.Objects += args

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
                force = obj1.gravity_force(obj2)
                # выисляем ускорение для каждого из двух объектов
                a1 = force / obj1.Mass
                a2 = -force / obj2.Mass  # сила противодействия (знак "-")
                # вычисляем направление действия силы (ускорения) для каждого из двух объектов
                ort_vector = obj1.orientation_to_obj(obj2)
                # умножаем модуль ускорения на направление и обновляем состояния каждого из двух объектов
                obj1.change_coord(t, ax=a1 * ort_vector[0], ay=a1 * ort_vector[1])
                obj2.change_coord(t, ax=a2 * ort_vector[0], ay=a2 * ort_vector[1])

    def save_obj(self):
        """
        Метод сохранения объектов и их состояния.

        """
        file_name = "save1.csv"
        with open(Settings.path + file_name, mode="w") as file:
            names = ["Название", "Масса", "Радиус", "X", "Y", "Vx", "Vy", "Ax", "Ay",
                     "Статические координаты", "Зависит от времени", "Цвет"]
            file_writer = csv.writer(file,
                                     delimiter=";",
                                     lineterminator="\r")
            file_writer.writerow(names)
            for o in self.Objects:

                file_writer.writerow(list(map(str, [o.Name,
                                                    o.Mass,
                                                    o.R,
                                                    o.X,
                                                    o.Y,
                                                    o.Vx,
                                                    o.Vy,
                                                    o.Ax,
                                                    o.Ay,
                                                    o.StaticCoord,
                                                    o.CoordFromTime,
                                                    o.Color])))
