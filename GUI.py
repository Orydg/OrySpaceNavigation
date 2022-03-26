import pygame
from win32api import GetSystemMetrics


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

        # ширина и высота окна берутся из системных настроек монитора (для режима FULLSCREEN)
        self.Wscreen, self.Hscreen = GetSystemMetrics(0), GetSystemMetrics(1)

        # ширина и высота расчетной области
        self.Wbg, self.Hbg = w, h

        # стартовые смещение камеры (середина области)
        self.offset_x = -self.Wbg // 2 + self.Wscreen // 2
        self.offset_y = -self.Hbg // 2 + self.Hscreen // 2

        # количество кадров в секунду
        self.fps = 30

        # создание пользовательского окна
        self.sc = pygame.display.set_mode((self.Wscreen, self.Hscreen), pygame.FULLSCREEN)

        # создание области отрисовки (может быть больше окна прогарммы)
        self.bg = pygame.Surface((self.Wbg, self.Hbg)).convert()

        # коэффициент масштабирования
        self.m = 1.6711229946524064e-08

        # флаг паузы
        self.pause = False

        # обработка событий (этот метод в конструкторе идет последним, после него конструктор читает)
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
                sp.draw(self.bg, shift=(self.Wbg//2, self.Hbg//2), m=self.m)

            # визуализация паузы
            # TODO добавить прозрачнуюповерхность с полупрозрачной надписью "ПАУЗА"

            # ограничитель движения камеры - проверка границ
            self.camera_motion_limiter()
            # отрисовка видимой области
            self.sc.blit(self.bg, (self.offset_x, self.offset_y))

            # после отрисовки всего, переворачиваем экран
            # pygame.display.flip()
            pygame.display.update()

            # держим цикл на правильной скорости
            pygame.time.Clock().tick(self.fps)