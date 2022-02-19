import requests
import lxml.html as html
import os
import datetime #para traer la fecha de hoy

# Creamos constantes

HOME_URL = 'https://larepublica.pe/'

XPATH_LINK_TO_ARTICLE = '//div/article/a/@href'
XPATH_TITLE = '//div/h1[@class="DefaultTitle"]/text()'
XPATH_SUMMARY = '//div/h2[@class="DefaultSubtitle"]/text()'
XPATH_BODY = '//div/section/p/text()'







def parse_notice(link,today):

    #A veces el link no contiene el base path por lo que se tiene que añadir
    if (link.__contains__(HOME_URL)):
        pass
    else:
        link=HOME_URL+link
        

    try:
        response=requests.get(link)
        if response.status_code==200:
            notice=response.content.decode('utf-8')
            parsed=html.fromstring(notice)

            

            try:
                title=parsed.xpath(XPATH_TITLE)[0] #esto nos devuelve una lista. Nosotros queremos el primero que es el title
                title=title.replace('\"','') #de existir comillas, reemplazalas por vacío.
                summary=parsed.xpath(XPATH_SUMMARY)[0]
                body=parsed.xpath(XPATH_BODY) #nos interesa traer toda la lista
            except IndexError: return #es posible que algunas no tengan summary.
      
            with open(f'{today}/{title}.txt','w',encoding='utf-8') as f: #manejador contextual. Permite manejar open. Open espera como input una ruta. Busco una carpeta del día de hoy y dentro de esa carpeta voy a guardar un archivo .txt con el nombre de nuestra noticia
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body: #el cuerpo es una lista de párrafos.
                    f.write(p)
                    f.write('\n')
                

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

# Creamos la función para extraer los links:

def parse_home():
    # Creamos un bloque try para manejar los errores. Y manejar los Status Code.
    try: 
        response= requests.get(HOME_URL) #Extrae el documento html y todo lo que involucra http
        #entra al if si el status code es de 200
        if response.status_code==200:
            home=response.content.decode('utf-8') #ayuda a transformar los caracteres especiales
            parsed=html.fromstring(home)
            links_to_notices=parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_notices)

            today=datetime.date.today().strftime('%d-%m-%Y') #Se crea la fecha
            if not os.path.isdir(today): #si existiese una carpeta con el nombre today
                os.mkdir(today) #se crea la carpeta con el nombre de today

            for link in links_to_notices:
                parse_notice(link,today)
            pass
        else:
            raise ValueError(f'Error: {response.status_code}') #para elevar un error
    except ValueError as ve:
        print(ve) #si hay un error que imprima el error



#Esta va a ser la función principal, que correra todas las funciones
def run():
    parse_home()

#Entry point
if __name__=="__main__": run()
