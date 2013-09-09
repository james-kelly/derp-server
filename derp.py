from flask import Flask, render_template_string, redirect, url_for
from random import randint
from datetime import datetime

app = Flask(__name__)
app.debug = True

def rps():

    if getattr(app, 'start_time', None):
        try:
            app.request_count += 1
            timedelta = datetime.utcnow() - app.start_time
            app.logger.debug("R: %d, RPS: %s" % (app.request_count, app.request_count / timedelta.seconds))
        except:
            pass
    else:
        app.start_time = datetime.utcnow()
        app.request_count = 1


def rand_depth(max=0):
    return "../" * randint(0, max)

def rand_file():
     exts = ['html','html','html','html','html','html','html','html','pdf','jpg']
     return ".".join([
         str(randint(0, 10000)),
         exts[randint(0, len(exts) - 1)]
         ])


@app.route('/')
@app.route('/<path:path>')
def derp(path = '.'):
    rps()

    template = """<!doctype html>Here's some links!<br/>{% for l in links %}<a href="/{{path}}/{{l}}">{{l}}</a><br/>{% endfor %}"""
    num_links = getattr(app, 'num_links', 100)

    depth = len(path.split('/'))
    links = [ rand_depth(depth) + rand_file() for _ in range(num_links)]

    return render_template_string(template, links=links, path=path)


@app.route('/reset')
def reset():
    app.start_time = datetime.utcnow()
    app.request_count = 1

    return redirect(url_for('derp'))

@app.route('/num_links/<int:num_links>')
def num_links(num_links=100):
    app.num_links = num_links

    return redirect(url_for('derp'))




if __name__ == "__main__":
    app.run('0.0.0.0', 5050)
