import requests
from collections import defaultdict
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import concurrent.futures


# Функції MapReduce
def map_function(text):
    words = text.split()
    return [(word, 1) for word in words]


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(shuffled_values):
    reduced = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced


# Виконання MapReduce
def map_reduce(text):
    # Крок 1: Мапінг
    mapped_values = map_function(text)

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Крок 3: Редукція
    reduced_values = reduce_function(shuffled_values)

    return reduced_values


# Функція для завантаження тексту з URL
def fetch_text_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    # Використання BeautifulSoup для вилучення тексту з HTML
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()


# Функція для візуалізації результатів
def visualize_top_words(word_counts, num_top_words=10):
    sorted_word_counts = sorted(
        word_counts.items(), key=lambda item: item[1], reverse=True
    )
    top_words = sorted_word_counts[:num_top_words]
    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 6))
    plt.barh(words, counts, color="skyblue")
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.title("Top 10 Most Frequent Words")
    plt.gca().invert_yaxis()
    plt.show()


# Головний блок коду
def main(url):
    try:
        text = fetch_text_from_url(url)
        text_blocks = [text[i : i + 10000] for i in range(0, len(text), 10000)]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            map_reduce_results = list(executor.map(map_reduce, text_blocks))

        # Об'єднання результатів з усіх блоків
        combined_results = defaultdict(int)
        for result in map_reduce_results:
            for word, count in result.items():
                combined_results[word] += count

        visualize_top_words(combined_results)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"  # Приклад URL
    main(url)
