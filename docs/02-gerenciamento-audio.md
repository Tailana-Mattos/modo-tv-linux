# Automação de áudio HDMI no Linux

## Objetivo

Automatizar a troca da saída de áudio entre o computador e a televisão durante a ativação e desativação do Modo TV.

A solução evita a necessidade de selecionar manualmente o dispositivo de áudio a cada utilização.

## Tecnologias utilizadas

- Linux
- Bash
- pactl
- Servidor de áudio compatível com PulseAudio, incluindo PipeWire com pipewire-pulse

## Identificação dos dispositivos

Para consultar as saídas de áudio disponíveis:

    pactl list short sinks

Para consultar as placas de áudio:

    pactl list short cards

Os identificadores variam conforme o equipamento e devem ser configurados individualmente.

## Ativação do áudio da televisão

O script utiliza a seguinte sequência:

1. Seleciona o perfil HDMI da placa de áudio.
2. Aguarda a saída de áudio da televisão aparecer.
3. Define a televisão como saída padrão.
4. Remove o silenciamento da saída.
5. Ajusta o volume configurado.

Exemplos dos comandos utilizados:

    pactl set-card-profile "$GPU_CARD" "$TV_PROFILE"
    pactl set-default-sink "$TV_SINK"
    pactl set-sink-mute "$TV_SINK" 0
    pactl set-sink-volume "$TV_SINK" "$TV_VOLUME"

As variáveis representam configurações locais e não devem ser substituídas por identificadores de outro computador sem verificação.

## Retorno ao áudio do computador

Ao desativar o Modo TV, a implementação:

1. Altera o perfil da placa de áudio para pro-audio.
2. Aguarda a saída habitual do computador aparecer.
3. Define essa saída como padrão.
4. Remove o silenciamento.

Comandos correspondentes:

    pactl set-card-profile "$GPU_CARD" pro-audio
    pactl set-default-sink "$PC_SINK"
    pactl set-sink-mute "$PC_SINK" 0

## Verificação e tratamento de falhas

A função wait_sink verifica se a saída desejada aparece na listagem de dispositivos.

O script realiza até 40 verificações, com intervalo de 0,25 segundo entre elas.

Se a saída não aparecer, a operação informa o erro e é interrompida.

Essa verificação evita tentar selecionar um dispositivo que ainda não está disponível.

## Consulta do estado atual

Para consultar a saída padrão:

    pactl get-default-sink

## Competências demonstradas

- Automação com Bash.
- Gerenciamento de dispositivos de áudio no Linux.
- Integração entre hardware e software.
- Parametrização de configurações.
- Verificação de disponibilidade de recursos.
- Tratamento de erros e diagnóstico.
