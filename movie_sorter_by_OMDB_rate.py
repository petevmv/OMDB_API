import requests_with_caching
import json
# requests_with_caching needs to be implemented first(it can be found in the folder)

def get_movies_from_tastedive(x):
    baseurl = "https://tastedive.com/api/similar"
    params_dict = {}
    params_dict["q"] = x
    params_dict["type"] = "movies"
    params_dict["limit"] = 5
    test_dive_response = requests_with_caching.get(baseurl, params = params_dict)
    #txt = test_dive_response.text
    #js = json.loads(txt)
    #print(json.dumps(txt, indend=4))
    return test_dive_response.json()



def extract_movie_titles(y):
    alist = []
    for i in y['Similar']['Results']:
        alist.append(i['Name'])
    return alist



def get_related_titles(z):
    m_list = []
    for k in z:
        related = get_movies_from_tastedive(k)
        for i in related['Similar']['Results']:
            if i["Name"] not in m_list:
                m_list.append(i['Name'])
    return m_list



def get_movie_data(movie_title):
    baseurl = "http://www.omdbapi.com/"
    info_dict = {}
    info_dict["t"] = movie_title
    info_dict['r'] = 'json'
    omdb_response = requests_with_caching.get(baseurl, params = info_dict)
    #txt = omdb_response.text
    #js = json.loads(txt)
    #print(json.dumps(js, indent=4))
    return omdb_response.json()



def get_movie_rating(mr):
    if len(mr["Ratings"]) > 1:
        rotten = mr["Ratings"][1]
    else:
        return 0

    if rotten["Source"] == "Rotten Tomatoes":
        return (int(rotten['Value'][0:2]))
    else:
        return 0



def get_sorted_recommendations(alist):
    mov = get_related_titles(alist)
    movie_rating = {}
    for movie_name in mov:
        rate = get_movie_rating(get_movie_data(movie_name))
        movie_rating[movie_name] = rate
    return sorted(movie_rating.keys(), key=lambda v: -movie_rating[v])




# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
#get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
