def levenshtein_distance(s, t):
    n, m = len(s), len(t)
    
    if n < m:
        s, t = t, s
        n, m = m, n

    prev_row = list(range(m + 1))
    curr_row = [0] * (m + 1)

    for i in range(1, n + 1):
        curr_row[0] = i
        char_s = s[i-1]
        
        for j in range(1, m + 1):
            if char_s == t[j-1]:
                curr_row[j] = prev_row[j-1]
            else:
                curr_row[j] = 1 + min(prev_row[j], curr_row[j-1], prev_row[j-1])
        
        prev_row, curr_row = curr_row, prev_row

    return prev_row[m]

def main():
    data = input().split()
    if len(data) >= 2:
        print(levenshtein_distance(data[0], data[1]))

if __name__ == "__main__":
    main()