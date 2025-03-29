import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Главное окно приложения
class Trajectory(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Траектория движения тела, брошенного под углом")
        self.setGeometry(100, 100, 800, 600)
        self.build_ui()

    # Построение интерфейса
    def build_ui(self):
        main_layout = QVBoxLayout()

        # Блок ввода параметров
        input_layout = QHBoxLayout()
        self.input_velocity = QLineEdit()
        self.input_angle = QLineEdit()

        # Подписи и поля ввода
        input_layout.addWidget(QLabel("Скорость (м/с):"))
        input_layout.addWidget(self.input_velocity)
        input_layout.addWidget(QLabel("Угол (градусы):"))
        input_layout.addWidget(self.input_angle)

        # Кнопка для построения графика
        plot_button = QPushButton("Построить")
        plot_button.clicked.connect(self.plot_graf)

        # Область вывода графика
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(plot_button)
        main_layout.addWidget(self.canvas)
        self.setLayout(main_layout)

    def plot_graf(self):
        # Обрабатывает ввод и строит график траектории полета
        try:
            velocity_str = self.input_velocity.text()
            angle_str = self.input_angle.text()

            velocity = float(velocity_str)
            angle_deg = float(angle_str)

            if velocity <= 0:
                self.show_error("Скорость должна быть положительной.")
                return
            if not (0 < angle_deg <= 90):
                self.show_error("Угол должен быть в диапазоне от 0 до 90 градусов.")
                return

            # Расчеты
            g = 9.806
            angle_rad = math.radians(angle_deg)
            vx = velocity * math.cos(angle_rad)
            vy = velocity * math.sin(angle_rad)
            t_flight = 2 * vy / g
            t_points = [t * t_flight / 100 for t in range(101)]
            x = [vx * t for t in t_points]
            y = [vy * t - 0.5 * g * t**2 for t in t_points]

            # Отрисовка графика
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x, y, color="blue", label="Траектория")
            ax.set_xlabel("X — расстояние (м)")
            ax.set_ylabel("Y — высота (м)")
            ax.set_title("Траектория движения тела")
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Trajectory()
    window.show()
    sys.exit(app.exec_())
