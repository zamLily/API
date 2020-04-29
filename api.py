from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)


SERVERS = {}
server_id = 0

# have the server or not
def abort_if_server_doesnt_exist(server_id):
    if server_id not in SERVERS:
        abort(404, message="Server {} doesn't exist".format(server_id))


parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('ip')
parser.add_argument('status')

# single server
class Servers(Resource):
    def get(self, server_id):
        abort_if_server_doesnt_exist(server_id)
        return SERVERS[server_id]

    def delete(self, server_id):
        abort_if_server_doesnt_exist(server_id)
        del SERVERS[server_id]
        return '', 204

    def put(self, server_id):
        args = parser.parse_args()
        task = {'id': args['id'], 'ip': args['ip'], 'status': args['status']}
        SERVERS[server_id] = task
        return task, 201


# serverlist
class ServerList(Resource):
    def get(self):
        return SERVERS

    def post(self):
        args = parser.parse_args()
        server_id = args['id']
        SERVERS[server_id] = {'id': args['id'], 'ip': args['ip'], 'status': args['status']}
        return SERVERS[server_id], 201


# Actually setup the Api resource
api.add_resource(ServerList, '/servers')
api.add_resource(Servers, '/servers/<server_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
