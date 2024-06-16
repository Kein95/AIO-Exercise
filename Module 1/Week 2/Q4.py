def levenshtein_distance(source, target):
    m, n = len(source), len(target)
    D = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        D[i][0] = i
    for j in range(n + 1):
        D[0][j] = j

    # Tính khoảng cách Levenshtein
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if source[i - 1] == target[j - 1]:
                cost = 0
            else:
                cost = 1
            D[i][j] = min(D[i - 1][j] + 1,
                          D[i][j - 1] + 1,
                          D[i - 1][j - 1] + cost)

    return D[m][n]

source = "kitten"
target = "sitting"
distance = levenshtein_distance(source, target)
print("Khoảng cách Levenshtein:", distance)

source = "yu"
target = "you"
distance = levenshtein_distance(source, target)
print("Khoảng cách Levenshtein:", distance)