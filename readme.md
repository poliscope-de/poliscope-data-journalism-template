Dieses Projekt enthält mehrere Python-Jupyter-Notebooks, die im Zuge einer datenjournalistischen Auswertung der Poliscope-Daten hilfreich sein können.

Je nach Anwendungsfall und Recherchefrage werden nicht alle Skripte benötigt, oder es müssen weitere eigene Filter ergänzt werden.

# 01_get_entities

Wenn wir Suchen nur über ein bestimmtes Set an Kommunen laufen lassen möchten, benötigen wir eine Liste der jeweiligen RIS of interest. Das Skript get_entites lädt alle aktuell angebundenen RIS inklusive Metadaten. Im Anschluss können daraus gefilterte Listen erstellt werden, die dazu dienen, im nächsten Schritt Daten für diese Kommunen zu ziehen.


# 02_find_agendaItems

# To Do

Done:
Wrapper für allgemeine API Anfragen
- soll auf Rate Limit reagieren, wenn der Header da was problematisches zurückmeldet (retry after)
- nach jeder Anfrage 100ms timeout
- die 60s Pause brauche ich dann nicht mehr, weil der wrapper aus 429 erfährt, wie lange er warten muss
- Dict für API responses, welches bei error direkt eine Erklärung mitliefert
- degurba Codes ergänzt
- east west classification ergänzt

Offen für Scicar:
- Großstadt-Filterung in der get_entities: Babys von Hamburg und Berlin mit einbeziehen und entsprechend dokumentieren + finde die 4 fehlenden Großstädte
- Skript anlegen, welches die bestehenden pipt. User sollen nur Thema für die research und einen search string eingeben müssen, um output zu erhalten
- Doku für venv creation für Laien ergänzen, inklusive spezielle Anforderungen für Windows
- Doku für .env creation ergänzen für Laien
- .env example anlegen
- .gitkeep fürs Behalten von Ordnerstruktur
- eine Recherche finalisieren und veröffentlichen

Offen Longterm:
- git so einrichten, dass Notebook-Output nicht mit angelegt wird
- get context skript anlegen
- manual classifier template anlegen
- ai classifier template anlegen





## Maintainance des Templates

```
pip install -r requirements.txt
nbstripout --install
```