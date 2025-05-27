from os import environ
from otree.project_template.settings import SESSION_CONFIG_DEFAULTS

DEBUG = False
# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

PARTICIPANT_FIELDS = ['endowment']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'
INSTALLED_APPS = ['my_experiment']
SESSION_CONFIGS = [
    {
        'name': 'my_experiment',
        'display_name': 'Regret + CTB Experiment',
        'num_demo_participants': 4,  # Adjust as needed
        'app_sequence': ['my_experiment'],  # Replace with your app name
    },
]
# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = True


ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5906595164318'


# ADD variables for today date and 3 weeks date and for the redirection link of prolific
