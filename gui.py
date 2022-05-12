import pygame
from win32api import GetSystemMetrics


pygame.init()


class GUI:
    """
    Класс, отвечающий за визуализацию

    w - Ширина экрана.
    h - Высота экрана.
    sm - Объект класса SpaceMath, отвечающего за математику.
    t - Время.
    fps - Количество обновлений окна в секунду.
    m - Коэффициент масштабирования отбражаемой области.

    """

    def __init__(self, width, height, space, t=1, fps=30, m=1.0e-08):

        # название окна
        pygame.display.set_caption('OSN')

        # ширина и высота окна берутся из системных настроек монитора (для режима FULLSCREEN)
        self.width_screen, self.height_screen = GetSystemMetrics(0), GetSystemMetrics(1)

        # ширина и высота расчетной области
        self.width_bg, self.height_bg = width, height

        # стартовые смещение камеры (середина области)
        self.offset_x = -self.width_bg // 2 + self.width_screen // 2
        self.offset_y = -self.height_bg // 2 + self.height_screen // 2

        # количество кадров в секунду
        self.fps = fps

        # создание пользовательского окна
        self.sc = pygame.display.set_mode((self.width_screen, self.height_screen), pygame.FULLSCREEN)

        # создание области отрисовки (может быть больше окна прогарммы)
        self.bg = pygame.Surface((self.width_bg, self.height_bg)).convert()

        # коэффициент масштабирования
        self.m = m

        # флаг паузы
        self.pause = False

        # обработка событий (этот метод в конструкторе идет последним, после него конструктор читает)
        self.event_loop(space, t / fps)

    def print_text(self, message, x, y, font_color=(255, 255, 255),
                   font_type=pygame.font.match_font(pygame.font.get_fonts()[0]),
                   font_size=50):
        """
        Метод отображения текста на экране

        """

        font_type = pygame.font.Font(font_type, font_size)
        text = font_type.render(message, True, font_color)
        self.sc.blit(text, (x, y))

    def draw_button(self, message,
                    x, y, width, height,
                    inactive_color=pygame.Color('steelblue'),
                    active_color=pygame.Color('deepskyblue')):
        """
        Отрисовка кнопки на экране.

        x, y - координаты кнопки
        width, height - ширина и высота кнопки
        message - сообщение

        """

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (x < mouse[0] < x + width) and (y < mouse[1] < y + height):
            pygame.draw.rect(self.sc, active_color, (x, y, width, height))
        else:
            pygame.draw.rect(self.sc, inactive_color, (x, y, width, height))

    def menu(self):
        """
        Отображение меню пользователя.

        """
        self.draw_button('TEST', -52 + self.width_screen // 2, self.height_screen // 2, 110, 58)
        self.print_text('TEST', -50 + self.width_screen // 2, self.height_screen // 2)

    def camera_motion_limiter(self):
        """
        Метод, который ограничивает движение камеры, границами области отрисовки.

        """

        if self.offset_x >= 0:
            self.offset_x = 0
        elif self.offset_x <= -self.width_bg + self.width_screen:
            self.offset_x = -self.width_bg + self.width_screen

        if self.offset_y >= 0:
            self.offset_y = 0
        elif self.offset_y <= -self.height_bg + self.height_screen:
            self.offset_y = -self.height_bg + self.height_screen

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
                    # закрыть программу
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        exit()
                    # блок перемещения камеры клавиатурой
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        offset_up = True
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        offset_down = True
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        offset_left = True
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        offset_right = True
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
                        offset_up = False
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        offset_down = False
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        offset_left = False
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        offset_right = False
                # анализ нажатия кнопок мыши
                if event.type == pygame.MOUSEBUTTONDOWN and event.button in [1]:  # ЛКМ
                    print(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button in [3]:  # ПКМ
                    pass
                # колесо мыши
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # вверх
                    # масштабирование области визуализации (удаление)
                    self.m /= 1.1
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  # вниз
                    # масштабирование области визуализации (приближение)
                    self.m *= 1.1

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
            if not self.pause:
                sm.gravity_interactions(t)

            # Визуализация (сборка)
            for sp in sm.Objects:
                sp.draw(self.bg, shift=(self.width_bg // 2, self.height_bg // 2), m=self.m)
                # TODO планеты и ракеты в реальном масштабе не видно - нужно придумать коэф-ты маштабирования визуалки

            # визуализация паузы
            # TODO добавить прозрачную поверхность с полупрозрачной надписью "ПАУЗА"

            # ограничитель движения камеры - проверка границ
            self.camera_motion_limiter()
            # отрисовка видимой области
            self.sc.blit(self.bg, (self.offset_x, self.offset_y))

            # отрисовка меню пользователя
            self.menu()

            # после отрисовки всего, переворачиваем экран
            # pygame.display.flip()
            pygame.display.update()

            # держим цикл на правильной скорости
            pygame.time.Clock().tick(self.fps)
