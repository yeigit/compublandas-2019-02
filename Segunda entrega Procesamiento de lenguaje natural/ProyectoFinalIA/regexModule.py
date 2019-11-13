import re

DEMAND = '(que|cuales|liste|deme|muestre)'
WHICH = '(cual(es)?|deme|muestre)'
GAMENAMES = '(juego(s)?|videojuego(s)?)'
PLAYER = '(jugador(es)?|jugadora(s)?)'
COMPANY = '(compania|compa\xA4\xA1)'
DO_PAST = '(ISO|hizo|hiz\xA2|creo|cre\xA2|desarrollo|desarroll\xA2)'
HAVE_DONE = '(han|ha) (desarrollado|creado|hecho)'
HAVE_PUBLISHED = 'ha(n)? (publicado|revelado|distribuido)'
PUBLISHED = '(publicado(s)?|revelado(s)?|distribuido(s)?)'
RELEASED = '(salio|publico|solto|revelo|libero)\s*'
WHO = '(quien(es)?)'
CREATION = '(desarrollaron|crearon|hicieron|(se)?\s?(han)?\s?(hecho|creado|desarrollado))'
WITH = '(con|el|motor de juego)'
BE = '(es(ta(n)?)?|fue|son|era|sera|seran|eran)'
OPT_BE = '('+BE+')?\s*'
ARTICLES = '(el|la|los|las)'
OF = '(de(l)?)'
DATE = '(fecha|ano|a\xA4o)\s*'
COMPOSED_DEMAND = '('+ DEMAND + '|' + WHICH + ')\s*'
PEGI = '(clasificacion\s*(de\s*edad)?|calificacion\s*(de\s*edad)?|pegi|rating(s)?)'
RATING = '(valoracion|calificacion|rating(s)?)'

class Ans():
    # Formato para la respuesta que dara el modulo
    def __init__(self, IdMongoQuery, args = {}):
        self.IdMongoQuery = IdMongoQuery # Id de la query del modulo mongoQueryMod
        self.args = args # Diccionario con argumentos y su valor

class RegexMod():
    def game_engines(self, string):
        #DONE
        #Que juegos se han hecho con _motor de juego_?
        query = DEMAND+ '.*'+CREATION+ '.*'+WITH+'\s*(?P<engine>.*)'
        queries = [query]
        for x in queries:
            match = re.search(x,string)
            if match:
                # print '...',match.group('engine')
                engine = match.group('engine')
                # Devuelve un id de la query de mongo (para el sgte modulo) y
                # los parametros que va a recibir el siguiente modulo
                # Ej ans = {idmongo: 1, args: {'engine: 'unreal engine'} }
                ans = Ans(1, {'engine':engine})
                return ans
        return None

    def company_created(self, string):
        #DONE
        #Que compania desarrollo _nombre de juego_
        query = DEMAND + '.*'+ COMPANY +'.*'+DO_PAST+ '\s*(?P<game>.*)'
        query2 = WHO + '\s*' + DO_PAST +'\s*(?P<game>.*)$'
        queries = [query, query2]
        for x in queries:
            match = re.search(x, string, re.I)
            if match:
                game = match.group('game')
                ans = Ans(2, {'game': game})
                return ans
        return None

    def list_company_games(self, string):
        #JP
        #Que juegos ha hecho _nombre de compania_
        query = DEMAND +'.*?'+ GAMENAMES + '.*' + HAVE_DONE + '\s*(?P<company>.*)'
        query2 = '^(?P<company>\S*)'+'\s*'+GAMENAMES+'$'
        queries = [query, query2]
        for x in queries:
            match = re.search(x,string, re.I)
            if match:
                company = match.group('company')
                ans = Ans(3, {'company': company})
                return ans
        return None

    def company_description(self, string):
        #compania  _Compania_ descripcion
        query = COMPANY + '\s*(?P<company>.*)\s*descripcion$'
        queries = [query]
        for x in queries:
            match = re.search(x,string, re.I)
            if match:
                company = match.group('company')
                ans = Ans(4, {'company': company})
                return ans
        return None

    def ask_genre(self, string):
        #Que genero es _juego_
        query = DEMAND + '\s*(genero|generos)\s*'+ BE + '\s*(?P<game>.*)$'
        query2 = '(?P<game>.*)\s*(genero|generos)$'
        query3 = 'genero(s)? de(l)?\s*( juego)?(?P<game>.*)$'
        queries = [query, query2, query3]
        for x in queries:
            match = re.search(x,string, re.I)
            if match:
                game = match.group('game')
                ans = Ans(5, {'game': game})
                return ans
        return None

    def ask_platforms(self, string):
        '''En cual plataforma esta x juego'''
        query = '(en\s*)' + DEMAND + '\s*(plataforma|plataformas)\s*' + BE + '\s*(?P<game>.*)$'
        query2 = '(?P<game>.*)\s*(plataforma|plataformas)$'
        queries = [query,query2]
        for x in queries:
            match = re.search(x,string, re.I)
            if match:
                game = match.group('game')
                ans = Ans(6, {'game': game})
                return ans
        return None

    def list_company_published_games(self, string):
        query = '(' + DEMAND + '|' + WHICH +')' + '\s*' + GAMENAMES + '\s*' +HAVE_PUBLISHED + '\s*(?P<company>.*)$'
        query2 = '(?P<company>.*)\s*' + GAMENAMES + '\s*' + PUBLISHED +'$'
        queries = [query,query2]
        for x in queries:
            match = re.search(x,string, re.I)
            if match:
                company = match.group('company')
                ans = Ans(7, {'company': company})
                return ans
        return None

    def game_keywords(self, string):
        #Cuales son las palabras clave de __juego__
        query = '(' + COMPOSED_DEMAND + OPT_BE + ARTICLES + ')?' + '\s*palabra(s)? clave(s)?\s*' + OF +'\s*(?P<game>.*)$'
        query2 = '^(?P<game>.*)\s*palabras clave$'
        queries = [query,query2]
        for x in queries:
            match = re.search(x,string, re.I)
            if match:
                game = match.group('game')
                ans = Ans(8, {'game': game})
                return ans
        return None

    def game_player_perspectives(self, string):
        '''_juego_ perspectivas'''
        query = '(' + COMPOSED_DEMAND + OPT_BE + ARTICLES + ')?' + '\s*(perspectiva(s)?)\s*' + OF + '\s*(' + PLAYER +'|' + GAMENAMES+ ')?\s*' + '(' + OF + ')?' + '\s*(?P<game>.*)$'
        query2 = '^(?P<game>.*)\s*(perspectiva(s)?)\s*' + OF +'\s*(' + PLAYER +'|' + GAMENAMES+ ')\s*$'
        query3 = DEMAND + '\s*' + BE + '\s*(las perspectivas )' + OF + '\s*(juego de )?((?P<game>.*))$'
        queries = [query, query2, query3]
        for x in queries:
            match = re.search(x,string, re.I)
            if match:
                game = match.group('game')
                ans = Ans(9, {'game': game})
                return ans
        return None

    def game_modes(self, string):
        #Cuales son los modos de juego de __juego__
        query = '(' + COMPOSED_DEMAND + OPT_BE + ARTICLES + ')?' + '\s*(modo(s)?)\s*' + OF + '\s*' + GAMENAMES+ '\s*' + OF + '\s*(?P<game>.*)$'
        query2 = '^(?P<game>.*)\s*(modo(s)?)\s*' + OF +'\s*' + GAMENAMES+ '\s*$'
        queries = [query, query2]
        for x in queries:
            match = re.search(x,string, re.I)
            if match:
                game = match.group('game')
                ans = Ans(10, {'game' : game})
                return ans
        return None
    def game_popularity(self, string):
        #Cual es la popularidad de __juego__
        query =  '(' + WHICH +'\s*' + OPT_BE + ARTICLES + ')?' +'\s*popularidad\s*' + OF + '\s*(?P<game>.*)$'
        query2 = '^(?P<game>.*)\s*popularidad$'
        queries = [query,query2]
        for x in queries:
            match = re.search(x,string, re.I)
            if match:
                game = match.group('game')
                ans = Ans(11, {'game' : game})
                return ans
        return None

    def game_hypes(self, string):
        #Cual es el hype de __juego__
        query = WHICH + '\s*'+ OPT_BE + ARTICLES + '\s*hype(s)?\s*' + OF +'\s*(?P<game>.*)$'
        query2 = '^(?P<game>.*)\s*hype(s)?$'
        query3 = '^hype(s)?\s*' + OF +'\s*(?P<game>.*)$'
        queries = [query, query2, query3]
        for x in queries:
            match = re.search(x,string, re.I)
            if match:
                game = match.group('game')
                ans = Ans(12, {'game' : game})
                return ans
        return None

    def game_rating(self, string):
        #Cual es la clasificacion de __juego__
        query = COMPOSED_DEMAND + OPT_BE + '\s*' + ARTICLES + '\s*' + RATING + '\s*' + OF + '\s*(?P<game>.*)$'
        query2 = '^(?P<game>.*)\s*' + RATING +'$'
        query3 = RATING + '\s*' + OF + '\s*(?P<game>.*)$'
        queries = [query, query2, query3]
        for x in queries:
            match = re.search(x,string, re.I)
            if match:
                game = match.group('game')
                ans = Ans(13, {'game' : game})
                return ans
        return None
    
    def game_release_year(self, string):
        #En que fecha salio __juego__
        query = 'en\s*que\s*' + DATE + RELEASED + '\s*(?P<game>.*)$'
        query2 = '^cuando\s*'+ RELEASED +'\s*(?P<game>.*)$'
        queries = [query,query2]
        for x in queries:
            match = re.search(x,string, re.I)
            if match:
                game = match.group('game')
                ans = Ans(14, {'game' : game})
                return ans
        return None

    def game_most_expected(self, string):
        #Juegos mas esperados de  __anio__
        query = '(' + WHICH + '\s*' +BE +'\s*'+ARTICLES +'\s*)?' + GAMENAMES +'\s*mas\s*esperado(s)?\s*' + OF + '\s*(?P<year>\d*)'
        queries = [query]
        for x in queries:
            match = re.search(x,string, re.I)
            if match:
                year = match.group('year')
                ans = Ans(15, {'year' : year})
                return ans
        return None

    def game_bestof_year(self, string):
        # Mejores juegos de __anio__
        query = '(' + WHICH + '\s*' +BE +'\s*'+ARTICLES +'\s*)?'+ 'mejor(es)?\s*' + GAMENAMES + '\s*'+ OF + '\s*(?P<year>\d*)'
        queries = [query]
        for x in queries:
            match = re.search(x,string, re.I)
            if match:
                year = match.group('year')
                ans = Ans(16, {'year' : year})
                return ans
        return None

    def game_mostpopularof_year(self, string):
        #Juegos mas populares de __anio__
        query = '(' + WHICH + '\s*' +BE +'\s*'+ARTICLES +'\s*)?'+ GAMENAMES + '\s*mas\s*popular(es)?\s*'+ OF + '\s*(?P<year>\d*)'
        queries = [query]
        for x in queries:
            match = re.search(x,string, re.I)
            if match:
                year = match.group('year')
                ans = Ans(17, {'year' : year})
                return ans
        return None
    #TODO Propuestas de preguntas importantes
    #popularidad de _juego_
    #historia de _juego_



    def get_query(self, question):
        functions = [self.game_engines,
            self.company_created,
            self.list_company_games,
            self.ask_genre,
            self.ask_platforms,
            self.company_description,
            self.ask_genre,
            self.ask_platforms,
            self.list_company_published_games,
            self.game_keywords,
            self.game_player_perspectives,
            self.game_modes,
            self.game_popularity,
            self.game_hypes,
            self.game_rating,
            self.game_release_year,
            self.game_most_expected,
            self.game_bestof_year,
            self.game_mostpopularof_year]
        for f in functions:
            query_id = f(question)
            if query_id:
                # Se envian el objeto para los siguientes modulos,
                # para el ejemplo, solo se imprime
                print '(IdMongoQuery: ', query_id.IdMongoQuery, ', args:', query_id.args, ' )'
                # print '...', query_id.args['engine']
                return query_id
