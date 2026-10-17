#!/usr/bin/env python3

from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import json
import threading
import subprocess
import time

PUBLIC_DIR = Path(__file__).resolve().parent
CACHE_DIR = PUBLIC_DIR / "dados-publicos/cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = PUBLIC_DIR / "config.json"

with CONFIG_FILE.open(encoding="utf-8") as arquivo_config:
    CONFIG = json.load(arquivo_config)

HOST = CONFIG["server"]["host"]
PORT = int(CONFIG["server"]["port"])

BASE = PUBLIC_DIR
HOME_HTML = BASE / "index.html"
REMOTE_HTML_FILE = BASE / "remote.html"
LAUNCHER = PUBLIC_DIR / "app-launcher-publico"

lock = threading.Lock()
commands = []
counter = 0
ACTIVE_APP_FILE = PUBLIC_DIR / "dados-publicos/cache/modo-tv-active-app"

try:
    active_app = ACTIVE_APP_FILE.read_text().strip() or "home"
except Exception:
    active_app = "home"

FOCUS_APP = PUBLIC_DIR / "focus-tv-app-gnome-publico"

def send_freetube_key(action):
    """Envia um comando de teclado ao FreeTube."""
    keys = {
        "search": ["29:1", "38:1", "38:0", "29:0"],       # Ctrl+L
        "back":   ["56:1", "105:1", "105:0", "56:0"],    # Alt+Left
        "ok":     ["28:1", "28:0"],                       # Enter
        "play":   ["57:1", "57:0"],                       # Space
    }

    sequence = keys.get(action)
    if not sequence:
        return False

    subprocess.run(
        [str(FOCUS_APP), "freetube"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Aguarda um instante para o aplicativo receber o foco.
    time.sleep(0.25)

    subprocess.Popen(
        ["ydotool", "key", *sequence],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return True


def type_freetube_text(text):
    """Digita texto no campo atualmente focado do FreeTube."""
    subprocess.run(
        [str(FOCUS_APP), "freetube"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    time.sleep(0.25)

    subprocess.Popen(
        ["ydotool", "type", "--key-delay", "20", text],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )



class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def send_bytes(self, data, content_type, status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        global counter, active_app

        u = urlparse(self.path)

        if u.path in ("/", "/remote"):
            self.send_bytes(
                REMOTE_HTML_FILE.read_bytes(),
                "text/html; charset=utf-8"
            )
            return

        if u.path == "/tv":
            with open(CACHE_DIR / "modo-tv-home-trace.log", "a") as f:
                f.write(
                    f"{time.strftime('%F %T')} GET /tv "
                    f"ip={self.client_address[0]} "
                    f"ua={self.headers.get('User-Agent','-')} "
                    f"referer={self.headers.get('Referer','-')}\n"
                )

            # Ao abrir a Home, descarta comandos antigos do controle.
            # Mantemos o contador para que apenas novos comandos sejam executados.
            with lock:
                commands.clear()

            self.send_bytes(HOME_HTML.read_bytes(), "text/html; charset=utf-8")
            return

        if u.path == "/wallpapers.js":
            js = BASE / "wallpapers.js"

            if not js.exists():
                self.send_bytes(b"not found", "text/plain", 404)
                return

            self.send_bytes(
                js.read_bytes(),
                "application/javascript; charset=utf-8"
            )
            return

        if u.path.startswith("/icons/"):
            nome = u.path[len("/icons/"):]

            if not nome or "/" in nome or "\\" in nome:
                self.send_bytes(b"bad path", "text/plain", 400)
                return

            arquivo = BASE / "recursos-publicos/icons" / nome

            if not arquivo.exists() or not arquivo.is_file():
                self.send_bytes(b"not found", "text/plain", 404)
                return

            ext = arquivo.suffix.lower()

            tipos = {
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".webp": "image/webp",
                ".svg": "image/svg+xml",
            }

            content_type = tipos.get(ext)

            if not content_type:
                self.send_bytes(b"unsupported", "text/plain", 415)
                return

            self.send_bytes(
                arquivo.read_bytes(),
                content_type
            )
            return

        if u.path.startswith("/wallpapers/"):
            nome = u.path[len("/wallpapers/"):]

            # Evita caminho malicioso.
            if not nome or "/" in nome or "\\" in nome:
                self.send_bytes(b"bad path", "text/plain", 400)
                return

            arquivo = BASE / "wallpapers" / nome

            if not arquivo.exists() or not arquivo.is_file():
                self.send_bytes(b"not found", "text/plain", 404)
                return

            ext = arquivo.suffix.lower()

            tipos = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".webp": "image/webp",
            }

            content_type = tipos.get(ext)

            if not content_type:
                self.send_bytes(b"unsupported", "text/plain", 415)
                return

            self.send_bytes(
                arquivo.read_bytes(),
                content_type
            )
            return

        if u.path == "/launch":
            app = parse_qs(u.query).get("app", [""])[0]

            allowed = {
                "freetube",
                "jellyfin",
                "jellyfin_primary",
                "jellyfin_secondary",
                "netflix",
                "prime",
                "disney",
                "spotify",
                "firefox",
                "iptv",
            }

            if app not in allowed:
                self.send_bytes(b"bad app", "text/plain", 400)
                return

            try:
                subprocess.Popen(
                    [str(LAUNCHER), app],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True,
                )
                # O app só vira "ativo" quando o launcher confirmar
                # que a janela real apareceu e chamar /activate.
                self.send_bytes(b"ok", "text/plain")
            except Exception as e:
                self.send_bytes(
                    ("launch error: " + str(e)).encode(),
                    "text/plain",
                    500,
                )
            return

        if u.path == "/activate":
            app = parse_qs(u.query).get("app", [""])[0]

            allowed = {
                "home",
                "freetube",
                "jellyfin",
                "jellyfin_primary",
                "jellyfin_secondary",
                "netflix",
                "prime",
                "disney",
                "spotify",
                "firefox",
                "iptv",
            }

            if app not in allowed:
                self.send_bytes(b"bad app", "text/plain", 400)
                return

            active_app = app
            ACTIVE_APP_FILE.write_text(active_app)
            self.send_bytes(b"ok", "text/plain")
            return

        if u.path == "/home":
            with open(CACHE_DIR / "modo-tv-home-trace.log", "a") as f:
                f.write(
                    f"{time.strftime('%F %T')} GET /home "
                    f"ip={self.client_address[0]} "
                    f"ua={self.headers.get('User-Agent','-')} "
                    f"referer={self.headers.get('Referer','-')}\n"
                )

            subprocess.Popen(
                [str(PUBLIC_DIR / "home-gnome-publico"), active_app],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            active_app = "home"
            ACTIVE_APP_FILE.write_text(active_app)
            self.send_bytes(b"ok", "text/plain")
            return

        if u.path == "/close":
            app_to_close = active_app

            subprocess.Popen(
                [
                    str(PUBLIC_DIR / "close-app-gnome-publico"),
                    app_to_close,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )

            active_app = "home"
            ACTIVE_APP_FILE.write_text(active_app)
            self.send_bytes(b"ok", "text/plain")
            return

        if u.path == "/power":
            modo_tv = PUBLIC_DIR / "modo-tv-gnome-publico"

            # O Power representa uma sessão real do Modo TV.
            # A saída de vídeo pode ser ativada automaticamente pelo sistema quando
            # o monitor do PC é desligado, portanto não serve como estado.
            MODO_TV_ENABLED = PUBLIC_DIR / "dados-publicos/cache/modo-tv-enabled"
            ligado = MODO_TV_ENABLED.exists()

            acao = "desligar" if ligado else "ligar"

            # Se estamos SAINDO do Modo TV, fecha primeiro o app
            # atualmente ativo. Assim nenhuma janela da TV volta
            # para o desktop do PC quando o LG for reativado.
            if acao == "desligar":
                try:
                    app_to_close = (
                        ACTIVE_APP_FILE.read_text().strip()
                        or active_app
                    )
                except Exception:
                    app_to_close = active_app

                if app_to_close and app_to_close != "home":
                    subprocess.run(
                        [
                            str(
                                PUBLIC_DIR / "close-app-gnome-publico"
                            ),
                            app_to_close,
                        ],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        timeout=5,
                    )

                    time.sleep(0.4)

                active_app = "home"
                ACTIVE_APP_FILE.write_text(active_app)

            subprocess.Popen(
                [str(modo_tv), acao],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )

            self.send_bytes(
                json.dumps({
                    "ok": True,
                    "action": acao
                }).encode(),
                "application/json; charset=utf-8",
            )
            return

        if u.path == "/status":
            # Estado lógico do Modo TV, independente da HDMI.
            MODO_TV_ENABLED = PUBLIC_DIR / "dados-publicos/cache/modo-tv-enabled"
            ligado = MODO_TV_ENABLED.exists()

            try:
                app_status = ACTIVE_APP_FILE.read_text().strip() or active_app
            except Exception:
                app_status = active_app

            if not ligado:
                app_status = "home"

            self.send_bytes(
                json.dumps({
                    "power": ligado,
                    "app": app_status,
                }).encode(),
                "application/json; charset=utf-8",
            )
            return

        if u.path == "/active":
            self.send_bytes(
                json.dumps({"app": active_app}).encode(),
                "application/json; charset=utf-8",
            )
            return

        if u.path == "/type":
            text = parse_qs(u.query).get("text", [""])[0]

            if active_app == "home":
                self.send_bytes(b"home has no text target", "text/plain", 400)
                return

            if not text:
                self.send_bytes(b"empty text", "text/plain", 400)
                return

            if len(text) > 1000:
                self.send_bytes(b"text too long", "text/plain", 400)
                return

            focus_tv = PUBLIC_DIR / "focus-tv-app-gnome-publico"

            ok = subprocess.run(
                [str(focus_tv), active_app],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            ).returncode == 0

            if not ok:
                self.send_bytes(b"app not available", "text/plain", 400)
                return

            time.sleep(0.20)

            subprocess.run(
                ["ydotool", "type", "--key-delay", "20", text],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            self.send_bytes(b"ok", "text/plain")
            return

        if u.path == "/key":
            key_name = parse_qs(u.query).get("key", [""])[0]

            keys = {
                "enter": ["28:1", "28:0"],
                "backspace": ["14:1", "14:0"],
                "tab": ["15:1", "15:0"],
            }

            sequence = keys.get(key_name)

            if not sequence or active_app == "home":
                self.send_bytes(b"bad key", "text/plain", 400)
                return

            focus_tv = PUBLIC_DIR / "focus-tv-app-gnome-publico"

            if subprocess.run(
                [str(focus_tv), active_app],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            ).returncode != 0:
                self.send_bytes(b"app not available", "text/plain", 400)
                return

            time.sleep(0.15)

            subprocess.Popen(
                ["ydotool", "key", *sequence],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            self.send_bytes(b"ok", "text/plain")
            return

        if u.path == "/mouse-start":
            mouse_enter = PUBLIC_DIR / "mouse-tv-enter-publico"

            subprocess.run(
                [str(mouse_enter)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            if active_app != "home":
                focus_tv = PUBLIC_DIR / "focus-tv-app-gnome-publico"
                subprocess.run(
                    [str(focus_tv), active_app],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

            self.send_bytes(b"ok", "text/plain")
            return

        if u.path == "/mouse":
            qs = parse_qs(u.query)

            try:
                dx = int(float(qs.get("dx", ["0"])[0]))
                dy = int(float(qs.get("dy", ["0"])[0]))
            except ValueError:
                self.send_bytes(b"bad mouse movement", "text/plain", 400)
                return

            dx = max(-180, min(180, dx))
            dy = max(-180, min(180, dy))

            subprocess.Popen(
                ["ydotool", "mousemove", "--", str(dx), str(dy)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            self.send_bytes(b"ok", "text/plain")
            return

        if u.path == "/click":
            mouse_enter = PUBLIC_DIR / "mouse-tv-enter-publico"
            subprocess.run(
                [str(mouse_enter)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            if active_app != "home":
                focus_tv = PUBLIC_DIR / "focus-tv-app-gnome-publico"
                subprocess.run(
                    [str(focus_tv), active_app],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

            subprocess.Popen(
                ["ydotool", "click", "0xC0"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            self.send_bytes(b"ok", "text/plain")
            return

        if u.path == "/wheel":
            qs = parse_qs(u.query)

            try:
                dy = int(float(qs.get("dy", ["0"])[0]))
            except ValueError:
                self.send_bytes(b"bad wheel", "text/plain", 400)
                return

            dy = max(-6, min(6, dy))

            subprocess.Popen(
                ["ydotool", "mousemove", "--wheel", "0", str(dy)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            self.send_bytes(b"ok", "text/plain")
            return

        if u.path == "/volume":
            action = parse_qs(u.query).get("action", [""])[0]

            tv_sink = str(CONFIG["audio"]["tv_sink"]).strip()

            if action == "up":
                subprocess.Popen(
                    ["pactl", "set-sink-volume", tv_sink, "+5%"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            elif action == "down":
                subprocess.Popen(
                    ["pactl", "set-sink-volume", tv_sink, "-5%"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            elif action == "mute":
                subprocess.Popen(
                    ["pactl", "set-sink-mute", tv_sink, "toggle"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            else:
                self.send_bytes(b"bad volume action", "text/plain", 400)
                return

            self.send_bytes(b"ok", "text/plain")
            return

        if u.path == "/playpause":
            if active_app != "home":
                focus_tv = PUBLIC_DIR / "focus-tv-app-gnome-publico"

                subprocess.run(
                    [str(focus_tv), active_app],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

                time.sleep(0.15)

            subprocess.Popen(
                ["ydotool", "key", "164:1", "164:0"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            self.send_bytes(b"ok", "text/plain")
            return

        if u.path == "/control":
            c = parse_qs(u.query).get("cmd", [""])[0]

            # Comandos específicos do FreeTube
            if active_app == "freetube" and c in {"search", "back", "ok", "play"}:
                if send_freetube_key(c):
                    self.send_bytes(b"ok", "text/plain")
                else:
                    self.send_bytes(b"bad command", "text/plain", 400)
                return

            # Navegacao real nos Web Apps Vivaldi.
            if active_app in {"freetube", "iptv", "netflix", "prime", "disney", "jellyfin_primary", "jellyfin_secondary"} and c in {"up", "down", "left", "right", "ok"}:
                focus_tv = PUBLIC_DIR / "focus-tv-app-gnome-publico"

                focus_name = "youtube" if active_app == "freetube" else active_app

                ok = subprocess.run(
                    [str(focus_tv), focus_name],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                ).returncode == 0

                if not ok:
                    self.send_bytes(b"app not available", "text/plain", 400)
                    return

                time.sleep(0.15)

                keys = {
                    "up":    ["103:1", "103:0"],
                    "down":  ["108:1", "108:0"],
                    "left":  ["105:1", "105:0"],
                    "right": ["106:1", "106:0"],
                    "ok":    ["28:1", "28:0"],
                }

                subprocess.Popen(
                    ["ydotool", "key", *keys[c]],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

                self.send_bytes(b"ok", "text/plain")
                return

            # Voltar real para os aplicativos atuais.
            if c == "back":
                if active_app == "home":
                    self.send_bytes(b"ok", "text/plain")
                    return

                focus_tv = PUBLIC_DIR / "focus-tv-app-gnome-publico"

                ok = subprocess.run(
                    [str(focus_tv), active_app],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                ).returncode == 0

                if not ok:
                    self.send_bytes(b"app not available", "text/plain", 400)
                    return

                time.sleep(0.15)

                if active_app == "spotify":
                    # No Spotify, Escape é mais útil que voltar página.
                    sequence = ["1:1", "1:0"]
                else:
                    # Alt + Left: voltar página/tela anterior.
                    sequence = ["56:1", "105:1", "105:0", "56:0"]

                subprocess.Popen(
                    ["ydotool", "key", *sequence],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

                self.send_bytes(b"ok", "text/plain")
                return

            if c in {"up","down","left","right","ok","back","home"}:
                with lock:
                    counter += 1
                    commands.append({"id": counter, "cmd": c})
                    if len(commands) > 100:
                        del commands[:-100]
                self.send_bytes(b"ok", "text/plain")
            else:
                self.send_bytes(b"bad command", "text/plain", 400)
            return

        if u.path == "/poll":
            try:
                after = int(parse_qs(u.query).get("after", ["0"])[0])
            except ValueError:
                after = 0

            with lock:
                out = [c for c in commands if c["id"] > after]

            self.send_bytes(
                json.dumps(out).encode(),
                "application/json; charset=utf-8"
            )
            return

        self.send_bytes(b"not found", "text/plain", 404)

ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
