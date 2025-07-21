# Managing the CLI tool itself

To install and uninstall the FRAME CLI tool, refer to the [Quick start](quick_start) section.


## `check`

Use the `check` command to verify that:
- The FRAME API is reachable
- `uv` is installed, needed to create Python virtual environments
- `git` is installed, needed to add new hybrid models or components to the FRAME library

```bash
frame check
```


## `version`

Use the `version` command to print the currently installed version of the FRAME CLI tool.

```bash
frame version
```


## `update`

If the FRAME CLI tool has been installed using `uv` (using `uv tool install frame-cli`), you can update it with:
```bash
frame update
```
