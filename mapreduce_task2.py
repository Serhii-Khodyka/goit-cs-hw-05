import string
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict, Counter
import requests
import re
import matplotlib.pyplot as plt

def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

# Функція для заміни знаків пунктуації пробілами
def replace_punctuation_with_spaces(text):
    return re.sub(r'[{}]'.format(string.punctuation), ' ', text)

def map_function(word):
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# Виконання MapReduce
def map_reduce(text, search_words=None):
    # Заміна знаків пунктуації пробілами
    text = replace_punctuation_with_spaces(text)
    words = text.lower().split()

    # Якщо задано список слів для пошуку, враховувати тільки ці слова
    if search_words:
        words = [word for word in words if word in search_words]

    # Паралельний Мапінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

def visualize_top_words(word_counts, top_n=10):
    # Конвертування словника в об'єкт Counter
    word_counter = Counter(word_counts)
    top_words = word_counter.most_common(top_n)
    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 5))
    plt.bar(words, counts)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title(f'Top {top_n} most frequent words')
    plt.show()

if __name__ == '__main__':
    # Вхідний текст для обробки
    url = 'https://goit.global/ua-ru/'
    text = get_text(url)
    if text:
        # Виконання MapReduce на вхідному тексті
        result = map_reduce(text)
        visualize_top_words(result, 10) #виводимо діаграму для ТОП-10 слів
        #print("Результат підрахунку слів:", result)
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")
    
  
