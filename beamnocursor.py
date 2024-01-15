import apache_beam as beam
from apache_beam import DoFn
from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud.sql.connector import Connector, IPTypes
import google.auth
import sqlalchemy
import pymysql

INSTANCE_CONNECTION_NAME = "GCP_PROJECT_ID:europe-west1:my-private-sql"
class selectfn(beam.Dofn):
    def connect_with_connector_auto_iam_authn() -> sqlalchemy.engine.base.Engine:
        instance_connection_name = INSTANCE_CONNECTION_NAME
        db_iam_user = "23453660003-compute@developer.gserviceaccount.com"  # e.g. 'service-account-name'
        db_name = "my-database"  # e.g. 'my-database'
        ip_type = IPTypes.PRIVATE 

        # initialize Cloud SQL Python Connector object
        connector = Connector()

        def getconn() -> pymysql.connections.Connection:
            conn: pymysql.connections.Connection = connector.connect(
                instance_connection_name,
                "pymysql",
                user=db_iam_user,
                db=db_name,
                enable_iam_auth=True,
                ip_type=ip_type,
            )
            return conn

        # The Cloud SQL Python Connector can be used with SQLAlchemy
        # using the 'creator' argument to 'create_engine'
        pool = sqlalchemy.create_engine(
            "mysql+pymysql://",
            creator=getconn,
        )
        for record in pool.execute(sqlalchemy.sql.text("SELECT table_name FROM information_schema.tables WHERE table_schema=information_schema"), query_params):
            yield dict(record)

# Define pipeline options
options = PipelineOptions(
    project='GCP_PROJECT_ID',
    runner='DataflowRunner',
    region='europe-west1',
    temp_location='gs://GCP_PROJECT_ID',
)


# Define the Dataflow pipeline
p = beam.Pipeline(options=options)

    # Read data from MySQL
(p
    | 'ReadFromMySQL' >> beam.io.ReadFromText("gs://GCP_PROJECT_ID/file1.txt")
    | 'ExeuteQuery'   >> beam.ParDo(selectfn())
)

p.run()
  