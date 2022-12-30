Flowdrive API
=============

## Deploy
1. Copy `.env.example` to `.env` and fill it up.
   To generate secret keys:
   ```python
   >>> import os
   >>> os.urandom(24)
   ```

2. Create a venv (or not). Run 
   ```bash
   pip install -r requirements.txt
   ```

3. Migrate database:
   ```bash
   set -a; source .env; set +a
   make init-db
   make migrate
   ``` 

4. Copy [`contrib/flowdrive_api.service`](contrib/flowdrive_api.service) to `/etc/systemd/user/flowdrive_api.service`

5. Run `systemctl --user daemon-reload`
6. Run `systemctl --user enable --now flowdrive_api`


## Development
1. Copy `.env.example` to `.env` and fill it up.
   To generate secret keys:
   ```python
   >>> import os
   >>> os.urandom(24)
   ```

2. Create a venv (or not). Run 
   ```bash
   pip install -r requirements.txt
   ```

3. Migrate database:
   ```bash
   set -a; source .env; set +a
   make init-db
   make migrate
   ```

4. Flask run:
   ```bash
   make run
   ``` 

### Insomnia Collection

Refer to the [Insomnia collection](insomnia.yaml) for development