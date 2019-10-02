:- use_module(library(pce)).
:- pce_image_directory('./imagenes').
:- use_module(library(pce_style_item)).
:- dynamic color/2.


conocimiento('rabia',
['el perro tiene babeo?', 'el perro tiene inquietud?',
'el perro tiene fiebre?','el perro tiene vomito?']).

conocimiento('parvovirosis',
['el perro tiene vomito', 'el perro esta debil?',
'el perro tiene fiebre?','el perro esta deshidratado?']).

conocimiento('moquillo',['el perro tiene descarga nazal?',
'el perro esta deshidratado?', 'el perro tiene diarrea?']).

conocimiento('sarna',
['el perro presenta hongos en la piel?', 'el perro tiene fiebre?',
 'el perro esta deshidratado?','el perro presenta heridas en el cuerpo?']).

conocimiento('otitis',
['el perro presenta heridas en las orejas?', 'el perro tiene fiebre?',
 'el perro esta deshidratado?', 'al perro le sangran las orejas?']).

id_imagen_preg('el perro tiene babeo?','babeo').
id_imagen_preg('el perro tiene inquietud?','inquietud').
id_imagen_preg('el perro tiene fiebre?','fiebre').
id_imagen_preg('el perro tiene vomito?','vomito').
id_imagen_preg('el perro esta devil?','debilidad').
id_imagen_preg('el perro esta deshidratado?','deshidratado').
id_imagen_preg('el perro tiene descarga nazal?','nazal').
id_imagen_preg('el perro tiene diarrea?','diarrea').
id_imagen_preg('el perro presenta hongos en la piel?','hongos').
id_imagen_preg('el perro presenta heridas en el cuerpo?','heridas').
id_imagen_preg('el perro presenta heridas en las orejas?','orejas').
id_imagen_preg('al perro le sangran las orejas','sangre').

:- dynamic conocido/1.

  mostrar_diagnostico(X):-haz_diagnostico(X),clean_scratchpad.
  mostrar_diagnostico(lo_siento_diagnostico_desconocido):-clean_scratchpad .

  haz_diagnostico(Diagnosis):-
                            obten_hipotesis_y_sintomas(Diagnosis, ListaDeSintomas),
                            prueba_presencia_de(Diagnosis, ListaDeSintomas).


obten_hipotesis_y_sintomas(Diagnosis, ListaDeSintomas):-
                            conocimiento(Diagnosis, ListaDeSintomas).


prueba_presencia_de(Diagnosis, []).
prueba_presencia_de(Diagnosis, [Head | Tail]):- prueba_verdad_de(Diagnosis, Head),
                                              prueba_presencia_de(Diagnosis, Tail).


prueba_verdad_de(Diagnosis, Sintoma):- conocido(Sintoma).
prueba_verdad_de(Diagnosis, Sintoma):- not(conocido(is_false(Sintoma))),
pregunta_sobre(Diagnosis, Sintoma, Reply), Reply = 'si'.


pregunta_sobre(Diagnosis, Sintoma, Reply):- preguntar(Sintoma,Respuesta),
                          process(Diagnosis, Sintoma, Respuesta, Reply).


process(Diagnosis, Sintoma, si, si):- asserta(conocido(Sintoma)).
process(Diagnosis, Sintoma, no, no):- asserta(conocido(is_false(Sintoma))).


clean_scratchpad:- retract(conocido(X)), fail.
clean_scratchpad.


conocido(_):- fail.

not(X):- X,!,fail.
not(_).




 resource(img_principal, image, image('img_principal.jpg')).
 resource(portada, image, image('portada.jpg')).


 resource(rabia, image, image('trat_rabia.jpg')).
 resource(parvovirosis, image, image('trat_parvovirosis.jpg')).
 resource(moquillo, image, image('trat_moquillo.jpg')).
 resource(sarna, image, image('trat_sarna.jpg')).
 resource(otitis, image, image('trat_otitis.jpg')).


 resource(lo_siento_diagnostico_desconocido, image, image('desconocido.jpg')).


 resource(babeo, image, image('babeo.jpg')).
 resource(inquietud, image, image('inquietud.jpg')).
 resource(fiebre, image, image('fiebre.jpg')).
 resource(vomito, image, image('vomito.jpg')).
 resource(debilidad, image, image('debilidad.jpg')).
 resource(deshidratado, image, image('deshidratado.jpg')).
 resource(nazal, image, image('nazal.jpg')).
 resource(diarrea, image, image('diarrea.jpg')).
 resource(hongos, image, image('hongos.jpg')).
 resource(heridas, image, image('heridas.jpg')).
 resource(orejas, image, image('orejas.jpg')).
 resource(sangre, image, image('sangre.jpg')).

 mostrar_imagen(Pantalla, Imagen) :- new(Figura, figure),
                                     new(Bitmap, bitmap(resource(Imagen),@on)),
                                     send(Bitmap, name, 1),
                                     send(Figura, display, Bitmap),
                                     send(Figura, status, 1),
                                     send(Pantalla, display,Figura,point(100,80)).
  mostrar_imagen_tratamiento(Pantalla, Imagen) :-new(Figura, figure),
                                     new(Bitmap, bitmap(resource(Imagen),@on)),
                                     send(Bitmap, name, 1),
                                     send(Figura, display, Bitmap),
                                     send(Figura, status, 1),
                                     send(Pantalla, display,Figura,point(20,100)).
 nueva_imagen(Ventana, Imagen) :-new(Figura, figure),
                                new(Bitmap, bitmap(resource(Imagen),@on)),
                                send(Bitmap, name, 1),
                                send(Figura, display, Bitmap),
                                send(Figura, status, 1),
                                send(Ventana, display,Figura,point(0,0)).
  imagen_pregunta(Ventana, Imagen) :-new(Figura, figure),
                                new(Bitmap, bitmap(resource(Imagen),@on)),
                                send(Bitmap, name, 1),
                                send(Figura, display, Bitmap),
                                send(Figura, status, 1),
                                send(Ventana, display,Figura,point(500,60)).

  botones:-borrado,
                send(@boton, free),
                send(@btntratamiento,free),
                mostrar_diagnostico(Enfermedad),
                send(@texto, selection('El Diagnostico a partir de los datos es:')),
                send(@resp1, selection(Enfermedad)),
                new(@boton, button('Iniciar consulta',
                message(@prolog, botones)
                )),

                new(@btntratamiento,button('Detalles y Tratamiento',
                message(@prolog, mostrar_tratamiento,Enfermedad)
                )),
                send(@main, display,@boton,point(20,450)),
                send(@main, display,@btntratamiento,point(138,450)).



  mostrar_tratamiento(X):-new(@tratam, dialog('Tratamiento')),
                          send(@tratam, append, label(nombre, 'Explicacion: ')),
                          send(@tratam, display,@lblExp1,point(70,51)),
                          send(@tratam, display,@lblExp2,point(50,80)),
                          tratamiento(X),
                          send(@tratam, transient_for, @main),
                          send(@tratam, open_centered).

tratamiento(X):- send(@lblExp1,selection('De Acuerdo Al Diagnostico El Tratamiento Es:')),
                 mostrar_imagen_tratamiento(@tratam,X).


   preguntar(Preg,Resp):-new(Di,dialog('Colsultar Datos:')),
                        new(L2,label(texto,'Responde las siguientes preguntas')),
                        id_imagen_preg(Preg,Imagen),
                        imagen_pregunta(Di,Imagen),
                        new(La,label(prob,Preg)),
                        new(B1,button(si,and(message(Di,return,si)))),
                        new(B2,button(no,and(message(Di,return,no)))),
                        send(Di, gap, size(25,25)),
                        send(Di,append(L2)),
                        send(Di,append(La)),
                        send(Di,append(B1)),
                        send(Di,append(B2)),
                        send(Di,default_button,'si'),
                        send(Di,open_centered),get(Di,confirm,Answer),
                        free(Di),
                        Resp=Answer.


  interfaz_principal:-new(@main,dialog('Sistema Experto Diagnosticador de Enfermedades de perros',
        size(1000,1000))),
        new(@texto, label(nombre,'El Diagnostico a partir de los datos es:',font('times','roman',18))),
        new(@resp1, label(nombre,'',font('times','roman',22))),
        new(@lblExp1, label(nombre,'',font('times','roman',14))),
        new(@lblExp2, label(nombre,'',font('times','roman',14))),
        new(@salir,button('SALIR',and(message(@main,destroy),message(@main,free)))),
        new(@boton, button('Iniciar consulta',message(@prolog, botones))),

        new(@btntratamiento,button('¿Tratamiento?')),

        nueva_imagen(@main, img_principal),
        send(@main, display,@boton,point(138,450)),
        send(@main, display,@texto,point(20,130)),
        send(@main, display,@salir,point(300,450)),
        send(@main, display,@resp1,point(20,180)),
        send(@main,open_centered).

       borrado:- send(@resp1, selection('')).


  crea_interfaz_inicio:- new(@interfaz,dialog('Bienvenido al Sistema Experto Diagnosticador*',
  size(1000,1000))),

  mostrar_imagen(@interfaz, portada),

  new(BotonComenzar,button('COMENZAR',and(message(@prolog,interfaz_principal) ,
  and(message(@interfaz,destroy),message(@interfaz,free)) ))),
  new(BotonSalir,button('SALIDA',and(message(@interfaz,destroy),message(@interfaz,free)))),
  send(@interfaz,append(BotonComenzar)),
  send(@interfaz,append(BotonSalir)),
  send(@interfaz,open_centered).

  :- crea_interfaz_inicio.
