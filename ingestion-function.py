from sqlalchemy.orm import Session
from models import System, Waypoint
from openapi_client.rest import ApiException

def ingest_system_and_waypoints(systems_api, system_symbol: str, session: Session) -> None:
    try:
        sys_resp = systems_api.get_system(system_symbol)
        wps_resp = systems_api.get_system_waypoints(system_symbol)
    except ApiException as e:
        print(f"[ingest] API error: {e}")
        raise

    sys_data = sys_resp.data # expects .symbol, .type, .x, .y
    session.merge(System(symbol=sys_data.symbol, type=getattr(sys_data, "type", None), x=sys_data.x, y=sys_data.y))
    for w in wps_resp.data: # each has .symbol, .type, .x, .y
        session.merge(Waypoint(symbol=w.symbol, system_symbol=system_symbol, type=getattr(w, "type", None), x=w.x, y=w.y))
        session.commit()