import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from google.cloud.sql.connector import connector, IPTypes

pipeline_options = PipelineOptions()
pipeline_options.view_as(StandardOptions).runner = 'DataflowRunner'
# ... other pipeline options

def create_mysql_connection():
    instance_connection_name = 'your-instance-connection-name'  # Replace with your connection name
    db_user = 'your-iam-user@gmail.com'  # IAM user email without domain
    db_name = 'your-database-name'

    def getconn() -> connector.Connector:
        return connector.connect(
            instance_connection_name,
            "pymysql",
            user=db_user,
            db=db_name,
            enable_iam_auth=True,  # Enable automatic IAM authentication
            ip_type=IPTypes.PRIVATE
        )

    return getconn

def query_and_print_records():
    conn = create_mysql_connection()()  # Get a new connection
    cursor = conn.cursor()
    cursor.execute("SELECT NOW()")  # Replace with your query
    records = cursor.fetchall()
    for record in records:
        print(record)
    cursor.close()
    conn.close()

# Define the Dataflow pipeline
p = beam.Pipeline(options=options)

    # Read data from MySQL
rows = (p
        | 'ExecuteandPrint' >> beam.Map(query_and_print_records)
        )

p.run()
