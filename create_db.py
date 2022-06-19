import sqlite3

con = sqlite3.connect('baza.db')

with open('schema.sql') as f:
    con.executescript(f.read())

#con.execute("insert into marka (nazwa_marka) values ('BMW'),('Audi'),('Toyota'),('Nissan'),('Mitsubishi');")
#con.execute("insert into model (nazwa_model, id_marka) values ('Seria 5', (select id_marka from marka where nazwa_marka = 'BMW'));")
#con.execute("insert into model (nazwa_model, id_marka) values ('A4', 2), ('Avensis', 3), ('Primera', 4), ('Galant', 5);")
#con.execute("insert into wpis (id_model, spalanie_miasto, spalanie_trasa, cykl_mieszany, moc) values (1, 12, 10, 11, 195), (5, 8, 6, 7, 120);")
#con.commit()
