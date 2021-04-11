# Topics to work on / research

## MVP flow

## Project structure & object model

## Infrastructure

### Managing secrets

- [Vault](https://github.com/hashicorp/vault)
- Tried installing on the VM
  - Had some issues using `wget`, kept getting 403 errors. But I think we can do it all through docker images
- Tried isntalling on my machine (macOS)

```sh
## download
brew install consul
brew install vault

## run
Consul agent — dev
Vault server -dev

## setup
export VAULT_ADDR='http://127.0.0.1:8200'

## An "unseal key" and "Root Token" are displayed...
# Unseal Key: ***
# Root Token: ***
```

```sh
## in a new terminal
vault operator unseal
# Unseal Key (will be hidden): ***
vault login
# Token (will be hidden): ***

## enable k/v storage
vault secrets enable -path=kv kv-v2

## Store a secret named 'mySecret'
vault kv put kv/mySecret key1=value1 key2=value2

## See the contents
vault kv get kv/mySecret

# ==== Data ====
# Key     Value
# ---     -----
# key1    value1
# key2    value2
```

I think the basic idea is that on the VM we add this secret to the vault (or possibly consul) instnace to store it encrypted. Then we add a way to access the vault to our CI/CD tool (probably Github). Although at that point, I don't know why we wouldn't just pass the secret itself instead of the vault access token...

Helpful links:
Secrets w/ Github: https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners
Secrets w/ Github+Vault: https://learn.hashicorp.com/tutorials/vault/github-actions?in=vault/new-release
Github self-hosted runners: https://learn.hashicorp.com/tutorials/vault/github-actions?in=vault/new-release

## Data sourcing & storage

## Frontend dashboard

## Wallets & arbitrage

## Other exchanges
