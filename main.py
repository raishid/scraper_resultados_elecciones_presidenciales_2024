from modules.Extractor import Extractor
from modules.DB import DB
import json
import traceback
from threading import Thread as T

def init_scraper(EDO: int, INIT_URL: str):
  cls = Extractor._launch(True)  
  municipios = cls.get_municipios(url=f'{INIT_URL}/estado/{str(EDO)}')
    
  DB.guardar_estado_if_no_exist(nombre=municipios[0]['estado'], estado_id=municipios[0]['estado_id'])
    
  for municipio in municipios:
    print('Municipio:', municipio['name'])
    DB.guardar_municipio_if_no_exist(nombre=municipio['name'], estado_id=municipio['estado_id'], municipio_id=municipio['id'])
    tryy = 0
    while tryy <= 5:
      try:
        print(f'Extrayendo datos Municipio: {INIT_URL}{municipio['url']}')
        cls.get_parroquia(f'{INIT_URL}{municipio['url']}')
        tryy = 6
      except:
        tryy += 1
        print('Error en get_parroquia')
        if tryy == 5:
          err = traceback.format_exc()
          open('error.txt', 'a').write(f'Error en get_parroquia:\n{INIT_URL}{municipio['url']}\n{err}\n')
      
    
  parroquias = cls.parroquias
  for parroquia in parroquias:
    print('Parroquia:', parroquia['name'])
    DB.guardar_parroquia_if_no_exist(nombre=parroquia['name'], municipio_id=parroquia['municipio_id'], parroquia_id=parroquia['id'])
    tryy = 0
    while tryy <= 5:
      try:
        print(f'Extrayendo datos Parroquia: {INIT_URL}{parroquia['url']}')
        cls.get_centros(f'{INIT_URL}{parroquia['url']}')
        tryy = 6
      except:
        tryy += 1
        print('Error en get_centros')
        if tryy == 5:
          err = traceback.format_exc()
          open('error.txt', 'a').write(f'Error en get_centros:\n{INIT_URL}{parroquia['url']}\n{err}\n')
    
  centros = cls.centros
  for centro in centros:
    print('Centro:', centro['name'])
    DB.guardar_centro_if_no_exist(nombre=centro['name'], parroquia_id=centro['parroquia_id'], centro_id=centro['id'])
    tryy = 0
    while tryy <= 5:
      try:
        print(f'Extrayendo datos Centro: {INIT_URL}{centro['url']}')        
        cls.get_mesas(f'{INIT_URL}{centro['url']}')
        tryy = 6
      except:
        tryy += 1
        print('Error en get_centros')
        if tryy == 5:
          err = traceback.format_exc()
          open('error.txt', 'a').write(f'Error en get_centros:\n{INIT_URL}{centro['url']}\n{err}\n')
    
  mesas = cls.mesas
  for mesa in mesas:
    print('Mesa:', mesa['name'])
    DB.guardar_mesa_if_no_exist(nombre=mesa['name'], centro_id=mesa['centro_id'], mesa_id=mesa['id'])
    tryy = 0
    while tryy <= 5:
      try:
        print(f'Extrayendo datos Mesa: {INIT_URL}{mesa['url']}')        
        results = cls.get_actas(f'{INIT_URL}{mesa['url']}')
        DB.guardar_acta_if_no_exist(
          id=results['id'],
          votos_edmundo=results['votos_edmundo'],
          votos_nicolas=results['votos_maduro'],
          votos_otros=results['votos_otros'],
          electores=results['electores'],
          votantes=results['votantes'],
          participacion=results['participacion'],
          mesa_id=mesa['id'],
          acta_image=results['acta_image']
          
        )
        tryy = 6
      except:
        tryy += 1
        print('Error en get_actas')
        if tryy == 5:
          err = traceback.format_exc()
          open('error.txt', 'a').write(f'Error en get_actas:\n{INIT_URL}{mesa['url']}\n{err}\n')

def main():
    
  print('Iniciando Extraccion de data...')
  
  db = DB()
  db._create_table()
  
  json_read = json.loads(open('secuencia.json', 'r').read())
  
  INIT_URL = f'https://www.resultadosconvzla.com'
  EDO = json_read['secuencia']
  
  while EDO < 25:
    print('Estado Nro:', EDO)
    print('URL:', f'{INIT_URL}/estado/{EDO}')
    pr = T(target=init_scraper, args=(EDO, INIT_URL))
    pr.start()
    pr.join()
    EDO += 1
    saveSecuencia(EDO)
            
def saveSecuencia(secuencia: int):
  open('secuencia.json', 'w').write(json.dumps({'secuencia': secuencia}, indent=2))

if __name__ == '__main__':
  main()
    