# Modo TV Linux

### Automação de ambiente multimídia no GNOME com Wayland

Estudo de caso de um projeto pessoal desenvolvido para transformar um computador Linux em uma central multimídia, utilizando uma televisão como segunda tela e um celular como controle remoto.

## Objetivo

Criar uma solução que permita alternar entre o ambiente de trabalho e um ambiente dedicado ao entretenimento, automatizando tarefas que normalmente exigiriam diversas configurações manuais.

O projeto surgiu de uma necessidade real e foi desenvolvido por meio de investigação técnica, testes, integração de ferramentas e resolução de problemas.

## Funcionalidades implementadas

- Ativação de um modo TV utilizando uma segunda tela.
- Alternância entre monitor principal e televisão.
- Direcionamento automático do áudio para a saída HDMI.
- Abertura de aplicativos e serviços de entretenimento.
- Interface de navegação adaptada para televisão.
- Controle remoto pelo navegador do celular.
- Comandos de navegação, teclado e controle de mídia.
- Retorno ao ambiente de trabalho com restauração das configurações.
- Integração com serviço de usuário do systemd.

## Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Linux | Ambiente operacional |
| GNOME / Wayland | Gerenciamento da sessão gráfica |
| Bash / Shell Script | Automação de comandos e processos |
| Python | Servidor local e integração de funcionalidades |
| HTML, CSS e JavaScript | Interfaces da Home e do controle remoto |
| systemd | Gerenciamento do serviço |
| Flatpak | Execução de aplicativos |
| PipeWire / ferramentas de áudio | Seleção da saída de som |

## Arquitetura da solução

O sistema integra três componentes principais:

**1. Automação do ambiente**

Scripts responsáveis pela configuração dos monitores, seleção do dispositivo de áudio e gerenciamento dos aplicativos.

**2. Servidor de controle**

Aplicação Python responsável por receber requisições e encaminhar comandos aos scripts do sistema.

**3. Interfaces web**

Uma interface visual para a televisão e um controle remoto acessível pelo navegador do celular.

### Fluxo simplificado

Celular → Interface web → Servidor Python → Scripts Bash → GNOME / aplicativos

## Desafios técnicos

Durante o desenvolvimento, foram trabalhados desafios como:

- Automação de monitores em uma sessão Wayland.
- Gerenciamento de janelas e aplicativos no GNOME.
- Integração entre comandos do sistema e interfaces web.
- Seleção e restauração da saída de áudio.
- Organização dos scripts para execução coordenada.
- Diagnóstico e correção de comportamentos inesperados.

## Documentação técnica

Este repositório apresenta um estudo de caso do Modo TV Linux, com explicações sobre as soluções desenvolvidas e exemplos dos comandos utilizados.

### Guias disponíveis

- [01 — Gerenciamento de monitores no GNOME com Wayland](docs/01-gerenciamento-monitores.md)
- [02 — Automação de áudio HDMI no Linux](docs/02-gerenciamento-audio.md)
- [03 — Arquitetura e integração entre Python e Bash](docs/03-arquitetura-integracao.md)

Os guias demonstram os desafios enfrentados, as ferramentas utilizadas e as decisões técnicas adotadas.

A documentação não contém configurações pessoais da instalação original.

## Exemplos de código

- [Alternância de monitores com Bash](exemplos/alternar-monitor.sh)

O exemplo demonstra a construção parametrizada dos comandos `gdctl` para alternar entre monitor e televisão.

Por segurança, o script é demonstrativo: imprime os comandos, mas não modifica a configuração dos monitores.

Este repositório apresenta documentação técnica e exemplos selecionados. Não é uma distribuição completa do sistema original.

## Segurança e privacidade

Os exemplos publicados não devem conter senhas, tokens, dados pessoais ou configurações privadas.

O controle remoto envolve comandos que interagem com o sistema operacional. Qualquer implementação que permita acesso pela rede deve incluir mecanismos adequados de autenticação e proteção da comunicação.

## Competências demonstradas

- Análise e resolução de problemas técnicos.
- Automação de processos.
- Administração e configuração de ambiente Linux.
- Integração entre sistemas e ferramentas.
- Desenvolvimento de soluções com Python e Shell Script.
- Testes, diagnóstico e documentação técnica.

## Status

Projeto pessoal funcional no ambiente original.

Documentação técnica e exemplo Bash disponíveis para consulta.

---

**Projeto desenvolvido por Tailana Mattos.**
