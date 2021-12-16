import requests as http
from os.path import dirname ,join
import getopt , json , sys


DATA_PATH = join(dirname(__file__),"data")
JAVA_SERVER = 'http://localhost:8080'


def get_data_from_file(filename):
    with open(join(DATA_PATH,filename) , 'r') as f :
        return json.load(f)

def insert_studios(studios,token):
    endpoint = JAVA_SERVER +''
    for line in studios :
        http.post(endpoint , data=line , headers= {"Autorization" : "Bearer " + token} )


def insert_actors(actors,token):
    endpoint = JAVA_SERVER +''
    for line in actors :
        http.post(endpoint , data=line , headers= {"Autorization" : "Bearer " + token} )
    

def insert_genres(genres,token):
    endpoint = JAVA_SERVER +''
    for line in genres :
        http.post(endpoint , data=line , headers= {"Autorization" : "Bearer " + token} )

def insert_films_and_associated_items(films,token):
    endpoint = JAVA_SERVER +''
    for line in films :
        http.post(endpoint , data=line , headers= {"Autorization" : "Bearer " + token} )


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

        insert_genres(genres)
        insert_studios(studios)
        insert_actors(actors)
        insert_films_and_associated_items(films)
    else:
        print("Ajoutez un token avec la commande -t ou --token ")



if __name__ == '__main__':
    main(sys.argv[1:])