# Architecture of JSON Config Merger

This document outlines the architectural design of the `json-config-merger` project. The core idea is to provide a robust, extensible, and intelligent mechanism for combining JSON configurations from various sources, catering to the needs of enterprise applications.

## Core Principles

*   **Modularity:** Separation of concerns into distinct components (loader, merger logic).
*   **Flexibility:** Support for different merging strategies and easy extension for new sources or validation methods.
*   **Robustness:** Comprehensive error handling for file operations and JSON parsing.
*   **Readability:** Clean, well-documented code with type hints for maintainability.

## High-Level Overview

The `JSONConfigMerger` operates around a central `merged_config` dictionary, which is progressively built by applying new configurations. The process involves:

1.  **Configuration Loading:** Retrieving JSON data from specified sources (files or strings).
2.  **Merging Engine:** Applying one or more incoming configurations to the current `merged_config` based on a chosen strategy.

```mermaid
graph TD
    A[Start] --> B(Initialize JSONConfigMerger);
    B --> C{Load Config Source};
    C -- From File --> D[load_config_file(path)];
    C -- From String --> E[load_config_string(str)];
    D --> F{Parsed Config (Dict)};
    E --> F;
    F --> G[merge(new_config, strategy)];
    G --> H{Apply Merge Strategy};
    H -- OVERWRITE --> I[Replace entire config];
    H -- DEEP_MERGE / APPEND_LIST --> J[Recursively merge dictionaries];
    J -- Handle Lists (Append/Overwrite) --> K[Update merged_config];
    K --> L[get_merged_config()];
    L --> M[End];
```

## Key Components

### `JSONConfigMerger` Class

This is the main entry point for the library. It encapsulates the state (`merged_config`) and provides the primary interface for loading and merging configurations.

*   **`__init__(self, default_strategy: MergeStrategy)`:**
    *   Initializes the merger with an empty `merged_config` and a `default_strategy` (e.g., `DEEP_MERGE`).
    *   The `MergeStrategy` enum defines the available strategies (`OVERWRITE`, `DEEP_MERGE`, `APPEND_LIST`).

*   **`load_config_file(self, file_path: str) -> Dict[str, Any]`:**
    *   Responsible for reading a JSON file from the filesystem.
    *   Handles `FileNotFoundError` if the file doesn't exist and `json.JSONDecodeError` for invalid JSON content.
    *   Ensures the root of the JSON is a dictionary.

*   **`load_config_string(self, config_string: str) -> Dict[str, Any]`:**
    *   Parses a JSON string directly.
    *   Handles `json.JSONDecodeError` for invalid JSON strings.
    *   Ensures the root of the JSON is a dictionary.

*   **`merge(self, new_config: Dict[str, Any], strategy: Optional[MergeStrategy] = None) -> None`:**
    *   The core method for combining configurations.
    *   Takes a `new_config` dictionary and an optional `strategy`. If `strategy` is `None`, it defaults to `self.default_strategy`.
    *   Delegates to internal `_deep_merge` or directly overwrites `self.merged_config` based on the chosen strategy.

*   **`_deep_merge(self, base: Dict[str, Any], new: Dict[str, Any], strategy: MergeStrategy) -> Dict[str, Any]`:**
    *   A private, recursive helper method that performs the actual deep merging logic.
    *   Iterates through keys in the `new` configuration:
        *   If a key exists in both `base` and `new` and both values are dictionaries, it recursively calls `_deep_merge`.
        *   If both values are lists, it applies the specific list handling based on the `strategy` (`APPEND_LIST` or overwrite for others).
        *   For all other types or type mismatches, the `new` value overwrites the `base` value.
        *   If a key only exists in `new`, it's added to the `base`.

*   **`get_merged_config(self) -> Dict[str, Any]`:**
    *   Returns a *copy* of the currently merged configuration to prevent external modification of the internal state.

*   **`reset(self) -> None`:**
    *   Resets the `merged_config` to an empty dictionary, useful for starting a new merging operation.

### `MergeStrategy` Enum

An `Enum` defining the distinct ways configurations can be merged:

*   **`OVERWRITE`:** The incoming configuration completely replaces the existing `merged_config`.
*   **`DEEP_MERGE`:** Dictionaries are recursively merged. If a key exists in both, and both values are dictionaries, they are merged. If values are lists, the new list overwrites the existing one. Primitive values are overwritten.
*   **`APPEND_LIST`:** Similar to `DEEP_MERGE` for dictionaries and primitives, but if both values are lists, the elements of the new list are appended to the existing list.

## Error Handling

The system is designed to provide clear error messages for common issues:

*   `FileNotFoundError`: When a specified configuration file does not exist.
*   `json.JSONDecodeError`: When a file or string contains malformed JSON.
*   `TypeError`: If the root of a configuration (file or string) is not a JSON object (dictionary).
*   `ValueError`: For unknown or unsupported merge strategies.

## Extensibility Points (Future Enhancements)

The current architecture lays a solid foundation for future growth:

*   **Schema Validation:** Integration with libraries like `jsonschema` to validate configurations against a defined schema before or after merging. This would add an `is_valid` method or a `validate` step in the merge process.
*   **Environment Variables:** A mechanism to override specific configuration values using environment variables (e.g., `APP_SETTINGS_DEBUG=false`).
*   **Custom Loaders:** Support for other configuration formats (YAML, TOML) or data sources (databases, remote URLs). This could involve an abstract `ConfigLoader` interface.
*   **Advanced Merge Rules:** More complex merging rules, such as merging arrays of objects based on a unique identifier.
*   **Change Tracking:** Optionally keep a history of merges or identify which source contributed which value.

By adhering to this modular and strategy-based design, the `json-config-merger` aims to be a flexible and reliable tool for managing complex application configurations.
