# Context

This directory should provide the interface for a dash app.

E.g., it contains the actual app which pieces together individual parts which could potentially live on their own.
This makes it easier to modularize and reuse parts.

![Current interface](docs/assets/interface.png)

## Todo
Plots & callbacks

## Tree

File/Folder | Purpose
---|---
`utils` | General function which help rendering the app
`plotting` | Specific functions which provide plotting data
`templates` | Specific `yml` or `markdown` files which. Translage all these texts to have localized versions
`layout` | The core of the dash app. Works modular. E.g., the `__init__` file glues all different parts together.

## How to use
Install the chime base module
```bash
> pip install [--user] [-r] requirements.txt
```
and run
```bash
> python src/dash_app.py
```
in the project root and visit the local url.
