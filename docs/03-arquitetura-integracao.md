# Arquitetura e integração do Modo TV Linux

## Visão geral

O Modo TV integra uma interface web, um servidor Python e scripts Bash para automatizar tarefas no ambiente gráfico Linux.

O objetivo foi permitir o controle de aplicativos e recursos do computador por uma interface acessível pelo navegador do celular.

## Arquitetura

    Celular
       |
       v
    Interface web (HTML, CSS e JavaScript)
       |
       v
    Servidor HTTP em Python
       |
       v
    Scripts Bash e comandos do sistema
       |
       v
    GNOME / Wayland / Aplicativos / Áudio

## Servidor Python

A implementação utiliza recursos da biblioteca padrão do Python para receber requisições HTTP e encaminhar ações aos componentes responsáveis.

Entre as funcionalidades desenvolvidas estão:

- Abertura e encerramento de aplicativos.
- Ativação e desativação do Modo TV.
- Consulta do aplicativo ativo.
- Controle de navegação e reprodução de mídia.
- Envio de comandos de teclado e mouse.

## Integração com scripts Bash

O servidor utiliza o módulo subprocess para executar scripts e comandos do sistema operacional.

Exemplo simplificado de execução:

    subprocess.Popen(
        [str(script), acao],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )

A utilização de uma lista de argumentos permite executar o programa sem construir uma linha de comando interpretada pelo shell.

Na implementação original, os comandos aceitos são tratados por rotas específicas e os aplicativos são selecionados a partir de opções previamente definidas.

## Controle de teclado e mouse

O projeto utiliza ydotool para enviar comandos de entrada em uma sessão Wayland.

Exemplos de funcionalidades:

- Navegação por teclas direcionais.
- Confirmação e retorno.
- Digitação de texto.
- Movimentação do ponteiro.
- Cliques e rolagem.

## Gerenciamento de processos

Foram utilizadas duas abordagens principais:

- subprocess.Popen: inicia processos sem aguardar sua conclusão.
- subprocess.run: executa comandos e permite aguardar ou consultar seu resultado.

A escolha depende da necessidade de cada operação.

## Integração com o ambiente gráfico

Os scripts coordenam diferentes ferramentas:

- gdctl para configuração de monitores.
- pactl para gerenciamento de áudio.
- Flatpak para execução de aplicativos.
- ydotool para comandos de entrada.
- systemd para gerenciamento do serviço.

## Cuidados de segurança

Um servidor capaz de executar comandos no sistema operacional exige proteção.

Os exemplos de arquitetura apresentados neste portfólio são demonstrativos e não constituem uma implementação pronta para exposição na rede.

Uma instalação real deve considerar autenticação, autorização, proteção contra requisições indevidas e comunicação criptografada.

## Competências demonstradas

- Integração entre Python e Bash.
- Desenvolvimento de interfaces web.
- Automação de tarefas no Linux.
- Gerenciamento de processos.
- Organização de componentes de software.
- Análise e resolução de problemas.
- Documentação de arquitetura técnica.
