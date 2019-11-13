from regexModule import RegexMod
from mongoQueryModule import MongoQueryMod
from voiceInputModule import VoiceInMod
from voiceOutputModule import VoiceOutMod
import sys, time

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

strings = [ 'que compania hizo league of legends',
            'Overwatch genero',
            'en que plataforma esta PES 2019',
            'Compania Ubisoft Montreal descripcion',
            'que juegos ha publicado Ubisoft',
            'Cuando salio Super Mario Bros',
            'juegos mas populares de 2018']

rm = RegexMod()
mq = MongoQueryMod()
VM = VoiceInMod()
VO = VoiceOutMod()
def main():
    listening = 1
    while (listening):
        print 'Escuchando...'
        question = VM.get_voice()
        if question:
            question.decode('utf-8')
            print 'Entrada de voz: ', color.PURPLE + question + color.END
            if question == 'salir' or question == 'Salir':
                sys.exit()
            query = rm.get_query(question)
            if query:
                ans = mq.get_data(query)
                if ans:
                    VO.speak(ans)
                    # time.sleep(2)
                    main()
            else:
                print color.RED + 'No encuentra resultados en DB' + color.END

main()
