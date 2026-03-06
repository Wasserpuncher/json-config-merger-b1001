# JSON Config Merger

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Lizenz](https://img.shields.io/badge/license-MIT-green)
![GitHub Actions Workflow Status](https://github.com/your-username/json-config-merger/actions/workflows/python-app.yml/badge.svg)

Ein leistungsstarker und intelligenter JSON-Konfigurations-Merger, der für Unternehmensanwendungen entwickelt wurde und strategisches Zusammenführen, Schema-Validierung (geplant) und umgebungsspezifische Überschreibungen unterstützt. Dieses Tool bietet eine flexible Möglichkeit, mehrere JSON-Konfigurationsquellen zu einem einzigen, kohärenten Konfigurationsobjekt zu kombinieren, was für komplexe Anwendungsbereitstellungen unerlässlich ist.

## Funktionen

*   **Intelligentes Tiefen-Zusammenführen:** Rekursives Zusammenführen von Dictionary-Strukturen, das verschachtelte Konfigurationen elegant handhabt.
*   **Konfigurierbare Zusammenführungsstrategien:** Wählen Sie zwischen `OVERWRITE`, `DEEP_MERGE` und `APPEND_LIST` für eine feingranulare Kontrolle darüber, wie Konflikte und Listenelemente behandelt werden.
*   **Mehrere Eingabequellen:** Laden Sie Konfigurationen aus Dateien oder direkt aus JSON-Strings.
*   **Typsicherheit & Robustheit:** Entwickelt mit Python-Type-Hints und umfassender Fehlerbehandlung für einen zuverlässigen Betrieb.
*   **Erweiterbarkeit:** Mit einer OOP-Struktur konzipiert, die eine einfache Erweiterung um neue Funktionen wie Schema-Validierung, Umgebungsvariablen-Überschreibungen oder benutzerdefinierte Datenquellen ermöglicht.

## Installation

Dieses Projekt hat derzeit keine externen Abhängigkeiten über die Standardbibliothek von Python hinaus.

1.  **Repository klonen:**
    ```bash
    git clone https://github.com/your-username/json-config-merger.git
    cd json-config-merger
    ```

## Verwendung

So verwenden Sie den `JSONConfigMerger`, um Ihre Konfigurationen zu kombinieren:

```python
from main import JSONConfigMerger, MergeStrategy
import json

# Initialisieren Sie den Merger mit einer Standardstrategie (z.B. DEEP_MERGE)
merger = JSONConfigMerger(default_strategy=MergeStrategy.DEEP_MERGE)

# --- Beispiel 1: Zusammenführen aus Dateien ---
# Erstellen Sie einige Dummy-Konfigurationsdateien
with open("base_config.json", "w") as f:
    json.dump({"app_name": "MyBaseApp", "settings": {"debug": True, "log_level": "INFO"}, "features": ["auth", "logging"]}, f, indent=2)
with open("prod_config.json", "w") as f:
    json.dump({"app_name": "MyProdApp", "settings": {"debug": False, "log_level": "WARNING"}, "database": {"host": "prod-db", "port": 5432}, "features": ["metrics"]}, f, indent=2)

# Basis-Konfiguration laden
base_config = merger.load_config_file("base_config.json")
merger.merge(base_config)
print("Zusammengeführt nach base_config.json:", merger.get_merged_config())

# Produktionsspezifische Konfiguration laden und zusammenführen
# Hier werden 'app_name' und 'settings.debug' überschrieben.
# 'settings.log_level' wird aktualisiert.
# 'database' wird hinzugefügt.
# Die 'features'-Liste wird standardmäßig durch die DEEP_MERGE-Strategie überschrieben.
prod_config = merger.load_config_file("prod_config.json")
merger.merge(prod_config) # Verwendet die Standardstrategie (DEEP_MERGE)
print("\nZusammengeführt nach prod_config.json (DEEP_MERGE):", merger.get_merged_config())
# Erwartete Features: ["metrics"] (überschrieben)

# --- Beispiel 2: Zusammenführen mit der APPEND_LIST-Strategie ---
merger.reset() # Zurücksetzen für einen Neustart

# Basis-Konfiguration erneut laden
base_config_data = {"app_name": "MyApp", "modules": ["core", "api"], "config": {"timeout": 30}}
merger.merge(base_config_data)

# Umgebungsspezifische Konfiguration laden, Module anhängen
env_config_data = {"environment": "dev", "modules": ["dev_tools", "testing"], "config": {"retries": 5}}
merger.merge(env_config_data, strategy=MergeStrategy.APPEND_LIST) # Explizit APPEND_LIST verwenden

print("\nZusammengeführt mit APPEND_LIST-Strategie:", merger.get_merged_config())
# Erwartete Module: ["core", "api", "dev_tools", "testing"]
# Erwartete Konfiguration: {"timeout": 30, "retries": 5} (tief zusammengeführt)

# Dummy-Dateien bereinigen
import os
os.remove("base_config.json")
os.remove("prod_config.json")
```

## Projektstruktur

```
.
├── .github/
│   └── workflows/
│       └── python-app.yml     # GitHub Actions CI/CD Workflow
├── docs/
│   ├── architecture_en.md     # Detaillierte Architekturbeschreibung auf Englisch
│   └── architecture_de.md     # Detaillierte Architekturbeschreibung auf Deutsch
├── main.py                    # Kernlogik des JSON-Mergers (OOP, Type Hints, deutsche Kommentare)
├── test_main.py               # Unit-Tests für main.py
├── README.md                  # Projekt-README auf Englisch
├── README_de.md               # Projekt-README auf Deutsch
├── CONTRIBUTING.md            # Richtlinien für Beiträge zum Projekt
├── LICENSE                    # MIT-Lizenz
└── .gitignore                 # Standardmäßige .gitignore-Datei für Python
```

## Mitwirken

Wir freuen uns über Beiträge! Bitte beachten Sie die `CONTRIBUTING.md` für Richtlinien zum Einreichen von Fehlerberichten, Funktionsanfragen und Pull Requests.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert – weitere Details finden Sie in der Datei `LICENSE`.
