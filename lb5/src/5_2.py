def solve():
    text = input().strip()
    pattern = input().strip()
    wildcard = input().strip()
    
    n = len(text)
    m = len(pattern)
    
    results = []
    
    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if pattern[j] != wildcard and pattern[j] != text[i + j]:
                match = False
                break
        
        if match:
            results.append(i + 1)
    
    for pos in results:
        print(pos)

solve()
