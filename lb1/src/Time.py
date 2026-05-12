import subprocess
import time
import os
import sys

PROGRAM_PATH = "PiAA.exe"

TEST_VALUES = [2, 3, 5, 10, 17, 20, 30, 33, 40]

RUNS_PER_TEST = 3

def measure_time(n, program_path):
    times = []
    
    for _ in range(RUNS_PER_TEST):
        start = time.perf_counter()
        
        result = subprocess.run(
            [program_path],
            input=f"{n}\n",
            text=True,
            capture_output=True,
            timeout=30 
        )
        
        end = time.perf_counter()
        
        if result.returncode == 0:
            elapsed_ms = (end - start) * 1000
            times.append(elapsed_ms)
        else:
            print(f"Ошибка для N={n}: {result.stderr.strip()}", file=sys.stderr)
            return None
    
    times.sort()
    return times[len(times) // 2]

def main():
    if not os.path.exists(PROGRAM_PATH):
        print(f"Файл {PROGRAM_PATH} не найден!")
        print("Скомпилируйте программу перед запуском:")
        print(f"   g++ -O3 -std=c++17 -o {PROGRAM_PATH.replace('.exe', '')} Test_1.cpp")
        return
    
    print(f"Замер времени для {PROGRAM_PATH}")
    print(f"Тестовые значения: {TEST_VALUES}")
    print(f"Прогонов на тест: {RUNS_PER_TEST}")
    
    results = []
    
    for n in TEST_VALUES:
        elapsed = measure_time(n, PROGRAM_PATH)
        
        if elapsed is not None:
            results.append((n, elapsed))
            print(f"N={n:2d} | время={elapsed:8.3f} мс")
        else:
            print(f"N={n:2d} | ошибка замера")
    
    if results:
        output_file = "times.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            for n, t in results:
                f.write(f"{n} {t:.6f}\n")
        
        print(f"Результаты сохранены в {output_file}")
        print(f"Всего замеров: {len(results)}")
        
        # Показать статистику
        if len(results) >= 2:
            min_t = min(t for _, t in results)
            max_t = max(t for _, t in results)
            print(f"Диапазон времени: {min_t:.3f} — {max_t:.3f} мс")
    else:
        print("Не удалось получить ни одного замера")

if __name__ == "__main__":
    main()