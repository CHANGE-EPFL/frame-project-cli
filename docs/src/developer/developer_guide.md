# Developer guide

```{toctree}
:maxdepth: 1
:caption: Contents

reference
```


## 💾 Installation for development

The FRAME CLI source code is hosted on [GitHub](https://github.com/CHANGE-EPFL/frame-project-cli). To install FRAME CLI for development in your current Python environment, you can use the following command. Feel free to use a virtual environment if you want to keep your system clean. Make sure that `pip` is installed in the current environment before proceeding with the installation.
```bash
git clone https://github.com/CHANGE-EPFL/frame-project-cli.git
cd frame-cli
make install
```

Create a `.env` file in the root of your project with the following content (or export environment variables in your shell):
```bash
FRAME_CLI_LOGGING_LEVEL=INFO
```

## ✅ Running tests

```bash
make test
```
