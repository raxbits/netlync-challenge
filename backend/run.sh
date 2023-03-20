#!/bin/bash

rm netlync.db

python create_db.py

uvicorn main:app


