# chess


## Contribution Guidelines

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

<details>
<summary>Click to see one-time setup</summary>

1. Install [yarn](https://classic.yarnpkg.com/en/docs/install) or [npm](https://www.npmjs.com/get-npm)
2. Clone this repo
    ```
    https://github.com/zachsirotto/chess.git
    ```
3. Run `yarn install` or `npm install`

</details>
