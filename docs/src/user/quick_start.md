# Quick start with the Frame CLI tool

To download models and components, and to setup environments to run those, your can use the dedicated CLI (command-line interface) [tool](https://github.com/CHANGE-EPFL/frame-project-cli).


## Requirements

- [uv](https://docs.astral.sh/uv/) Python package and project manager
- [git](https://git-scm.com/) version control system


## 💾 Installation

Frame CLI relies on [uv](https://docs.astral.sh/uv/) to manage Python virtual environments. You need to install it first if you don't already have it. Refer to the official [uv documentation](https://docs.astral.sh/uv/getting-started/installation/).

Then, run the following command to install Frame CLI:
```bash
uv tool install frame-cli
```


## ⌨️ Usage

To see the list of available commands, run:
```bash
frame --help
```
Hybrid model and component pages show which command must be run to download and setup specific units.

You may want to install autocompletion for easier usage. To do so, run:
```bash
frame --install-completion
```


## ☹️ Uninstallation

To remove the CLI tool from your system, run the following command:
```bash
uv tool uninstall frame-cli
```
