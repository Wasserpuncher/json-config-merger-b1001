# Architektur des JSON Config Mergers

Dieses Dokument beschreibt das architektonische Design des Projekts `json-config-merger`. Die Kernidee ist es, einen robusten, erweiterbaren und intelligenten Mechanismus zum Kombinieren von JSON-Konfigurationen aus verschiedenen Quellen bereitzustellen, der den Anforderungen von Unternehmensanwendungen gerecht wird.

## Kernprinzipien

*   **Modularität:** Trennung der Zuständigkeiten in verschiedene Komponenten (Lader, Zusammenführungslogik).
*   **Flexibilität:** Unterstützung verschiedener Zusammenführungsstrategien und einfache Erweiterung für neue Quellen oder Validierungsmethoden.
*   **Robustheit:** Umfassende Fehlerbehandlung für Dateivorgänge und JSON-Parsing.
*   **Lesbarkeit:** Sauberer, gut dokumentierter Code mit Typ-Hints für Wartbarkeit.

## Überblick auf hoher Ebene

Der `JSONConfigMerger` arbeitet um ein zentrales `merged_config`-Dictionary herum, das durch das Anwenden neuer Konfigurationen schrittweise aufgebaut wird. Der Prozess umfasst:

1.  **Konfigurationsladen:** Abrufen von JSON-Daten aus den angegebenen Quellen (Dateien oder Strings).
2.  **Zusammenführungs-Engine:** Anwenden einer oder mehrerer eingehender Konfigurationen auf die aktuelle `merged_config` basierend auf einer gewählten Strategie.

```mermaid
graph TD
    A[Start] --> B(JSONConfigMerger initialisieren);
    B --> C{Konfigurationsquelle laden};
    C -- Aus Datei --> D[load_config_file(Pfad)];
    C -- Aus String --> E[load_config_string(String)];
    D --> F{Geparsedte Konfiguration (Dict)};
    E --> F;
    F --> G[merge(neue_Konfiguration, Strategie)];
    G --> H{Zusammenführungsstrategie anwenden};
    H -- OVERWRITE --> I[Gesamte Konfiguration ersetzen];
    H -- DEEP_MERGE / APPEND_LIST --> J[Dictionaries rekursiv zusammenführen];
    J -- Listen behandeln (Anhängen/Überschreiben) --> K[merged_config aktualisieren];
    K --> L[get_merged_config()];
    L --> M[Ende];
```

## Schlüsselkomponenten

### `JSONConfigMerger`-Klasse

Dies ist der Haupteinstiegspunkt für die Bibliothek. Sie kapselt den Zustand (`merged_config`) und bietet die primäre Schnittstelle zum Laden und Zusammenführen von Konfigurationen.

*   **`__init__(self, default_strategy: MergeStrategy)`:**
    *   Initialisiert den Merger mit einer leeren `merged_config` und einer `default_strategy` (z.B. `DEEP_MERGE`).
    *   Das `MergeStrategy`-Enum definiert die verfügbaren Strategien (`OVERWRITE`, `DEEP_MERGE`, `APPEND_LIST`).

*   **`load_config_file(self, file_path: str) -> Dict[str, Any]`:**
    *   Verantwortlich für das Lesen einer JSON-Datei vom Dateisystem.
    *   Behandelt `FileNotFoundError`, wenn die Datei nicht existiert, und `json.JSONDecodeError` für ungültigen JSON-Inhalt.
    *   Stellt sicher, dass die Wurzel des JSON ein Dictionary ist.

*   **`load_config_string(self, config_string: str) -> Dict[str, Any]`:**
    *   Parst einen JSON-String direkt.
    *   Behandelt `json.JSONDecodeError` für ungültige JSON-Strings.
    *   Stellt sicher, dass die Wurzel des JSON ein Dictionary ist.

*   **`merge(self, new_config: Dict[str, Any], strategy: Optional[MergeStrategy] = None) -> None`:**
    *   Die Kernmethode zum Kombinieren von Konfigurationen.
    *   Nimmt ein `new_config`-Dictionary und eine optionale `strategy` entgegen. Wenn `strategy` `None` ist, wird `self.default_strategy` verwendet.
    *   Delegiert an die interne `_deep_merge`-Methode oder überschreibt `self.merged_config` direkt, basierend auf der gewählten Strategie.

*   **`_deep_merge(self, base: Dict[str, Any], new: Dict[str, Any], strategy: MergeStrategy) -> Dict[str, Any]`:**
    *   Eine private, rekursive Hilfsmethode, die die eigentliche Tiefen-Zusammenführungslogik ausführt.
    *   Iteriert über Schlüssel in der `new`-Konfiguration:
        *   Wenn ein Schlüssel sowohl in `base` als auch in `new` existiert und beide Werte Dictionaries sind, wird `_deep_merge` rekursiv aufgerufen.
        *   Wenn beide Werte Listen sind, wird die spezifische Listenbehandlung basierend auf der `strategy` angewendet (`APPEND_LIST` oder Überschreiben für andere).
        *   Für alle anderen Typen oder Typ-Fehlpaarungen überschreibt der `new`-Wert den `base`-Wert.
        *   Wenn ein Schlüssel nur in `new` existiert, wird er zu `base` hinzugefügt.

*   **`get_merged_config(self) -> Dict[str, Any]`:**
    *   Gibt eine *Kopie* der aktuell zusammengeführten Konfiguration zurück, um eine externe Modifikation des internen Zustands zu verhindern.

*   **`reset(self) -> None`:**
    *   Setzt die `merged_config` auf ein leeres Dictionary zurück, nützlich, um einen neuen Zusammenführungsvorgang zu starten.

### `MergeStrategy`-Enum

Ein `Enum`, das die verschiedenen Arten definiert, wie Konfigurationen zusammengeführt werden können:

*   **`OVERWRITE`:** Die eingehende Konfiguration ersetzt die bestehende `merged_config` vollständig.
*   **`DEEP_MERGE`:** Dictionaries werden rekursiv zusammengeführt. Wenn ein Schlüssel in beiden existiert und beide Werte Dictionaries sind, werden sie zusammengeführt. Wenn Werte Listen sind, überschreibt die neue Liste die bestehende. Primitive Werte werden überschrieben.
*   **`APPEND_LIST`:** Ähnlich wie `DEEP_MERGE` für Dictionaries und Primitive, aber wenn beide Werte Listen sind, werden die Elemente der neuen Liste an die bestehende Liste angehängt.

## Fehlerbehandlung

Das System ist so konzipiert, dass es klare Fehlermeldungen für häufige Probleme liefert:

*   `FileNotFoundError`: Wenn eine angegebene Konfigurationsdatei nicht existiert.
*   `json.JSONDecodeError`: Wenn eine Datei oder ein String fehlerhaftes JSON enthält.
*   `TypeError`: Wenn die Wurzel einer Konfiguration (Datei oder String) kein JSON-Objekt (Dictionary) ist.
*   `ValueError`: Für unbekannte oder nicht unterstützte Zusammenführungsstrategien.

## Erweiterungspunkte (Zukünftige Verbesserungen)

Die aktuelle Architektur bildet eine solide Grundlage für zukünftiges Wachstum:

*   **Schema-Validierung:** Integration mit Bibliotheken wie `jsonschema`, um Konfigurationen vor oder nach dem Zusammenführen gegen ein definiertes Schema zu validieren. Dies würde eine `is_valid`-Methode oder einen `validate`-Schritt im Zusammenführungsprozess hinzufügen.
*   **Umgebungsvariablen:** Ein Mechanismus zum Überschreiben spezifischer Konfigurationswerte mithilfe von Umgebungsvariablen (z.B. `APP_SETTINGS_DEBUG=false`).
*   **Benutzerdefinierte Lader:** Unterstützung für andere Konfigurationsformate (YAML, TOML) oder Datenquellen (Datenbanken, Remote-URLs). Dies könnte eine abstrakte `ConfigLoader`-Schnittstelle umfassen.
*   **Erweiterte Zusammenführungsregeln:** Komplexere Zusammenführungsregeln, z.B. das Zusammenführen von Objekt-Arrays basierend auf einem eindeutigen Bezeichner.
*   **Änderungsverfolgung:** Optionales Speichern einer Historie von Zusammenführungen oder Identifizierung, welche Quelle welchen Wert beigesteuert hat.

Durch die Einhaltung dieses modularen und strategiebasierten Designs soll der `json-config-merger` ein flexibles und zuverlässiges Werkzeug für die Verwaltung komplexer Anwendungskonfigurationen sein.
