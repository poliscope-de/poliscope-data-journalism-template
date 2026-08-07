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

Offen:
To Do: Babys von Hamburg und Berlin mit einbeziehen und entsprechend dokumentieren
finde die 4 fehlenden Großstädte

To Do: Dict für API responses, welches bei error direkt eine Erklärung mitliefert
TO Do: Liste für Start-Codes pro Bundesland, id vom Bundesland und *

Doku für venv creation mit anfügen, inklusive Windows specials
Doku für .evn creation
.env example
.gitkeep fürs Behalten von Ordnerstruktur

Doku 
Alles lässt sich paginieren, außer Search
Scan liefert Chunks


search endpoint: gruppiert Treffer in groups - und zwar entweder Document, oder Agenda Item, oder Proposal, je nachdem wo es im RIS visuell hängt


## Maintainance des Templates

```
pip install -r requirements.txt
nbstripout --install
```