def prefix_function(pattern):
    m = len(pattern)
    pi = [0] * m
    j = 0
    
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            pi[i] = j
    return pi

def kmp(pattern, text):
    n = len(text)
    m = len(pattern)
    
    if m == 0 or n == 0 or m > n:
        return []
    
    pi = prefix_function(pattern)
    occurrences = []
    j = 0
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]
        
        if text[i] == pattern[j]:
            j += 1
        
        if j == m:
            occurrences.append(i - m + 1)
            j = pi[j - 1]
    return occurrences

P = input().strip()
T = input().strip()

result = kmp(P, T)

if result:
    print(','.join(map(str, result)))
else:
    print(-1)
