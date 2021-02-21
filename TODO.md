# SQL:

- Tables
  - Asset snapshot with dollar amount somehow (pull latest or use our own table?)
  - Transactions

# Next steps:

- Implement more order types
- **Include time in force**
- Stub out more parts of the API
  - There's already a Python SDK for this but I think we'd benefit from basically writing our own, since we don't need to expose it publicly and we're still so much in the learning stage.

# Need-to-figure-out:

- Object model (different types of orders, etc.)
- ...

MVP logic:

1. Get data
2. Make decision
3. Execute/confirm decision
4. Log total assets
