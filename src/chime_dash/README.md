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
Install the chime base module
```bash
> pip install [--user] [-e] .
```
and run
```bash
> python src/dash_app.py
```
in the project root.
