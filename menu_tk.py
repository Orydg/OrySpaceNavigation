from tkinter import *
from tkinter import filedialog as fd


class Run:
    def __init__(self, sm, main):
        self.sm = sm
        self.main = main

        root = Tk()

        b1 = Button(text="Загрузить", command=self.load_data)
        b1.grid(row=1, column=0, sticky=W)
        b2 = Button(text="Сохранить", command=self.save_data)
        b2.grid(row=1, column=1, sticky=W)
        b3 = Button(text="Очистить", command=self.clear)
        b3.grid(row=1, column=2, sticky=W)

        root.mainloop()

    def load_data(self):
        file_name = fd.askopenfilename()
        self.sm.load_obj(file_name)
        self.main.update()
        self.main.draw()

    def save_data(self):
        file_name = fd.asksaveasfilename(
            filetypes=(("CSV files", "*.csv"),
                       ("All files", "*.*")))
        self.sm.save_obj(file_name)

    def clear(self):
        self.sm.clear_objects()
        self.main.update()
        self.main.draw()
