from os import getenv

# Swagger
API_TITLE = getenv('API_TITLE', 'Flask RESTFul Template')
API_VERSION = getenv('API_VERSION', 'v1')
SWAGGER_UI_URL = getenv('SWAGGER_UI_URL', '/')
SWAGGER_API_URL = getenv('SWAGGER_API_URL', '/swagger-api/')
AUTHORIZATION_HEADERS = {
    'Authorization': {
        'description': 'Bearer >TOKEN<',
        'in': 'header',
        'type': 'string',
        'required': True
    }
}

# DBase
DATABASE_URI = getenv('DATABASE_URI', 'sqlite:///data.db')

# Security
BLACKLIST = set()
