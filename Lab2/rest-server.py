from flask import Flask, make_response, g, request
from flask.helpers import make_response, send_file
import sqlite3
import base64

app = Flask(__name__) 

@app.route('/')
def hello():
    return make_response({'message': 'Hello World'})

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            'files.db',
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
 
def write_file(filename, data):
    #binary_data = base64.b64decode(data)
    #base64_string = base64.b64encode(binary_data)
    if not filename:
        filename_len = 8
        filename = ''.join([random.SystemRandom().choice(string.ascii_letters + string.digits) for n in range(filename_len)])
        filename += '.bin'
    try:
        file = open('./'+filename+'.bin', 'wb')
        file.close()
        with open('./'+filename+'.bin', 'r+b') as f:
            f.write(data)
    except EnvironmentError as e:
        print(f'Error writing file: {e}')
        return None
    return filename

 
@app.route('/files', methods=['POST'])
def add_files():
    payload = request.get_json()
    filename = payload.get('filename')
    content_type = payload.get('content_type')
    file_data = base64.b64decode(payload.get('contents_b64'))
    size = len(file_data)

    blob_name = write_file(filename, file_data)

    db = get_db()
    cursor = db.execute(
        "INSERT INTO 'file'('filename', 'size', 'content_type', 'blob_name') VALUES (?,?,?,?)",
        (filename, size, content_type, blob_name)
    )
    db.commit()

    return make_response({"id":cursor.lastrowid}, 201)


@app.route('/files', methods=['GET'])
def list_files():
    db = get_db()
    cursor = db.execute("SELECT * FROM 'file'")
    if not cursor:
        return make_response({"message": "Error connection to the database"}, 500)
    files = cursor.fetchall()

    files = [dict(f) for f in files]
    return make_response({"files":files})


@app.route('/files/<int:file_id>', methods=['GET'])
def download_file(file_id):
    db = get_db()
    print(file_id)
    cursor = db.execute("SELECT * FROM 'file' WHERE 'id'=?", [file_id])
    print(cursor)
    if not cursor:
        return make_response({"message": "Error connecting to database"}, 500)
    f = cursor.fetchone()
    print(f)
    f = dict(f)
    print("File requested: {}".format(f))
    return send_file(f['blob_name'], mimetype=f['content_type'])


# Close the DB connection after serving a request 
app.teardown_appcontext(close_db) 

app.run(host="localhost", port=9000)