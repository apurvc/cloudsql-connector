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
        "shared-vpc-proj-:us-central1:my-postgres",
        "pg8000",
        user="21344782222-compute@developer", #IAM user, the one visible in users section
        db="postgres",  
        enable_iam_auth=True,
        ip_type=IPTypes.PRIVATE
    )
    return conn


# create connection pool
pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
    creator=getconn,
)

# connect to connection pool
with pool.connect() as db_conn:
    # get current datetime from database
    results = db_conn.execute(sqlalchemy.text("SELECT NOW()")).fetchone()

    # output time
    print("Current time: ", results[0])

# cleanup connector
connector.close()