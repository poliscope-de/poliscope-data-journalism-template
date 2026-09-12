Dieses Projekt enthält mehrere Python-Module, die im Zuge einer datenjournalistischen Auswertung der Poliscope-Daten hilfreich sein können.

Je nach Anwendungsfall und Recherchefrage werden nicht alle Skripte benötigt, oder es müssen weitere eigene Filter ergänzt werden.

# Schnellstart

Wer nur schnell zu einem Thema recherchieren möchte, ohne sich mit den einzelnen Notebooks zu beschäftigen, kann direkt [00_ddj_template.ipynb](00_ddj_template.ipynb) öffnen: Dort müsst ihr nur ein Thema und eure Suchbegriffe eintragen, der Rest der Pipeline (Entities laden, suchen, gruppieren, auswerten, Grafiken erzeugen) läuft automatisch.

Voraussetzung dafür ist eine eingerichtete Python-Umgebung (venv) und eine ausgefüllte `.env`-Datei. Beides wird in den folgenden zwei Abschnitten für Einsteiger:innen erklärt.

# Einrichtung für Einsteiger:innen

## 1. Python-Umgebung (venv) einrichten

Eine "venv" (virtual environment) ist ein isolierter Ordner mit einer eigenen Python-Installation für dieses Projekt, damit sich die hier benötigten Pakete nicht mit anderen Projekten auf eurem Rechner in die Quere kommen.

Voraussetzung: [Python](https://www.python.org/downloads/) (Version 3.10 oder neuer) ist installiert. Unter Windows beim Installieren unbedingt das Häkchen bei **"Add python.exe to PATH"** setzen.

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
3. Speichern und Datei schließen. Die Notebooks laden die Werte automatisch über `setup.py` (bzw. `python-dotenv`).

Wichtig: Die `.env`-Datei niemals per E-Mail verschicken, in Screenshots zeigen oder in ein Git-Repository committen - sie enthält geheime Zugangsdaten.

## Maintenance des Templates

```bash
pip install -r requirements.txt
nbstripout --install
```

## Status

Das Basis-Template für die allgemeine Recherchepipeline ist abgeschlossen. Der AI-Classifer bleibt bewusst separat und ist nicht Teil der veröffentlichten Standard-Version des Templates.

## Zukünftige Erweiterungen

- Ein Skript, das pro Treffer die umgebenden Textschnipsel ausliefert (erleichtert AI-basierte oder manuelle Prüfung der Relevanz)
- Notebook für manuelle Treffer-Klassifikation
- Notebook für KI-gestützte Klassifikation