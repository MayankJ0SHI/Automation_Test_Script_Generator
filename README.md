# Automation Test Script Generator

[![License](https://img.shields.io/github/license/MayankJ0SHI/Automation_Test_Script_Generator)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/MayankJ0SHI/Automation_Test_Script_Generator)](https://github.com/MayankJ0SHI/Automation_Test_Script_Generator/commits/main)

**Automation Test Script Generator** is a powerful tool designed to simplify and automate the process of creating robust test scripts for a wide variety of software projects. By leveraging inputs, code analysis, or predefined templates, the generator ensures consistent, accurate, and maintainable tests, streamlining QA workflows and letting your developers focus on features rather than repetitive scripting.

---

## Table of Contents

- [Features](#features)
- [Supported Technologies](#supported-technologies)
- [Architecture Overview](#architecture-overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
  - [Generating Test Scripts](#generating-test-scripts)
  - [Custom Templates](#custom-templates)
  - [Integration with CI/CD](#integration-with-cicd)
- [Examples](#examples)
- [Contributing](#contributing)
- [FAQ](#faq)
- [License](#license)
- [Contact](#contact)

---

## Features

- **Automated Test Generation**: Instantly create test scripts with minimal manual effort.
- **Template Support**: Choose or design templates for your preferred language and framework.
- **Custom Input Parsing**: Accepts test case files, code comments, or user prompts.
- **Extensible Architecture**: Add support for new frameworks via plugins or templates.
- **CI/CD Integration**: Easily fits into your DevOps workflow for continuous quality.
- **Code Coverage**: Option to generate tests to maximize code coverage.
- **Error Handling**: Warnings and logs for skipped or failed script generations.
- **User-Friendly CLI**: Intuitive command-line interface for power and scripting.
- **Documentation & Logging**: Detailed logs and optional documentation output.

---

## Supported Technologies

- **Languages**:  
  - Python (pytest, unittest)
  - JavaScript/TypeScript (Mocha, Jest)
  - Java (JUnit, TestNG)
  - [List yours or planned support here]
- **Test File Formats**:
  - YAML
  - JSON
  - CSV
  - Custom input files

---

## Architecture Overview

```
+----------------------------+
|    User Config / Input     |
+------------+---------------+
             |
             v
+----------------------------+
|    Automation Script Gen   |
+------------+---------------+
             |
      +------v-------+
      |   Templates  |
      +--------------+
             |
             v
    +----------------------+
    |  Output Test Scripts |
    +----------------------+
```

- **Input Parsing**: Reads user test cases, code, or config files.
- **Core Generator**: Processes inputs, applies templates, and generates scripts.
- **Output**: Structured, high-quality test files ready to run.

---

## Getting Started

### Prerequisites

- Python ≥ 3.8   (or mention Node.js ≥ if project is in JS)
- [Git](https://git-scm.com/)
- Pip or npm as appropriate
- OS: Windows / macOS / Linux (cross-platform)
- [Optional] Docker

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/MayankJ0SHI/Automation_Test_Script_Generator.git
   cd Automation_Test_Script_Generator
   ```

2. **Install Dependencies**

   For Python:
   ```bash
   pip install -r requirements.txt
   ```
   For Node.js:
   ```bash
   npm install
   ```
   *Or see specific language instructions in the `docs/` folder.*

3. **Quick Start**

   ```bash
   python generate_tests.py --config config.yaml
   ```
   Or for Node.js:
   ```bash
   node generate.js --config config.yaml
   ```

### Configuration

- **config.yaml** (or `.json`)
  - Define input test cases location, output directory, frameworks, and additional options.
  - Example:
    ```yaml
    test_cases: ./cases/
    framework: pytest
    template: default
    output_dir: ./generated/
    include_comments: true
    coverage: 90
    ```

- **Environment Variables**
  - `LOG_LEVEL=INFO` (or `DEBUG`, etc.)
  - `GENERATOR_MAX_FILES=100`

- **Command-Line Flags**
  - `--config <file>`: Path to configuration file.
  - `--verbose`: Turns on detailed logging.
  - `--dry-run`: Preview script generation without writing files.

---

## Usage

### Generating Test Scripts

1. Place your input files (or code) in the defined directory.
2. Adjust `config.yaml` for your framework and output paths.
3. Run:
   ```bash
   python generate_tests.py --config ./config.yaml
   ```
4. Generated scripts are saved to the output directory.

### Custom Templates

- Add new templates under the `templates/` directory.
- Reference your template in `config.yaml`:
  ```yaml
  template: my_template
  ```
- Templates can include custom logic, code comments, or test structure.

### Integration with CI/CD

Automate test script generation in CI using:
```yaml
# Example GitHub Actions step
- name: Generate Tests
  run: python generate_tests.py --config config.yaml
```
Add as a pre-test step to always regenerate scripts from updated cases/inputs.

---

## Examples

**Sample Input Test Case:**
```yaml
- test_name: User login
  steps:
    - open: "/login"
    - input: { username: "user", password: "pass" }
    - click: "Login"
    - assert: "dashboard is visible"
```

**Sample Generated Pytest:**
```python
def test_user_login(client):
    client.open("/login")
    client.input(username="user", password="pass")
    client.click("Login")
    assert client.is_visible("dashboard")
```

**Custom Output Location**
```yaml
output_dir: ./tests/generated
```
All scripts will be saved here.

---

## Contributing

Contributions are welcome! To contribute:

1. [Fork](https://github.com/MayankJ0SHI/Automation_Test_Script_Generator/fork) this repository.
2. Create your feature branch:  
   `git checkout -b feature/my-feature`
3. Commit your changes:  
   `git commit -am 'Describe your feature'`
4. Push the branch:  
   `git push origin feature/my-feature`
5. Open a [Pull Request](https://github.com/MayankJ0SHI/Automation_Test_Script_Generator/pulls)

*Please ensure code style consistency and add tests for new functionality.*

---

## FAQ

**Q:** What frameworks are supported?  
**A:** See [Supported Technologies](#supported-technologies) above. You can also add your own templates!

**Q:** Can I use this as a GitHub Action?  
**A:** Yes, add it to your workflow `.github/workflows/` as a job step.

**Q:** How do I debug my configuration?  
**A:** Use `--verbose` to get detailed logs and trace any errors.

---

## License

This project is licensed under the [MIT License](LICENSE). See the LICENSE file for details.

---

## Contact

For feature requests, issues, or questions:
- Open an [issue](https://github.com/MayankJ0SHI/Automation_Test_Script_Generator/issues)
- Contact the maintainer: [MayankJ0SHI](https://github.com/MayankJ0SHI)
