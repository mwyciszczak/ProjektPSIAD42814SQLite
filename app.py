from flask import Flask, render_template, request, redirect
import sqlite3
from ml import przewidywanie_spalanie


app = Flask(__name__)
db = sqlite3.connect('baza.db', check_same_thread=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wprowadzanie', methods=['POST', 'GET'])
def wprowadzanie():
    if request.method == 'POST':
        w = [request.form.get('lista_modele'),
                    request.form['sp_miasto'],
                    request.form['sp_trasa'],
                    request.form['sp_mieszane'],
                    request.form['moc']]
        cur = db.cursor()
        try:
            cur.execute("""insert into wpis (id_model, spalanie_miasto, spalanie_trasa, cykl_mieszany, moc) values (
                        (select id_model from model where nazwa_model = '{}'), {}, {}, {}, {})""".format(w[0], w[1], w[2], w[3], w[4]))
            db.commit()
        except:
            return redirect('/blad')

    cur = db.cursor()
    cur.execute("""select marka.nazwa_marka, model.nazwa_model, wpis.spalanie_miasto, wpis.spalanie_trasa, wpis.cykl_mieszany, wpis.moc, wpis.id_wpis
                    from marka, model, wpis
                    where
                    wpis.id_model = model.id_model and
                    model.id_model = marka.id_marka;""")
    wpisy = cur.fetchall()

    cur = db.cursor()
    cur.execute("select (select nazwa_marka from marka where marka.id_marka = model.id_marka), nazwa_model from model order by 1 asc")
    modele = cur.fetchall()

    cur = db.cursor()
    cur.execute("select nazwa_marka from marka order by 1 asc")
    marki = cur.fetchall()
    return render_template('wprowadzanie.html', wpisy=wpisy, modele=modele, marki=marki)


@app.route('/usun/<int:id>')
def usun(id):
    cur = db.cursor()
    cur.execute("delete from wpis where id_wpis = {}".format(id))
    db.commit()
    return redirect('/wprowadzanie')


@app.route('/uaktualnij/<int:id>', methods=['POST', 'GET'])
def uaktualnij(id):
    cur = db.cursor()
    cur.execute("""select marka.nazwa_marka, model.nazwa_model, wpis.spalanie_miasto, wpis.spalanie_trasa, wpis.cykl_mieszany, wpis.moc, wpis.id_wpis
                    from marka, model, wpis
                    where
                    wpis.id_model = model.id_model and
                    model.id_model = marka.id_marka and
                    wpis.id_wpis = {};""".format(id))
    wpis = cur.fetchall()

    if request.method == 'POST':
        w = [request.form.get('lista_modele'),
             request.form['sp_miasto'],
             request.form['sp_trasa'],
             request.form['sp_mieszane'],
             request.form['moc']]
        cur = db.cursor()
        try:
            cur.execute("""update wpis set id_model = (select id_model from model where nazwa_model = '{}'), spalanie_miasto = {}, 
            spalanie_trasa = {}, cykl_mieszany={}, moc={} where id_wpis = {}""".format(w[0], w[1], w[2], w[3], w[4], id))
            db.commit()
        except:
            return redirect('/blad')
        return redirect('/wprowadzanie')

    else:
        cur = db.cursor()
        cur.execute("select (select nazwa_marka from marka where marka.id_marka = model.id_marka), nazwa_model from model order by 1 asc")
        modele = cur.fetchall()

        cur = db.cursor()
        cur.execute("select nazwa_marka from marka order by 1 asc")
        marki = cur.fetchall()
        return render_template('uaktualnij.html', modele=modele, marki=marki, wpisy=wpis)


@app.route('/predicty', methods=['POST', 'GET'])
def predicty():

    if request.method == 'POST':
        cur = db.cursor()
        cur.execute("select spalanie_miasto, spalanie_trasa, cykl_mieszany, moc from wpis")
        wartosci = cur.fetchall()
        try:
            spalanie_klient = int(request.form.get('moc_klient'))
        except ValueError:
            spalanie_klient = 0

        rodzaj_spalania = request.form.get('spalania')
        spalanie = []
        moc = []
        spalanie_pred = 0
        if rodzaj_spalania == 'miasto':
            for x in wartosci:
                spalanie.append(float(x[0]))
                moc.append(float(x[3]))
            spalanie_pred = przewidywanie_spalanie(moc, spalanie, spalanie_klient)
        elif rodzaj_spalania == 'trasa':
            for x in wartosci:
                spalanie.append(float(x[1]))
                moc.append(float(x[3]))
            spalanie_pred = przewidywanie_spalanie(moc, spalanie, spalanie_klient)
        elif rodzaj_spalania == 'mieszany':
            for x in wartosci:
                spalanie.append(float(x[2]))
                moc.append(float(x[3]))
            spalanie_pred = przewidywanie_spalanie(moc, spalanie, spalanie_klient)

        return render_template('predicty.html', wynik=round(spalanie_pred, 2))
    else:
        return render_template('predicty.html')


@app.route('/o_autorze')
def o_autorze():
    return render_template('o_autorze.html')


@app.route('/blad')
def blad():
    return render_template('blad.html')


if __name__ == "__main__":
    app.run(debug=True)
