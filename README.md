# Summary
Stock Price Predictor uses publicly available historical stock data to extract share price movement patterns and generates predictions on unseen data.

## Use case
Stock Price Predictor is an application that demonstrates the skeleton of the end-to-end Data Science workflow. The application demonstrates several parts of the process from scratch.

At a high level, the application showcases a Data Science workflow consisting of
1. Infrastructure deployment using Docker
    * Create a Docker image with all necessary dependencies
    * Start the service with one command


2. Data sourcing
    * Download the required data for model training


3. Data preparation
    * Create model features
    * Split the data into training and validation

4. Algorithm training
    * Model fitting
    * Inference or predictions


5. Front-end application build for business users
    * Demonstrate prediction accuracy
    * Demonstrate how model fit can be enhanced using various algorithm types and data settings


While Stock Price Predictor is able to train a model using historical data, it should not be used to make personal investment decisions driven by the predictions. The goal of the project is not to create the best possible model, but to demonstrate an end-to-end approach to building a self-contained Data Science application.
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