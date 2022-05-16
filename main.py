from flask import *
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime
import re
import DB, utils


# Timeout duration in seconds for IP (Guestbook):
POST_TIMEOUT = 3600 # 3600s = 1h
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


public = Flask(__name__)
public.wsgi_app = ProxyFix(public.wsgi_app, x_for=1, x_host=1)


# /index
@public.route('/', methods=['GET'])
def index():
    return render_template('sites/index.html')

# /archive
@public.route('/archive', methods=['GET'])
def archive():
    posts = DB.getPostList()
    posts.reverse()

    return render_template('sites/archive.html', posts=posts)

@public.route('/posts/<postName>', methods=['GET'])
def posts(postName):
    postName = request.path[1:]
    post = DB.getPostByPostName(postName)

    if len(post) > 0:
        post = post[0]
                
        return render_template('sites/postTemplate.html', title=post[1], content=post[2])
    else:
        return not_found(None)

# /Guestbook
@public.route('/guestbook', methods=['GET'])
def guestbook():
    entries = DB.getMessages()
    entries.reverse()

    return render_template('sites/guestbook.html', entries=entries)

@public.route('/newGuestbookEntry', methods=['POST'])
def newGuestbookEntry():
    tmp = request.form

    if ('username' in tmp and tmp.get('username') != '') and canPlace(request):
        website = tmp.get('website')[:100]
        DB.newMessage(tmp.get('username')[:25], tmp.get('message')[:1000], re.sub('^http[s]?:\/\/', '', website))
        print(f"[{datetime.now().strftime(DATETIME_FORMAT)}] New Post from {request.remote_addr}")
    
    return redirect(url_for('guestbook'))

# /about
@public.route('/about', methods=['GET'])
def about():
    return render_template('sites/about.html')


# 404
@public.errorhandler(404)
def not_found(e):
    return render_template("sites/404.html"), 404



def canPlace(request):
    ip = request.remote_addr
    lastPost = DB.getLastComment(ip)

    if len(lastPost) > 0:
        lastPost = datetime.strptime(lastPost[0][1], DATETIME_FORMAT)
        now = datetime.now().strftime(DATETIME_FORMAT)
        now = datetime.strptime(now, DATETIME_FORMAT)
        
        diff = now - lastPost

        if diff.total_seconds() <= POST_TIMEOUT:
            return False
    
    DB.setLastPost(ip)
    return True