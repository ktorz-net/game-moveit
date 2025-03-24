# Game-MoveIt

An _HackaGames_ game based on the multi-paths planning problem.

/!\ THIS VERSION IS OBSOLETE !


## Install:

_MoveIt_ uses _pip_ for a local install. We supose that _python3_ and _pip_ are installed on the machine.  
This project needs _HackaGames (v0.3.0)_ (including _hacka.py_, its python3 librairie).

```sh
git clone https://github.com/ktorz-net/hackagames.git
git -C ./hackagames checkout v0.3.0
pip install ./hackagames
git clone https://github.com/ktorz-net/game-moveit.git
pip install ./game-moveit
```

## Get Stated:

For trying the game start a simple version with the `debug.py` version:

```sh
python3 ./game-moveit/play/debug.py
```

Then open `./shot-moveIt.png` file for a view of the game board.

## Documentation

_MoveIt_ is dedicated to create automous player based on AI (Artificial Intelligence) and CO (Combinatorial Optimization).
The documentation is served on [https://ktorz-net.github.io/game-moveit/](ktorz-net.github.io/game-moveit).


For a local wriding, the documentation is develloped on [Markdown](https://en.wikipedia.org/wiki/Markdown) format in the `docs/` directory.
It can be generated and served as a _HTML_ web site thanks to [MkDocs](https://www.mkdocs.org/).

```
cd game-moveit
pip install mkdocs
mkdocs serve
```

## Contribute 

Doc. deployment is achieved with a public github repository (_imt-mobisyst.github.io.git_):

```sh
git clone git@github.com:imt-mobisyst/imt-mobisyst.github.io.git ../imt-mobisyst-site
./bin/docs-deploy.sh
```

To notice that the documentation repository can be cloned any where on your computer while the `config.toml` is updated accordingly.
