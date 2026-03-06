# JSON Config Merger

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![GitHub Actions Workflow Status](https://github.com/your-username/json-config-merger/actions/workflows/python-app.yml/badge.svg)

A powerful and intelligent JSON configuration merger designed for enterprise applications, supporting strategic merging, schema validation (planned), and environment-specific overrides. This tool provides a flexible way to combine multiple JSON configuration sources into a single, cohesive configuration object, essential for complex application deployments.

## Features

*   **Intelligent Deep Merging:** Recursively merges dictionary structures, handling nested configurations gracefully.
*   **Configurable Merge Strategies:** Choose between `OVERWRITE`, `DEEP_MERGE`, and `APPEND_LIST` for fine-grained control over how conflicts and list items are handled.
*   **Multiple Input Sources:** Load configurations from files or directly from JSON strings.
*   **Type Safety & Robustness:** Built with Python type hints and comprehensive error handling for reliable operation.
*   **Extensibility:** Designed with an OOP structure, making it easy to extend with new features like schema validation, environment variable overrides, or custom data sources.

## Installation

This project currently has no external dependencies beyond Python's standard library.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/json-config-merger.git
    cd json-config-merger
    ```

## Usage

Here's how to use the `JSONConfigMerger` to combine your configurations:

```python
from main import JSONConfigMerger, MergeStrategy
import json

# Initialize the merger with a default strategy (e.g., DEEP_MERGE)
merger = JSONConfigMerger(default_strategy=MergeStrategy.DEEP_MERGE)

# --- Example 1: Merging from files ---
# Create some dummy config files
with open("base_config.json", "w") as f:
    json.dump({"app_name": "MyBaseApp", "settings": {"debug": True, "log_level": "INFO"}, "features": ["auth", "logging"]}, f, indent=2)
with open("prod_config.json", "w") as f:
    json.dump({"app_name": "MyProdApp", "settings": {"debug": False, "log_level": "WARNING"}, "database": {"host": "prod-db", "port": 5432}, "features": ["metrics"]}, f, indent=2)

# Load base configuration
base_config = merger.load_config_file("base_config.json")
merger.merge(base_config)
print("Merged after base_config.json:", merger.get_merged_config())

# Load and merge production-specific configuration
# Here, 'app_name' and 'settings.debug' will be overwritten.
# 'settings.log_level' will be updated.
# 'database' will be added.
# 'features' list will be overwritten by default DEEP_MERGE strategy.
prod_config = merger.load_config_file("prod_config.json")
merger.merge(prod_config) # Uses default_strategy (DEEP_MERGE)
print("\nMerged after prod_config.json (DEEP_MERGE):", merger.get_merged_config())
# Expected features: ["metrics"] (overwritten)

# --- Example 2: Merging with APPEND_LIST strategy ---
merger.reset() # Reset for a fresh start

# Load base config again
base_config_data = {"app_name": "MyApp", "modules": ["core", "api"], "config": {"timeout": 30}}
merger.merge(base_config_data)

# Load environment-specific config, append modules
env_config_data = {"environment": "dev", "modules": ["dev_tools", "testing"], "config": {"retries": 5}}
merger.merge(env_config_data, strategy=MergeStrategy.APPEND_LIST) # Explicitly use APPEND_LIST

print("\nMerged with APPEND_LIST strategy:", merger.get_merged_config())
# Expected modules: ["core", "api", "dev_tools", "testing"]
# Expected config: {"timeout": 30, "retries": 5} (deep merged)

# Clean up dummy files
import os
os.remove("base_config.json")
os.remove("prod_config.json")
```

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── python-app.yml     # GitHub Actions CI/CD workflow
├── docs/
│   ├── architecture_en.md     # English architecture deep dive
│   └── architecture_de.md     # German architecture deep dive
├── main.py                    # Core JSON merger logic (OOP, type hints, German comments)
├── test_main.py               # Unit tests for main.py
├── README.md                  # Project README in English
├── README_de.md               # Project README in German
├── CONTRIBUTING.md            # Guidelines for contributing to the project
├── LICENSE                    # MIT License
└── .gitignore                 # Standard Python .gitignore file
```

## Contributing

We welcome contributions! Please see `CONTRIBUTING.md` for guidelines on how to submit bug reports, feature requests, and pull requests.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
