# app/config.py
import os
from dash_bootstrap_components import themes



class Config:

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Bootstrap theme courtesy of https://bootswatch.com (.css in app/static/ as well)"
    THEME     = [themes.JOURNAL]
    META_TAGS = [dict(
        name = "viewport",
        content = "width=device-width, initial-scale=1")]

    # Penn Medicine masthead - .css also provided in /app/static/"
    PENN_HEADER  = "https://www1.pennmedicine.org/styles"+\
                            "/shared/penn-medicine-header.css"
    # URL links
    PENN_MED_URL = "http://predictivehealthcare.pennmedicine.org/"
    CONTACT_URL  = "http://predictivehealthcare.pennmedicine.org/contact/"
    GITHUB_URL   = "https://github.com/pennsignals/chime"
    SLACK_REF    = "https://codeforphilly.org/chat?channel=covid19-chime-penn"

class DevelopmentConfig(Config):
    TESTING = False
    DEBUG   = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False



config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
