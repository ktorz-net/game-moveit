# Game-MoveIt

An _HackaGames_ game based on the multi-paths planning problem.


## Install:

_Hacka-MoveIt_ uses _pip_ for a local install. 
The project relies on _HackaGames_ (including _hackaPy_, its python3 librairie).

```sh
git clone https://github.com/ktorz-net/hackagames.git
pip install ./hackagames
git clone https://github.com/ktorz-net/hacka-moveit.git
pip install ./hacka-moveit
```


## Get Stated:



## Documentation

The documentation is on [Markdown](https://en.wikipedia.org/wiki/Markdown) format.
It can be served as a _HTML_ web site thanks to [MkDocs](https://www.mkdocs.org/).

```sh
pip install mkdocs
mkdocs serve
```

You can then refer to the [http://127.0.0.1:8000/](documentation).

This documentation is also on line: [https://ktorz-net.github.io/hackamove](ktorz-net.github.io/hackamove)


## Contribute 

Doc. deployment is achieved with a public github repository (_imt-mobisyst.github.io.git_):

```sh
git clone git@github.com:imt-mobisyst/imt-mobisyst.github.io.git ../imt-mobisyst-site
./bin/docs-deploy.sh
```

To notice that the documentation repository can be cloned any where on your computer while the `config.toml` is updated accordingly.
