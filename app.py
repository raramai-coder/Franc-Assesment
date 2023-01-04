from flask import Flask, render_template, jsonify, Response, request

app = Flask(__name__)

@app.route('/')
def index_view():
    username = request.args.get('username')
    return render_template('index.html', username = username)

@app.route('/users')
def users_view():
    with open('./users.json', 'r') as f:
        users = f.read()
    return Response(users, mimetype="application/json")

@app.route('/posts')
def posts_view():
    with open('./posts.json', 'r') as f:
        posts = f.read()
    return Response(posts, mimetype="application/json")

if __name__ == '__main__':
    app.run(host='127.0.0.1')