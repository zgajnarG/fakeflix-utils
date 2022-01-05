import requests as http
from os.path import dirname ,join
import getopt , json , sys


DATA_PATH = join(dirname(__file__),"data")
JAVA_SERVER = 'http://localhost:8080'


def get_data_from_file(filename):
    with open(join(DATA_PATH,filename) , 'r') as f :
        return json.load(f)

def insert_studios(studios,token):

    success = 0
    error = 0

    endpoint = JAVA_SERVER +'/distribution'
    for line in studios :
        response =  http.post(endpoint , data= json.dumps(line) , headers= {"Authorization" : "Bearer " + token , "content-type" : "application/json"} )

        if response.status_code == 200 :
            success +=1
        else:
            print(response.content)
            error +=1
    print('Studios : ' + str(success) +' success et '+ str(error) +' error')


def insert_actors(actors,token):
    
    success = 0
    error = 0
    endpoint = JAVA_SERVER +'/person'
    for line in actors :
        response =  http.post(endpoint , data= json.dumps(line) , headers= {"Authorization" : "Bearer " + token , "content-type" : "application/json"} )

        if response.status_code == 200 :
            success +=1
        else:
            print(response.status_code)
            error +=1

    print('Actors : ' + str(success) +' success et '+ str(error) +' error')
    

def insert_genres(genres,token):
      
    success = 0
    error = 0
    endpoint = JAVA_SERVER +'/categorie'
    for line in genres :
        response =  http.post(endpoint , data= json.dumps(line) , headers= {"Authorization" : "Bearer " + token , "content-type" : "application/json"} )

        if response.status_code == 200 :
            success +=1
        else:
            error +=1
    print('Genres : ' + str(success) +' success et '+ str(error) +' error')

def insert_films_and_associated_items(films,token):
    success = 0
    error = 0
    endpoint = JAVA_SERVER +'/film'
    for line in films :
        data = { "id" : line["id"],"nom" :line["nom"] , "annee" :line["annee"] , "description" :line["description"] , "score" :line["score"] , "categoryAge":line["categoryAge"] , "urlImageFilm" : line["urlImageFilm"]}
        response =  http.put(endpoint , data= json.dumps(data) , headers= {"Authorization" : "Bearer " + token , "content-type" : "application/json"})

        if response.status_code == 200 :
            insert_film_categories(line,token)
            insert_film_participation(line,token)
            success +=1
        else:
            error +=1
    print('Films : ' + str(success) +' success et '+ str(error) +' error')

def insert_film_categories(film,token):
    success = 0
    error = 0
  
    for categorie in film['filmCategories']:
        endpoint = JAVA_SERVER +'/film/'+str(film["id"])+'/categorie/'+str(categorie["id"])
        responsecategorie = http.post(endpoint, headers= {"Authorization" : "Bearer " + token , "content-type" : "application/json"})
        if responsecategorie.status_code == 200 :
            success +=1
        else :
            error +=1

def insert_film_participation(film,token):
    success = 0
    error = 0
    for participation in film['participants']:
        if participation['role'] == "Acting" or participation['role'] == "Directing" :
            data = {"filmId" : film["id"] , "personneId" : participation["id"] , "role" : participation["role"].upper()}
            endpoint = JAVA_SERVER +"/participation"
            responsecategorie = http.post(endpoint, data= json.dumps(data)  , headers= {"Authorization" : "Bearer " + token , "content-type" : "application/json"})
            if responsecategorie.status_code == 200 :
                success +=1
            else :
                error +=1

def get_token(argv):
    opts, args = getopt.getopt(argv,"p:t:",["ifile=","ofile="])
    for key, value in opts:
        if key == '-t' or key == '--token':
            return value
    return None


def main(argv):

    token = get_token(argv)

    if token is not None:
        actors = get_data_from_file('actors.json')
        studios = get_data_from_file('distributions.json')
        genres = get_data_from_file('genres.json')
        films = get_data_from_file('films.json')

        insert_genres(genres,token)
        insert_studios(studios,token)
        insert_actors(actors,token)
        insert_films_and_associated_items(films,token)
    else:
        print("Ajoutez un token avec la commande -t ou --token ")



if __name__ == '__main__':
    main(sys.argv[1:])