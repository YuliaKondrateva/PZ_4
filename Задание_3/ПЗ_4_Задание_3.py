import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Главное окно приложения
class Oscillation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Затухающие колебания маятника")
        self.setMinimumSize(600, 400)
        self.build_ui()

    # Построение интерфейса
    def build_ui(self):
        main_layout = QVBoxLayout()

        # Блок ввода параметров
        input_layout = QHBoxLayout()
        self.amp_input = QLineEdit()
        self.damping_input = QLineEdit()
        self.freq_input = QLineEdit()

        # Подписи и поля ввода
        input_layout.addWidget(QLabel("Амплитуда A (°):"))
        input_layout.addWidget(self.amp_input)
        input_layout.addWidget(QLabel("Коэф. затухания β (1/с):"))
        input_layout.addWidget(self.damping_input)
        input_layout.addWidget(QLabel("Частота f (Гц):"))
        input_layout.addWidget(self.freq_input)
        main_layout.addLayout(input_layout)

        # Кнопка для построения графика
        plot_button = QPushButton("Построить")
        plot_button.clicked.connect(self.plot_graf)
        main_layout.addWidget(plot_button)

        # Область вывода графика
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)
        self.setLayout(main_layout)

    # Построение графика
    def plot_graf(self):
        try:
            # Считывание и валидация данных
            A = float(self.amp_input.text())
            beta = float(self.damping_input.text())
            f = float(self.freq_input.text())

            if A < 0:
                self.show_error("Амплитуда не может быть отрицательной.")
                return
            if beta < 0:
                self.show_error("Коэффициент затухания должен быть неотрицательным.")
                return
            if f <= 0:
                self.show_error("Частота должна быть положительной.")
                return

            # Расчеты
            t = np.linspace(0, 10, 1000)
            theta = A * np.exp(-beta * t) * np.cos(2 * np.pi * f * t)

            # Отрисовка графика
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(t, theta, label='θ(t) = A·e^(-βt)·cos(2πft)')
            ax.set_xlabel("Время (с)")
            ax.set_ylabel("Угол отклонения (°)")
            ax.set_title("Затухающие колебания маятника")
            ax.grid(True)
            ax.legend()
            self.canvas.draw()

        except ValueError:
            self.show_error("Введите корректные числовые значения.")
        except Exception as e:
            self.show_error(f"Произошла ошибка: {str(e)}")

    def show_error(self, message):
        # Отображает всплывающее окно с сообщением об ошибке
        QMessageBox.warning(self, "Ошибка", message)


# Точка входа
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Oscillation()
    window.show()
    sys.exit(app.exec_())
