# Context

This directory should provide the interface for a dash app.

E.g., it contains the actual app which pieces together individual parts which could potentially live on their own.
This makes it easier to modularize and reuse parts.

## Tree

File/Folder | Purpose
---|---
`app` | Launches the dash app
`utils` | General function which help rendering the app
`plotting` | Specific functions which provide plotting data
`tmp_data` | Temp submodule for data which will be removed and actual `penn_chime` data is used
`templates` | Specific `html` or `markdown` files
