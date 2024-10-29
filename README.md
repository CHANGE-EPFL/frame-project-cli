# frame-cli

_Command line interface for managing Frame hybrid models_


# 🐇 Quick start

## Requirements

- Python 3.9 or higher


## Installation

```bash
pip install git+https://gitlab.com/sphamba/frame-cli.git
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
git clone https://gitlab.com/sphamba/frame-cli.git
cd frame-cli
make install
```


# ✅ Running tests

```bash
make test
```
