# Context

This directory should provide the interface for a dash app.

E.g., it contains the actual app which pieces together individual parts which could potentially live on their own.
This makes it easier to modularize and reuse parts.

![Current interface](interface.png)

## Todo
Plots & callbacks

## Tree

File/Folder | Purpose
---|---
`app` | Launches the dash app
`utils` | General function which help rendering the app
`plotting` | Specific functions which provide plotting data
`presentation` | More sophisticated rendering functions
`templates` | Specific `html` or `markdown` files

## How to use
Run
```bash
> python penn_chime/dash/app.py
```
in the project root (after installing requirements).

You can also
```bash
> pip install [--user] [-e] .
```
which installs the command line script
```bash
> penn_chime
```
which launches the dash app.
