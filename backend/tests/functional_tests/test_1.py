import pytest
import json

def test_hello_world(app, client):
    res = client.get('/hello-world')
    assert res.status_code == 200
    assert res.get_data(as_text=True) == 'Hello world!'

def test_register(app, client):
    register_result = client.post('/auth/register', data={
        "email": "some-email@gmail.com",
        "password": "admin",
        "role": "admin",
        "name": "Test user"
    })
    response = json.loads(register_result.get_data(as_text=True))
    success = response.get('success'); result = response.get('result'); error = response.get('error')
    assert success == True
    assert result.get('email') == "some-email@gmail.com"
    assert result.get('name') == "Test user"
    assert result.get('role') == "admin" 

def test_add_book(app, client):
    login_result = client.post('/auth/login', data={
        "email": "some-email@gmail.com",
        "password": "admin",
        "remember": True
    })

    res = client.post('/api/book', data={
        "title": "Test book",
        "isbn": "123456789",
        "publish_year": 2000,
        "description": "Some description",
        "stock": 3,
        "authors": '["Author 1", "Author 2"]',
        "genres": '["Genre 1", "Genre 2"]'
    })

    response = json.loads(res.get_data(as_text=True))
    success = response.get('success'); result = response.get('result'); error = response.get('error')
    print(error)
    assert success == True
    assert result.get('title') == "Test book"
    assert result.get('isbn') == "123456789"
    if success == True:
        delete_res = client.delete('/api/book', data={
            "book_id": result.get('id')
        })
