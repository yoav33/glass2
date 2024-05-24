import requests


def search_duckduckgo(query):
    url = f"http://api.duckduckgo.com/?q={query}&format=json"
    response = requests.get(url)
    data = response.json()

    if 'AbstractText' in data:
        return data['AbstractText']
    elif 'Answer' in data:
        return data['Answer']
    else:
        return "Sorry, I couldn't find an answer to that question."


if __name__ == "__main__":
    user_query = input("What do you want to know? ")
    result = search_duckduckgo(user_query)
    print(result)
