import unittest
import json
import requests
URL = "http://127.0.0.1:8000"

def test_user_register():
    payload = json.dumps({
    "email": "t@m.com",
    "password": "123"
    })
    headers = {}
    response = requests.request("POST", URL+'/register', headers=headers, data=payload)
    token = response.json().get('token')
    
    assert(token == 't@m.com$123') #note : the token is used in authorization field in all tests after this


def test_unauthorized_access():

    payload = json.dumps({
    "url": "http://www.google.com",
    "private": False
    })
    
    headers = {
    'Authorization': 'BAD_TOKEN',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", URL+'/bookmarks', headers=headers, data=payload)

    assert(response.status_code == 401)

def test_bookmark_create_public():

    payload = json.dumps({
    "url": "http://www.google.com",
    "private": False
    })
    headers = {
    'Authorization': 't@m.com$123',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", URL+'/bookmarks', headers=headers, data=payload)

    assert(response.status_code == 201)

def test_bookmark_create_private():

    payload = json.dumps({
    "url": "http://www.netlync.com",
    "private": True
    })
    headers = {
    'Authorization': 't@m.com$123',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", URL+'/bookmarks', headers=headers, data=payload)

    assert(response.status_code == 201)

def test_get_all_user_bookmarks():
    
    headers = {
    'Authorization': 't@m.com$123',
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", URL+'/bookmarks', headers=headers, data={})
    response = response.json()

    # we have 2 bookmarks in total for this user, so we can check the length as confirmation
    assert(len(response) == 2)

def test_delete_bookmark():

    url = "http://localhost:8000/bookmarks/2"
    headers = {
    'Authorization': 't@m.com$123'
    }

    response = requests.request("DELETE", url, headers=headers, data={}).json()

    assert(response.get('success') == 'ok')

