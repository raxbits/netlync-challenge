# netlync backend challenge - bookmarking tool with login

## Setup
- Install require packages `pip install -r requirements.txt`
- Run: `./run.sh` in bash

## Usage
The app exposes couple endpoints to enable functionality required. The routes are arranged based on use case flow:
- user can signup for an account, using their email and password using "/register" endpoint, and recieve a token to use when requesting service subsequently. See test for more info.
- user can login after account creation and recieve a token to use when requesting service subsequently. See test for more info.
- can create, get and delete "bookmarks" through "/bookmark" endpoint. 

## Scaling thoughts

- Currently we use sqlite which is not a production database. We can move to postgres or mysql to handle more loads.
- We can dockerize the application logic to enable scaling using autoscaling tools, enable metrics and monitoring key KPIs like p95 , p99 etc.
- We can introduce caching, like redis to cache most visited/highly popular non private bookmarks, reducing database reads.
- We can add rate-limiting per user to uniform or shed load on the backend.

## Documentation
- After running the app, visit http://127.0.0.1/docs for endpoints, modals etc.
