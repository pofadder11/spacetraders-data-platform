[ SpaceTraders API ]
         |
         v
+----------------------------+
|  OpenAPI-generated client  |   <-- already exists
|  - apis/ (FleetApi, ...)   |
|  - models/ (Ship, Waypoint)|
+----------------------------+
         |
         v
+----------------------------+      +-------------------+
|    adapters (you build)    | ---> | domain models     |   <-- you build
| - turn DTO -> domain       |      | (immutable)       |
+----------------------------+      +-------------------+
         |                                  |
         v                                  v
+----------------------------+      +-------------------+
|   state/cache (you build)  | ---> | DbWriter queue    |   <-- you build
| - per-entity dicts         |      | (async write-thru)|
| - copy-on-write updates    |      +-------------------+
+----------------------------+                 |
         |                                      v
         |                              +-------------------+
         |                              |   Postgres (ORM)  |  <-- you build (SQLModel)
         '----------------------------> |   repositories    |
                                        +-------------------+
