import os
from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras
from waitress import serve

class DBManager:
    def __init__(self,
                 database=os.environ.get("POSTGRES_DB"),
                 host="db",
                 user=os.environ.get("POSTGRES_USER"),
                 password=os.environ.get("POSTGRES_PASSWORD")):
        self.connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password)

        self.connection.autocommit = True

        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

    def get_scores(self):
        sql = "SELECT * FROM scores;"
        self.cursor.execute(sql);
        return self.cursor.fetchall()

    def update_score(self, partyname, score):
        sql = "UPDATE scores SET score = %s WHERE partyname = %s;"
        self.cursor.execute(sql, (score, partyname))
        return True

    def remove_party(self, partyname):
        sql = "DELETE FROM scores WHERE partyname = %s;"
        self.cursor.execute(sql, (partyname,))
        return True

    def add_party(self, partyname):
        sql = "INSERT INTO scores (score, partyname) VALUES (0,%s);"
        self.cursor.execute(sql, (partyname,))
        return True

server = Flask(__name__)
conn = None

@server.route('/api/score', methods=['GET', 'PUT'])
def api_scores():
    global conn
    if not conn:
        conn = DBManager()
    if request.method == "GET":
        return jsonify({"success": True, "scores": conn.get_scores()})
    elif request.method == "PUT":
        if 'party' in request.json and 'value' in request.json:
            party = request.json['party']
            value = request.json['value']
            try:
                value = int(value)
            except ValueError:
                return jsonify({"success": False, "error": "Give integer value"})
            return jsonify({"success": conn.update_score(party, value)})
        else:
            return jsonify({"success": False, "error": "Give party name and score"})
    else:
        return jsonify({"success": False, "error": "Request type not supported"})

@server.route("/api/party", methods=['POST', 'DELETE'])
def api_party():
    global conn
    if not conn:
        conn = DBManager()
    if 'party' in request.json:
        party = request.json['party']
        if request.method == "POST":
            # add new party
            conn.add_party(party)
        elif request.method == "DELETE":
            # delete party
            conn.remove_party(party)
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Add party in request JSON"})

if __name__ == '__main__':
    #server.run(host='localhost', port=3000, debug=True)
    serve(server, listen='*:3000')
