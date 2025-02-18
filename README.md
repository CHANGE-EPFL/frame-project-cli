# frame-cli

_Command line interface for managing Frame hybrid models_


# 🐇 Quick start

## Requirements

- Python 3.10 or higher


## Installation

We recommend you install the FRAME CLI inside a Python virtual environment, for example using [uv](https://github.com/astral-sh/uv) or [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html). To install, run the following command in your terminal:
```bash
pip install git+https://github.com/CHANGE-EPFL/frame-project-cli.git
```

## Usage

Create a `.env` file in the root of your project with the following content (or export environment variables in your shell):
```bash
FRAME_CLI_LOGGING_LEVEL=INFO
```


Then run:

```bash
frame-cli --help
```


# 💾 Installation for development

```bash
git clone https://github.com/CHANGE-EPFL/frame-project-cli.git
cd frame-cli
make install
```


# ✅ Running tests

```bash
make test
```
