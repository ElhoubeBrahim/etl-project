import mysql.connector
import subprocess
import time

print("Starting ELT script ...")

db_config = {
  "source": {
    "host": "source_database",
    "database": "source_db",
    "user": "root",
    "password": "password",
  },
  "target": {
    "host": "target_database",
    "database": "target_db",
    "user": "root",
    "password": "password",
  },
}

def connect(label="source", retries=10, delay=5):
  print(f"  Checking connection to {label} database ...")

  for i in range(retries):
    try:
      conn = mysql.connector.connect(
        host=db_config[label]["host"],
        user=db_config[label]["user"],
        password=db_config[label]["password"],
        database=db_config[label]["database"]
      )
      print(f"  Connection to {label} database is OK")
      return conn
    except Exception as e:
      print(f"  Attempt {i + 1} of {retries} failed. Retrying in {delay} seconds ...")
      time.sleep(delay)

  print(f"  Connection to {label} database failed")
  return None

    

def dump(config):
  print("Dumping source database ...")
  source_conn = connect("source")

  if source_conn is None:
    print("Dumping source database failed")
    return
  
  command = [
    "mysqldump",
    "-h", config["host"],
    "-u", config["user"],
    "-p" + config["password"],
    config["database"]
  ]

  try:
    with open("dump.sql", "w") as file:
      subprocess.run(command, stdout=file)
  except Exception as e:
    print(f"Dumping source database failed: {e}")
    return
  
  print("Dumping source database is OK")


def load(config):
  print("Loading target database ...")
  target_conn = connect("target")

  if target_conn is None:
    print("Loading target database failed")
    return
  
  command = [
    "mysql",
    "-h", config["host"],
    "-u", config["user"],
    "-p" + config["password"],
    config["database"]
  ]

  try:
    with open("dump.sql", "r") as file:
      subprocess.run(command, stdin=file)
  except Exception as e:
    print(f"Loading target database failed: {e}")
    return
  
  print("Loading target database is OK")

if __name__ == "__main__":
  dump(db_config["source"])
  load(db_config["target"])

  print("ELT script finished")