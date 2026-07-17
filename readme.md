Dieses Projekt enthält mehrere Python-Jupyter-Notebooks, die im Zuge einer datenjournalistischen Auswertung der Poliscope-Daten hilfreich sein können.

Je nach Anwendungsfall und Recherchefrage werden nicht alle Skripte benötigt, oder es müssen weitere eigene Filter ergänzt werden.

# 01_get_entities

Wenn wir Suchen nur über ein bestimmtes Set an Kommunen laufen lassen möchten, benötigen wir eine Liste der jeweiligen RIS of interest. Das Skript get_entites lädt alle aktuell angebundenen RIS inklusive Metadaten. Im Anschluss können daraus gefilterte Listen erstellt werden, die dazu dienen, im nächsten Schritt Daten für diese Kommunen zu ziehen.

# 02_find_agendaItems