# MoveIt - an HackaGame game

_MoveIt_ est a un jeu vidéo imaginé sur un aspect pédagogique pour le challenge de développer des joueurs IA.
Il s'articule autour du problème de chemins multiagent ([Multi-agent pathfinding](https://en.wikipedia.org/wiki/Multi-agent_pathfinding)).

Cependant, au-delà du problème d’évitement de collision le but est: 

- Deprendre en charge des missions aléatoires, 
- Avec des équipes en concurrence sur le terrain
- Avec des Vips à éviter absolument.

_MoveIt_ est accéssible via son [repo-git](https://github.com/ktorz-net/game-moveit), merci à github pour ce service.

## Briques technologiques

Pour ce faire _MoveIt_ s'appuie sur [HackaGames](https://ktorz-net.github.io/hackagames/) une libraire modeste basée sur [ZeroMQ](https://zeromq.org/) pour séparer le processus du jeu (le maître du jeu) et les joueurs autonomes (_Bot_).

[ZeroMG] se veux être une `An open-source universal messaging library`.
Par universel, il faut entendre `Connecting your code in any language, on any platform`.
Cependant, aujourd’hui _HackaGames_ est développé exclusivement sous `Python3`.


## Objectifs

- Mises-en oeuvre de techniques d'optimisation combinatoire et d'Intelligence Artificielle.
- Conduire un projet de façon itératif.
- Travailler en équipes.
- Intégrer de bonne pratique de développement de projet informatique (versionning, tests, documentation).
