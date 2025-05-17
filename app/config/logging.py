import logging

from app.config.settings import settings


class RequireDebugTrueFilter(logging.Filter):
    def filter(self, record):
        return settings.DEBUG is True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': RequireDebugTrueFilter
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'minimal': {
            'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'minimal': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'minimal',
        },
    },
    'loggers': {
        'uvicorn.error': {
            'level': 'ERROR',
            'handlers': ['console', 'minimal'],
        },
        'app': {
            'level': 'INFO',
            'handlers': ['console', 'minimal'],
        },
    }
}
