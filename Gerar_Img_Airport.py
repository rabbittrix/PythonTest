import matplotlib.pyplot as plt
import numpy as np
import random

# Lista de aeroportos da UE com seus códigos ICAO
airports = ['LPPT', 'LEMD', 'LFPG', 'EDDB', 'LIRF', 'EHAM', 'LOWW', 'EBBR', 'EKCH', 'EIDW']

def draw_radar(airport_code):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_facecolor('black')

    # Desenhar círculos concêntricos
    for radius in range(50, 300, 50):
        circle = plt.Circle((0, 0), radius, color='green', fill=False, linewidth=1)
        ax.add_artist(circle)

    # Desenhar linhas radiais
    for angle in range(0, 360, 45):
        x = [0, 300 * np.cos(np.radians(angle))]
        y = [0, 300 * np.sin(np.radians(angle))]
        ax.plot(x, y, color='green', linewidth=1)

    # Adicionar aviões (pontos)
    for _ in range(10):  # Adicionar 10 aviões aleatórios
        x = random.uniform(-250, 250)
        y = random.uniform(-250, 250)
        ax.plot(x, y, 'yo', markersize=5)

    ax.set_xlim(-300, 300)
    ax.set_ylim(-300, 300)
    ax.set_aspect('equal', 'box')
    ax.axis('off')

    # Salvar a imagem
    plt.savefig(f"assets/{airport_code}.png", bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close()

# Gerar imagens para todos os aeroportos
for airport in airports:
    draw_radar(airport)

if __name__ == '__main__':
    print("Imagens geradas com sucesso!")