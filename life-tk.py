from random import sample
from time import sleep
from copy import deepcopy

import tkinter as tk


# класс приложения: наследуется от tk.Tk
class App(tk.Tk):
    def __init__(self, sizex=16, sizey=16, cell_size=40, fill_count=80):
        # значения по умолчанию заданы в конструкторе, чтобы при
        # инициализации приложения можно было их переопределять, не меняя класс
        super().__init__()              # инициилизировать конструктор базового класса!

        self.title('Игра "Жизнь"')      # заголовок окна
        self.config(bg="skyblue")       # цвет заливки окна (рамка)

        self.sizex = sizex              # количество ячеек по горизонтали
        self.sizey = sizey              # количество ячеек по вертикали
        self.cell_size = cell_size      # ширина/высота 1 ячейки в пикселях
        # создать cells - массив нулевых (мертвых) ячеек при иницииализации приложения
        self.cells = [[0 for i in range(self.sizex)] for j in range(self.sizey)]
        self.fill_count = fill_count    # количество ячеек для заполнения
        self.counter = 1                # номер поколения, начать с 1
        self.has_changes = True         # наличие изменений в матрце за последний шаг
        # игра прекращается при отсутствии изменений за одно поколение

        # вертикальный фрейм/Layout главного окна: сверху меню (кнопки), ниже полотно
        self.main = tk.Frame(self, bg="white")
        self.main.grid(row=0, column=0, padx=5, pady=5)

        # горизонтальный фрейм/Layout для размещения кнопок меню
        self.menu = tk.Frame(self.main, bg="white")
        self.menu.grid(row=1, column=0, padx=0, pady=0)


        # создать кнопки меню
        self.btnFill = tk.Button(self.menu, text="Заполнить", command=self.fill,
                                 font=16,bg="Cyan")
        self.btnStep = tk.Button(self.menu, text="Следующий", command=self.step,
                                 font=16,bg="GreenYellow")
        self.btnPlay = tk.Button(self.menu, text="Выполнить", command=self.play,
                                 font=16,bg="Gold")

        # разместить кнопки горизонтально в фрейме menu
        self.btnFill.grid(row=0, column=1, padx=5, pady=5)
        self.btnStep.grid(row=0, column=2, padx=5, pady=5)
        self.btnPlay.grid(row=0, column=3, padx=5, pady=5)

        # создать и разместить полотно Canvas ниже меню
        self.canvas = tk.Canvas(self.main, width=self.sizex * self.cell_size,
                                height=self.sizey * self.cell_size, bg="Cornsilk")
        self.canvas.grid(row=2, column=0, padx=0, pady=0)
        self.canvas.bind("<Button-1>", self.handle_click)

        self.paint()    # отрисовка кружочков по нулевой матрице


    # отрисовка на полотне состояния игры по данным матрицы self.cells
    def paint(self):
        for i in range(self.sizey):         # внешний цикл по строкам
            for j in range(self.sizex):     # вложенный цикл по столбцам
                if self.cells[i][j] == 1:   # цвет закраски "живых" ячеек
                    cell_fill = "LawnGreen"
                else:                       # цвет закраски "мертвых" ячеек
                    cell_fill = "Bisque"
                #  рисуем круглый овал =)
                self.canvas.create_oval(j * self.cell_size + 2,     # отступ 5 px
                                        i * self.cell_size + 2,     # отступ 5 px
                                        (j + 1) * self.cell_size - 2,
                                        (i + 1) * self.cell_size - 2,
                                        fill=cell_fill,     # цвет выбран выше
                                        outline="Cornsilk") # обводка под цвет фона
        self.canvas.update()    # обновление отрисованного canvas на экране
        print("Идет поколение:", self.counter)  # напоминалка номера поколения


    # обработчик кнопки "Заполнить"
    def fill(self):
        life = sample(range(self.sizex * self.sizey), k = self.fill_count)
        life.sort()
        self.cells = [[0 for i in range(self.sizex)] for j in range(self.sizey)]
        life_list = []
        for one in life:
            i, j = divmod(one, self.sizex)
            self.cells[i][j] = 1
            life_list.append([i, j])
        print(life_list)
        self.counter = 1
        self.has_changes = True
        self.paint()


    # обработчик кнопки "Следующий" (делает 1 итерацию)
    def step(self):
        new_cells = deepcopy(self.cells)
        self.counter += 1
        self.has_changes = False
        # в x0, x1, y0, y1 хотим получить границы прямоугольной области соседей,
        # включая саму ячейку - для подсчета соседей
        for i in range(self.sizey):         # цикл по всем строкам матрицы
            y0 = max(0, i - 1)              # учесть границы поля по y
            y1 = min(i + 2, self.sizey)
            for j in range(self.sizex):     # цикл по всем столбцам матрицы
                x0 = max(0, j - 1)          # учесть границы поля по x
                x1 = min(j + 2, self.sizex)
                # подсчет соседей текущей ячейки
                neighbors = -self.cells[i][j]
                for y in range(y0, y1):
                    for x in range(x0, x1):
                        neighbors += int(self.cells[y][x])
                # рождение новой ячейки тремя соседями
                if self.cells[i][j] == 0 and neighbors == 3:
                    new_cells[i][j] = 1
                    self.has_changes = True
                # смерть, если соседей не 2 или 3
                elif self.cells[i][j] == 1 and (neighbors < 2 or neighbors > 3):
                    new_cells[i][j] = 0
                    self.has_changes = True
        self.cells = deepcopy(new_cells)    # замена матрицы после рождения / смерти
        if not self.has_changes:
            return                  # прекратить, если ничто не изменилось
        self.paint()                # перерисовка полотна


    # обработчик кнопки "Выполнить" - итерирует в цикле с таймером через self.step()
    def play(self):
        while self.has_changes:
            sleep(0.2)
            self.step()


    # обработчик клика левой кнопкой мыши по canvas
    def handle_click(self, event):
        #print("x={}, y={}".format(event.x, event.y))
        # сопоставить координаты щелчка с индексами матрицы
        i = event.y // self.cell_size   # номер строки матрицы
        j = event.x // self.cell_size   # номер столбца матрицы
        # инвертируем значение в матрице 0 <-> 1
        if self.cells[i][j] == 1:
            self.cells[i][j] = 0
        else:
            self.cells[i][j] = 1
        # сброс счетчика, поставить флаг измнененной матрицы
        self.counter = 1        # сброс счетчика итераций
        self.has_changes = True # установить флаг измнененной матрицы
        self.paint()            # перерисовка полотна



# точка вызова: будет проигнорирована, если программу подключить как модуль
if __name__ == "__main__":
    app = App()     # создать объект приложения
    app.mainloop()  # цикл обработки сообщений приложения
