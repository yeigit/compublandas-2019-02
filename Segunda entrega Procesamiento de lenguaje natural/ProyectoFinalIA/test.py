from regexModule import RegexMod
from mongoQueryModule import MongoQueryMod
from voiceInputModule import VoiceInMod
from voiceOutputModule import VoiceOutMod
import sys

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

if __name__ == "__main__":
    rm = RegexMod()
    mq = MongoQueryMod()
    VM = VoiceInMod()
    VO = VoiceOutMod()
    speak = 1
    if len(sys.argv) > 1:
        question = sys.argv[1]
        if len(sys.argv) > 2:
            speak = sys.argv[2]
    else:
        question = VM.get_voice()
    print 'Entrada de voz: ', color.PURPLE + question + color.END
    print color.BOLD + 'RegexModule' + color.END
    q = rm.get_query(question)
    if q:
        print color.BOLD + 'QueryMongoModule' + color.END
        ans = mq.get_data(q)
        if ans:
            print color.CYAN + ans + color.END
            if speak == 1:
                VO.speak(ans)
    else:
        print color.RED + 'No encontro resultados en DB' + color.END
