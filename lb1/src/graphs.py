import matplotlib.pyplot as plt
import numpy as np
import math

def load_data(filename='times.txt'):
    x, y = [], []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    x.append(float(parts[0]))
                    y.append(float(parts[1]))
    return np.array(x), np.array(y)

def normalize_theory(x_practical, y_practical, x_theory):

    y_theory_raw = np.array([2**n for n in x_theory])
    
    k_sum = 0
    count = 0
    for i, n in enumerate(x_practical):
        idx = int(n) - 1
        if 0 <= idx < len(y_theory_raw) and y_practical[i] > 0:
            k_sum += y_theory_raw[idx] / y_practical[i]
            count += 1
    
    if count == 0:
        return y_theory_raw
    
    k = k_sum / count
    return y_theory_raw / k

def plot_graph(x_practical, y_practical, output_file='graph.png'):

    x_theory = np.linspace(min(x_practical), max(x_practical), 100)
    y_theory = normalize_theory(x_practical, y_practical, x_theory)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(x_practical, y_practical, 'ro-', 
            label='Практическое время', 
            linewidth=2, markersize=6, markerfacecolor='red')
    
    ax.plot(x_theory, y_theory, 'b--', 
            label='Теоретическая оценка $O(2^N)$', 
            linewidth=1.5)
    
    ax.set_xlabel('Размер задачи $N$', fontsize=12)
    ax.set_ylabel('Время выполнения (мс)', fontsize=12)
    ax.set_title('Зависимость времени работы алгоритма от размера задачи', 
                 fontsize=14, fontweight='bold')
    
    ax.set_yscale('log')
    ax.grid(True, which='both', linestyle=':', alpha=0.7)
    
    ax.legend(fontsize=10, loc='upper left')
    
    stats = f"Замеров: {len(x_practical)}\n"
    stats += f"Диапазон: {int(min(x_practical))}–{int(max(x_practical))}\n"
    stats += f"Время: {min(y_practical):.3f}–{max(y_practical):.3f} мс"
    
    ax.text(0.98, 0.02, stats, transform=ax.transAxes, 
            fontsize=9, verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"График сохранён в {output_file}")
    plt.show()

def plot_linear_graph(x_practical, y_practical, output_file='graph_linear.png'):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(x_practical, y_practical, 'go-', linewidth=2, markersize=6)
    
    ax.set_xlabel('Размер задачи $N$', fontsize=12)
    ax.set_ylabel('Время выполнения (мс)', fontsize=12)
    ax.set_title('Время работы алгоритма (линейная шкала)', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, linestyle=':', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Линейный график сохранён в {output_file}")
    plt.show()

def main():
    print("Загрузка данных...")
    
    try:
        x, y = load_data('times.txt')
    except FileNotFoundError:
        print("Файл times.txt не найден!")
        print("Сначала запустите collect_times.py для сбора данных.")
        return
    
    if len(x) < 2:
        print("Недостаточно данных для построения графика")
        return
    
    print(f"Загружено {len(x)} точек")
    print(f"Диапазон N: {int(min(x))} – {int(max(x))}")
    
    print("\nПостроение графика (логарифмическая шкала)...")
    plot_graph(x, y, 'graph_log.png')
    
    if max(x) <= 25:
        print("Построение графика (линейная шкала)...")
        plot_linear_graph(x, y, 'graph_linear.png')
    
    print("\nСтатистика:")
    print(f"   Мин. время: {min(y):.4f} мс (N={int(x[np.argmin(y)])})")
    print(f"   Макс. время: {max(y):.4f} мс (N={int(x[np.argmax(y)])})")
    
    # Оценка роста
    if len(x) >= 2:
        ratio = y[-1] / y[0]
        n_ratio = x[-1] / x[0]
        print(f"   Рост при увеличении N в {n_ratio:.1f} раз: время выросло в {ratio:.1f} раз")

if __name__ == "__main__":
    main()