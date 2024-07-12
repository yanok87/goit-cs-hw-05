import requests
import collections
import concurrent.futures
import matplotlib.pyplot as plt
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def map_function(text):
    words = re.findall(r"\b\w+\b", text.lower())
    return collections.Counter(words)


def reduce_function(counters):
    total_counter = collections.Counter()
    for counter in counters:
        total_counter.update(counter)
    return total_counter


def fetch_text_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    # Використання BeautifulSoup для вилучення тексту з HTML
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()


def visualize_top_words(word_counts, num_top_words=10):
    top_words = word_counts.most_common(num_top_words)
    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 6))
    plt.barh(words, counts, color="skyblue")
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.title("Top 10 Most Frequent Words")
    plt.gca().invert_yaxis()
    plt.show()


def main(url):
    try:
        text = fetch_text_from_url(url)
        text_blocks = [text[i : i + 10000] for i in range(0, len(text), 10000)]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            map_results = list(executor.map(map_function, text_blocks))

        word_counts = reduce_function(map_results)
        visualize_top_words(word_counts)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"  # Приклад URL
    main(url)
