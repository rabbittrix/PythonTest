import sys
import random
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, \
    QTableWidgetItem, QScrollBar
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QTimer, QDateTime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MESDashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MES Monitoring Dashboard")
        self.setGeometry(100, 100, 1280, 720)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.create_buttons()
        self.create_status_label()
        self.create_plots()
        self.create_table()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(5000)  # Update data every 5 seconds

        self.data_log_file = 'mes_data_log.txt'
        self.init_log_file()

        self.last_row_flash = False

    def create_buttons(self):
        button_layout = QHBoxLayout()

        self.btn_emergency_stop = QPushButton('Emergency Stop', self)
        self.btn_emergency_stop.clicked.connect(self.emergency_stop)
        self.btn_emergency_stop.setStyleSheet(
            "QPushButton { border-radius: 25px; padding: 10px; background-color: red; }")
        button_layout.addWidget(self.btn_emergency_stop)

        self.btn_start_production = QPushButton('Start Production', self)
        self.btn_start_production.clicked.connect(self.start_production)
        self.btn_start_production.setStyleSheet(
            "QPushButton { border-radius: 25px; padding: 10px; background-color: green; }")
        button_layout.addWidget(self.btn_start_production)

        self.layout.addLayout(button_layout)

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

    def create_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(5)  
        self.table.setHorizontalHeaderLabels(["Date & Time", "Temperature (°C)", "Pressure (Pa)", "Production", "Performance"])

        header = self.table.horizontalHeader()
        header.setStyleSheet("QHeaderView::section { background-color: lightgray; font-weight: bold; }")

        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 150)

        self.table.verticalHeader().setVisible(False)

        self.table.setMinimumHeight(200)

        self.layout.addWidget(self.table)

        self.scrollbar = QScrollBar(Qt.Vertical)
        self.scrollbar.setInvertedAppearance(True)  # Inverter a aparência do scrollbar
        self.scrollbar.sliderMoved.connect(lambda: self.table.verticalScrollBar().setValue(self.scrollbar.maximum()))
        self.layout.addWidget(self.scrollbar)

    def emergency_stop(self):
        self.label_status.setText("Status: Emergency Stop")
        self.timer.stop()
        # Obter data e hora atual
        import datetime
        now = datetime.datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.log_data("Emergency Stop", date_time, 0, 0, 0, 0)


    def start_production(self):
        self.label_status.setText("Status: Running")
        self.timer.start(5000)

    def update_data(self):
        temperature, pressure, production, performance = self.fetch_realtime_data()

        self.temperature_data.append(temperature)
        self.pressure_data.append(pressure)
        self.production_data.append(production)
        self.performance_data.append(performance)

        self.ax[0].clear()
        self.ax[0].plot(self.temperature_data, label='Temperature', color='red')
        self.ax[0].plot(self.pressure_data, label='Pressure', color='blue')
        self.ax[0].legend()

        self.ax[1].clear()
        self.ax[1].plot(self.production_data, label='Production', color='green')
        self.ax[1].plot(self.performance_data, label='Performance', color='orange')
        self.ax[1].legend()

        self.canvas.draw()

        date_time = "2024-03-17T02:00:00"  # Substitua pela data e hora atual
        self.log_data("Running", date_time, temperature, pressure, production, performance)
        self.update_table()

    def fetch_realtime_data(self):
        temperature = random.randint(20, 40)
        pressure = random.randint(800, 1200)
        production = random.randint(0, 100)
        performance = random.randint(0, 100)
        return temperature, pressure, production, performance

    def init_log_file(self):
        if not os.path.exists(self.data_log_file):
            with open(self.data_log_file, 'w') as file:
                file.write("Date & Time, Temperature (°C), Pressure (Pa), Production, Performance\n")

    def log_data(self, message, date_time, temperature, pressure, production, performance):
        with open(self.data_log_file, 'a') as file:
            file.write(f"{message}: {date_time}, {temperature}, {pressure}, {production}, {performance}\n")

    def update_table(self):
        row_count = len(self.temperature_data)
        self.table.setRowCount(row_count)
        for i in range(row_count):
            date_time = QDateTime.currentDateTime().toString(Qt.ISODate)
            self.table.setItem(i, 0, QTableWidgetItem(date_time))
            self.table.setItem(i, 1, QTableWidgetItem(str(self.temperature_data[i])))
            self.table.setItem(i, 2, QTableWidgetItem(str(self.pressure_data[i])))
            self.table.setItem(i, 3, QTableWidgetItem(str(self.production_data[i])))
            self.table.setItem(i, 4, QTableWidgetItem(str(self.performance_data[i])))

        if self.last_row_flash:
            for j in range(5):
                self.table.item(0, j).setBackground(QColor(255, 255, 153))  # Amarelo claro
        else:
            for j in range(5):
                self.table.item(0, j).setBackground(QColor(255, 255, 255))  # Branco

        self.last_row_flash = not self.last_row_flash

        self.scrollbar.setMaximum(max(0, row_count - 5))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MESDashboard()
    window.show()
    sys.exit(app.exec_())
