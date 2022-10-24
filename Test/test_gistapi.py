import gistapi
import json
import pytest




@pytest.fixture
def client(request):
    # db_fd, gistapi.app.config['DATABASE'] = tempfile.mkstemp()
    gistapi.app.config['TESTING'] = True
    client = gistapi.app.test_client()

    # with gistapi.app.app_context():
    #    gistapi.init_db()
    
    # def teardown():
    #    os.close(db_fd)
    #    os.unlink(flaskr.app.config['DATABASE'])
    # request.addfinalizer(teardown)

    return client


def test_ping(client):
    rv = client.get('/ping')
    assert b'pong' in rv.data


def test_search(client):
    post_data = {'username': 'justdionysus', 'pattern': 'import requests'}
    rv = client.post('/api/v1/search', 
                     data=json.dumps(post_data),
                     headers={'content-type':'application/json'})
    result_dict = json.loads(rv.data.decode('utf-8'))
    expected_dict = {'status': 'success', 
                     'username': 'justdionysus',
                     'pattern': 'import requests',
                     'matches': [['https://gist.github.com/justdionysus/65e6162d99c2e2ea8049b0584dd00912']]}
    assert result_dict == expected_dict

