# Summary
## Use case
todo
## Project directory overview
```
share_price_predictor
|--dash_app
    |--assets
        |--favicon.ico
        |--app_overview.jpg
    |--app.py
    |--app_start.sh    
    |--graphs.py  
    |--model_input_selectors.py
    |--stock_codes.py      
|--helpers
    |--dates.py
    |--download.py
    |--engine.py
    |--features.py
|--Dockerfile
|--requirements.txt
|--start_app.sh
|--stop_app.sh
```
## Deployment
To deploy the application in the environment of your choice, follow the process below.

1. Clone the github repo
> `git clone git@github.com:lethalwombat/share_price_predictor.git`

2. Navigate to the `share_price_predictor` folder and run `start_app.sh`
> `./start_app.sh`

> **Share Price Predictor** will be available at port 8050

3. Run `stop_app.sh` to shut down the application
> `./stop_app.sh`

## Dashboard
![Share Price Predictor](https://github.com/lethalwombat/share_price_predictor/blob/main/dash_app/assets/app_overview.jpg "Share Price Predictor")
## Engine
todo