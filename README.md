# Frame CLI

_Command line interface for managing [Frame hybrid models](https://frame-dev.epfl.ch/)_

[![PyPI version](https://badge.fury.io/py/frame-cli.svg)](https://badge.fury.io/py/frame-cli)


# 🐇 Quick start

## Requirements

- [uv](https://docs.astral.sh/uv/) Python package and project manager
- [git](https://git-scm.com/) version control system


## Installation

Frame CLI relies on [uv](https://docs.astral.sh/uv/) to manage Python virtual environments. You need to install it first if you don't already have it. Refer to the official [uv documentation](https://docs.astral.sh/uv/getting-started/installation/).

Then, run the following command to install Frame CLI:
```bash
uv tool install frame-cli
```


## Usage

To see the list of available commands, run:
```bash
frame --help
```
Hybrid model and component pages show which command must be run to download and setup specific units.

You may want to install autocompletion for easier usage. To do so, run:
```bash
frame --install-completion
```


# 💾 Installation for development

To install Frame CLI for development in your current Python environment, you can use the following command. Feel free to use a virtual environment if you want to keep your system clean.
```bash
git clone https://github.com/CHANGE-EPFL/frame-project-cli.git
cd frame-cli
make install
```

Create a `.env` file in the root of your project with the following content (or export environment variables in your shell):
```bash
FRAME_CLI_LOGGING_LEVEL=INFO
```

# ✅ Running tests

```bash
make test
```
