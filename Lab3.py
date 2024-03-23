import os
import time
import threading
import json

cale_director = "E:\TEMPORARE\OOP_Mihai"
cale_snapshot = os.path.join(cale_director, "SnapShots")

timp_snapshot = None
snapshot_curent = []
ultimul_commit = []
snapshot_anterior = []
lista_fisiere_curenta = []
lista_fisiere = os.listdir(cale_director)

class DateFisier:
    def __init__(self, nume_fisier, dimensiune, creat, modificat):
        self.nume_fisier = nume_fisier
        self.dimensiune = dimensiune
        self.creat = creat
        self.modificat = modificat

def preia_date_fisier(nume_fisier):
    cale_fisier = os.path.join(cale_director, nume_fisier)
    if not os.path.exists(cale_fisier):
        print(f"Fisierul '{nume_fisier}' nu a fost gasit.")
        return None

    stat = os.stat(cale_fisier)
    date_fisier = DateFisier(
        nume_fisier=nume_fisier,
        dimensiune=stat.st_size,
        creat=time.ctime(stat.st_ctime),
        modificat=time.ctime(stat.st_mtime)
    )
    return date_fisier

def gaseste_fisiere():
    lista_date_fisiere = []
    for nume_fisier in lista_fisiere:
        date_fisier = preia_date_fisier(nume_fisier)
        if date_fisier:
            lista_date_fisiere.append(date_fisier)
    return lista_date_fisiere

def salveaza_snapshot(nume_snapshot):
    global snapshot_curent

    snapshot_curent = gaseste_fisiere()
    date_snapshot = json.dumps([ob.__dict__ for ob in snapshot_curent], indent=2)

    cale_fisier_snapshot = os.path.join(cale_snapshot, nume_snapshot)
    cale_fisier_timp_snapshot = os.path.join(cale_snapshot, "Creat.txt")

    snap = time.time()
    with open(cale_fisier_timp_snapshot, "w") as sTime:
        sTime.write(f"{time.ctime(snap)}\n")

    with open(cale_fisier_snapshot, "w") as fisier_snapshot:
        fisier_snapshot.write(date_snapshot)
        print(f"Snapshot salvat in {nume_snapshot}")

def citeste_snapshot(nume_snapshot):
    global timp_snapshot
    cale_fisier_snapshot = os.path.join(cale_snapshot, nume_snapshot)
    cale_fisier_timp_snapshot = os.path.join(cale_snapshot, "Creat.txt")

    with open(cale_fisier_timp_snapshot, 'r') as t:
        timp_snapshot = t.read().strip()

    with open(cale_fisier_snapshot, 'r') as fisier_json:
        date = json.load(fisier_json)

    lista_date_fisiere = []
    for item in date:
        date_fisier = DateFisier(
            nume_fisier=item['nume_fisier'],
            dimensiune=item['dimensiune'],
            creat=item['creat'],
            modificat=item['modificat']
        )
        lista_date_fisiere.append(date_fisier)
    return lista_date_fisiere

def afiseaza_date_fisier(lista_fisiere):
    if lista_fisiere:
        print("Lista de fisiere nu este goala:")
    else:
        print("Lista de fisiere este goala")

    for fisier in lista_fisiere:
        print(f"Fisier: {fisier.nume_fisier}\t\t{fisier.dimensiune} bytes\t\tCreat: {fisier.creat}\t\tModificat: {fisier.modificat}")
def verifica_modificari(lista_prima, lista_ultima):
    nume_fisiere_ultima = {date_fisier.nume_fisier for date_fisier in lista_ultima}

    for date_fisier_curent in lista_prima:
        if date_fisier_curent.nume_fisier not in nume_fisiere_ultima:
            print(f"{date_fisier_curent.nume_fisier} - Fisier nou")
        else:
            date_fisier_ultim = next(date_fisier for date_fisier in lista_ultima if date_fisier.nume_fisier == date_fisier_curent.nume_fisier)
            if date_fisier_curent.modificat != date_fisier_ultim.modificat or date_fisier_curent.dimensiune != date_fisier_ultim.dimensiune:
                print(f"{date_fisier_curent.nume_fisier} - A fost modificat")

    for date_fisier_ultim in lista_ultima:
        if date_fisier_ultim.nume_fisier not in {date_fisier.nume_fisier for date_fisier in lista_prima}:
            print(f"{date_fisier_ultim.nume_fisier} - A fost șters")

while True:
    ultimul_commit = snapshot_anterior = snapshot_curent = citeste_snapshot("Snapshot.json")
    thread = threading.Thread(target=repeta_verificare, daemon=True)
    thread.start()

    actiune = input("Introduceți acțiunea (commit | info | status | exit): ").strip().lower()

    if actiune == "commit":
        salveaza_snapshot("Snapshot.json")
    elif actiune == "info":
        afiseaza_date_fisier(snapshot_curent)
    elif actiune == "status":
        snapshot_curent = gaseste_fisiere()
        verifica_modificari(snapshot_curent, ultimul_commit)
    elif actiune == "exit":
        print("Programul se închide.")
        break
    else:
        print("Acțiune invalidă. Acțiunile disponibile sunt: (commit | info | status | exit)")
