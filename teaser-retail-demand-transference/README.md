## Demand Transference
Dash app to visualize transference of demand between products.

### Built with
* [Dash](https://plot.ly/dash/)
* [Plotly](https://plot.ly/python/)
* [Dash Design Kit](https://plot.ly/dash/design-kit)
* [Dash Snapshot Engine](https://plot.ly/dash/snapshot-engine/)

### Before Running the Application
To run this app locally, it is recommended to create a virtual environment before installing the dependencies in `requirements.txt`.

```
python3 -m virtualenv venv  
# Windows: 
venv\Scripts\activate
# Linux: 
source venv/bin/activate
```
Install requirements by the following command:

```
pip install -r requirements.txt
```

**For initializing this app with conda environment:**
```
conda create -n newvenv python=3.9.4
conda activate newvenv
```

Certain required packages are unavailable via anaconda. Use pip for installation into conda environment.

```
conda install pip
pip install -r requirements.txt
```


## How to Run the Application

#### Running the app
This app uses [Dash Snapshot Engine](https://plot.ly/dash/snapshot-engine/) for saving and loading interactive views as report.
To run this app locally you will need a redis instance running at port 6379. See the [Redis documentation](https://redis.io/documentation) to download Redis and set up a local database.

After the aforementioned prerequisites are met, you may run the app locally by running:

```
python3 index.py
```

To enable snapshot-saving functionality locally, in a separate terminal, run celery process (reminder — make sure redis is also running with `redis-server`):

```
# Mac/Linux:
celery -A app:celery_instance worker --loglevel=info
# Windows:
pip install gevent
celery -A app:celery_instance worker -l info -P gevent
```

Open http://127.0.0.1:8050/ and load your app in browser.

## Screenshots
 ![Screencast](assets/app_screenshot.png)


