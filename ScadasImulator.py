import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import QTimer
import random

class SCADASimulator(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_values)
        self.init_ui()

    def init_ui(self):
        # Create labels to display process variables
        self.lbl_temperature = QLabel("Temperature: 0°C")
        self.lbl_pressure = QLabel("Pressure: 0 Pa")
        self.lbl_flow_rate = QLabel("Flow Rate: 0 L/min")

        # Create buttons for control
        self.btn_start = QPushButton("Start Process")
        self.btn_stop = QPushButton("Stop Process")

        # Set button styles
        self.btn_start.setStyleSheet("QPushButton { background-color: green; color: white; }")
        self.btn_stop.setStyleSheet("QPushButton { background-color: red; color: white; }")

        # Connect buttons to functions
        self.btn_start.clicked.connect(self.start_process)
        self.btn_stop.clicked.connect(self.stop_process)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.lbl_temperature)
        layout.addWidget(self.lbl_pressure)
        layout.addWidget(self.lbl_flow_rate)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.btn_stop)

        self.setLayout(layout)

        self.setWindowTitle("SCADA Simulator")
        self.setGeometry(100, 100, 1280, 800)
        self.show()

    def start_process(self):
        self.timer.start(1000)  # Update values every 1 second
        print("Process started.")

    def stop_process(self):
        self.timer.stop()
        print("Process stopped.")

    def update_values(self):
        # Generate mock values
        temperature = random.randint(0, 100)
        pressure = random.randint(0, 10000)
        flow_rate = random.randint(0, 100)

        # Update labels with mock values
        self.lbl_temperature.setText(f"Temperature: {temperature}°C")
        self.lbl_pressure.setText(f"Pressure: {pressure} Pa")
        self.lbl_flow_rate.setText(f"Flow Rate: {flow_rate} L/min")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SCADASimulator()
    sys.exit(app.exec_())
