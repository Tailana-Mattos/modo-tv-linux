# Gerenciamento de monitores no GNOME com Wayland

## Objetivo

Automatizar a alternância entre o monitor do computador e uma televisão conectada por HDMI, sem precisar alterar manualmente as configurações do GNOME.

## Tecnologias

- GNOME com Wayland
- Bash
- gdctl
- Logs e verificação de estado

## Identificação dos monitores

Antes de configurar as telas, consultar os monitores e modos disponíveis:

    gdctl show

## Exemplo: ativar a televisão

Os identificadores e modos abaixo são exemplos e devem ser adaptados ao equipamento:

    gdctl set --logical-monitor --primary --monitor HDMI-1 --mode 1920x1080@60.000 --scale 1 --x 0 --y 0

## Exemplo: retornar ao monitor principal

    gdctl set --logical-monitor --primary --monitor DP-1 --mode 2560x1440@60.000 --scale 1 --x 0 --y 0

**Atenção:** os comandos acima alteram a configuração de vídeo. Devem ser executados somente após conferir os monitores disponíveis.

## Como a automação foi implementada

O script Bash do projeto utiliza o gdctl para aplicar as configurações de vídeo.

A implementação inclui:

1. Identificação das saídas de vídeo por variáveis configuráveis.
2. Aplicação de resolução, frequência, escala e posição.
3. Verificação do monitor ativo.
4. Novas tentativas quando a mudança não é aplicada imediatamente.
5. Registro de informações de diagnóstico em logs.

## Desafios resolvidos

A automação foi desenvolvida para funcionar em uma sessão GNOME com Wayland, na qual o gerenciamento de monitores é diferente do ambiente X11 tradicional.

## Competências demonstradas

- Automação com Shell Script.
- Configuração e administração de Linux.
- Integração com ferramentas do GNOME.
- Diagnóstico e tratamento de falhas.
- Parametrização de scripts.
