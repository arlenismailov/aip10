import requests
import json


# Функция для запроса данных из API
def fetch_api_data(url):
    response = requests.get(url)
    return response.json()


# Пример API URL для тестирования
api_urls = [
    "https://jsonplaceholder.typicode.com/users",
    "https://jsonplaceholder.typicode.com/posts",
    "https://jsonplaceholder.typicode.com/comments",
    "https://jsonplaceholder.typicode.com/albums",
    "https://jsonplaceholder.typicode.com/photos",
    "https://jsonplaceholder.typicode.com/todos",
    "https://jsonplaceholder.typicode.com/posts/1/comments",
    "https://jsonplaceholder.typicode.com/albums/1/photos",
    "https://jsonplaceholder.typicode.com/users/1/posts",
    "https://jsonplaceholder.typicode.com/users/1/todos"
]

# Получение данных из всех API
data = {}
for url in api_urls:
    key = url.split('/')[-1] if url.split('/')[-1] else url.split('/')[-2]
    data[key] = fetch_api_data(url)


# Функция поиска данных
def search_data(data, search_term):
    results = {key: [] for key in data}
    search_term = search_term.lower()

    for key, items in data.items():
        for item in items:
            if isinstance(item, dict):
                if 'name' in item and search_term in item['name'].lower():
                    results[key].append(item)
                elif 'username' in item and search_term in item['username'].lower():
                    results[key].append(item)
                elif str(item.get('id', '')).lower() == search_term:
                    results[key].append(item)
    return results

# Вывод результатов поиска в терминал
def display_results(results):
    total_results = sum(len(items) for items in results.values())
    print(f"Found {total_results} result(s) across all APIs:")
    for key, items in results.items():
        if items:
            print(f"\nResults from {key}:")
            for item in items:
                print(json.dumps(item, indent=4))
                print("\n")


# Ввод поискового термина
search_term = input("Поиск по (имя, фамилия, id): ")

# Поиск данных
results = search_data(data, search_term)

# Вывод результатов поиска
display_results(results)
