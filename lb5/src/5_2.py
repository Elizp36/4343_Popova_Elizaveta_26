def solve():
    text = input().strip()
    pattern = input().strip()
    wildcard = input().strip()
    
    n = len(text)
    m = len(pattern)
    
    results = []
    
    # Проверяем каждую позицию в тексте
    for i in range(n - m + 1):
        match = True
        for j in range(m):
            # Если символ в шаблоне не джокер и не совпадает с текстом
            if pattern[j] != wildcard and pattern[j] != text[i + j]:
                match = False
                break
        
        if match:
            results.append(i + 1)  # 1-индексация
    
    # Выводим результаты
    for pos in results:
        print(pos)

solve()