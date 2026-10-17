#!/usr/bin/env python3
import json
import sys
from pathlib import Path
import os

if len(sys.argv) != 2:
    raise SystemExit("Uso: ler-config.py CHAVE")

config_file = Path(
    os.environ.get(
        "MODO_TV_CONFIG",
        str(Path(__file__).with_name("config.json"))
    )
)

with config_file.open(encoding="utf-8") as arquivo:
    config = json.load(arquivo)

valor = config
for parte in sys.argv[1].split("."):
    valor = valor[parte]

if not isinstance(valor, (str, int, float, bool)):
    raise SystemExit("Valor de configuração inválido")

print(valor)
