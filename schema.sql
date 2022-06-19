create table if not exists marka
(
id_marka integer primary key,
nazwa_marka text not null
);

create table if not exists model
(
id_model integer primary key,
id_marka integer not null,
nazwa_model text not null,
foreign key(id_marka) references marka(id_marka)
);

create table if not exists wpis
(
id_wpis integer primary key,
id_model integer not null,
spalanie_miasto float not null,
spalanie_trasa float not null,
cykl_mieszany float not null,
moc text not null,
foreign key(id_model) references model(id_model)
);