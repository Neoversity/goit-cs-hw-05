import requests
from collections import Counter
import matplotlib.pyplot as plt
import re
from concurrent.futures import ThreadPoolExecutor


# Функція для завантаження тексту з URL
def fetch_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return ""


# Функція для обробки тексту: перетворюємо його на список слів
def process_text(text):
    # Видаляємо всі небажані символи та розбиваємо текст на слова
    words = re.findall(r"\b\w+\b", text.lower())
    return words


# Функція для підрахунку частоти слів за допомогою MapReduce
def map_reduce_word_count(text):
    # Обробляємо текст і отримуємо слова
    words = process_text(text)

    # Використовуємо ThreadPoolExecutor для паралельної обробки
    with ThreadPoolExecutor() as executor:
        word_counts = list(executor.map(Counter, [words]))

    # Об'єднуємо результати
    total_counts = Counter()
    for count in word_counts:
        total_counts.update(count)

    return total_counts


# Функція для візуалізації топ N слів
def visualize_top_words(word_counts, top_n=10):
    top_words = word_counts.most_common(top_n)

    words, counts = zip(*top_words)

    plt.barh(words, counts, color="skyblue")
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.title(f"Top {top_n} Most Frequent Words")
    plt.gca().invert_yaxis()
    plt.show()


# Головна функція
def main():
    url = "https://www.gutenberg.org/files/84/84-0.txt"  # URL для завантаження тексту (Можна змінити на інший)

    # Завантажуємо текст
    text = fetch_text_from_url(url)

    if not text:
        return

    # Застосовуємо MapReduce для підрахунку частоти слів
    word_counts = map_reduce_word_count(text)

    # Візуалізуємо результати для топ 10 найчастіших слів
    visualize_top_words(word_counts, top_n=10)


if __name__ == "__main__":
    main()
