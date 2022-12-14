# Summary
**Share Price Predictor** uses publicly available historical stock data to extract share price movement patterns and generate predictions on the specified unseen data.

## Use case
**Share Price Predictor** is an application that demonstrates the skeleton of the end-to-end Data Science workflow. The application demonstrates several parts of the process from scratch.

At a high level, the application showcases a Data Science workflow consisting of:
1. Infrastructure deployment using Docker
    * Create a Docker image with all necessary dependencies
    * Start the service with one command
    * Stop the service with one command


2. Data sourcing
    * Download the required data for model training


3. Data preparation
    * Create model features
    * Split the data into training and validation

4. Algorithm training
    * Model fitting
    * Generate predictions using inference


5. Front-end application for business users
    * Visually demonstrate prediction accuracy
    * Visually demonstrate how model fit can be enhanced using various algorithm types and settings


While **Share Price Predictor** is able to train a model using historical data, it should not be used to make personal investment decisions driven by the predictions. The goal of the project is not to create the best possible model, but to demonstrate an end-to-end approach to building a self-contained Data Science application.
## Project directory overview
`|--dash_app` contains all code and assets required for the dashboard

`|--helpers` contains data preparation and model training code

`|--Dockerfile` contains Docker image build definition

`|--requirements.txt` contains required Python libraries
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

### Model inputs
| Input | Description |
| -----------: | :----------- |
| Stock code | Which stock code the prediction should be generated for |
| Last year of training data | What is the latest year of the training data |
| Training data years | How many full years of training data should be included |
| Learning rate | What is the learning rate of the algorithm (not applicable to LinReg) |
| Number of estimators | How many estimators should be used in training (not applicable to LinReg) |
| Model type | Linear Regression or Gradient Boosting |

### Visualisations
| Location | Description |
| -----------: | :----------- |
| Top left | Model fit for training data |
| Top right | Model fit for validation data |
| Bottom left | See 'Metrics' below |
| Bottom right | Direction match breakdown. <span style="color:green">Green</span> when both prediction and actual price movement match, e.g. `increase == increase` or `decrease == decrease` and <span style="color:red">red</span> otherwise

### Metrics
| Name | Description |
| -----------: | :----------- |
| R2 Score| Coefficient of determination |
| Direction match | Percentage of predictions where prediction direction matches with actual |

## Model features and target
### Target
| Code variable name | Description |
| -----------: | :----------- |
| `price_increase_next_day` | Price change on the next trading day |

### Features
| Code variable name | Description |
| -----------: | :----------- |
| `price_increase_today` | Price change compared to the previous trading day |
| `price_highest_5` | Is the price highest in 5 days? |
| `price_highest_10` | Is the price highest in 10 days? |
| `price_highest_30` | Is the price highest in 30 days? |
| `price_highest_ever` | Is the price highest ever? |
| `increase_highest_5` | Is the increase highest in 5 days? |
| `increase_highest_10` | Is the increase highest in 10 days? |
| `increase_highest_30` | Is the increase highest in 30 days? |
| `increase_highest_ever` | Is the increase highest ever? |
| `increase_highest_2` | Increase rolling mean for last 2 days |
| `increase_highest_3` | Increase rolling mean for last 3 days |
| `increase_highest_5` | Increase rolling mean for last 5 days |
| `increase_highest_7` | Increase rolling mean for last 7 days |
