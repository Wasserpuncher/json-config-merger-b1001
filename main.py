import argparse
import json
import sys
from enum import Enum
from typing import Any, Dict, List, Optional
import os

class MergeStrategy(Enum):
    """
    Definiert die Strategien zum Zusammenführen von Konfigurationen.
    Defines strategies for merging configurations.
    """
    OVERWRITE = "overwrite"  # Überschreibt Werte vollständig. Overwrites values completely.
    DEEP_MERGE = "deep_merge"  # Führt Dictionaries rekursiv zusammen, Listen werden überschrieben. Recursively merges dictionaries, lists are overwritten.
    APPEND_LIST = "append_list" # Führt Dictionaries rekursiv zusammen, Listen werden angehängt. Recursively merges dictionaries, lists are appended.

class JSONConfigMerger:
    """
    Eine Klasse zum intelligenten Zusammenführen von JSON-Konfigurationsdateien.
    Unterstützt verschiedene Zusammenführungsstrategien und das Laden aus Dateien oder Strings.

    A class for intelligently merging JSON configuration files.
    Supports various merge strategies and loading from files or strings.
    """

    def __init__(self, default_strategy: MergeStrategy = MergeStrategy.DEEP_MERGE):
        """
        Initialisiert den JSONConfigMerger mit einer Standard-Zusammenführungsstrategie.
        Initializes the JSONConfigMerger with a default merge strategy.

        :param default_strategy: Die Standardstrategie für das Zusammenführen.
                                 The default strategy for merging.
        :type default_strategy: MergeStrategy
        """
        self.merged_config: Dict[str, Any] = {} # Das Ergebnis der zusammengeführten Konfiguration. The result of the merged configuration.
        self.default_strategy = default_strategy # Die voreingestellte Strategie. The default strategy.

    def _deep_merge(self, base: Dict[str, Any], new: Dict[str, Any], strategy: MergeStrategy) -> Dict[str, Any]:
        """
        Führt zwei Dictionaries rekursiv zusammen basierend auf der angegebenen Strategie.
        Recursively merges two dictionaries based on the specified strategy.

        :param base: Das Basis-Dictionary, in das neue Werte integriert werden.
                     The base dictionary into which new values are integrated.
        :type base: Dict[str, Any]
        :param new: Das neue Dictionary, dessen Werte die Basis aktualisieren oder erweitern.
                    The new dictionary whose values update or extend the base.
        :type new: Dict[str, Any]
        :param strategy: Die anzuwendende Zusammenführungsstrategie.
                         The merge strategy to apply.
        :type strategy: MergeStrategy
        :return: Das zusammengeführte Dictionary.
                 The merged dictionary.
        :rtype: Dict[str, Any]
        """
        merged = base.copy() # Erstellt eine Kopie des Basis-Dictionaries, um das Original nicht zu modifizieren. Creates a copy of the base dictionary to avoid modifying the original.

        for key, value in new.items():
            if key in merged:
                if isinstance(merged[key], dict) and isinstance(value, dict):
                    # Wenn beide Werte Dictionaries sind, rekursiv zusammenführen.
                    # If both values are dictionaries, merge recursively.
                    merged[key] = self._deep_merge(merged[key], value, strategy)
                elif isinstance(merged[key], list) and isinstance(value, list):
                    # Wenn beide Werte Listen sind, Strategie anwenden.
                    # If both values are lists, apply strategy.
                    if strategy == MergeStrategy.APPEND_LIST:
                        merged[key].extend(value) # Hängt Elemente der neuen Liste an die Basisliste an. Appends elements of the new list to the base list.
                    elif strategy == MergeStrategy.OVERWRITE or strategy == MergeStrategy.DEEP_MERGE:
                        merged[key] = value # Überschreibt die Basisliste mit der neuen Liste. Overwrites the base list with the new list.
                    else:
                        merged[key] = value # Standardmäßig überschreiben, falls Strategie nicht spezifisch. Overwrite by default if strategy is not specific.
                else:
                    # Skalare oder Typkonflikte (z.B. dict vs. str): der neue Wert überschreibt den alten.
                    # Scalars or type mismatches (e.g. dict vs. str): the new value overwrites the old one.
                    merged[key] = value
            else:
                # Wenn der Schlüssel nicht in der Basis existiert, einfach hinzufügen.
                # If the key does not exist in the base, simply add it.
                merged[key] = value
        return merged

    def load_config_file(self, file_path: str) -> Dict[str, Any]:
        """
        Lädt eine JSON-Konfiguration aus einer Datei.
        Loads a JSON configuration from a file.

        :param file_path: Der Pfad zur JSON-Datei.
                          The path to the JSON file.
        :type file_path: str
        :raises FileNotFoundError: Wenn die Datei nicht gefunden wird.
                                   If the file is not found.
        :raises json.JSONDecodeError: Wenn der Dateiinhalt kein gültiges JSON ist.
                                      If the file content is not valid JSON.
        :return: Das geladene Konfigurations-Dictionary.
                 The loaded configuration dictionary.
        :rtype: Dict[str, Any]
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Konfigurationsdatei nicht gefunden: {file_path}") # Konfigurationsdatei wurde nicht gefunden. Configuration file not found.
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f) # Lädt den JSON-Inhalt aus der Datei. Loads the JSON content from the file.
            if not isinstance(config_data, dict):
                raise TypeError("Die Root der Konfigurationsdatei muss ein JSON-Objekt sein.") # Die Root muss ein JSON-Objekt sein. The root must be a JSON object.
            return config_data
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Ungültiges JSON in {file_path}: {e}", e.doc, e.pos) # Fehler beim Dekodieren der JSON-Datei. Error decoding JSON file.
        except Exception as e:
            raise Exception(f"Fehler beim Laden der Konfigurationsdatei {file_path}: {e}") # Allgemeiner Fehler beim Laden. General loading error.

    def load_config_string(self, config_string: str) -> Dict[str, Any]:
        """
        Lädt eine JSON-Konfiguration aus einem String.
        Loads a JSON configuration from a string.

        :param config_string: Der JSON-Konfigurationsstring.
                              The JSON configuration string.
        :type config_string: str
        :raises json.JSONDecodeError: Wenn der String-Inhalt kein gültiges JSON ist.
                                      If the string content is not valid JSON.
        :return: Das geladene Konfigurations-Dictionary.
                 The loaded configuration dictionary.
        :rtype: Dict[str, Any]
        """
        try:
            config_data = json.loads(config_string) # Lädt den JSON-Inhalt aus dem String. Loads the JSON content from the string.
            if not isinstance(config_data, dict):
                raise TypeError("Die Root der Konfigurationszeichenkette muss ein JSON-Objekt sein.") # Die Root muss ein JSON-Objekt sein. The root must be a JSON object.
            return config_data
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Ungültiges JSON im String: {e}", e.doc, e.pos) # Fehler beim Dekodieren des JSON-Strings. Error decoding JSON string.
        except Exception as e:
            raise Exception(f"Fehler beim Laden der Konfiguration aus String: {e}") # Allgemeiner Fehler beim Laden. General loading error.

    def merge(self, new_config: Dict[str, Any], strategy: Optional[MergeStrategy] = None) -> None:
        """
        Führt eine neue Konfiguration mit der aktuell zusammengeführten Konfiguration zusammen.
        Merges a new configuration with the currently merged configuration.

        :param new_config: Das neue Konfigurations-Dictionary, das zusammengeführt werden soll.
                           The new configuration dictionary to be merged.
        :type new_config: Dict[str, Any]
        :param strategy: Die spezifische Zusammenführungsstrategie für diesen Vorgang.
                         Wenn None, wird die Standardstrategie verwendet.
                         The specific merge strategy for this operation.
                         If None, the default strategy is used.
        :type strategy: Optional[MergeStrategy]
        """
        actual_strategy = strategy if strategy is not None else self.default_strategy # Wählt die anzuwendende Strategie. Selects the strategy to apply.

        if actual_strategy == MergeStrategy.OVERWRITE:
            self.merged_config = new_config # Überschreibt die gesamte Konfiguration. Overwrites the entire configuration.
        elif actual_strategy == MergeStrategy.DEEP_MERGE or actual_strategy == MergeStrategy.APPEND_LIST:
            self.merged_config = self._deep_merge(self.merged_config, new_config, actual_strategy) # Führt Dictionaries rekursiv zusammen. Recursively merges dictionaries.
        else:
            raise ValueError(f"Unbekannte Zusammenführungsstrategie: {actual_strategy}") # Unbekannte Strategie. Unknown strategy.

    def get_merged_config(self) -> Dict[str, Any]:
        """
        Gibt die aktuell zusammengeführte Konfiguration zurück.
        Returns the currently merged configuration.

        :return: Das zusammengeführte Konfigurations-Dictionary.
                 The merged configuration dictionary.
        :rtype: Dict[str, Any]
        """
        return self.merged_config.copy() # Gibt eine Kopie zurück, um externe Modifikationen zu verhindern. Returns a copy to prevent external modifications.

    def reset(self) -> None:
        """
        Setzt die zusammengeführte Konfiguration zurück.
        Resets the merged configuration.
        """
        self.merged_config = {} # Setzt die Konfiguration auf ein leeres Dictionary zurück. Resets the configuration to an empty dictionary.


# Standardname der Merge-Steuerungsdatei, falls kein Pfad angegeben wird.
# Default name of the merge control file if no path is provided.
DEFAULT_MERGE_CONFIG_FILENAME = "merge-config.json"


class MergeRunConfig:
    """
    Beschreibt einen kompletten Merge-Lauf, geladen aus einer JSON-Steuerungsdatei.
    Die Steuerungsdatei benennt die Eingabedateien, die Merge-Strategie und das Ausgabeziel,
    sodass ein Merge ohne Code-Änderungen konfiguriert werden kann.

    Describes a complete merge run loaded from a JSON control file.
    The control file names the input files, the merge strategy and the output target,
    so a merge can be configured without code changes.
    """

    def __init__(
        self,
        inputs: List[str],
        strategy: MergeStrategy = MergeStrategy.DEEP_MERGE,
        output: Optional[str] = None,
    ) -> None:
        """
        :param inputs: Reihenfolge der zu mergenden JSON-Eingabedateien.
                       Ordered list of JSON input files to merge.
        :param strategy: Die anzuwendende Merge-Strategie. The merge strategy to apply.
        :param output: Optionaler Pfad, in den das Ergebnis geschrieben wird.
                       Optional path the result is written to.
        """
        self.inputs = inputs
        self.strategy = strategy
        self.output = output

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MergeRunConfig":
        """
        Erzeugt eine MergeRunConfig aus einem bereits geparsten JSON-Objekt und validiert die Felder.
        Creates a MergeRunConfig from an already parsed JSON object and validates the fields.

        :raises ValueError: Wenn Pflichtfelder fehlen oder Werte ungültig sind.
                            If required fields are missing or values are invalid.
        """
        if not isinstance(data, dict):
            raise ValueError("Die Merge-Steuerungsdatei muss ein JSON-Objekt sein.")  # Root must be an object.

        raw_inputs = data.get("inputs")
        if not isinstance(raw_inputs, list) or not raw_inputs:
            raise ValueError("Die Steuerungsdatei benötigt ein nicht-leeres 'inputs'-Array.")  # Needs non-empty 'inputs'.
        inputs: List[str] = []
        for item in raw_inputs:
            if not isinstance(item, str):
                raise ValueError("Jeder Eintrag in 'inputs' muss ein Dateipfad (String) sein.")  # Each input must be a path.
            inputs.append(item)

        raw_strategy = data.get("strategy", MergeStrategy.DEEP_MERGE.value)
        if not isinstance(raw_strategy, str):
            raise ValueError("'strategy' muss ein String sein.")  # 'strategy' must be a string.
        try:
            strategy = MergeStrategy(raw_strategy)
        except ValueError:
            valid = ", ".join(s.value for s in MergeStrategy)
            raise ValueError(f"Unbekannte Strategie '{raw_strategy}'. Gültig sind: {valid}.")  # Unknown strategy.

        raw_output = data.get("output")
        if raw_output is not None and not isinstance(raw_output, str):
            raise ValueError("'output' muss ein Dateipfad (String) oder null sein.")  # 'output' must be a path or null.

        return MergeRunConfig(inputs=inputs, strategy=strategy, output=raw_output)


def load_merge_run_config(config_path: str = DEFAULT_MERGE_CONFIG_FILENAME) -> MergeRunConfig:
    """
    Lädt und validiert eine Merge-Steuerungsdatei von der Festplatte.
    Loads and validates a merge control file from disk.

    :raises FileNotFoundError: Wenn die Steuerungsdatei fehlt. If the control file is missing.
    :raises json.JSONDecodeError: Wenn die Steuerungsdatei kein gültiges JSON ist. If it is not valid JSON.
    :raises ValueError: Wenn der Inhalt kein gültiges Merge-Schema ist. If the content is not a valid merge schema.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Merge-Steuerungsdatei nicht gefunden: {config_path}")  # Control file not found.
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return MergeRunConfig.from_dict(data)


def run_from_config(config_path: str = DEFAULT_MERGE_CONFIG_FILENAME) -> Dict[str, Any]:
    """
    Führt einen kompletten Merge anhand einer Steuerungsdatei aus:
    lädt die Eingabedateien, merged sie mit der konfigurierten Strategie und
    schreibt bei Bedarf das Ergebnis in die Ausgabedatei.

    Runs a complete merge driven by a control file: loads the input files,
    merges them with the configured strategy and, if requested, writes the
    result to the output file. Returns the merged configuration.
    """
    run_config = load_merge_run_config(config_path)
    merger = JSONConfigMerger(default_strategy=run_config.strategy)
    for input_path in run_config.inputs:
        merger.merge(merger.load_config_file(input_path), strategy=run_config.strategy)
    result = merger.get_merged_config()
    if run_config.output is not None:
        with open(run_config.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    return result


def main(argv: Optional[List[str]] = None) -> int:
    """
    Kommandozeilen-Einstiegspunkt: steuert einen Merge über eine JSON-Steuerungsdatei.
    Command line entry point: drives a merge via a JSON control file.
    """
    parser = argparse.ArgumentParser(
        description="Merge JSON configuration files driven by a JSON control file.",
    )
    parser.add_argument(
        "-c",
        "--config",
        default=DEFAULT_MERGE_CONFIG_FILENAME,
        help=f"Path to the merge control file (default: {DEFAULT_MERGE_CONFIG_FILENAME}).",
    )
    args = parser.parse_args(argv)
    try:
        result = run_from_config(args.config)
    except (FileNotFoundError, json.JSONDecodeError, ValueError, TypeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
