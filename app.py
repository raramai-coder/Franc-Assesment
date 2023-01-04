from flask import Flask, render_template, jsonify, Response, request
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index_view():
    username = request.args.get('username')
    with open('./posts.json', 'r') as f:
        data = json.load(f)
        #print(data['Kyle'][0]['status'])
    with open('./users.json', 'r') as f:
        userdata = json.load(f)
        #print(userdata['Franc'][0])
    return render_template('index.html', username = username, tweets = data, users = userdata, tweets_processor = tweets_processor())

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
def tweets_processor():
    tweets_dictionary = dict()
    following = []

    def format_time(date_str):
        date_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        return date_object

    def order_tweets():
        ordered_tweets= sorted(tweets_dictionary.items(), key=lambda x:x[1], reverse=True)
        #print(ordered_tweets)
        return ordered_tweets

    def get_tweets():
        username = request.args.get('username')
        
        with open('./posts.json', 'r') as f:
            all_tweets = json.load(f)
        with open('./users.json', 'r') as f:
            userdata = json.load(f)
        
        for user in userdata:
            if user in userdata[username]:
                #print(user)
                following.append(user)
            elif user == username:
                if len(user)!=0:
                    following.append(user)
        
        for tweet in all_tweets:
            if tweet in following:
                #print(all_tweets[tweet][0]['status'])
                values = range(len(all_tweets[tweet])) 
                for i in values:
                    status = all_tweets[tweet][i]['status']
                    time = format_time(all_tweets[tweet][i]['time'])
                    #print (time)
                    tweets_dictionary[status] = time
        
        #print(tweets_dictionary)


    #date_str = '2019-08-02T17:55:09Z'
    #date_object = datetime.strptime(date_str, '%Y-%d-%mT%H:%M:%SZ')
    get_tweets()
    tweets_dictionary = order_tweets()
    #print ("The date is", date_object)
    #return None
    return tweets_dictionary


if __name__ == '__main__':
    app.run(host='127.0.0.1')