from sqlalchemy import create_engine, text

  # Configurația pentru conexiune
conf = {
      'host': "mysql-cca70b9-cnaic-44df.f.aivencloud.com",
      'port': '23157',
      'user': "avnadmin",
      'password': "AVNS_cUJm7IhN4qNPcWKWWKP",
      'database': "defaultdb"  # Specifică numele bazei de date
  }

  # Creează engine-ul pentru MySQL folosind pymysql
engine = create_engine(
      "mysql+pymysql://{user}:{password}@{host}:{port}/{database}".format(**conf)
  )

