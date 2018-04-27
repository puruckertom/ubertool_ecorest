import os
import logging
from celery import Celery

from temp_config.set_environment import DeployEnv
runtime_env = DeployEnv()
runtime_env.load_deployment_environment()

redis_server = os.environ.get('REDIS_HOSTNAME')
redis_port = os.environ.get('REDIS_PORT')

celery_tasks = [
    'hms_flask.modules.hms_controller',
    'pram_flask.tasks'
]

redis = 'redis://' + redis_server + ':' + redis_port + '/0'
logging.info("Celery connecting to redis server: " + redis)

celery = Celery('flask_qed', broker=redis, backend=redis, include=celery_tasks)

celery.conf.update(
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_IGNORE_RESULT=True,
    CELERY_TRACK_STARTED=True,
)
