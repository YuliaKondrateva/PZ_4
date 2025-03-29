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
        self.setWindowTitle("Гармоническое колебание")
        self.setMinimumSize(700, 500)
        self.build_ui()

    # Построение интерфейса
    def build_ui(self):
        main_layout = QVBoxLayout()

        # Блок ввода параметров
        input_layout = QHBoxLayout()
        self.amp_input = QLineEdit()
        self.freq_input = QLineEdit()
        self.phase_input = QLineEdit()

        # Подписи и поля ввода
        input_layout.addWidget(QLabel("Амплитуда A (м):"))
        input_layout.addWidget(self.amp_input)
        input_layout.addWidget(QLabel("Частота f (Гц):"))
        input_layout.addWidget(self.freq_input)
        input_layout.addWidget(QLabel("Фаза φ (°):"))
        input_layout.addWidget(self.phase_input)
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
            # Получение и проверка входных значений
            amplitude = float(self.amp_input.text())
            frequency = float(self.freq_input.text())
            phase_deg = float(self.phase_input.text())

            if amplitude < 0:
                self.show_error("Амплитуда не может быть отрицательной.")
                return
            if frequency <= 0:
                self.show_error("Частота должна быть положительной.")
                return

            # Расчёты
            phase_rad = np.radians(phase_deg)
            t = np.linspace(0, 2, 1000)
            x = amplitude * np.sin(2 * np.pi * frequency * t + phase_rad)

            # Отрисовка графика
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(t, x, label="x(t) = A·sin(2πft + φ)")
            ax.set_xlabel("Время, с")
            ax.set_ylabel("Смещение, м")
            ax.set_title("Гармоническое колебание")
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Oscillation()
    window.show()
    sys.exit(app.exec_())
