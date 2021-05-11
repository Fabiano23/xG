# **_xG_**

![GitHub Logo](https://github.com/Fabiano23/xG/blob/main/Imagens/Xg.jpg)

## **O que é _xG_?**

##### Do inglês _expected goals_, o termo _xG_ diz respeito à probabilidade de uma finalização no jogo de futebol terminar em gol dado algumas de suas características. Nesse sentido, é uma medida estatística que mede a qualidade de um chute.

## **Por que _xG_ é importante?**

##### O _xG_ conta uma história sobre uma partida ou partidas recentes de um clube/campeonato/jogador específico. Elas predizem, por exemplo, os gols de uma equipe para a próxima partida melhor do que o próprio número de gols feitos pela equipe até então. Assim, a métrica é muito importante na ajuda a treinadores e jogadores em tomadas de decisões. Por exemplo: de onde o jogador/a equipe mais finaliza, direcionamentos nos treinamentos do time visando finalizações de regiões e contextos com maior probabilidade de gol etc.

## **Como é calculado?**

##### O seu cálculo é bem simples: dividimos o total de gols feitos por cada região do campo pelo total de chutes dados daquela região. Assim, nós temos a resposta para a pergunta: qual a porcentagem de chutes que resultam em gol de cada local do campo? Esta é a base do modelo xG, porém outras variáveis podem ser adicionadas, tais como as que foram utilizadas neste projeto.

# **Dados**

##### Os dados são provenientes do Wyscout e é um dos datasets de futebol abertos mais robustos disponíveis atualmente. Nós temos eventos de todas as partidas de uma temporada completa (2016-2017) [das cinco principais ligas europeias segundo a UEFA](https://www.uefa.com/memberassociations/uefarankings/country/#/yr/2019) (as primeiras divisões das ligas espanhola; italiana; alemã; francesa e inglesa), do campeonato europeu de seleções de 2016 e da Copa do Mundo da Rússia de 2018.

## [Notebook preparacaoDosDados](https://github.com/Fabiano23/xG/blob/main/preparacaoDosDados.ipynb) -> Para cada finalização de todos os campeonatos identificamos:

  a) [todos_os_chutes_modelo.csv](https://raw.githubusercontent.com/Fabiano23/xG/main/todos_os_chutes_modelo.csv):
    
    1. A posição x (horizontal) e y (vertical) do chute no campo;
    2. Distância do chute em relação à linha central;
    3. Distância do chute (em relação ao gol) em metros;
    4. O ângulo do chute em relação à baliza;
    5. O campeonato em que o chute foi dado (para análises depois de construir o modelo);
    6. Se o chute foi dado a partir de um contra ataque; uma falta; pênalti ou em organização ofensiva da equipe (a equipe adversária estava posicionada defensivamente);
    7. id do time nos dados do Wyscout;
    8. id do jogador nos dados do Wyscout;
    9. A variável que queremos prever: dado as características acima (tirando o campeonato) foi gol ou não (sua probabilidade)?.
  
  b) [chutes_modelo_com_xg.csv](https://raw.githubusercontent.com/Fabiano23/xG/main/chutes_modelo_com_xg.csv):
    
    1. Todas as variáveis indicadas acima acrescido o xG de cada finalização.

## Notebook [analiseDosDadosEModelos](https://github.com/Fabiano23/xG/blob/main/analiseDosDadosEModelos.ipynb):

  Notebook com a análise dos dados, teste e justificativa do modelo.
  
## Arquivos:

  1. funcoes_projeto.py -> funções utilizadas no projeto para manter os notebooks menos "poluídos".
  2. FCPython.py -> Arquivo do repositório [SoccermaticsForPython](https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython) para visualização dos dados em um campo de jogo.
  
## Pasta Imagens:
  Imagens que ajudam a ilustrar as ideias e justificativas do modelo além de um pdf com as definições das variáveis pela Wyscout.
  
## Links:

- https://www.nature.com/articles/s41597-019-0247-7 -> Artigo com informações detalhadas sobre como se dá a coleta de dados dos jogos de futebol pela Wyscout e a definição das variáveis.

- https://www.uefa.com/memberassociations/uefarankings/country/#/yr/2019 -> artigo com o ranking das ligas europeias pela UEFA.

- https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython -> Repositório SoccermaticsForPython.
 
