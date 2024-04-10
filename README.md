# Database backed Celery Beat Scheduler

## Description

This is an sqlmodel based implementation of the celery beat scheduler.
It persists periodic celery tasks in a SQLAlchemy-compatible database.

## Usage

You can install this package using pip.
After installation, specify the database connection string in the Celery config, using the name `beat_dburi`. Modified
from sqlmodel-celery-beat to support pydantic v2. and optimize some functions

You can run the beat instance using:

install
```bash
pip install celery-sqlmodel-beat
```

init_models.py
```bash
from sqlmodel import SQLModel, create_engine

from app.ext.sqlmodel_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    PeriodicTasksChanged,
    SolarSchedule,
)

if __name__ == "__main__":
    engine = create_engine('sqlite:///schedule.db')
    def create_db_and_tables() -> None:
        """
        create table
        """
        SQLModel.metadata.create_all(engine)

    create_db_and_tables()

```

tasks.py

```bash
from celery import Celery
from sqlmodel_celery_beat.schedulers import (  # pylint: disable=unused-import
    DatabaseScheduler,
)

beat_scheduler = "sqlmodel_celery_beat.schedulers:DatabaseScheduler"

beat_dburi = 'sqlite:///schedule.db'
# beat_dburi = 'mysql+mysqlconnector://root:root@127.0.0.1/celery-schedule'

config = {
    "broker_url": "redis://:127.0.0.1:6379/1",
    "result_backend": "redis://:127.0.0.1:6379/2",
    "beat_dburi": beat_dburi,
}

celery = Celery(__name__)

celery.config_from_object(config)

celery.autodiscover_tasks()

@celery.task(name='tasks.add')
def add(x, y):
    return x + y

```

Run Celery
```bash
celery -A tasks:celery worker -l info
celery -A tasks:celery beat -S tasks:DatabaseScheduler -l info
```