# Contributing to Webhook Reporter

Thank you for considering contributing to **Webhook Reporter**! We welcome contributions of all kinds, including bug reports, feature suggestions, code improvements, and documentation enhancements.

## Getting Started

To contribute, you'll need:
- Basic understanding of Git and Python.
- A webhook URL to test your changes (e.g., for Discord, Slack, or Teams).

If you're new to open-source contributions, check out [this guide](https://opensource.guide/how-to-contribute/) to learn the basics.

---

## How to Contribute

### Reporting Issues
If you've found a bug or have a feature request:
1. **Check Existing Issues**: Look through [open issues](https://github.com/Moeh-Jama/webhook-reporter/issues) to see if your concern has already been addressed.
2. **Open a New Issue**: Provide a clear and descriptive title and include as much relevant information as possible:
   - Steps to reproduce (for bugs).
   - Expected behavior.
   - Screenshots, logs, or other helpful context.

### Suggesting Features
1. Check if a similar suggestion already exists in [open issues](https://github.com/Moeh-Jama/webhook-reporter/issues).
2. If not, create a [new feature request issue](https://github.com/Moeh-Jama/webhook-reporter/issues/new?template=feature_request.md).

### Code Contributions
We appreciate code contributions that fix bugs, introduce new features, or improve the project. Follow these steps to get started:

#### Prerequisites
1. Fork the repository to your own GitHub account.
2. Clone your forked repository:
   ```bash
   git clone https://github.com/Moeh-Jama/webhook-reporter.git
   ```
3. Create a new `.env` file using the provided [.env.sample](https://github.com/Moeh-Jama/webhook-reporter/blob/main/.env.sample):
   ```bash
   cp .env.sample .env
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### Making Changes
1. **Create a new branch for your work:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
   Example: `git checkout -b feature/coverage-parser-jest`

2. **Make your changes in the codebase.**

3. **Test your changes:**
   - Ensure all existing tests pass.
   - Add new tests for any new functionality you've introduced.
   - Use the `.env` file to test with a webhook URL for Discord, Slack, or Teams.

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Describe your changes"
   ```
   - Write clear, concise, and descriptive commit messages.
   - Follow best practices for writing commit messages:
     - Use the imperative mood (e.g., "Add feature" instead of "Added feature").
     - Be concise but informative.
     - Explain the "what" and "why" of the change, not just the "how."
   - For detailed guidance, refer to this excellent resource: [How to Write a Git Commit Message by cbeams](https://cbea.ms/git-commit/).


#### Submitting Your Work
1. Push your branch to your forked repository:
   ```bash
   git push origin feature/your-feature-name
   ```
2. Open a pull request:
   - Go to the original repository on GitHub.
   - Click **Pull Requests** and then **New Pull Request**.
   - Select your branch and describe your changes in detail.

---

## Guidelines

### Code Style
- Follow [PEP 8](https://pep8.org/) guidelines for Python code.
- Use meaningful variable and function names.
- Write concise and clear comments where necessary.

### Testing
- Ensure existing tests pass before submitting your PR:
  ```bash
  pytest
  ```
- Write tests for new functionality using [Pytest](https://docs.pytest.org/).

### Commit Messages
- Use clear and descriptive commit messages:
  - ✅ **Good**: `Add coverage parser for Jest framework`
  - ❌ **Bad**: `Fix stuff`

---

## Opening a Pull Request
When opening a pull request:
1. Ensure your branch is up to date with the latest changes from `main`.
2. Provide a clear and detailed description of the changes.
3. Reference any relevant issues (e.g., `Closes #123`).

For major changes, open an issue first to discuss your proposal.

---

Thank you for your contribution! 🎉