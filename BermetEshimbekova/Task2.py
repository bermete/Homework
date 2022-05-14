# Task 5.2
import re

def most_common_words(filepath, number_of_words=3):
    with open(filepath, 'r') as f:
        data = re.findall('\w+', f.read().lower())
        f.close()
    words = sorted(set(data))
    words_dict = {word: data.count(word) for word in words}
    words_dict = sorted(words_dict.items(), key=lambda x: x[1], reverse=True)[:number_of_words]
    return [i[0] for i in words_dict]


print(most_common_words('../data/lorem_ipsum.txt'))
# >>> ['donec', 'etiam', 'aliquam']
