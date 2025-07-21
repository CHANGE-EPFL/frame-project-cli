# Adding new hybrid models or components

To contribute to the [FRAME library](https://frame-dev.epfl.ch) of hybrid models and components, you may follow these steps:
1. Use the CLI tool to [create a FRAME metadata file](create-a-frame-metadata-file).
2. [Fill the metadata file](filling-the-metadata-file).
3. [Validate the metadata file](validate-the-metadata-file) to ensure it follows the FRAME metadata schema.
4. Commit the metadata file to your own repository and [submit a pull request to reference your unit](submit-a-pull-request-to-reference-your-unit-in-the-frame-library) in the FRAME library using the CLI tool. Alternatively, [add your metadata file to the FRAME repository directly](add-your-metadata-file-to-the-frame-repository-directly) and file a pull request.


## Create a FRAME metadata file

Use the following command to create a new metadata file for your hybrid model or component:
```bash
frame init
```
This command must be run inside a local Git repository. It will create a `frame_metadata.yaml` file at the root of the repository, copied from the [FRAME metadata template](https://github.com/CHANGE-EPFL/frame-project/blob/main/backend/api/metadata_files/template.yaml).


## Filling the metadata file

The `frame_metadata.yaml` must follow [FRAME metadata schema](https://raw.githubusercontent.com/CHANGE-EPFL/frame-project/refs/heads/main/backend/api/metadata_files/schema.json). If you use any decent code editor to edit your metadata file, you will get hints on the validity of the fields you add or edit. You can also request suggestions to automatically add missing fields that are required (_e.g._ hitting `ctrl + space` in Visual Studio Code).


## Validate the metadata file

Run the following command to validate your metadata file:
```bash
frame validate
```

This will warn you of missing fields, extraneous field, or field values that do not have the correct type.


## Submit a pull request to reference your unit in the FRAME library

Once your metadata file is ready, you can submit a pull request to the FRAME library repository using the CLI tool:
```bash
frame push
```
You will be prompted for a GitHub token to authenticate your request. If you do not have a GitHub token, create one with the `repo` scope by following the instructions on [GitHub's documentation](https://github.com/settings/tokens/new).

A Fork of the FRAME library repository will be created in your GitHub account, and a pull request will be submitted to the main FRAME library repository to add a reference to your unit's repository. You can then review the pull request and make any necessary changes before its review.

After the pull request is merged, your unit will be visible in the FRAME library. Any changes on the `frame_metadata.yaml` file you push to your repository will be reflected on the FRAME library website without needing to file new pull requests.


## Add your metadata file to the FRAME repository directly

If you desire, your can put the `frame_metadata.yaml` in the FRAME library repository directly. In this case, you can skip the `frame push` command and instead follow these steps:
1. Fork the [FRAME library repository](https://github.com/CHANGE-EPFL/frame-project)
2. Follow the instructions in the `README.md` file to add your metadata file and validate its integration.
3. Commit your changes, push them to your fork, and file a pull request to the main FRAME library repository.

In this case, any changes you want to make to the `frame_metadata.yaml` file will require a new pull request to the FRAME library repository. The CLI tool will not be able to update your unit's metadata automatically.
