#! /usr/bin/env bash

set -euo pipefail

function main(){
  python /app/main.py --action prepare
  python /app/trend_following_cli.py /tmp/candles.json /tmp/accounts.json > /tmp/decision.json
  python /app/main.py --action execute
}

main
