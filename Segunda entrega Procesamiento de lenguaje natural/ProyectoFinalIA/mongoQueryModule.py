# -*- coding: utf-8 -*
import pymongo
import datetime
import unicodedata
# from googletrans import Translator
from pymongo import MongoClient
# translator = Translator()
from py_translator import Translator
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.gameDB
games_db = db.games
engines_db = db.engines
companies_db = db.companies
genres_db = db.genres
platforms_db = db.platforms
keywords_db = db.keywords
perspectives_db = db.perspectives
game_modes_db = db.modes

def get_epochs(year):
    timedate = datetime.datetime.strptime(str(year), '%Y').date()
    epoch_year = int(timedate.strftime('%s'))
    ny = str(year+1)
    ny_timedate = datetime.datetime.strptime(ny, '%Y').date()
    epoch_next_year = int(ny_timedate.strftime('%s'))
    return [epoch_year*1000, epoch_next_year*1000]

class MongoQueryMod():
    def game_engines(self, args = {}):
        '''Describe las busquedas relacionadas con el motor de juego\n
        Que juegos se han hecho con _motor de juego_?'''
        engine = args['engine']
        if engine:
            engine_match = engines_db.find_one({'name': {'$regex':engine, '$options':'i'}})
            if engine_match:
                id = engine_match['id']
                if (isinstance(id,int)):
                    games_result = games_db.find({'game_engines':id}).sort('total_rating', -1)
                    if games_result:
                        games_names = [x['name'] for x in games_result]
                        ans = ['Con el motor de juego ' + engine + ' se han creado:'] + games_names
                        return ans
                    else:
                        print 'No se encontraron resultados'
            else:
                print 'No se encontro el motor '+ engine
        else:
            print 'No se envio el parametro engine'
        return [] # Si no encuentra nada devuelve una lista vacia

    def company_created(self, args = {}):
        '''Que compania desarrollo el juego?'''
        game = args['game']
        if game:
            game_match = games_db.find_one({'name':{'$regex': game, '$options':'i'}})
            if game_match:
                print 'Buscando la compania que desarrollo', game_match['name']
                if game_match.has_key('developers'):
                    developers = game_match['developers']
                    devobjects = companies_db.find({'id': {'$in': developers}})
                    if devobjects:
                        devnames = [dev['name'] for dev in devobjects]
                        ans = [game_match['name'] + ' fue desarrollado por: '] + devnames
                        return ans
                    else:
                        print "No se encontraron desarrolladores"
                else:
                    print 'El juego no cuenta con info del desarrollador'
            else:
                print "No se encontro el juego"
        else:
            print 'No se envio el parametro juego'
        return []

    def list_company_games(self, args = {}):
        '''Que juegos ha hecho x compania'''
        company = args['company']
        if company:
            company_match = companies_db.find_one({'name':{'$regex': company, '$options':'i'}})
            if company_match:
                print 'Buscando los juegos desarrollados por', company_match['name'] 
                if company_match.has_key('developed'):
                    games_id = company_match['developed']
                    games_objects = games_db.find({'id': {'$in': games_id}, 'total_rating': {'$exists': True}}).sort('total_rating', -1)
                    if games_objects:
                        game_names = [game['name'] for game in games_objects]
                        ans = [company_match['name'] + ' ha desarrollado '] + game_names
                        return ans
                    else:
                        print 'No se encontraron juegos'
                else:
                    print 'No se encontro informacion de juegos desarrollados por este estudio'                    
        else:
            print 'No se encontro la compania'
        return []

    def company_description(self, args = {}):
        '''Compania descripcion'''
        company = args['company']
        if company:
            company_match = companies_db.find_one({'name':{'$regex': company, '$options':'i'}})
            if company_match:
                print 'Buscando la descipcion de', company_match['name']
                if company_match.has_key('description'):                    
                    unicode_desc = company_match['description']
                    desc = unicodedata.normalize('NFKD', unicode_desc).encode('ascii','ignore')
                    ans = [company_match['name'] + ': '] + [desc]
                    return ans
                else:
                    print 'No se encontro la descripcion'
            else:
                # si no se encuentra el nombre en la primera busqueda se vuelve a buscar cortando la 'ultima letra
                if (len(company) > 3):
                    args['company'] = args['company'][0:len(company)-1]
                    self.company_description(args)
                else:
                    print 'No se encontro la compania'
        return []
    
    def ask_genre(self, args = {}):
        '''Que genero es _juego_'''
        game = args['game']
        if game:
            game_match = games_db.find_one({'name':{'$regex': game, '$options':'i'}})
            if game_match:
                print 'Buscando generos de', game_match['name']
                if game_match.has_key('genres'):
                    genres_id = game_match['genres']
                    genres_obj = genres_db.find({'id': {'$in': genres_id}})
                    if genres_obj:
                        genre_names = [genre['name'] for genre in genres_obj]
                        return genre_names
                    else:
                        print 'No se encontraron generos'
                else:
                    print 'El juego no cuenta con info de su genero'
            else:
                print "No se encontro el juego"
        else:
            print 'No se envio el parametro juego'
        return []
    
    def ask_platforms(self, args = {}):
        '''En que plataforma esta hecho x juego'''
        game = args['game']
        if game:
            game_match = games_db.find_one({'name':{'$regex': game, '$options':'i'}})
            if game_match:
                print 'Buscando plataformas de', game_match['name']
                if game_match.has_key('platforms'):
                    platforms_id = game_match['platforms']
                    platforms_obj = platforms_db.find({'id': {'$in': platforms_id}})
                    if platforms_obj:
                        platforms_names = [plat['name'] for plat in platforms_obj]
                        ans = [game_match['name'] + ' fue creado para las plataformas: '] + platforms_names
                        return ans
                    else:
                        print 'No se encontraron las plataformas'
                else:
                    print 'El juego no cuenta con info de sus plataformas'
            else:
                print "No se encontro el juego"
        else:
            print 'No se envio el parametro juego'
        return []

    def list_company_published_games(self, args = {}):
        '''Que juegos ha publicado x\n ubisoft juegos publicados'''
        company = args['company']
        # aqui hay algo raro
        if company:
            company_match = companies_db.find_one({'name':{'$regex': company, '$options':'i'}})
            if company_match:
                print 'Buscando los juegos publicados de', company_match['name']
                if company_match.has_key('published'):
                    games_id = company_match['published']
                    games_objects = games_db.find({'id': {'$in': games_id}, 'total_rating': {'$exists': True}}).sort('total_rating', -1)
                    if games_objects:
                        game_names = [game['name'] for game in games_objects]
                        ans = [company_match['name'] + ' ha publicado '] + game_names
                        return ans
                    else:
                        print 'No se encontraron juegos'
                else:
                    print 'No se encontro informacion de juegos publicados por este estudio'   
            else:
                print 'Buscando de nuevo'
                if (len(company) > 3):
                    args['company'] = args['company'][0:len(company)-1]
                    self.list_company_published_games(args)
                else:
                    print 'No se encontro la compania'                 
        else:
            print 'No se encontro la compania'
        return []
    
    def game_keywords(self, args = {}):
        '''Cuales son las palabras clave de x'''
        game = args['game']
        if game:
            game_match = games_db.find_one({'name':{'$regex': game, '$options':'i'}})
            if game_match:
                print 'Buscando palabras clave de', game_match['name']
                if game_match.has_key('keywords'):
                    keywords_id = game_match['keywords']
                    keywords_obj = keywords_db.find({'id': {'$in': keywords_id}})
                    if keywords_obj:
                        keywords_names = [plat['name'] for plat in keywords_obj]
                        if len(keywords_names) > 1:
                            ans = ['Las palabras clave de ' + game_match['name'] + ' son: '] + keywords_names
                            return ans
                    else:
                        print 'No se encontraron las palabras clave'
                else:
                    print 'El juego no cuenta con info de sus palabras clave'
            else:
                print "No se encontro el juego"
        else:
            print 'No se encio el parametro juego'
        return []
    
    def game_player_perspectives(self, args = {}):
        '''Cuales son las perspectivas de _juego_'''
        game = args['game']
        if game:
            game_match = games_db.find_one({'name':{'$regex': game, '$options':'i'}})
            if game_match:
                print 'Buscando perspectivas de', game_match['name']
                if game_match.has_key('player_perspectives'):
                    perspectives_id = game_match['player_perspectives']
                    perspectives_obj = perspectives_db.find({'id': {'$in': perspectives_id}})
                    if perspectives_obj:

                        perspectives_names = [plat['name'] for plat in perspectives_obj]
                        per = 'Las pérspectivas de '.decode('utf-8')
                        ans = [per + game_match['name'] + ' son'] + perspectives_names
                        return ans
                    else:
                        print 'No se encontraron las perspectivas de juego'
                else:
                    print 'El juego no cuenta con info de sus perspectivas de juego'
            else:
                print "No se encontro el juego"
        else:
            print 'No se envio el parametro juego'
        return []

    def game_modes(self, args = {}):
        '''cuales son los modos de juego de _juego_'''
        game = args['game']
        if game:
            game_match = games_db.find_one({'name':{'$regex': game, '$options':'i'}})
            if game_match:
                print 'Buscando modos de juego de', game_match['name']
                if game_match.has_key('game_modes'):
                    game_modes_id = game_match['game_modes']
                    game_modes_obj = game_modes_db.find({'id': {'$in': game_modes_id}})
                    if game_modes_obj:
                        game_modes_names = [plat['name'] for plat in game_modes_obj]
                        return ['Los modos de juego de ' + game_match['name'] + ' son: '] + game_modes_names
                    else:
                        print 'No se encontraron los modos de juego'
                else:
                    print 'El juego no cuenta con info de sus modoss de juego'
            else:
                print "No se encontro el juego"
        else:
            print 'No se envio el parametro juego'
        return []

    def game_popularity(self, args = {}):
        '''popularidad de _juego_'''
        game = args['game']
        if game:
            game_match = games_db.find_one({'name':{'$regex': game, '$options':'i'}})
            if game_match:
                print 'Buscando popularidad de', game_match['name']
                if game_match.has_key('popularity'):
                    pop = ['La popularidad de ' + game_match['name'] + ' es de: ' + "{0:.3f}".format(game_match['popularity'])]
                    return pop
                else:
                    print 'El juego no cuenta con info de su popularidad'
            else:
                print "No se encontro el juego"
        else:
            print 'No se envio el parametro juego'
        return []

    def game_hypes(self, args = {}):
        '''hypes de _juego_'''
        game = args['game']
        if game:
            game_match = games_db.find_one({'name':{'$regex': game, '$options':'i'}})
            if game_match:
                print 'Buscando hypes de', game_match['name']
                if game_match.has_key('hypes'):
                    hype = ['El hype de ' + game_match['name'] + ' es de: ' + "{0:.3f}".format(game_match['hypes'])]
                    return hype
                else:
                    print 'El juego no cuenta con info de su hype'
            else:
                print "No se encontro el juego"
        else:
            print 'No se envio el parametro juego'
        return []

    def game_rating(self, args = {}):
        '''rating de _juego_'''
        game = args['game']
        if game:
            game_match = games_db.find_one({'name':{'$regex': game, '$options':'i'}})
            if game_match:
                print 'Buscando rating de', game_match['name']
                if game_match.has_key('total_rating'):
                    val ='La valoración de '.decode('utf-8')
                    rat = [val + game_match['name'] + ' es de: ' + "{0:.3f}".format(game_match['total_rating'])]
                    return rat
                else:
                    print 'El juego no cuenta con info de su valoracion'
            else:
                print "No se encontro el juego"
        else:
            print 'No se envio el parametro juego'
        return []

    def game_release_date(self, args = {}):
        '''cuando salio _juego_'''
        game = args['game']
        if game:
            game_match = games_db.find_one({'name':{'$regex': game, '$options':'i'}})
            if game_match:
                print 'Buscando release date de ', game_match['name']
                if game_match.has_key('first_release_date'):
                    epoch = game_match['first_release_date']/1000
                    rel = datetime.datetime.fromtimestamp(
                        epoch
                    ).strftime('%Y, %m, %d')
                    rel = ['Fecha de salida de ' + game_match['name'] + ': ' + str(rel)]
                    return rel
                else:
                    print 'El juego no cuenta con info de su valoracion'
            else:
                print "No se encontro el juego"
        else:
            print 'No se envio el parametro juego'
        return []
    
    def game_most_expected(self, args = {}):
        '''Juego mas esperado de _anio_'''
        year = int(args['year']) #Esto lleva un procesamiento adicional cuando se vaya a hacer el input de voz
        epochs = get_epochs(year)
        if year:
            games_query = games_db.find({'$and': [
                {'first_release_date': {'$gte': epochs[0]}},
                {'first_release_date': {'$lte': epochs[1]}}
                ], 'hypes': {'$exists': True}}).sort('hypes', -1)
            if games_query:
                game_names = []
                for g in games_query:
                    if g.has_key('hypes'):
                        unicode_name = g['name']
                        name = unicodedata.normalize('NFKD', unicode_name).encode('ascii','ignore')
                        game_names.append(name + ', con: ' + str(g['hypes']))  
                ppt = ['Los juegos mas esperados de ' + str(year) + ' fueron:']
                ans = ppt + game_names[0:5]
                return ans
            else:
                print 'No se encontraron juegos para esta fecha'
        else:
            print 'No se envio el parametro year'
        return []

    def game_bestof_year(self, args = {}):
        '''mejores juegos de _year_'''
        year = int(args['year']) #Esto lleva un procesamiento adicional cuando se vaya a hacer el input de voz
        epochs = get_epochs(year)
        if year:
            games_query = games_db.find({'$and': [
                {'first_release_date': {'$gte': epochs[0]}},
                {'first_release_date': {'$lte': epochs[1]}}
                ], 'total_rating': {'$exists': True}}).sort('total_rating', -1)
            if games_query:
                game_names = []
                for g in games_query:
                    if g.has_key('total_rating'):
                        unicode_name = g['name']
                        name = unicodedata.normalize('NFKD', unicode_name).encode('ascii','ignore')
                        game_names.append(name + ' con ' + "{0:.3f}".format(g['total_rating']))  
                ppt = ['Los mejores juegos de ' + str(year) + ' fueron:']
                ans = ppt + game_names[0:5]
                return ans
            else:
                print 'No se encontraron juegos para esta fecha'
        else:
            print 'No se envio el parametro year'
        return []
    
    def game_mostpopularof_year(self, args = {}):
        '''juegos mas populares de _year_'''
        year = int(args['year']) #Esto lleva un procesamiento adicional cuando se vaya a hacer el input de voz
        epochs = get_epochs(year)
        if year:
            games_query = games_db.find({'$and': [
                {'first_release_date': {'$gte': epochs[0]}},
                {'first_release_date': {'$lte': epochs[1]}}
                ], 'popularity': {'$exists': True}}).sort('popularity', -1)
            if games_query:
                game_names = []
                for g in games_query:
                    if g.has_key('popularity'):
                        unicode_name = g['name']
                        name = unicodedata.normalize('NFKD', unicode_name).encode('ascii','ignore')
                        game_names.append(name + ', con: ' + "{0:.3f}".format(g['popularity']))  
                ppt = ['Los juegos mas populares de ' + str(year) + ' fueron:']
                ans = ppt + game_names[0:5]
                return ans
            else:
                print 'No se encontraron juegos para esta fecha'
        else:
            print 'No se envio el parametro year'
        return []

    def get_string(self, data):
        if len(data) > 0:
            string = ''
            print 'Se encontraron ' + str(len(data)) + ' resultado/s.\n'
            for d in data[0:10]:
                string += d
                string += '\n'  
        else:
            string = 'No se encontraron resultados'
        return string

    def get_data(self, ans):
        print "...Getting data...\n"
        print "string for voiceOutputMod"
        args = ans.args
        func_dict = {
            1: self.game_engines,
            2: self.company_created,
            3: self.list_company_games,
            4: self.company_description,
            5: self.ask_genre,
            6: self.ask_platforms,
            7: self.list_company_published_games,
            8: self.game_keywords,
            9: self.game_player_perspectives,
            10: self.game_modes,
            11: self.game_popularity,
            12: self.game_hypes,
            13: self.game_rating,
            14: self.game_release_date,
            15: self.game_most_expected,
            16: self.game_bestof_year,
            17: self.game_mostpopularof_year,
        }
        data = func_dict[ans.IdMongoQuery](ans.args)
        string = self.get_string(data)
        return string
