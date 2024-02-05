# Dash Enterprise Demo Apps

This monorepo holds code for the apps deployed to https://dash-enterprise-demo.plotly.com created for the marketing gallery. using the full dash enterprise stack.

## Running an example app

You will need to run applications, and specify filenames, from the
root directory of the repository. e.g., if the name of the app you
want to run is `my_dash_app` and the app filename is `app.py`, you
would need to run `python my_dash_app/app.py` from the root
of the repository.

Each app in this repository has a `requirements.txt` which specifies app-specific package dependencies, install all packages in a virtual environment.

## Adding a new app to this repository

For example, if the deployment will eventually be hosted at https://dash-enterprise-demo.plotly.com/my-dash-app, where the directory name is used as the app name.

If a pull request is opened with a new app added, that app will be deployed to `my-dash-app-<EVENT-NUMBER>` where `EVENT-NUMBER` is the PR number.