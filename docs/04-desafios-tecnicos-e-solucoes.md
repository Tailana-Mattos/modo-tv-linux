# Desafios técnicos e soluções — Modo TV Linux

## Contexto do projeto

O Modo TV Linux surgiu da necessidade de utilizar um computador com GNOME e Wayland como central multimídia, permitindo alternar entre monitor e televisão e controlar aplicativos pelo celular.

O projeto integra Bash, Python, tecnologias web e ferramentas do Linux.

Este documento apresenta desafios técnicos, decisões de implementação e resultados observados.

## 1. Alternância de monitores no Wayland

**Problema:** automatizar a troca entre monitor e televisão sem depender de ajustes manuais no GNOME.

**Investigação:** identificar os monitores, modos disponíveis e ferramentas compatíveis com a sessão Wayland.

**Solução:** utilizar `gdctl` em scripts Bash, com parâmetros configuráveis, verificações de estado, novas tentativas e registros de diagnóstico.

**Resultado:** a alternância passou a ser acionada pelo Modo TV, com possibilidade de retornar ao monitor principal.

**Competências:** administração Linux, automação, diagnóstico e tratamento de falhas.

## 2. Troca automática de áudio

**Problema:** a mudança de imagem para a televisão não garante que o áudio utilize a saída HDMI.

**Investigação:** consultar dispositivos e perfis disponíveis com `pactl` e considerar o tempo necessário para a saída desejada aparecer.

**Solução:** alternar perfis de áudio, aguardar a disponibilidade da saída, definir o dispositivo padrão e restaurar o áudio do computador ao encerrar.

**Resultado:** o processo de ativação e desativação do Modo TV passou a incluir o gerenciamento da saída de som.

**Competências:** integração de hardware e software, scripts Bash e verificação de recursos.

## 3. Controle remoto pelo navegador

**Problema:** permitir o uso do computador à distância, sem depender de teclado e mouse físicos durante a reprodução de conteúdo na televisão.

**Investigação:** separar a interface de controle das operações executadas no sistema.

**Solução:** integrar HTML, CSS e JavaScript a um servidor HTTP em Python, responsável por encaminhar ações para scripts e comandos previamente definidos.

**Resultado:** o celular pode funcionar como interface de controle para navegação, aplicativos e reprodução de mídia.

**Competências:** integração de sistemas, Python, desenvolvimento web e organização de responsabilidades.

## 4. Comandos de entrada no Wayland

**Problema:** enviar comandos de teclado e mouse para os aplicativos em uma sessão Wayland.

**Solução:** integrar `ydotool` ao sistema de controle para navegação direcional, confirmação, digitação, cliques e movimentação do ponteiro.

**Resultado:** o controle remoto passou a oferecer operações de navegação e interação com os aplicativos.

**Competências:** automação de interface, integração com Linux e resolução de problemas.

## 5. Integração de aplicativos e processos

**Problema:** coordenar abertura de aplicativos, alternância de telas, áudio e comandos de controle em uma única solução.

**Solução:** organizar responsabilidades entre servidor Python, scripts Bash e ferramentas como Flatpak e systemd. Utilizar `subprocess.Popen` ou `subprocess.run` conforme a necessidade da operação.

**Resultado:** diferentes recursos do ambiente Linux passaram a funcionar de maneira integrada por meio do Modo TV.

**Competências:** arquitetura de soluções, automação, gerenciamento de processos e documentação técnica.

## Limitações e cuidados de segurança

A documentação apresenta a arquitetura e as decisões técnicas do projeto, mas não deve ser interpretada como uma solução pronta para exposição irrestrita na internet.

Um servidor que recebe comandos e executa operações no sistema exige controles adequados de autenticação, autorização e proteção de rede.

Os exemplos públicos devem evitar credenciais, endereços privados, informações pessoais e configurações sensíveis.

## Aprendizados

O projeto demonstra a aplicação prática de conhecimentos de Linux, automação, integração de sistemas e investigação técnica.

Além de implementar funcionalidades, foi necessário coordenar componentes diferentes, verificar estados do sistema e considerar situações em que dispositivos ou processos não estão imediatamente disponíveis.
