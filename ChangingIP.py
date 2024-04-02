import os
import ctypes
import sys

# Função para solicitar permissão de administrador
def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:
        changeIP()

# Change the IP address of local machine
def changeIP():
    # Change IP address for Windows
    os.system("netsh interface ip set address name='Local Area Connection' static 192.168.1.10 255.255.255.0 192.168.1.1")

    # Change default gateway
    os.system("route delete 0.0.0.0")
    os.system("route add 0.0.0.0 mask 0.0.0.0 192.168.1.1")

if __name__ == '__main__':
    run_as_admin()
