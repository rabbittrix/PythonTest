import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MESDashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MES Monitoring Dashboard")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.create_status_label()
        self.create_plots()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(5000)  # Update data every 5 seconds

        self.data_log_file = 'mes_data_log.txt'
        self.init_log_file()

    def create_status_label(self):
        self.label_status = QLabel("Status: Running", self)
        self.label_status.setFont(QFont('Arial', 14))
        self.label_status.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_status)

    def create_plots(self):
        self.fig, self.ax = plt.subplots(2, 1, figsize=(8, 8))

        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        self.temperature_data = []
        self.pressure_data = []
        self.production_data = []
        self.performance_data = []

        self.ax[0].set_title('Temperature and Pressure Monitoring')
        self.ax[0].set_xlabel('Time')
        self.ax[0].set_ylabel('Temperature (°C)')
        self.ax[0].set_ylim(0, 100)

        self.ax[1].set_title('Production and Performance Monitoring')
        self.ax[1].set_xlabel('Time')
        self.ax[1].set_ylabel('Production')
        self.ax[1].set_ylim(0, 100)

    def update_data(self):
        # Fetch real-time data (simulated)
        temperature, pressure, production, performance = self.fetch_realtime_data()

        # Append data to lists
        self.temperature_data.append(temperature)
        self.pressure_data.append(pressure)
        self.production_data.append(production)
        self.performance_data.append(performance)

        # Update plots
        self.ax[0].clear()
        self.ax[0].plot(self.temperature_data, label='Temperature', color='red')
        self.ax[0].plot(self.pressure_data, label='Pressure', color='blue')
        self.ax[0].legend()

        self.ax[1].clear()
        self.ax[1].plot(self.production_data, label='Production', color='green')
        self.ax[1].plot(self.performance_data, label='Performance', color='orange')
        self.ax[1].legend()

        self.canvas.draw()

        # Log data
        self.log_data(temperature, pressure, production, performance)

    def fetch_realtime_data(self):
        # Simulated real-time data fetching
        temperature = random.randint(20, 40)
        pressure = random.randint(800, 1200)
        production = random.randint(0, 100)
        performance = random.randint(0, 100)
        return temperature, pressure, production, performance

    def init_log_file(self):
        with open(self.data_log_file, 'w') as file:
            file.write("Temperature (°C), Pressure (Pa), Production, Performance\n")

    def log_data(self, temperature, pressure, production, performance):
        with open(self.data_log_file, 'a') as file:
            file.write(f"{temperature}, {pressure}, {production}, {performance}\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MESDashboard()
    window.show()
    sys.exit(app.exec_())
