import requests

def deranged_meter(username):
    query = '''
query ($name: String, $page: Int, $perPage: Int) { # Define which variables will be used in the query (id)
      Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            mediaList(userName: $name, type: ANIME, status_in: [COMPLETED, CURRENT], sort: SCORE_DESC)
            {
                score
                media 
                {
                    genres
                    tags
                    {
                        name
                        rank
                    }
                    title 
                    {
                        romaji
                    }
                }
            }
        }
  User(name: $name) {
    avatar {
      medium
    }
  }
}
    '''

    # Define our query variables and values that will be used in the query request
    variables = {
        'name': username,
        'page': 1,
        'perPage': 50
    }

    url = 'https://graphql.anilist.co'

    genres = {
        "Ecchi": 1,
        "Hentai": 2,
        "Horror": 0.5,
        "Thriller": 0.2,
        "Mahou Shoujo": 0.1,
    }

    tags = {
        "Age Gap": 0.6,
        "Primarily Animal Cast": 0.1,
        "Post-Apocalyptic": 0.3,
        "Body Horror": 0.8,
        "Cannibalism": 1.0,
        "Cosmic Horror": 0.2,
        "Death Game": 0.6,
        "Drugs": 0.2,
        "Ero Guro": 1.3,
        "Gambling": 0.1,
        "Gore": 0.6,
        "Slavery": 0.4,
        "Terrorism": 0.3,
        "Torture": 0.7,
        "War": 0.4,
        "Succubus": 0.6,
        "Yandere": 0.8,
        "Dystopian": 0.4,
        "Omegaverse": 3,
        "Suicide": 0.8,
        "Denpa": 0.5,
        "Otaku Culture": 0.2,
        "Male Harem": 0.4,
        "Female Harem": 0.4,
        "Mixed Gender Harem": 0.4,
        "Tragedy": 0.3,
        "Memory Manipulation": 0.2,
        "Incest": 1,
        "Rape": 2,
        "Feet": 0.4,
        "Masochism": 0.6,
        "Nudity": 0.2,
        "Sadism": 0.7,
        "Large Breasts": 0.4,
    }

    # Make the HTTP Api request
    deranged = 0
    count = 0
    nextPage = True
    # derangest = [0, ""] #score, name, user
    avatar = ""
    deranged_list = []
    while nextPage:
        response = requests.post(url, json={'query': query, 'variables': variables})

        if response.status_code != 200:
            print(f"Error fetching users: {response.text}")

        avatar = response.json()["data"]["User"]["avatar"]["medium"]
        #print(response.text)
        #print(response.json()["data"]["Page"]["pageInfo"]["total"])
        for element in response.json()["data"]["Page"]["mediaList"]:
            anime_score = 0
            partial_scores = []
            #print(element["media"]["title"]["romaji"])
            #print(element["media"]["genres"])
            #print(element["media"]["tags"])
            for genre in element["media"]["genres"]:
                if genre in genres:
                    partial_scores.append(genres[genre])
            for tag in element["media"]["tags"]:
                if tag["name"] in tags:
                    temp = tags[tag["name"]]*tag["rank"]/100
                    partial_scores.append(temp)
            partial_scores.sort(reverse=True)
            try:
                anime_score += partial_scores[0]
                anime_score += partial_scores[1]
                anime_score += partial_scores[2]
            except:
                pass
            deranged_list.append((element["media"]["title"]["romaji"], round(anime_score,2)))
            # if anime_score > derangest[0]:
            #     derangest = [round(anime_score,2), element["media"]["title"]["romaji"]]
            deranged += anime_score
            count += 1
            #print(element["media"]["title"]["romaji"] + " " + str(anime_score))
        nextPage = response.json()["data"]["Page"]["pageInfo"]["hasNextPage"]
        variables["page"] += 1
    deranged_list = list(set(deranged_list)) #remove duplicates
    deranged_list.sort(key=lambda tup: -tup[1])
    top = deranged_list[:5]
    return [round(deranged,2), round(deranged/count, 2), top, avatar]
