from typing import Any, Union
from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext
import os
import base64

class Extractor:

  municipios = []
  parroquias = []
  centros = []
  mesas = []
  opts: Any
  profile_url: str
  cookies: Any
  driver: Browser
  context: BrowserContext
  page: Page
  
  @staticmethod
  def _launch(headless: bool = True, view_port: Union[dict, None] = None):
    args = ['--disable-blink-features=AutomationControlled']
    if headless:
        args.append('--headless=new')
        
    cls = Extractor()

    cls.driver = sync_playwright().start().chromium.launch(
        channel='chrome',
        headless=False,
        args=args,

        ignore_default_args=['--enable-automation']
    )

    cls.context = cls.driver.new_context(
        viewport=view_port,
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    )
    
    cls.page = cls.context.new_page()
    
    return cls
    
  def get_municipios(self, url: str):
    self.page.goto(url)
    
    estado = self.page.query_selector('#tabla > div h2').text_content().replace('Resultados - ', '').strip()
    estado_id = url.split('/')[-1]
    
    municipios = self.page.locator('//a[contains(@href, "municipio")]').all()
    municipios_nombre = self.page.locator('//a[contains(@href, "municipio")]/parent::td/parent::tr/td[1]').all()
    for municipio, nombre in zip(municipios, municipios_nombre):
      self.municipios.append({
        'url': municipio.get_attribute('href'),
        'name': nombre.text_content(),
        'estado': estado,
        'estado_id': estado_id,
        'id': municipio.get_attribute('href').split('/')[-1]
      })
      
    return self.municipios
    
  def get_parroquia(self, url: str):
    self.page.goto(url)
    
    parroquias = self.page.locator('//a[contains(@href, "parroquia")]').all()
    parroquia_nombre = self.page.locator('//a[contains(@href, "parroquia")]/parent::td/parent::tr/td[1]').all()

    for parroquia, nombre in zip(parroquias, parroquia_nombre):
      self.parroquias.append({
        'url': parroquia.get_attribute('href'),
        'name': nombre.text_content(),
        'id': parroquia.get_attribute('href').split('/')[-1],
        'municipio_id': url.split('/')[-1],
      })
    
    return self.parroquias
      
  def get_centros(self, url: str):
    self.page.goto(url)
    
    centros = self.page.locator('//a[contains(@href, "centro")]').all()
    centros_nombre = self.page.locator('//a[contains(@href, "centro")]/parent::td/parent::tr/td[1]').all()
    for centro, nombre in zip(centros, centros_nombre):
      self.centros.append({
        'url': centro.get_attribute('href'),
        'name': nombre.text_content(),
        'id': centro.get_attribute('href').split('/')[-1],
        'parroquia_id': url.split('/')[-1],
      })
      
    return self.centros
      
  def get_mesas(self, url: str):
    self.page.goto(url)
    
    mesas = self.page.locator('//a[contains(@href, "mesa")]').all()
    mesa_numero = self.page.locator('//a[contains(@href, "mesa")]/parent::td/parent::tr/td[1]').all()
    for mesa, numero in zip(mesas, mesa_numero):
      self.mesas.append({
        'url': mesa.get_attribute('href'),
        'name': numero.text_content(),
        'id': mesa.get_attribute('href').split('/')[-1],
        'centro_id': url.split('/')[-1],
      })
      
    return self.mesas
  
  def get_actas(self, url: str):
    self.page.goto(url)
    
    votos_edmundo = self.page.locator('//h3[text()="Edmundo González"]/parent::div/h4').first.text_content().replace('votos', '').strip()
    votos_maduro = self.page.locator('//h3[text()="Nicolás Maduro"]/parent::div/h4').first.text_content().replace('votos', '').strip()
    votos_otros =  self.page.locator('//h3[text()="Otros"]/parent::div/h4').first.text_content().replace('votos', '').strip()
    electores = self.page.locator('//h5[text()="Electores"]/parent::div/div').first.text_content()
    votantes = self.page.locator('//h5[text()="Votantes"]/parent::div/div').first.text_content()
    participacion = self.page.locator('//h5[text()="Participación"]/parent::div/div').first.text_content().replace('%', '')
    #convert to float
    participacion = float(participacion.replace(',', '.'))
    
    acta = self.page.query_selector('#acta img').get_attribute('src')
    
    print('Votos Edmundo:', votos_edmundo)
    print('Votos Maduro:', votos_maduro)
    print('Votos Otros:', votos_otros)
    print('Electores:', electores)
    print('Votantes:', votantes)
    print('Participacion:', participacion)
    print('Acta:', acta)
    
    self.page.goto(acta)
    
    #download images
    image_data = self.page.evaluate('''(selector) => {
          const img = document.querySelector(selector);
          const canvas = document.createElement('canvas');
          const context = canvas.getContext('2d');
          canvas.width = img.naturalWidth;
          canvas.height = img.naturalHeight;
          context.drawImage(img, 0, 0);
          return canvas.toDataURL().split(',')[1];
      }''', 'img')
    
    open(f'{os.getcwd()}/actas/{acta.split("/")[-1]}', 'wb').write(base64.b64decode(image_data))
    
    
    return {
      'id': url.split('/')[-1],
      'votos_edmundo': votos_edmundo,
      'votos_maduro': votos_maduro,
      'votos_otros': votos_otros,
      'electores': electores,
      'votantes': votantes,
      'participacion': participacion,
      'acta_image': f'/actas/{acta.split("/")[-1]}'
    }
    
    
  
    
    
    