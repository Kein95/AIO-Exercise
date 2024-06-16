def my_function_(s):
    result = {}
    for char in s:
        if char in result:
            result[char] += 1
        else:
            result[char] = 1
    return result

string = 'Happiness'
print(my_function_(string))

string = 'smiles'
print(my_function_(string))