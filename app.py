from flask import Flask, render_template, jsonify, Response, request
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index_view():
    username = request.args.get('username')
    return render_template('index.html', username = username, ordered_posts = posts_processor())

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

@app.context_processor
def posts_processor():
    posts_dictionary = dict()
    following = []
    username = request.args.get('username')

    def format_time(date_str):
        date_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        return date_object

    def order_posts():
        ordered_posts= sorted(posts_dictionary.items(), key=lambda x:x[1], reverse=True)
        return ordered_posts

    def get_posts():
        with open('./posts.json', 'r') as f:
            all_posts = json.load(f)
        with open('./users.json', 'r') as f:
            userdata = json.load(f)
        
        for user in userdata:
            if user in userdata[username]:
                following.append(user)
            elif user == username:
                if len(user)!=0:
                    following.append(user)
        
        for post in all_posts:
            if post in following:
                values = range(len(all_posts[post])) 
                for i in values:
                    status = all_posts[post][i]['status']
                    time = format_time(all_posts[post][i]['time'])
                    posts_dictionary[status] = [time,post]
 

    if username !=None:
        get_posts()
        posts_dictionary = order_posts()

    return posts_dictionary


if __name__ == '__main__':
    app.run(host='127.0.0.1')