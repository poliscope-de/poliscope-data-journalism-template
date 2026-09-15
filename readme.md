Dieses Projekt enthält ein Notebook und mehrere Python-Module, die im Zuge einer datenjournalistischen Auswertung der Poliscope-Daten hilfreich sein können.

Je nach Anwendungsfall und Recherchefrage werden nicht alle Funktionen benötigt, oder es müssen weitere eigene Filter ergänzt werden.

# Schnellstart

Wer nur schnell zu einem Thema recherchieren möchte, kann direkt [00_ddj_template.ipynb](00_ddj_template.ipynb) öffnen: Dort müsst ihr nur ein Thema und eure Suchbegriffe eintragen, der Rest der Pipeline (Entities laden, suchen, gruppieren, auswerten, Grafiken erzeugen) läuft automatisch.

Voraussetzung dafür ist eine eingerichtete Python-Umgebung (venv) und eine ausgefüllte `.env`-Datei. Beides wird in den folgenden zwei Abschnitten für Einsteiger:innen erklärt.

# Projektstruktur

| Pfad | Inhalt |
| --- | --- |
| `00_ddj_template.ipynb` | Die komplette Recherche-Pipeline als Notebook |
| `ddj_scripts/` | Wiederverwendbare Module: `entities.py` (Kommunen laden), `search.py` (Suche), `grouping.py` (Treffer zu Sitzungen/Vorgängen bündeln), `analysis.py` (Auswertungen, Theme) |
| `setup.py`, `api_client.py` | Laden der `.env`, API-Header und ein Request-Wrapper, der Rate-Limits der API automatisch beachtet |
| `data/metadata/`, `data/raw/`, `data/processed/` | Zwischenstände und Ergebnisse. Werden **nicht** in Git eingecheckt |
| `data/styles/` | Poliscope-Farbschema für Altair-Grafiken |
| `experimental/ai_classifier/` | Experimentelles Notebook zur KI-gestützten Klassifikation, nicht Teil der Standard-Pipeline |
| `tests/` | Unit-Tests für API-Wrapper und Auswertungslogik (`python -m unittest`) |

# Einrichtung für Einsteiger:innen

## 1. Python-Umgebung (venv) einrichten

Eine "venv" (virtual environment) ist ein isolierter Ordner mit einer eigenen Python-Installation für dieses Projekt, damit sich die hier benötigten Pakete nicht mit anderen Projekten auf eurem Rechner in die Quere kommen.

Voraussetzung: [Python](https://www.python.org/downloads/) (Version 3.11 oder neuer) ist installiert. Unter Windows beim Installieren unbedingt das Häkchen bei **"Add python.exe to PATH"** setzen.

**macOS / Linux** (Terminal, im Projektordner):

```bash
python3 -m venv poliscope-venv
source poliscope-venv/bin/activate
pip install -r requirements.txt
nbstripout --install
```

**Windows** (PowerShell, im Projektordner):

```powershell
py -m venv poliscope-venv
.\poliscope-venv\Scripts\Activate.ps1
pip install -r requirements.txt
nbstripout --install
```

Falls PowerShell die Aktivierung mit einem Fehler zu "Ausführung von Skripts deaktiviert" (execution policy) verweigert, einmalig folgenden Befehl in der PowerShell ausführen und danach die Aktivierung erneut versuchen:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Alternativ könnt ihr unter Windows auch die "Eingabeaufforderung" (cmd.exe) statt PowerShell verwenden, dort lautet der Aktivierungsbefehl:

```cmd
poliscope-venv\Scripts\activate.bat
```

Wenn die venv aktiv ist, steht `(poliscope-venv)` am Anfang der Terminalzeile. In VS Code müsst ihr zusätzlich oben rechts im Notebook den passenden Python-Kernel auswählen (`poliscope-venv`), damit die Notebooks die richtige Umgebung nutzen.

Die venv muss bei jeder neuen Terminal-Sitzung erneut aktiviert werden (Notebooks in VS Code übernehmen den ausgewählten Kernel automatisch, dafür braucht es kein Aktivieren im Terminal).

`nbstripout --install` sorgt dafür, dass beim Committen die Ausgaben (Tabellen, Grafiken, Zwischenergebnisse) automatisch aus den Notebooks entfernt werden. So landen keine Daten versehentlich in Git.

## 2. `.env`-Datei einrichten

Die `.env`-Datei enthält eure persönlichen API-Zugangsdaten. Sie wird **nicht** in Git eingecheckt (siehe `.gitignore`), damit niemand versehentlich seine Schlüssel veröffentlicht.

1. Kopiert die Datei `.env.example` und benennt die Kopie in `.env` um (im selben Ordner).
   - macOS/Linux: `cp .env.example .env`
   - Windows (PowerShell): `Copy-Item .env.example .env`
2. Öffnet `.env` in einem Texteditor und tragt eure eigenen Werte hinter dem `=` ein, z. B.:
   ```
   POLISCOPE_API_URL=https://api.poliscope.de/v2
   POLISCOPE_API_KEY=euer-poliscope-api-schluessel
   POLISCOPE_CLIENT_NAME=euer-client-name
   OPEN_ROUTER_KEY=euer-openrouter-schluessel
   ```
   `OPEN_ROUTER_KEY` wird nur für das experimentelle KI-Notebook gebraucht und kann sonst leer bleiben.
3. Speichern und Datei schließen. Das Notebook lädt die Werte automatisch über `setup.py` (bzw. `python-dotenv`).

Wichtig: Die `.env`-Datei niemals per E-Mail verschicken, in Screenshots zeigen oder in ein Git-Repository committen - sie enthält geheime Zugangsdaten.

# Hinweise zur Arbeit mit den Daten

- Die Kommunen-IDs (amtliche Regionalschlüssel wie `03401`) haben führende Nullen. Wer gespeicherte CSVs wieder einliest, sollte dafür `ddj_scripts.search.load_search_results` bzw. `ddj_scripts.entities.load_entities` nutzen, sonst macht pandas aus `03401` die Zahl `3401` und die Zuordnung zu Kommunen schlägt fehl.
- Poliscope bietet erst ab etwa Anfang 2024 einen nahezu vollständigen Datensatz. Zeitliche Auswertungen sollten daher nicht zu weit zurückreichen (Standard im Template: ab Mitte 2023).

# Maintenance des Templates

```bash
pip install -r requirements.txt
nbstripout --install
python -m unittest
```

## Status

Das Basis-Template für die allgemeine Recherchepipeline ist abgeschlossen. Der AI-Classifier bleibt bewusst separat unter `experimental/` und ist nicht Teil der Standard-Version des Templates.

## Zukünftige Erweiterungen

- Ein Skript, das pro Treffer die umgebenden Textschnipsel ausliefert (erleichtert AI-basierte oder manuelle Prüfung der Relevanz)
- Notebook für manuelle Treffer-Klassifikation
- Überführung des experimentellen KI-Classifiers in die Standard-Pipeline
