import os
from dotenv import load_dotenv; load_dotenv()
import openapi_client
from session import SessionLocal, init_db
from ingestion_function import ingest_system_and_waypoints

configuration = openapi_client.Configuration(access_token=os.getenv("BEARER_TOKEN"))
apicl = openapi_client.ApiClient(configuration)
systems = openapi_client.SystemsApi(apicl)
agents = openapi_client.AgentsApi(apicl)

me = agents.get_my_agent()
my_system = "-".join(me.data.headquarters.split("-")[:2])
init_db() # ensure tables exist once at startup
with SessionLocal() as session:
    ingest_system_and_waypoints(systems, my_system, session)