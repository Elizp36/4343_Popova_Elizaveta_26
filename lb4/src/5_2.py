import sys
import array

def prefix_function(pattern):
    m = len(pattern)
    pi = array.array('i', [0]) * m
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
        return -1
    pi = prefix_function(pattern)
    j = 0
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            return i - m + 1
    return -1

def main():
    A = input().strip()
    B = input().strip()
    if len(A) != len(B):
        print(-1)
        return
    pos = kmp(B, A + A)
    if pos != -1 and pos < len(A):
        print(pos)
    else:
        print(-1)

if __name__ == '__main__':
    main()