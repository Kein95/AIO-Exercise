def count_words(file_path):
    word_count = {}
    with open(file_path, 'r') as file:
        for line in file:
            words = line.strip().split()
            for word in words:
                word = word.lower()
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
    return word_count

file_path = r'D:\00 AIO\AIO GIT HUB\AIO-Exercise\Module 1\Week 2\P1_data.txt'
word_counts = count_words(file_path)
print(word_counts)
