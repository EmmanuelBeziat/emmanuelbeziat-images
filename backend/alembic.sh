#!/bin/bash
# Helper script to run alembic commands
# Usage: ./alembic.sh <alembic_command> [args...]

cd "$(dirname "$0")"
python3 -m alembic "$@"

