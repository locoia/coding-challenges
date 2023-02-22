"""
Exposes a simple HTTP API to search a users Gists via a regular expression.

Github provides the Gist service as a pastebin analog for sharing code and
other develpment artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""

import requests, json   
from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route("/ping")
def ping():
    """Provide a static response to a simple GET request."""
    return "pong"

@app.route("/user/<string:username>")
def gists_for_user(username: str):
    """Provides the list of gist metadata for a given user.

    This abstracts the /users/:username/gist endpoint from the Github API.
    See https://developer.github.com/v3/gists/#list-a-users-gists for
    more information.

    Args:
        username (string): the user to query gists for

    Returns:
        The dict parsed from the json response from the Github API.  See
        the above URL for details of the expected structure.
    """
    

    dic_results = {}
    gists_url = 'https://api.github.com/users/{username}/gists'.format(username=username)
    response = requests.get(gists_url)
    diction=response.json()
    dic_results['User']=username
    for n in diction:
        dic_results['Files']=n['files']      
        dic_results['User_url']=n["owner"]["html_url"]

    return dic_results
    

@app.route("/api/v1/search", methods=['POST'])
def search():
    """Provides matches for a single pattern across a single users gists.

    Pulls down a list of all gists for a given user and then searches
    each gist for a given regular expression.

    Returns:
        A Flask Response object of type application/json.  The result
        object contains the list of matches along with a 'status' key
        indicating any failure conditions.
    """
    request_data = request.get_json()

    username = request_data['username']
    pattern = request_data['pattern']

    if username=="" or username==None or pattern==None or pattern=="":
        return "You need a user and a pattern", 400

    gists_url = 'https://api.github.com/search/code?q={pattern}+user:{username}'.format(username=username, pattern=pattern)
    response = requests.get(gists_url)      
    gists = response.json()

    clean_results=[]

    for data in gists['items']:
        clean_results.append({"Repository_name": data['repository']['name'],
                              "File_name": data['path'],
                              "HTML_url_file":data['html_url'],
                            })


    result = {}
    result['status'] = 'success'
    result['username'] = username
    result['pattern'] = pattern
    if clean_results==[]:
        result['matches'] = "Matches not found"
    else:
        result['matches'] = clean_results

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9876)
