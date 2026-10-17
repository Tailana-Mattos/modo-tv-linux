#!/usr/bin/env bash
set -euo pipefail

# Exemplo demonstrativo baseado no projeto Modo TV Linux.
# Por padrão, apenas mostra os comandos; não altera os monitores.

TV_OUTPUT="${TV_OUTPUT:-HDMI-1}"
PC_OUTPUT="${PC_OUTPUT:-DP-1}"

TV_MODE="${TV_MODE:-1920x1080@60.000}"
PC_MODE="${PC_MODE:-2560x1440@60.000}"

mostrar_comando() {
    printf 'Comando:'
    printf ' %q' "$@"
    printf '\n'
}

case "${1:-}" in
    tv)
        mostrar_comando gdctl set \
            --logical-monitor --primary \
            --monitor "$TV_OUTPUT" \
            --mode "$TV_MODE" \
            --scale 1 --x 0 --y 0
        ;;
    pc)
        mostrar_comando gdctl set \
            --logical-monitor --primary \
            --monitor "$PC_OUTPUT" \
            --mode "$PC_MODE" \
            --scale 1 --x 0 --y 0
        ;;
    status)
        mostrar_comando gdctl show
        ;;
    *)
        echo "Uso: bash alternar-monitor.sh {tv|pc|status}"
        exit 1
        ;;
esac
