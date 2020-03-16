# CHIME
The **C**OVID-19 **H**ospital **I**mpact **M**odel for **E**pidemics

[![CHIME](https://user-images.githubusercontent.com/1069047/76693244-5e07e980-6638-11ea-9e02-1c265c86fd2b.gif)](http://predictivehealthcare.pennmedicine.org/chime)

Join out [Code For America](https://codeforphilly.org/projects/chime--covid-19_hospital_impact_model_for_epidemics) team or our [Slack channel](https://codeforphilly.org/chat?channel=covid19-chime-penn) if you'd like to chat with us. We'd appreciate your [feedback](http://predictivehealthcare.pennmedicine.org/contact/).

## Development
To test the app locally just run:

`streamlit run app.py`

This will open a browser window with the app running.

### With `pipenv`
```bash
pipenv shell
pipenv install
streamlit run app.py
```

### With `conda` 
```bash
conda create -f environment.yml
source activate chime
streamlit run app.py
```

### Developing with `docker`

Copy `.env.example` to be `.env` and run the container.

```bash
cp .env.example .env
docker-compose up
```

You should be able to view the app via `localhost:8000`. If you want to change the
port, then set `PORT` in the `.env` file.

**NOTE** this is just for usage, not for development--- you would have to restart and possibly rebuild the app every time you change the code. 

## Deployment
**Before you push your changes to master make sure that everything works in development mode.**

Changes merged to `master` will be automatically deployed to [http://penn-chime.phl.io/](http://predictivehealthcare.pennmedicine.org/chime).
