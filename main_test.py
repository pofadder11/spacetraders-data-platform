# main_test.py (usage sketch)
from dotenv import load_dotenv
from session import init_db, SessionLocal
from services.client_service import OpenAPIService
from services.write_through import WriteThrough, default_handlers

def main():
    load_dotenv()
    init_db()

    svc = OpenAPIService()
    wt = WriteThrough(svc, SessionLocal, handlers=default_handlers())

    # Call returns the inner `.data`, and auto-updates fleet_nav
    ships = wt.fleet.get_my_ships()
    print(f"Ships fetched: {len(ships)}")

if __name__ == "__main__":
    main()
