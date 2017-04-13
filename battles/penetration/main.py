from flask import Flask, request, render_template
from contextlib import contextmanager
import sqlite3
from hashlib import md5


app = Flask(__name__, static_folder='static', static_url_path='')

DATABASE = "ips.db"

image_mappings = {
    "55f312f84e7785aa1efa552acbf251db": "cat1.jpg",
    "6d0443367e522b1f550ebbfa4e81b13a": "cat2.jpeg",
    "35ca49184b4fb3b425fb78be3d35282a": "cat3.png",
    "3747455f1b41e5355b3d5f313d73f07d": "cat4.jpg",
    "cf6555d45f3abd2a3e8f04729280a4ee": "enot5.jpeg",
    "eb371437ea2462882e1565723f0c8b8b": "cat6.jpg",
    "5a0ad51ace8a5101e143edfe2f264efd": "cat7.jpg",
    "db968881cd30343d156c038e53b0f180": "cat8.jpeg",
    "5c1aab3d3a70351eb28fc29e07731bb6": "panda9.gif"
}


@contextmanager
def db_connection():
    conn = sqlite3.connect(DATABASE)
    try:
        cursor = conn.cursor()
        cursor\
            .execute(
             'CREATE TABLE IF NOT EXISTS ips'
             ' (ip TEXT UNIQUE)'
        )
        yield cursor
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.commit()
        conn.close()


def add_ip(ip):
    with db_connection() as cursor:
        cursor.execute(
            'INSERT INTO ips VALUES (?)', (ip,))


def ip_in_db(ip):
    with db_connection() as cursor:
        cursor.execute(
            'SELECT * FROM ips WHERE ip=?', (ip,))
        row = cursor.fetchone()
    return row is not None


def next_url(old_url):
    return md5(("salt" + old_url).encode()).hexdigest()


@app.route("/")
def catch_first_request():
    if not ip_in_db(request.remote_addr):
        add_ip(request.remote_addr)
    return render_template("index.html", content={
        "link": next_url("1"),
        "text": "You need to go through 10 links and get the flag!"
    })


@app.route("/<some_hash>")
def catch_hash_page(some_hash):
    if ip_in_db(request.remote_addr):
        if some_hash in image_mappings:
            image = 'Banned!<p></p><img src="images/{}">'\
                .format(image_mappings[some_hash])
            return render_template(
                "index.html", content={"link": "", "text": image})
        else:
            return render_template(
                "index.html", content={"link": "", "text": "wrong way:("})

    add_ip(request.remote_addr)
    return render_template(
        "index.html",
        content={
            "link": next_url(some_hash),
            "text": "You're on the right way!"})


@app.route("/405a30b7c035bd6002ce49a921b9b0df")
def success():
    return render_template(
        "index.html",
        content={
            "text": "All done! <p></p> Flag: AllCatsAreCaught", "link": ""})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
