# AntiWordly

Service for solving Wordly puzzles

## Run

API:

```shell
poetry shell
cd src
uvicorn --port 8000 anti_wordly.api.v1.app:app
x-www-browser http://127.0.0.1:8000/docs
```

CLI:

```shell
poetry shell
cd src
python -m anti_wordly.cli --help
# E.g.
python -m anti_wordly.cli -- '---о-,----н,сал--' '--но-,-----,би--м' '-енок,-----,в----'
```


## How-tos

Run tests:

```shell
poetry shell
cd src
python -m unittest
```

Format code:

```shell
poetry shell
cd src
black .
```

Check code quality:

```shell
poetry shell
cd src
prospector .
```