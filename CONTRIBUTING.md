# Contributing to JSON Config Merger

We welcome contributions to the `json-config-merger` project! Your help is invaluable in making this tool better for everyone.

## How to Contribute

There are several ways you can contribute:

1.  **Report Bugs:** If you find a bug, please open an issue on our [GitHub Issues page](https://github.com/your-username/json-config-merger/issues). Provide a clear description of the bug, steps to reproduce it, and expected behavior.
2.  **Suggest Features:** Have an idea for a new feature or improvement? Open an issue and describe your suggestion. We appreciate detailed proposals.
3.  **Submit Pull Requests:** If you'd like to contribute code, follow the guidelines below.

## Submitting Pull Requests (PRs)

To ensure a smooth contribution process, please follow these steps:

1.  **Fork the Repository:** Start by forking the `json-config-merger` repository to your GitHub account.
2.  **Clone Your Fork:** Clone your forked repository to your local machine:
    ```bash
    git clone https://github.com/your-username/json-config-merger.git
    cd json-config-merger
    ```
3.  **Create a New Branch:** Create a new branch for your feature or bug fix. Use a descriptive name (e.g., `feat/add-validation`, `fix/invalid-json-error`).
    ```bash
    git checkout -b your-branch-name
    ```
4.  **Make Your Changes:** Implement your changes. Remember the bilingual code requirements:
    *   **English variable names:** All variables, function names, and class names must be in English.
    *   **German inline comments:** Explain complex logic or design decisions using German comments (`# Kommentar auf Deutsch`).
    *   **Type hints and docstrings:** Use Python type hints and docstrings for all functions and classes (in English).
5.  **Write Tests:** Add or update unit tests in `test_main.py` to cover your changes. Ensure all existing tests still pass.
6.  **Run Tests:** Before committing, run the tests to ensure everything is working:
    ```bash
    python -m unittest discover
    ```
7.  **Update Documentation:** If your changes introduce new features or alter existing behavior, update the relevant documentation files (`README.md`, `README_de.md`, `docs/architecture_en.md`, `docs/architecture_de.md`).
8.  **Commit Your Changes:** Write clear and concise commit messages.
    ```bash
    git add .
    git commit -m "feat: Add new feature X"
    ```
9.  **Push to Your Fork:** Push your changes to your fork on GitHub:
    ```bash
    git push origin your-branch-name
    ```
10. **Create a Pull Request:** Go to the original `json-config-merger` repository on GitHub and create a new pull request from your branch to our `main` branch.
    *   Provide a clear title and description of your changes.
    *   Reference any related issues (e.g., `Fixes #123`, `Closes #456`).

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project, you agree to abide by its terms.

## License

By contributing to `json-config-merger`, you agree that your contributions will be licensed under its [MIT License](LICENSE).

Thank you for your contributions!
