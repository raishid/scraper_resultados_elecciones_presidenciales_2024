import sqlite3
import os

class DB:
  
  def __init__(self) -> None:
    self.conexion = sqlite3.connect(f'{os.getcwd()}/db/actas.db')
    self.conexion.row_factory = sqlite3.Row
    self.cursor = self.conexion.cursor()
    
  def _create_table(self):
    self.cursor.execute('''
      CREATE TABLE IF NOT EXISTS estados(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT
      )
    ''')
    
    self.cursor.execute('''
      CREATE TABLE IF NOT EXISTS municipios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        estado_id INTEGER
      )
    ''')
    
    self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS parroquias(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        municipio_id INTEGER
      )
    ''')
    
    self.cursor.execute('''
      CREATE TABLE IF NOT EXISTS centros(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        parroquia_id INTEGER
      )
    ''')
    
    self.cursor.execute('''
      CREATE TABLE IF NOT EXISTS mesas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        centro_id INTEGER
      )
    ''')
    
    self.cursor.execute('''
      CREATE TABLE IF NOT EXISTS actas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        votos_edmundo INTEGER,
        votos_nicolas INTEGER,
        votos_otros INTEGER,
        electores INTEGER,
        votantes INTEGER,
        participacion REAL,
        acta_image TEXT,
        mesa_id INTEGER
      )
    ''')

  @staticmethod  
  def guardar_estado_if_no_exist( nombre: str, estado_id: int):
    cls = DB()
    conexion = cls.conexion
    cursor = cls.cursor
    
    exist = cursor.execute(f"""
      SELECT * FROM estados WHERE id = ?
    """, (estado_id,)).fetchone()

    if exist:
      return
    
    cursor.execute(f"""
      INSERT INTO estados(id, nombre) VALUES(?, ?)
    """, (estado_id, nombre))
    conexion.commit()

  @staticmethod  
  def guardar_municipio_if_no_exist( nombre: str, municipio_id: int, estado_id: int):
    cls = DB()
    conexion = cls.conexion
    cursor = cls.cursor  
    
    exist = cursor.execute(f"""
      SELECT * FROM municipios WHERE id = ?
    """, (municipio_id,)).fetchone()

    if exist:
      return
    
    cursor.execute(f"""
      INSERT INTO municipios(id, nombre, estado_id) VALUES(?, ?, ?)
    """, (municipio_id, nombre, estado_id))
    conexion.commit()

  @staticmethod  
  def guardar_parroquia_if_no_exist( nombre: str, parroquia_id: int, municipio_id: int):
    cls = DB()
    conexion = cls.conexion
    cursor = cls.cursor
    
    exist = cursor.execute(f"""
      SELECT * FROM parroquias WHERE id = ?
    """, (parroquia_id,)).fetchone()

    if exist:
      return
    
    cursor.execute(f"""
      INSERT INTO parroquias(id, nombre, municipio_id) VALUES(?, ?, ?)
    """, (parroquia_id, nombre, municipio_id))
    conexion.commit()

  @staticmethod  
  def guardar_centro_if_no_exist( nombre: str, centro_id: int, parroquia_id: int):
    cls = DB()
    conexion = cls.conexion
    cursor = cls.cursor
    
    exist = cursor.execute(f"""
      SELECT * FROM centros WHERE id = ?
    """, (centro_id,)).fetchone()

    if exist:
      return
    
    cursor.execute(f"""
      INSERT INTO centros(id, nombre, parroquia_id) VALUES(?, ?, ?)
    """, (centro_id, nombre, parroquia_id))
    conexion.commit()

  @staticmethod  
  def guardar_mesa_if_no_exist( nombre: str, mesa_id: int, centro_id: int): 
    cls = DB()
    conexion = cls.conexion
    cursor = cls.cursor
    
    exist = cursor.execute(f"""
      SELECT * FROM mesas WHERE id = ?
    """, (mesa_id,)).fetchone()

    if exist:
      return
    
    cursor.execute(f"""
      INSERT INTO mesas(id, nombre, centro_id) VALUES(?, ?, ?)
    """, (mesa_id, nombre, centro_id))
    conexion.commit()

  @staticmethod  
  def guardar_acta_if_no_exist( id: int, votos_edmundo: int, votos_nicolas: int, votos_otros: int, electores: int, votantes: int, participacion: float, acta_image: str, mesa_id: int):
    cls = DB()
    conexion = cls.conexion
    cursor = cls.cursor
    
    exist = cursor.execute(f"""
      SELECT * FROM actas WHERE mesa_id = ?
    """, (mesa_id,)).fetchone()

    if exist:
      return
    
    cursor.execute(f"""
      INSERT INTO actas(id, votos_edmundo, votos_nicolas, votos_otros, electores, votantes, participacion, acta_image, mesa_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (id, votos_edmundo, votos_nicolas, votos_otros, electores, votantes, participacion, acta_image, mesa_id))
    conexion.commit()