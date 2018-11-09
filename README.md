# Rockstat cookie-sync service example

## Hot to start

For testing purposes run `make start-dev`. 
To start service in production mode use Rockstat dashboard located at `app.YOUR-TRACKING-DOMAIN`

### Structure

```
my_images
| - your_service_name
    | - .dockerignore
    | - config.yaml
    | - Dockerfile
    | - requirements.txt
    | - start_dev
    | - your_service_name
        | - __init__.py
        | - __main__.py
        | - main.py
```

### Short introduction into Band services.

All of code splitting in logocal services. Service can contains number of functions, that can exposed to other services or event outside (to works) using `front` service proxing mechanics. Each function can take one of roles:

- **listener**: listene for all events matching provided key. That role uses database writers and streaming services
- **enricher**: provides additional data chunks (enrichments) for events matched provided rules. Returened data will be attached to incoming event
- **handler**: fucnctin which result will be returned back to request initiator

Moreover you can define function as woker which load initial data or packet hanldle incoming data

- **task**: worker function

### Build your service

Look at the `yourservice/yourservice/main.py` template. It contains typical example 

### Running for debug

execute 
```
make start-dev
```

### Env variables

Possible to store vars at: `.env`, `.env.local`. 
These paths was excluded from git to avoid of commit sensitive data.

### Old skeleton example


```python
import asyncio
from itertools import count
from prodict import Prodict as pdict
from band import expose, cleanup, worker, settings, logger, response


"""
Service state
"""
state = pdict(
    counter=settings.initial_counter_value,
    loaded=False,
    loop=0
)


@expose.handler()
async def main(data, **params):
    """
    Registering handler which can be accessible through http
    Регистрируем обработчика запросов
    """
    return state


@expose.handler()
async def tick(data, **params):
    """
    Second method, for example request counter
    Еще один метод6 в касестве проимера считающий запросы
    """
    return {}


@worker()
async def service_worker():
    """
    Это каркас воркера, который используется для начально 
    загрузки/подготовки данных и последующей оброботки новых данных
    вызывается при инициализации приложения
    """
    for num in count():
        """
        Avoid crush
        """
        try:
            """
            initial execution
            """
            if num == 0:
                state.loaded = True
            """
            periodically execution
            """
            state.loop = num
        except asyncio.CancelledError:
            break
        except Exception:
            logger.exception('my service exeption')
        await asyncio.sleep(30)


@cleanup()
async def service_cleanup():
    """
    Handle graceful shutdown
    Операции выполняемые при завершении
    """
    state.loaded = False
```


## License

```
Copyright 2018 Dmitry Rodin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```