from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy

# IAM database user parameter (IAM user's email before the "@" sign, mysql truncates usernames)
# ex. IAM user with email "demo-user@test.com" would have database username "demo-user"
#IAM_USER = current_user[0].split("@")[0]

# initialize connector
connector = Connector()

# getconn now using IAM user and requiring no password with IAM Auth enabled


def getconn():
    conn = connector.connect(
        "shared-vpc-proj-394917:us-central1:my-sql",
        "pymysql",
        user="213447898298-compute@developer.gserviceaccount.com",
        db="sandwich",  # log in to instance but don't connect to specific database
        enable_iam_auth=True,
        ip_type=IPTypes.PRIVATE
    )
    return conn


# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# connect to connection pool
with pool.connect() as db_conn:
  db_conn.execute(
    sqlalchemy.text(
      "CREATE TABLE IF NOT EXISTS ratings "
      "( id SERIAL NOT NULL, name VARCHAR(255) NOT NULL, "
      "origin VARCHAR(255) NOT NULL, rating FLOAT NOT NULL, "
      "PRIMARY KEY (id));"
    )
  )

  # commit transaction (SQLAlchemy v2.X.X is commit as you go)
  db_conn.commit()

  # insert data into our ratings table
  insert_stmt = sqlalchemy.text(
      "INSERT INTO ratings (name, origin, rating) VALUES (:name, :origin, :rating)",
  )

  # insert entries into table
#  db_conn.execute(insert_stmt, parameters={"name": "HOTDOG", "origin": "Germany", "rating": 7.5})
#  db_conn.execute(insert_stmt, parameters={"name": "BÀNH MÌ", "origin": "Vietnam", "rating": 9.1})
#  db_conn.execute(insert_stmt, parameters={"name": "CROQUE MADAME", "origin": "France", "rating": 8.3})

# commit transactions
  db_conn.commit()

  # query and fetch ratings table
  results = db_conn.execute(sqlalchemy.text("SELECT * FROM ratings")).fetchall()

  # show results
  for row in results:
    print(row)

# cleanup connector object
connector.close()