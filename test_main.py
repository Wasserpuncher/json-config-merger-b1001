import unittest
import json
import os
from main import JSONConfigMerger, MergeStrategy

class TestJSONConfigMerger(unittest.TestCase):
    """
    Testklasse für den JSONConfigMerger.
    Test class for the JSONConfigMerger.
    """

    def setUp(self):
        """
        Setzt den Testzustand vor jedem Test zurück.
        Resets the test state before each test.
        """
        self.merger = JSONConfigMerger() # Erstellt eine neue Instanz des Mergers für jeden Test. Creates a new merger instance for each test.
        self.temp_file_path = "temp_config.json" # Temporärer Dateipfad für Dateitests. Temporary file path for file tests.

    def tearDown(self):
        """
        Bereinigt nach jedem Test.
        Cleans up after each test.
        """
        if os.path.exists(self.temp_file_path):
            os.remove(self.temp_file_path) # Löscht die temporäre Datei, falls vorhanden. Deletes the temporary file if it exists.

    def _create_temp_file(self, content: Dict[str, Any]):
        """
        Hilfsfunktion zum Erstellen einer temporären JSON-Datei.
        Helper function to create a temporary JSON file.
        """
        with open(self.temp_file_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2) # Schreibt den Inhalt in die temporäre Datei. Writes content to the temporary file.

    def test_load_config_file_success(self):
        """
        Testet das erfolgreiche Laden einer Konfigurationsdatei.
        Tests successful loading of a configuration file.
        """
        config_content = {"app": {"name": "TestApp"}, "version": "1.0"} # Beispiel-Konfigurationsinhalt. Example config content.
        self._create_temp_file(config_content)
        loaded_config = self.merger.load_config_file(self.temp_file_path)
        self.assertEqual(loaded_config, config_content) # Überprüft, ob die geladene Konfiguration korrekt ist. Checks if loaded config is correct.

    def test_load_config_file_not_found(self):
        """
        Testet das Laden einer nicht existierenden Datei.
        Tests loading a non-existent file.
        """
        with self.assertRaises(FileNotFoundError): # Erwartet einen FileNotFoundError. Expects a FileNotFoundError.
            self.merger.load_config_file("non_existent_file.json")

    def test_load_config_file_invalid_json(self):
        """
        Testet das Laden einer Datei mit ungültigem JSON.
        Tests loading a file with invalid JSON.
        """
        with open(self.temp_file_path, 'w', encoding='utf-8') as f:
            f.write("{invalid json") # Schreibt ungültiges JSON. Writes invalid JSON.
        with self.assertRaises(json.JSONDecodeError): # Erwartet einen json.JSONDecodeError. Expects a json.JSONDecodeError.
            self.merger.load_config_file(self.temp_file_path)

    def test_load_config_string_success(self):
        """
        Testet das erfolgreiche Laden einer Konfiguration aus einem String.
        Tests successful loading of a configuration from a string.
        """
        config_string = '{"app": {"name": "TestApp"}, "version": "1.0"}' # Beispiel-Konfigurationsstring. Example config string.
        loaded_config = self.merger.load_config_string(config_string)
        self.assertEqual(loaded_config, json.loads(config_string)) # Überprüft, ob der geladene String korrekt ist. Checks if loaded string is correct.

    def test_load_config_string_invalid_json(self):
        """
        Testet das Laden eines Strings mit ungültigem JSON.
        Tests loading a string with invalid JSON.
        """
        invalid_string = '{invalid json string' # Ungültiger JSON-String. Invalid JSON string.
        with self.assertRaises(json.JSONDecodeError): # Erwartet einen json.JSONDecodeError. Expects a json.JSONDecodeError.
            self.merger.load_config_string(invalid_string)

    def test_merge_deep_merge_strategy(self):
        """
        Testet die DEEP_MERGE-Strategie.
        Tests the DEEP_MERGE strategy.
        """
        base_config = {"a": 1, "b": {"c": 2, "d": 3}, "e": [1, 2]} # Basis-Konfiguration. Base configuration.
        new_config = {"b": {"c": 4, "f": 5}, "g": 6, "e": [3, 4]} # Neue Konfiguration. New configuration.
        expected_config = {"a": 1, "b": {"c": 4, "d": 3, "f": 5}, "e": [3, 4], "g": 6} # Erwartete Konfiguration. Expected configuration.

        self.merger.merge(base_config, strategy=MergeStrategy.DEEP_MERGE)
        self.merger.merge(new_config, strategy=MergeStrategy.DEEP_MERGE)
        self.assertEqual(self.merger.get_merged_config(), expected_config) # Überprüft das Ergebnis des tiefen Zusammenführens. Checks the result of deep merge.

    def test_merge_overwrite_strategy(self):
        """
        Testet die OVERWRITE-Strategie.
        Tests the OVERWRITE strategy.
        """
        base_config = {"a": 1, "b": {"c": 2}} # Basis-Konfiguration. Base configuration.
        new_config = {"a": 10, "d": 4} # Neue Konfiguration. New configuration.
        expected_config = {"a": 10, "d": 4} # Erwartete Konfiguration (vollständiges Überschreiben). Expected configuration (complete overwrite).

        self.merger.merge(base_config, strategy=MergeStrategy.OVERWRITE)
        self.merger.merge(new_config, strategy=MergeStrategy.OVERWRITE)
        self.assertEqual(self.merger.get_merged_config(), expected_config) # Überprüft das Ergebnis des Überschreibens. Checks the result of overwriting.

    def test_merge_append_list_strategy(self):
        """
        Testet die APPEND_LIST-Strategie.
        Tests the APPEND_LIST strategy.
        """
        base_config = {"a": 1, "b": {"c": 2}, "e": [1, 2]} # Basis-Konfiguration. Base configuration.
        new_config = {"b": {"c": 4, "f": 5}, "g": 6, "e": [3, 4]} # Neue Konfiguration. New configuration.
        expected_config = {"a": 1, "b": {"c": 4, "d": 3, "f": 5}, "e": [1, 2, 3, 4], "g": 6} # Erwartete Konfiguration.

        merger_append = JSONConfigMerger(default_strategy=MergeStrategy.APPEND_LIST) # Merger mit APPEND_LIST-Strategie initialisieren. Initialize merger with APPEND_LIST strategy.
        merger_append.merge(base_config)
        merger_append.merge(new_config)
        expected_config_for_append = {"a": 1, "b": {"c": 4, "d": 3, "f": 5}, "e": [1, 2, 3, 4], "g": 6}
        self.assertEqual(merger_append.get_merged_config(), expected_config_for_append)

    def test_merge_with_default_strategy(self):
        """
        Testet das Zusammenführen mit der Standardstrategie (DEEP_MERGE).
        Tests merging with the default strategy (DEEP_MERGE).
        """
        base_config = {"a": 1, "b": {"c": 2}, "e": [1, 2]}
        new_config = {"b": {"c": 4, "f": 5}, "g": 6, "e": [3, 4]}
        expected_config = {"a": 1, "b": {"c": 4, "d": 3, "f": 5}, "e": [3, 4], "g": 6} # Listen werden bei DEEP_MERGE überschrieben. Lists are overwritten with DEEP_MERGE.

        self.merger.merge(base_config) # Nutzt die Standardstrategie (DEEP_MERGE). Uses default strategy (DEEP_MERGE).
        self.merger.merge(new_config)
        self.assertEqual(self.merger.get_merged_config(), expected_config)

    def test_reset_config(self):
        """
        Testet das Zurücksetzen der Konfiguration.
        Tests resetting the configuration.
        """
        initial_config = {"key": "value"} # Anfangskonfiguration. Initial configuration.
        self.merger.merge(initial_config)
        self.assertFalse(self.merger.get_merged_config() == {})
        self.merger.reset()
        self.assertEqual(self.merger.get_merged_config(), {})

    def test_get_merged_config_returns_copy(self):
        """
        Testet, ob get_merged_config eine Kopie zurückgibt.
        Tests if get_merged_config returns a copy.
        """
        initial_config = {"key": "value"}
        self.merger.merge(initial_config)
        retrieved_config = self.merger.get_merged_config()
        retrieved_config["new_key"] = "new_value" # Modifiziert die zurückgegebene Kopie. Modifies the returned copy.
        self.assertNotIn("new_key", self.merger.get_merged_config()) # Überprüft, ob die interne Konfiguration nicht modifiziert wurde. Checks if internal config was not modified.

    def test_merge_empty_configs(self):
        """
        Testet das Zusammenführen mit leeren Konfigurationen.
        Tests merging with empty configurations.
        """
        self.merger.merge({})
        self.assertEqual(self.merger.get_merged_config(), {})
        self.merger.merge({"a": 1})
        self.assertEqual(self.merger.get_merged_config(), {"a": 1})
        self.merger.merge({})
        self.assertEqual(self.merger.get_merged_config(), {"a": 1})

    def test_merge_different_types_overwrite(self):
        """
        Testet das Zusammenführen unterschiedlicher Typen (sollte überschreiben).
        Tests merging different types (should overwrite).
        """
        base_config = {"key": "string_value"}
        new_config_dict = {"key": {"nested": "dict"}}
        new_config_list = {"key": [1, 2, 3]}
        new_config_int = {"key": 123}

        self.merger.reset()
        self.merger.merge(base_config)
        self.merger.merge(new_config_dict) # string -> dict
        self.assertEqual(self.merger.get_merged_config(), {"key": {"nested": "dict"}})

        self.merger.reset()
        self.merger.merge(base_config)
        self.merger.merge(new_config_list) # string -> list
        self.assertEqual(self.merger.get_merged_config(), {"key": [1, 2, 3]})

        self.merger.reset()
        self.merger.merge(base_config)
        self.merger.merge(new_config_int) # string -> int
        self.assertEqual(self.merger.get_merged_config(), {"key": 123})

    def test_merge_strategy_override_in_merge_call(self):
        """
        Testet, ob die Strategie im merge-Aufruf die Standardstrategie überschreibt.
        Tests if the strategy in the merge call overrides the default strategy.
        """
        merger = JSONConfigMerger(default_strategy=MergeStrategy.OVERWRITE) # Standard ist OVERWRITE. Default is OVERWRITE.
        merger.merge({"a": {"b": 1}, "c": [1]}, strategy=MergeStrategy.DEEP_MERGE) # Erster Merge mit DEEP_MERGE. First merge with DEEP_MERGE.
        merger.merge({"a": {"d": 2}, "c": [2]}, strategy=MergeStrategy.APPEND_LIST) # Zweiter Merge mit APPEND_LIST. Second merge with APPEND_LIST.

        expected = {"a": {"b": 1, "d": 2}, "c": [1, 2]} # Erwartetes Ergebnis. Expected result.
        self.assertEqual(merger.get_merged_config(), expected)

if __name__ == '__main__':
    unittest.main()
