# Getting hybrid models or components

## `list`

Use the `list` command to list the [available](https://frame-dev.epfl.ch) and downloaded hybrid models and components. You can list either hybrid models:
```bash
frame list models
```
or components:
```bash
frame list components
```

Use the `--only-local` or `--only-remote` to restrict the lists to only units that are on your computer, or to only units available in the [FRAME library](https://frame-dev.epfl.ch). For example:
```bash
frame list models --only-remote
```
will list hybrid models available online.


## `show`

Use the `show` command to display summarized information about a hybrid model or a component. This will also display the CLI command that can be used to download a unit (see below).

Example:

```bash
frame show model tandc
```


## `pull`

Use the `pull` command to download a hybrid model or a component from the FRAME library to your computer. If the unit's metadata contains information on how to setup an environment to run it, it will be created.

Example:

```bash
frame pull model tandc
```
