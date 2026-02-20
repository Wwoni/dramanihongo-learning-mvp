# util

Shared resources used across projects.

## Structure
- `credentials/` : service account JSON and other secrets (do not commit)

## Usage
Load the service account JSON as an env var:
```bash
export GOOGLE_SERVICE_ACCOUNT_JSON="$(cat /Users/wonheelee/Documents/Cursor/util/credentials/service-account.json)"
```
