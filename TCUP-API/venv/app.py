from flask import Flask, send_from_directory, request, jsonify
import logging as log
# from pymongo import MongoClient
import os
app = Flask(__name__)
# client = MongoClient('mongodb://localhost:27017/')
# db = client['mydatabase']

# Serve Angular build files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_angular_build(path):
    # log.info(path)
    # app.logger.info(path, type(path))
    if path != "" and os.path.exists("./tcup-dashboard/" + path):
        
        # Set MIME type based on file extension
        if path.endswith('.js'):
            mimetype = 'application/javascript'
        elif path.endswith('.css'):
            mimetype = 'text/css'
        else:
            mimetype = None
        return send_from_directory("./tcup-dashboard/", path, mimetype=mimetype)
    else:
        return send_from_directory("./tcup-dashboard/", "index.html")

# @app.after_request
# def add_header(response):
#     response.cache_control.no_cache = True
#     response.cache_control.no_store = True
#     response.cache_control.must_revalidate = True
#     response.cache_control.max_age = 0
#     return response

# API endpoints that make queries to MongoDB
# @app.route('/api/users', methods=['GET'])
# def get_users():
#     users = db.users.find()
#     return jsonify(list(users))

# @app.route('/api/users', methods=['POST'])
# def create_user():
#     data = request.json
#     db.users.insert_one(data)
#     return jsonify({'message': 'User created successfully.'})

# @app.route('/api/users/<user_id>', methods=['GET'])
# def get_user(user_id):
#     user = db.users.find_one({'_id': user_id})
#     return jsonify(user)

if __name__ == '__main__':
    app.run(debug=True)
