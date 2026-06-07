#!/usr/bin/env sh
set -eu

: "${BACKUP_TIME:=03:00}"
: "${BACKUP_RUN_ON_STARTUP:=false}"

to_number() {
  value="$1"
  while [ "${value#0}" != "$value" ]; do
    value="${value#0}"
  done

  if [ -z "$value" ]; then
    value=0
  fi

  echo "$value"
}

validate_backup_time() {
  hour="${BACKUP_TIME%:*}"
  minute="${BACKUP_TIME#*:}"

  if [ "$hour" = "$BACKUP_TIME" ] || [ -z "$hour" ] || [ -z "$minute" ]; then
    echo "BACKUP_TIME debe tener formato HH:MM, por ejemplo 03:00" >&2
    exit 1
  fi

  case "$hour$minute" in
    *[!0-9]*)
      echo "BACKUP_TIME debe tener solo numeros y dos puntos, por ejemplo 03:00" >&2
      exit 1
      ;;
  esac

  hour="$(to_number "$hour")"
  minute="$(to_number "$minute")"

  if [ "$hour" -lt 0 ] || [ "$hour" -gt 23 ] || [ "$minute" -lt 0 ] || [ "$minute" -gt 59 ]; then
    echo "BACKUP_TIME fuera de rango. Usa HH:MM entre 00:00 y 23:59" >&2
    exit 1
  fi
}

run_backup() {
  if ! sh /usr/local/bin/db-backup.sh; then
    echo "El backup fallo; se reintentara en la proxima hora programada" >&2
  fi
}

seconds_until_next_backup() {
  target_hour="$(to_number "${BACKUP_TIME%:*}")"
  target_minute="$(to_number "${BACKUP_TIME#*:}")"
  current_hour="$(to_number "$(date +%H)")"
  current_minute="$(to_number "$(date +%M)")"
  current_second="$(to_number "$(date +%S)")"

  target_seconds=$((target_hour * 3600 + target_minute * 60))
  current_seconds=$((current_hour * 3600 + current_minute * 60 + current_second))
  delay=$((target_seconds - current_seconds))

  if [ "$delay" -le 0 ]; then
    delay=$((delay + 86400))
  fi

  echo "$delay"
}

validate_backup_time

if [ "$BACKUP_RUN_ON_STARTUP" = "true" ]; then
  run_backup
fi

while true; do
  delay="$(seconds_until_next_backup)"
  echo "Proximo backup diario a las $BACKUP_TIME. Esperando $delay segundos"
  sleep "$delay"
  run_backup
done
