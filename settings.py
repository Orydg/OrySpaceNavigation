"""
Файл первичных настроек

"""


class Settings:

    # ускорение
    t = 3000

    # количество кадров в секунду
    fps = 30

    # коэффициент начального масштабирования космического пространства
    m = 1.0e-08

    # скорость смещения камеры (пикселей за кадр)
    key_move = 20

    # минимальный радиус космических тел для отрисовки
    min_r = 10

    # путь для сохранения/загрузки данных
    path = "./date/"


class Buttons:

    """
    Класс для различных кнопок.

    """

    def __init__(self, button_function, button_figure, *args):
        """
        Конструктор кнопки.

        """

        # метод, вызываемый кнопкой
        self.Button_function = button_function

        # фигура кнопки
        self.Button_figure = button_figure

        # размер кнопки
        self.Button_size = None

        # координаты кнопки
        self.Button_coord = None

        # плоскости для отрисовки кнопки
        self.Button_plane = None

        # статический цвет кнопки
        self.Button_main_color = None

        # цвет активной кнопки
        self.Button_active_color = None

        # кнопка содержит текст действует как флаг (если есть значение, то будет отрисован текст)
        self.Button_text = None

        # координаты текста
        self.Button_text_coord = None

        # шрифт текста
        self.Button_text_font = None

        # цвет текста
        self.Button_text_color = None

    def set_button_coord(self):
        pass

    def get_button_coord(self):
        pass

    def click(self):
        self.Button_function()
