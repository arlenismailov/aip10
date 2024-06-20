from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import httpx
import json
import asyncio
from asgiref.sync import sync_to_async
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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


async def search_by_id(data, search_term):
    results = {key: [] for key in data}
    search_term = search_term.lower()

    for key, items in data.items():
        for item in items:
            if isinstance(item, dict) and str(item.get('id', '')).lower() == search_term:
                results[key].append(item)
    return results


async def search_by_name(data, search_term):
    results = {key: [] for key in data}
    search_term = search_term.lower()

    for key, items in data.items():
        for item in items:
            if isinstance(item, dict) and 'name' in item and search_term in item['name'].lower():
                results[key].append(item)
    return results


async def search_by_username(data, search_term):
    results = {key: [] for key in data}
    search_term = search_term.lower()

    for key, items in data.items():
        for item in items:
            if isinstance(item, dict) and 'username' in item and search_term in item['username'].lower():
                results[key].append(item)
    return results


@swagger_auto_schema(method='get', manual_parameters=[
    openapi.Parameter('q', openapi.IN_QUERY, description="Search term", type=openapi.TYPE_STRING)
])
@api_view(['GET'])
def search_id(request):
    search_term = request.GET.get('q', '')
    data = asyncio.run(fetch_all_data(api_urls))
    results = asyncio.run(search_by_id(data, search_term))

    print("Search term (ID):", search_term)
    print("Search results by ID:")
    print(json.dumps(results, indent=4))

    return Response({'results': results, 'search_term': search_term}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='get', manual_parameters=[
    openapi.Parameter('q', openapi.IN_QUERY, description="Search term", type=openapi.TYPE_STRING)
])
@api_view(['GET'])
def search_name(request):
    search_term = request.GET.get('q', '')
    data = asyncio.run(fetch_all_data(api_urls))
    results = asyncio.run(search_by_name(data, search_term))

    print("Search term (Name):", search_term)
    print("Search results by Name:")
    print(json.dumps(results, indent=4))

    return Response({'results': results, 'search_term': search_term}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='get', manual_parameters=[
    openapi.Parameter('q', openapi.IN_QUERY, description="Search term", type=openapi.TYPE_STRING)
])
@api_view(['GET'])
def search_username(request):
    search_term = request.GET.get('q', '')
    data = asyncio.run(fetch_all_data(api_urls))
    results = asyncio.run(search_by_username(data, search_term))

    print("Search term (Username):", search_term)
    print("Search results by Username:")
    print(json.dumps(results, indent=4))

    return Response({'results': results, 'search_term': search_term}, status=status.HTTP_200_OK)


def index(request):
    return render(request, 'search/index.html', {'swagger_url': '/swagger/'})
