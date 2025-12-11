#!/usr/bin/env bash
# simple wait-for PostgreSQL then run the command
set -e
host="$1"
port="$2"
shift 2
until pg_isready -h "$host" -p "$port" >/dev/null 2>&1; do
  echo "Waiting for Postgres at $host:$port..."
  sleep 1
done

exec "$@"