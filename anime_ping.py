import requests
import json

url = 'https://graphql.anilist.co'

media_query = '''
    query ($search: String, $type: MediaType) {
      Media(search: $search, type: $type) {
        id
        title {
          english
          romaji
        }
      }
    }
'''

media_list_query = '''
    query ($mediaId: Int, $userIds: [Int], $type: MediaType) {
      Page {
        mediaList(mediaId: $mediaId, userId_in: $userIds, type: $type) {
          user {
            name
          }
        }
      }
    }
'''

user_query = '''
query User($name: String, $sort: [UserStatisticsSort], $limit: Int) {
  User(name: $name) {
    avatar {
      medium
    }
    bannerImage
    createdAt
    statistics {
      anime {
        minutesWatched
        meanScore
        count
        genres(sort: $sort, limit: $limit) {
          count
          genre
          meanScore
        }
      }
      manga {
        count
        chaptersRead
        meanScore
        genres(sort: $sort, limit: $limit) {
          count
          genre
          meanScore
        }
      }
    }
  }
}
'''


def get_media_id(title, media_type):
    response = requests.post(url, json={'query': media_query, 'variables': {'search': title, 'type': media_type}})
    if response.status_code != 200: return None, None
    data = response.json()
    if 'errors' in data: return None, None

    media = data['data']['Media']
    title_text = media['title']['english'] or media['title']['romaji']
    return media['id'], title_text


def get_user_ids(user_names):
    """
    Dynamically builds a GraphQL query using aliases to fetch multiple users
    by name in a single request.
    """
    # Build the query string dynamically
    # Result looks like: { u0: User(name: "Rei"){id} u1: User(name: "Josh"){id} }
    query_parts = []
    for i, name in enumerate(user_names):
        # We use json.dumps(name) to handle special characters/quotes safely
        query_parts.append(f'u{i}: User(name: {json.dumps(name)}) {{ id name }}')

    full_query = "query { " + " ".join(query_parts) + " }"

    response = requests.post(url, json={'query': full_query})

    if response.status_code != 200:
        print(f"Error fetching users: {response.text}")
        return []

    data = response.json()

    # Anilist returns 'null' for users that don't exist, rather than erroring the whole batch.
    # We filter those out here.
    valid_ids = []
    if 'data' in data and data['data']:
        for key, user_data in data['data'].items():
            if user_data:  # If user_data is not None
                valid_ids.append(user_data['id'])
            else:
                # Optional: Print which user wasn't found
                # We can deduce the name from the index if needed, but simple valid_ids is enough for now
                pass

    return valid_ids


def check_watch_status(anime_id, user_ids, media_type):
    variables = {
        'mediaId': anime_id,
        'userIds': user_ids,
        'type': media_type
    }
    response = requests.post(url, json={'query': media_list_query, 'variables': variables})

    if response.status_code != 200:
        print(f"API Error: {response.text}")
        return []

    data = response.json()
    if 'errors' in data:
        print("GraphQL Error:", data['errors'])
        return []

    return data['data']['Page']['mediaList']

def find_watchers(target_users, target_media, media_type):
    out = []
    anime_id, title = get_media_id(target_media, media_type)
    if anime_id:
        user_ids = get_user_ids(target_users)
        if user_ids:
            results = check_watch_status(anime_id, user_ids, media_type)
            if results:
                for entry in results:
                    out.append(entry['user']['name'])
    return out, title

def fetch_user(username):
    variables = {
          "name": "TsarOfBulgaria",
          "sort": "COUNT_DESC",
          "limit": 3
    }
    response = requests.post(url, json={'query': user_query, 'variables': variables})
    if response.status_code != 200:
        print(f"API Error: {response.text}")
        return []
    data = response.json()
    # print(data)
    return data.get('data').get('User')
