# Experimentell: KI-gestützte Klassifikation

Dieses Notebook ist **nicht** Teil der Standard-Pipeline und wird nicht aktiv gepflegt. Es zeigt beispielhaft, wie Treffer pro Kommune mit einem LLM (über OpenRouter, optional mit dem Poliscope-MCP) nach Status klassifiziert werden können.

Voraussetzungen:

- `pip install -r experimental/ai_classifier/requirements-ai.txt` (zusätzlich zur normalen `requirements.txt`)
- `OPEN_ROUTER_KEY` in der `.env`
- eine Treffer-CSV mit den Spalten `context`, `date` und `hits` (wird von der Standard-Pipeline aktuell nicht erzeugt, Pfad in der Zelle "Analyse" anpassen)

Das Notebook wird aus dem Projekt-Root heraus ausgeführt (Kernel-Arbeitsverzeichnis = Projektordner), die erste Zelle setzt den Pfad entsprechend.
