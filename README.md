# GitHub Issue Maker

Make batch issues based on template. Used to prepare for Hacktoberfest.

Can use the GitHub import API so it won't create notifications.

## Installation

```sh
pip install .
```

## Usage

```sh
issuemaker --help
```

When using the import API each job is queued up and not processed right away. To get the status of your import job use the status CLI command:

```sh
issuemaker status --help
```
