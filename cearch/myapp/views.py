from django.shortcuts import render
import httpx
import json
import asyncio

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


async def fetch_api_data(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()


async def fetch_all_data(urls):
    tasks = [fetch_api_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    data = {}
    for url, result in zip(urls, results):
        key = url.split('/')[-1] if url.split('/')[-1] else url.split('/')[-2]
        data[key] = result
    return data


async def search_data(data, search_term):
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


async def index(request):
    return render(request, 'search/index.html', {'swagger_url': '/swagger/'})


async def search(request):
    search_term = request.GET.get('q', '')

    data = await fetch_all_data(api_urls)
    results = await search_data(data, search_term)

    print("Search term:", search_term)
    print("Search results:")
    print(json.dumps(results, indent=4))

    return render(request, 'search/results.html', {'results': results, 'search_term': search_term})
