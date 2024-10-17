# Financial Markets AI-Powered Dashboard

This Dash app is a tool focused on financial markets, leveraging AI technologies to provide smart insights and interactive visualizations.

## Description

This dashboard combines the power of financial data with advanced AI capabilities to deliver a unique user experience. Key features include:

- Financial markets theme with stock data visualization
- Generative AI powered by GPT's Large Language Model from OpenAI
- Smart insights generation for selected stocks and market trends
- Streaming outputs for real-time analysis and updates
- Structured outputs for clear, actionable information

The app showcases how AI can be seamlessly integrated into financial analysis tools, providing users with intelligent, on-demand insights about the stock market and individual companies.

```
pip install -r requirements-dev.txt
```

## Running this application

1. Install the Python dependencies

```
pip install -r requirements.txt --extra-index-url <your-dash-enterprise-packages-url>
```
2. Install & Run Redis (Deployed application ONLY)
This only applies to the Deployed application. Ensure Redis is attached in the services tab.
This application uses `celery` to run tasks in a background job queue.
Celery uses Redis to transfer data between the Dash app and its job queue.


3. In separate terminals, run the following commands:

```python
python app.py
```

> Note:

> 1. These commands were adapted from the Procfile, which is the list of commands that are used when the application is deployed. The only difference is that `gunicorn` was replaced with `python` for running the application locally with Dash's devtools and reloading features.

> 2. If you get an error message like
>    "`REDIS_URL` needs to be available as an environment variable."
>    Then prepend the env variable `REDIS_URL=redis://127.0.0.1:6379` on every command:
>    REDIS_URL=redis://127.0.0.1:6379 python app.py
>    REDIS_URL=redis://127.0.0.1:6379 celery -A app:celery_instance worker --loglevel=INFO --concurrency=2


