from os import getenv

API_TITLE = getenv('API_TITLE', 'Flask RESTFul Template')
API_VERSION = getenv('API_VERSION', 'v1')
DATABASE_URI = getenv('DATABASE_URI', 'sqlite:///data.db')
SWAGGER_UI_URL = getenv('SWAGGER_UI_URL', '/')
SWAGGER_API_URL = getenv('SWAGGER_API_URL', '/swagger-api/')
