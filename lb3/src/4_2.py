def levenshtein_distance(s, t):
    n, m = len(s), len(t)
    
    if n < m:
        s, t = t, s
        n, m = m, n

    prev2_row = list(range(m + 1))
    prev1_row = [0] * (m + 1) 
    prev1_row[0] = 1
    for i in range(1, m + 1):
        if s[0] == t[i-1]:
            prev1_row[i] = prev2_row[i-1]
        else:
            prev1_row[i] = 1 + min(prev2_row[i], prev1_row[i-1], prev2_row[i-1])

    if n == 1:
        return prev1_row[m]

    for i in range(2, n + 1):
        curr_row = [0] * (m + 1)
        curr_row[0] = i 
        char_s = s[i-1]
        
        for j in range(1, m + 1):
            if char_s == t[j-1]:
                curr_row[j] = prev1_row[j-1]
            else:
                curr_row[j] = 1 + min(prev1_row[j], curr_row[j-1], prev1_row[j-1], prev2_row[j] if s[i-1] != s[i-2] else float('inf'))
        prev2_row = prev1_row
        prev1_row, curr_row = curr_row, prev1_row

    return prev1_row[m]

def main():
    data = input().split()
    if len(data) >= 2:
        print(levenshtein_distance(data[0], data[1]))

if __name__ == "__main__":
    main()
