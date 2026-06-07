#!/usr/bin/env sh
set -eu

: "${POSTGRES_HOST:=db}"
: "${POSTGRES_PORT:=5432}"
: "${POSTGRES_DB:?POSTGRES_DB es obligatorio}"
: "${POSTGRES_USER:?POSTGRES_USER es obligatorio}"
: "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD es obligatorio}"
: "${BACKUP_DIR:=/backups}"
: "${BACKUP_RETENTION_DAYS:=7}"

mkdir -p "$BACKUP_DIR"

timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
backup_file="$BACKUP_DIR/${POSTGRES_DB}_${timestamp}.sql.gz"
tmp_file="$backup_file.tmp"
tmp_sql="$BACKUP_DIR/${POSTGRES_DB}_${timestamp}.sql.tmp"

export PGPASSWORD="$POSTGRES_PASSWORD"

echo "Creando backup: $backup_file"

if pg_dump \
  --host "$POSTGRES_HOST" \
  --port "$POSTGRES_PORT" \
  --username "$POSTGRES_USER" \
  --dbname "$POSTGRES_DB" \
  --no-owner \
  --no-privileges \
  --file "$tmp_sql"; then
  if gzip -c "$tmp_sql" > "$tmp_file"; then
    mv "$tmp_file" "$backup_file"
    rm -f "$tmp_sql"
    echo "Backup creado correctamente: $backup_file"
  else
    rm -f "$tmp_file" "$tmp_sql"
    echo "Error comprimiendo backup de Postgres" >&2
    exit 1
  fi
else
  rm -f "$tmp_file" "$tmp_sql"
  echo "Error creando backup de Postgres" >&2
  exit 1
fi

if [ "$BACKUP_RETENTION_DAYS" -gt 0 ] 2>/dev/null; then
  retention_minutes=$((BACKUP_RETENTION_DAYS * 24 * 60))
  echo "Eliminando backups con mas de $BACKUP_RETENTION_DAYS dias"
  find "$BACKUP_DIR" \
    -type f \
    -name "${POSTGRES_DB}_*.sql.gz" \
    -mmin +"$retention_minutes" \
    -delete
fi
