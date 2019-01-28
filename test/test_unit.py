# -*- coding: utf-8 -*-
import os
import tempfile

import pytest
from app import APP as app

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()
    client.get('/reset')

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_index(client):
    """welcome response from index"""
    response = client.get('/')
    assert u'Szybka piłka' in response.data.decode('utf-8')

def test_forms(client):
    """welcome response from index"""
    response = client.get('/forms', follow_redirects=True)
    assert u'brak uprawnień' in response.data.decode('utf-8')

def test_add_team(client):
    """welcome response from index"""
    response = client.get('/addteam', follow_redirects=True)
    assert u'brak uprawnień' in response.data.decode('utf-8')

def test_register_wizzard(client):
    """ try to register a wizzard"""
    response = client.get('/register/wizzard')
    assert response.status_code == 404

def test_form_submit(client):
    """ try to register a wizzard"""
    response = client.post('/forms', data={
        'accepted': 'true',
        'reason': '',
        'form_id': '1'
    })
    assert response.status_code == 403

def test_add_team_submit(client):
    """ try to register a wizzard"""
    response = client.post('/addteam', data={})
    assert response.status_code == 403
