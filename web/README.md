

- [Setup](#setup)
  - [VSCode](#vscode)
  - [Installing Node.js and npm](#installing-nodejs-and-npm)
  - [Installing app dependencies](#installing-app-dependencies)
  - [Run the app](#run-the-app)
  - [How to: Convert Models](#how-to-convert-models)
  - [How to: Convert Models (Older)](#how-to-convert-models-older)

# Setup

## [VSCode](https://code.visualstudio.com/download)


## Installing Node.js and npm
Node.js comes with npm (Node Package Manager) bundled, which means installing Node.js will also install npm.

1. Visit the [Node.js website](https://nodejs.org/).
2. Download the installer for your operating system (choose LTS version recommended for most users).
3. Run the installer and follow the prompts to install Node.js and npm.

Verify Install with:

```bash
node -v
npm -v
```

## Installing app dependencies

In your project folder:

```bash
npm install
```

## Run the app

```bash
npm start
```

## How to: Convert Models

1. In Blender Export to `file_name.glb`
2. Copy to `/public`

```bash
npm run convert-model file_name
```

3. In `src/App.js` change the import statement to `file_name`

```bash
import Model from './models/globe';

# Change to

import Model from ./models/file_name
```

Reload app

## How to: Convert Models (Older)

```bash
npx --shadows public/{file_name}.glb --output src/models/{file_name}.jsx
```

Edit the `{file_name}.jsx`:

```js
export function Model(props) 
// becomes
export default function Model(props) {
```
