import flask
from flask import request, jsonify
import db
import footballFuncs as ff

app = flask.Flask(__name__)
# app.config["DEBUG"] = True

@app.route("/", methods=["GET"])
def home():
    return "<h1>Wowee you did it this is a website</h1>"

@app.route("/api/v1/football-stats/teams", methods=["GET"])
def apiTeam():
    """
    /football-stats/teams?team=NAME&week=WEEKNUM
    """
    
    query_params = request.args

    name = ff.lengthenName(query_params.get('team').upper())
    week = query_params.get('week')

    results = db.find(int(week), name)
    
    return jsonify(results)

@app.route("/api/v1/football-stats/teams/all", methods=["GET"])
def apiAllTeams():
    query_params = request.args

    week = query_params.get('week')

    results = db.find_all(int(week))
    return jsonify(results)

@app.errorhandler(404)
def pageNotFound():
    return "<h1>404</h1><p>The resource could not be found</p>"

if __name__ == '__main__':
        import os  
        port = int(os.environ.get('PORT', 33507)) 
        app.run(host='0.0.0.0', port=port)