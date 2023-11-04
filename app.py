from flask import Flask, render_template, request, redirect, url_for
import urllib.parse
from bson.objectid import ObjectId
import pymongo
import pandas as pd
import datetime
# from waitress import serve

app = Flask(__name__, template_folder='template')
app.secret_key = '04b5b13cbe98a52f7a8cd06b353e5e0c20d18e4b04b0d6125126fb687297b1b2'

# CLIENT = 'mongodb+srv://crefaz:Cr3faz123@cluster.tpxt8fp.mongodb.net/?retryWrites=true&w=majority'
CLIENT = f'mongodb+srv://{urllib.parse.quote_plus("felipequagliagambini")}:{urllib.parse.quote_plus("bPxvVuy7VoEql8h7")}@convidados.ku5xrqf.mongodb.net/'
DB = 'convidados'


def insert_db(_client, _db, _collection, dict):
    client = pymongo.MongoClient(_client)
    db = client.get_database(_db)
    collection = db.get_collection(_collection)
    collection.insert_one(dict)
    client.close()

def delete_db(_client, _db, _collection, id):
    client = pymongo.MongoClient(_client)
    db = client.get_database(_db)
    collection = db.get_collection(_collection)
    collection.delete_one({'_id': ObjectId(id)})
    client.close()

def read_db(_client, _db, _collection, filter=None):
    client = pymongo.MongoClient(_client)
    db = client.get_database(_db)
    collection = db.get_collection(_collection)
    data = [row for row in collection.find(filter)]
    df = pd.json_normalize(data)
    client.close()
    return df

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        nome = str(request.form['name']).strip().title()
        data_confirmacao = datetime.datetime.now()
        try:
            acompanhante = bool(request.form['acompanhantes'])
        except KeyError:
            acompanhante = False
        acompanhante
        convidado = {'nome': nome, 'acompanhante': acompanhante, 'datahora_confirmacao': data_confirmacao}
        insert_db(CLIENT, DB, 'lista_convidados', convidado)
        return render_template('index.html', dados={'nome': nome, 'show': True})

    return render_template('index.html', dados={'nome': '', 'show': False})

@app.route('/confirmacoes')
def confirmacoes():
    df = read_db(CLIENT, DB, 'lista_convidados')
    return render_template('Confirmado.html', dados={'df': df})


@app.route('/confirmacoes/delete/<id>', methods=['GET'])
def delete_painel(id):
    delete_db(CLIENT, DB, 'lista_convidados', id)
    return redirect(url_for('confirmacoes'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
 