---
title: "How the documentation is organized"
permalink: /docs/how-to-write-documentation/
excerpt: "How to contribute to Prompt Sail documentation"
last_modified_at: 2023-12-22T18:48:35+01:00
redirect_from:
  - /theme-setup/
toc: true
---




## How the documentation is organized

Our project documentation is hosted on GitHub Pages and built using Jekyll. Here's a brief overview of the structure and how to work with it:

1. **Branch**: The "docs" branch is the source for the documentation build process, which is handled via GitHub Actions.

2. **Template**: We use the custom template `mmistakes/minimal-mistakes@4.24.0`. You can find more about it [here](https://github.com/mmistakes/minimal-mistakes/tree/master).

3. **Configuration**: The main configuration file is [`docs/_config.yml`](https://github.com/PromptSail/prompt_sail/tree/docs/docs/_config.yml). This file contains all the template variables.

4. **Home Page**: The home page is [`docs/_pages/home.md`](https://github.com/PromptSail/prompt_sail/tree/docs/docs/_pages/home.md). This page serves as the entry point to our documentation and contains basic information about the project.

5. **Documentation Pages**: Specific documentation pages are stored in the [`docs/_docs`](https://github.com/PromptSail/prompt_sail/tree/docs/docs/_docs) folder.

6. **Navigation**: The main navigation is defined in [`docs/_data/navigation.yml`](https://github.com/PromptSail/prompt_sail/tree/docs/docs/_data/navigation.yml).

7. **Contributor Posts**: The [`docs/_posts`](https://github.com/PromptSail/prompt_sail/tree/docs/docs/_posts) folder is reserved for main contributors' posts. Each post should be reviewed and accepted as a pull request.

