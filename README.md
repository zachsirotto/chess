# chess

## Setup nodemon and pre-commit hooks

1. Install [yarn](https://classic.yarnpkg.com/en/docs/install) or [npm](https://www.npmjs.com/get-npm)
2. Clone this repo, `git clone https://github.com/zachsirotto/chess.git`
3. Run `yarn install` or `npm install`

## Install python

**If you do not have >= Python 3.9.x**, install [pyenv](https://github.com/pyenv/pyenv) with the [easy-installer](https://github.com/pyenv/pyenv-installer#install), then install a Python version >= `3.9.x`.

## Install dependencies

Use either pip or pipenv to install dependencies from `setup.py` from within the cloned repository. i.e. `cd chess`

### [Pipenv (recommended)](https://github.com/pypa/pipenv)

Run `pipenv install -e .` to install dependencies using pipenv within a virtualenv.

### Pip (less recommended)

Run `pip install .` to install dependencies to your global pip package list.

## Run and watch for file changes

`nodemon --exec pipenv run python __init__.py`

## Run without watching for file changes

`pipenv run python __init__.py`

## Future plans

- Move Analysis
- Neural Network: https://github.com/CSSLab/maia-chess

## Contribution guidelines

This repository follows [conventional commits](https://www.conventionalcommits.org/), meaning commit messages should be structured as follows:

```html
<type>(optional scope): <description>
```

<details>
<summary>Commit Types</summary>

| Type     | Emoji                 | Markdown                    |
|:---------|:----------------------|:------------------------|
| feat     | :sparkles:            | `:sparkles:`            |
| fix      | :bug:                 | `:bug:`                 |
| docs     | :books:               | `:books:`               |
| style    | :gem:                 | `:gem:`                 |
| refactor | :hammer:              | `:hammer:`              |
| perf     | :rocket:              | `:rocket:`              |
| test     | :rotating_light:      | `:rotating_light:`      |
| build    | :package:             | `:package:`             |
| ci       | :construction_worker: | `:construction_worker:` |
| chore    | :wrench:              | `:wrench:`              |

</details>

<br>

To add emojis automatically to commit messages, setup the pre-commit hook for this repo in order to run commit messages through [devmoji](https://github.com/folke/devmoji):

