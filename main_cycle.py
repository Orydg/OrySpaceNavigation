"""
Основной цикл.

Внутри основного цикла есть три основных операции:
обработка событий, обновление состояния и отрисовка текущего состояния на экране.

"""


import pygame
# import pygame_widgets
from win32api import GetSystemMetrics
from settings import Settings
from pygame_widgets.button import ButtonArray
import menu_tk as tk


pygame.init()


class MainLoop:
    """
    Класс, отвечающий за визуализацию

    w - Ширина экрана.
    h - Высота экрана.
    sm - Объект класса SpaceMath, отвечающего за математику.
    t - Время.
    fps - Количество обновлений окна в секунду.
    m - Коэффициент масштабирования отбражаемой области.

    """

    def __init__(self, space, t=1, fps=30, m=1.0e-08):

        # название окна
        pygame.display.set_caption('OSN')

        # ширина и высота окна берутся из системных настроек монитора (для режима FULLSCREEN)
        self.width_screen, self.height_screen = GetSystemMetrics(0), GetSystemMetrics(1)

        # стартовые смещение камеры (середина области)
        self.offset_x = self.width_screen // 2
        self.offset_y = self.height_screen // 2

        # количество кадров в секунду
        self.fps = fps

        # создание пользовательского окна
        self.sc = pygame.display.set_mode((self.width_screen, self.height_screen), pygame.FULLSCREEN)

        # расчетное пространство
        self.sm = space

        # коэффициент масштабирования
        self.m = m

        # Время
        self.t = t / self.fps

        # События
        self.events = None

        # флаг паузы
        self.pause = False

        # флаг отображения меню
        self.menu_on = False

        # Список обрабатываемых объектов
        self.objects = []

        # флаги направлений смещения камеры
        self.offset_up = False
        self.offset_down = False
        self.offset_left = False
        self.offset_right = False

        # Создание кнопок
        self.MenuButtonArray = ButtonArray(
            # Mandatory Parameters
            self.sc,  # Surface to place button array on
            self.width_screen * 0.2,  # X-coordinate
            self.height_screen * 0.2,  # Y-coordinate
            self.width_screen * 0.6,  # Width
            self.height_screen * 0.6,  # Height
            (1, 4),  # Shape: 2 buttons wide, 2 buttons tall
            border=50,  # Distance between buttons and edge of array
            # Sets the texts of each button (counts left to right then top to bottom)
            texts=('Очистить список объектов', 'SAVE', 'LOAD', '4'),
            # When clicked, print number
            onClicks=(self.sm.clear_objects,
                      self.sm.save_obj,
                      lambda: self.sm.load_obj(file_name="save1.csv"),
                      lambda: print('4'))
        )

        # обработка событий (этот метод в конструкторе идет последним, после него конструктор не читает)
        self.event_loop()

    def handle_events(self):
        """
        Метод обрабатывает события и вызывает соответствующие методы/функции.

        """

        # цикл обработки событий
        self.events = pygame.event.get()
        for event in self.events:

            # проверить закрытие окна
            if event.type == pygame.QUIT:
                exit()

            # обработка нажатий клавиш
            if event.type == pygame.KEYDOWN:

                # закрыть программу
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    exit()

                # блок перемещения камеры клавиатурой
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.offset_up = True
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.offset_down = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.offset_left = True
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.offset_right = True

                # отображение меню
                if event.key == pygame.K_TAB:
                    # if self.menu_on:
                    #     self.menu_on = False
                    # else:
                    #     self.menu_on = True
                    tk.Run(self.sm, self)

                # пауза
                if event.key == pygame.K_SPACE or event.key == pygame.K_p:
                    if self.pause:
                        self.pause = False
                    else:
                        self.pause = True

                # отрисовка гравитационного поля
                if event.key == pygame.K_g and self.pause:
                    pass
                    # TODO включить отрисовку гравитационного поля во всей расчетной области или отключить
                    #  поле должно отрисоваться один раз (протестировать, если не получится,
                    #  то один раз создать рисунок поля и в цикле его выводить)
                if not self.pause:
                    pass
                    # TODO если пауза снята, принудительно отключить отрисовку поля гравитации

            # обработка отжатий клавиш
            elif event.type == pygame.KEYUP:

                # блок перемещения камеры клавиатурой
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.offset_up = False
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.offset_down = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.offset_left = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.offset_right = False

            # анализ нажатия кнопок мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in [1]:  # ЛКМ
                    print(event.pos)
                if event.button in [3]:  # ПКМ
                    pass

            # анализ отжатия кнопок мыши
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in [1]:  # ЛКМ
                    pass
                if event.button in [3]:  # ПКМ
                    print(event.pos)

            # колесо мыши
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # вверх

                # масштабирование области визуализации (удаление)
                self.m /= 1.1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  # вниз

                # масштабирование области визуализации (приближение)
                self.m *= 1.1

            # События нажатия кнопки интерфейса
            pass

        # держим цикл на правильной скорости
        pygame.time.Clock().tick(self.fps)

    def update(self):
        if not self.pause:
            self.sm.gravity_interactions(self.t)

    def draw(self):
        """
        Метод отрисовки сцены и объектов сцены.
        Метод только отрисовывает объекты - не обрабатывает события.

        """

        def print_text(message, x, y, font_color=(255, 255, 255),
                       font_type=pygame.font.match_font(pygame.font.get_fonts()[0]),
                       font_size=50):
            """
            Метод отображения текста на экране

            """

            font_type = pygame.font.Font(font_type, font_size)
            text = font_type.render(message, True, font_color)
            self.sc.blit(text, (x, y))

        def string_of_status():
            # нижняя строка состояния
            size_text = self.height_screen * 0.03
            pygame.draw.rect(self.sc, pygame.Color('lavender'),
                             (0, self.height_screen - size_text,
                              self.width_screen, self.height_screen))
            print_text(f'Коэф. масш.: {self.m:1.3g}',
                       5, self.height_screen - size_text,
                       font_size=int(size_text),
                       font_color=(0, 0, 0))

        # Цвет фона
        self.sc.fill(pygame.Color('#000020'))

        # Визуализация объектов
        for object_in_space in self.sm.Objects:
            object_in_space.draw(self.sc, shift=(self.offset_x, self.offset_y), m=self.m)

        # отрисовка сообщения о паузе
        if self.pause:
            print_text('ПАУЗА',
                       -75 + self.width_screen // 2,
                       -25 + self.height_screen // 2)

        # отрисовка меню пользователя
        if self.menu_on:
            # pygame_widgets.update(self.events)
            pass

        # отрисовка статусной строки
        string_of_status()

        # после отрисовки всего, переворачиваем экран
        # pygame.display.flip()
        pygame.display.update()

    def event_loop(self):

        # скорость смещения камеры (пикселей за кадр)
        key_move = Settings.key_move

        # Обработка событий
        while True:

            # цикл обработки событий
            self.handle_events()

            # смещение камеры
            if self.offset_up:
                self.offset_y += key_move
            elif self.offset_down:
                self.offset_y -= key_move
            if self.offset_left:
                self.offset_x += key_move
            elif self.offset_right:
                self.offset_x -= key_move

            # Обновление данных
            self.update()

            # Визуализация объектов
            self.draw()
