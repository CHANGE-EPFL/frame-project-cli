# Frame CLI

_Command line interface for managing [Frame hybrid models](https://frame-dev.epfl.ch/)_


# 🐇 Quick start

## Requirements

- [uv](https://docs.astral.sh/uv/) Python package and project manager


## Installation

Frame CLI relies on [uv](https://docs.astral.sh/uv/) to manage Python virtual environments. You need to install it first if you don't already have it:
```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```
Then, run the following command to install Frame CLI:
```bash
uv tool install git+https://github.com/CHANGE-EPFL/frame-project-cli.git
```


## Usage

To see the list of available commands, run:
```bash
frame-cli --help
```


# 💾 Installation for development

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
