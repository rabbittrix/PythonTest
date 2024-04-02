from datetime import datetime
from opcenter import WinCC

# Create an instance of the WinCC class
scada = WinCC()

# Define the tags used in the SCADA application
tags = {
    'Temperature': 'PLC1.Temperature',
    'Pressure': 'PLC1.Pressure',
    'Production': 'PLC1.Production',
    'Performance': 'PLC1.Performance',
    'Emergency_Stop': 'PLC1.Emergency_Stop'
}

# Define the HMI screen layout
hmi_layout = [
    {'type': 'label', 'text': 'Temperature (°C)', 'tag': tags['Temperature'], 'position': (100, 100)},
    {'type': 'label', 'text': 'Pressure (Pa)', 'tag': tags['Pressure'], 'position': (100, 150)},
    {'type': 'label', 'text': 'Production', 'tag': tags['Production'], 'position': (100, 200)},
    {'type': 'label', 'text': 'Performance', 'tag': tags['Performance'], 'position': (100, 250)},
    {'type': 'button', 'text': 'Emergency Stop', 'tag': tags['Emergency_Stop'], 'position': (100, 300)}
]

# Initialize the HMI screen
scada.initialize_screen(title='Process Monitoring', layout=hmi_layout)

# Main loop to update data and handle user interaction
while True:
    # Read data from PLC and update HMI screen
    temperature = scada.read_tag(tags['Temperature'])
    pressure = scada.read_tag(tags['Pressure'])
    production = scada.read_tag(tags['Production'])
    performance = scada.read_tag(tags['Performance'])

    scada.update_tag_value('Temperature', temperature)
    scada.update_tag_value('Pressure', pressure)
    scada.update_tag_value('Production', production)
    scada.update_tag_value('Performance', performance)

    # Check for emergency stop button press
    if scada.read_tag(tags['Emergency_Stop']):
        # Perform emergency stop procedure
        scada.update_tag_value('Emergency_Stop', False)
        scada.log_event('Emergency Stop Triggered', timestamp=datetime.now())

    # Wait for a short interval before updating again
    scada.sleep(1)
