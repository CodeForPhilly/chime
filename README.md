# CHIME

## Development
To test the app locally just run:

`streamlit run app.py`

This will open a browser window with the app running.

### Developing with docker

Copy `.env.example` to be `.env` and run the container.

```bash
cp .env.example .env
docker-compose up
```

You should be able to view the app via `localhost:8000`. If you want to change the
port, then set `PORT` in the `.env` file.

## Deployment
**Before you push your changes to master make sure that everything works in development mode.**

Changes merged to `master` will be automatically deployed to [pennchime.herokuapp.com](https://pennchime.herokuapp.com/).
