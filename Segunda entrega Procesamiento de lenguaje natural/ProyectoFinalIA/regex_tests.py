import pymongo
from pymongo import MongoClient
import re

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.gameDB
games_db = db.games
engines_db = db.engines
companies_db = db.companies

DEMAND = '(que|cuales|liste|deme|muestre)'
WHICH = '(cual(es)?|deme|muestre)'
GAMENAMES = '(juego(s)?|videojuego(s)?)'
PLAYER = '(jugador(es)?|jugadora(s)?)'
COMPANY = '(compania|compa\xA4\xA1)'
DO_PAST = '(hizo|hiz\xA2|creo|cre\xA2|desarrollo|desarroll\xA2)'
HAVE_DONE = 'han (desarrollado|creado|hecho)'
HAVE_PUBLISHED = 'ha(n)? (publicado|revelado|distribuido)'
PUBLISHED = '(publicado(s)?|revelado(s)?|distribuido(s)?)'
RELEASED = '(salio|publico|solto|revelo|libero)\s*'
WHO = '(quien(es)?)'
CREATION = '(desarrollaron|crearon|hicieron)'
WITH = '(con|el|motor de juego)'
BE = '(es(ta(n)?)?|fue|son|era|sera|seran|eran)'
OPT_BE = '('+BE+')?\s*'
ARTICLES = '(el|la|los|las)'
OF = '(de(l)?)'
DATE = '(fecha|ano|a\xA4o)\s*'
COMPOSED_DEMAND = '('+ DEMAND + '|' + WHICH + ')\s*'
RATING = '(clasificacion\s*(de\s*edad)?|calificacion\s*(de\s*edad)?|pegi|rating(s)?)'
def game_engines(string):
    #DONE
    #Que juegos se han hecho con _motor de juego_?
    query = DEMAND + '.*'+CREATION + '.*'+WITH+'\s*(?P<engine>.*)'
    match = re.search(query,string)
    engine = None
    games_result = None
    games_names = None
    if match:
        engine = match.group('engine')
        engine_match = engines_db.find_one({'name': {'$regex': engine}})
        if engine_match:
            id = engine_match['id']
            if (isinstance(id,int)):
                games_result = games_db.find({'game_engines':id})
                games_names = [x['name'] for x in games_result]
    return games_names

def company_created(string):
    #DONE
    #Que compania desarrollo _nombre de juego_
    query = DEMAND + '.*'+ COMPANY +'.*'+DO_PAST+ '\s*(?P<game>.*)'
    query2 = WHO + '\s*' + DO_PAST +'\s*(?P<game>\S)'
    queries = [query, query2]

    game = None
    devnames = None
    for x in queries:
        match = re.search(x, string, re.I)
        if match:
            game = match.group('game')
            break
    if game:
        game_match = games_db.find_one({'name':{'$regex': game}})
        if game_match:
            developers = game_match['developers']
            devobjects = companies_db.find({'id': {'$in': developers}})
            if devobjects:
                devnames = [dev['name'] for dev in devobjects]

    return devnames

def list_company_games(string):
    #JP
    #Que juegos ha hecho _nombre de compania_
    query = DEMAND +'.*'+ GAMENAMES + '.*' + HAVE_DONE + '\s*(?P<company>.*)'
    query2 = '^(?P<company>\S*)'+'\s*'+GAMENAMES+'$'
    queries = [query, query2]
    company = None
    for x in queries:
        match = re.search(x,string, re.I)
        if match:
            company = match.group('company')
    return company
def company_description(string):
    # _Compania_ descripcion
    query = COMPANY + '\s*(?P<company>.*)\s*descripcion$'
    queries = [query]
    company = None
    for x in queries:
        match = re.search(x,string, re.I)
        if match:
            company = match.group('company')
    return company

def ask_genre(string):
    #Que genero es _juego_
    query = DEMAND + '\s*(genero|generos)\s*'+ BE + '\s*(?P<game>.*)'
    query2 = '(?P<game>.*)\s*(genero|generos)$'
    queries = [query,query2]
    game = None
    for x in queries:
        match = re.search(x,string, re.I)
        if match:
            game = match.group('game')
    return game

def ask_platforms(string):
    query = 'en\s*' + DEMAND + '\s*(plataforma|plataformas)\s*' + BE + '\s*(?P<game>.*)$'
    query2 = '(?P<game>.*)\s*(plataforma|plataformas)$'
    queries = [query,query2]
    game = None
    for x in queries:
        match = re.search(x,string, re.I)
        if match:
            game = match.group('game')
    return game
def list_company_published_games(string):
    query = DEMAND + '\s*'+ GAMENAMES + '\s*' +HAVE_PUBLISHED + '\s*(?P<company>.*)$'
    query2 = '(?P<company>.*)\s*' + GAMENAMES + '\s*' + PUBLISHED +'$'
    queries = [query,query2]
    for x in queries:
        match = re.search(x,string, re.I)
        if match:
            company = match.group('company')
            return company
    return None
def game_keywords(string):
    query = COMPOSED_DEMAND + OPT_BE + ARTICLES + '\s*palabras clave\s*' + OF +'\s*(?P<game>.*)$'
    query2 = '^(?P<game>.*)\s*palabras clave$'
    queries = [query,query2]
    for x in queries:
        match = re.search(x,string, re.I)
        if match:
            game = match.group('game')
            return game
    return None

def game_player_perspectives(string):
    #Cuales son las perspectivas de jugador|juego de __juego__
    query = COMPOSED_DEMAND + OPT_BE + ARTICLES + '\s*(perspectiva(s)?)\s*' + OF + '\s*(' + PLAYER +'|' + GAMENAMES+ ')\s*' + OF + '\s*(?P<game>.*)$'
    query2 = '^(?P<game>.*)\s*(perspectiva(s)?)\s*' + OF +'\s*(' + PLAYER +'|' + GAMENAMES+ ')\s*$'

    queries = [query,query2]
    for x in queries:
        match = re.search(x,string, re.I)
        if match:
            game = match.group('game')
            return game
    return None
def game_modes(string):
    #Cuales son los modos de juego de __juego__
    query = COMPOSED_DEMAND + OPT_BE + ARTICLES + '\s*(modo(s)?)\s*' + OF + '\s*' + GAMENAMES+ '\s*' + OF + '\s*(?P<game>.*)$'
    query2 = '^(?P<game>.*)\s*(modo(s)?)\s*' + OF +'\s*' + GAMENAMES+ '\s*$'
    queries = [query,query2]
    for x in queries:
        match = re.search(x,string, re.I)
        if match:
            game = match.group('game')
            return game

    return None

def game_popularity(string):
    #Cual es la popularidad de __juego__
    query = WHICH +'\s*' + OPT_BE + ARTICLES +'\s*popularidad\s*' + OF + '\s*(?P<game>.*)$'
    query2 = '^(?P<game>.*)\s*popularidad$'
    queries = [query,query2]
    for x in queries:
        match = re.search(x,string, re.I)
        if match:
            game = match.group('game')
            return game
    return None
def game_hypes(string):
    #Cual es el hype de __juego__
    query = WHICH + '\s*'+ OPT_BE + ARTICLES + '\s*hype(s)?\s*' + OF +'\s*(?P<game>.*)$'
    query2 = '^(?P<game>.*)\s*hype(s)?$'
    queries = [query,query2]
    for x in queries:
        match = re.search(x,string, re.I)
        if match:
            game = match.group('game')
            return game
    return None
def game_rating(string):
    #Cual es la clasificacion de __juego__
    query = COMPOSED_DEMAND + OPT_BE + '\s*' + ARTICLES + '\s*' + RATING + '\s*' + OF + '\s*(?P<game>.*)$'
    query2 = '^(?P<game>.*)\s*' + RATING +'$'
    queries = [query,query2]
    for x in queries:
        match = re.search(x,string, re.I)
        if match:
            game = match.group('game')
            return game
    return None
def game_release_year(string):
    #En que fecha salio __juego__
    query = 'en\s*que\s*' + DATE + RELEASED + '\s*(?P<game>.*)$'
    query2 = '^cuando\s*'+ RELEASED +'\s*(?P<game>.*)$'
    queries = [query,query2]
    for x in queries:
        match = re.search(x,string, re.I)
        if match:
            game = match.group('game')
            return game
    return None
def game_most_expected(string):
    #Juegos mas esperados de  __anio__
    query = '(' + WHICH + '\s*' +BE +'\s*'+ARTICLES +'\s*)?' + GAMENAMES +'\s*mas\s*esperado(s)?\s*' + OF + '\s*(?P<year>\d*)'
    queries = [query]
    for x in queries:
        match = re.search(x,string, re.I)
        if match:
            year = match.group('year')
            return year
    return None
def game_bestof_year(string):
    # Mejores juegos de __anio__
    query = '(' + WHICH + '\s*' +BE +'\s*'+ARTICLES +'\s*)?'+ 'mejor(es)?\s*' + GAMENAMES + '\s*'+ OF + '\s*(?P<year>\d*)'
    queries = [query]
    for x in queries:
        match = re.search(x,string, re.I)
        if match:
            year = match.group('year')
            return year
    return None
def game_mostpopularof_year(string):
    #Juegos mas populares de __anio__
    query = '(' + WHICH + '\s*' +BE +'\s*'+ARTICLES +'\s*)?'+ GAMENAMES + '\s*mas\s*popular(es)?\s*'+ OF + '\s*(?P<year>\d*)'
    queries = [query]
    for x in queries:
        match = re.search(x,string, re.I)
        if match:
            year = match.group('year')
            return year
    return None
def main():
    strings = [ 'que compania hizo league of legends',
                'Overwatch genero',
                'en que plataforma esta PES 2019',
                'Compania Ubisoft Montreal descripcion',
                'que juegos ha publicado Ubisoft',
                'Cuando salio Super Mario Bros',
                'juegos mas populares de 2018']
    functions = [game_engines, company_created, list_company_games, ask_genre, ask_platforms, company_description, list_company_published_games, game_keywords, game_player_perspectives, game_modes, game_popularity, game_hypes, game_rating, game_release_year, game_most_expected, game_bestof_year, game_mostpopularof_year]

    #print game_engines(strings[0])
    # print company_created(strings[1])
    # print strings[2]
    # print list_company_games(strings[2])
    # print list_company_games(strings[0])
    # print ask_genre(strings[3])
    # print ask_platforms(strings[4])
    # print company_description(strings[5])
    for function in functions:
        for string in strings:
            result = function(string)
            if result:
                print "----------------------\n", string, "\n",# function
                if (isinstance(result,list)):
                    for x in result:
                        print x
                else:
                    print result, "\n\n"


if __name__ == '__main__':
    main()
