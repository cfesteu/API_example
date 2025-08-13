# A simple Python API 
## Project description
For the Python Module assignment I have built a simple Python API on top of the database (dimensionally modelled) created previously on the ETL assignment. The API exposes two endpoints (but can be easily extended with a lot more) serving reports regarding various topics related to employees activity data stored in the database.

## Overview
The API was developed using the FastAPI Python Framework. A request made to the root path would retrieve the currently available endpoints in a suggestively manner for their usage. Each request made towards an endpoint would trigger a query on the source database that would retrieve the specific information related (as of now) for only one employee. 

At the startup of the application, a connection pool is instantiate. Every request would acquire a connection from the pool and pass a SQL query using a pre-defined template (stored in the queries module) with a bind variable that's initially passed as a query parameter within the request. The data retrieved from the database is then formatted in a JSON-like structure built using the information exposed by the connection's cursor.

To be able to persist and track all of the requests made using the API, a logging middleware has been created (see the middleware module). The middleware captures the information, parses it in SQLModel(a wrapper on top of Pydantic and SQLAlchemy) object and logs it into a PostgreSQL database.


All of this components were then containerized in a docker-compose setup. Since the source database has initially been created in another environment and had to be reconstructed using a dumpfile, additional steps were required to ensure the availability of the data at the startup moment. Hence, the dependencies related to the web service and also the healtcheck script. What this does is to make sure the data has already been inserted within the database and queries can be made before starting up the web server.


## Usage
The app can be run locally by using the command **docker-compose up --build**, provided that the ports described in the .yaml file are not already used for communication on the host machine. A request towards root would expose the available endpoints. For the currently available endpoints, the only query parameter is the employee_id. 



## Plans for extension
- More reporting endpoints
- A frontend component (at least using Streamlit) with all sorts of data visualisations.
- Caching as the application would increase the volume of data exported. 






