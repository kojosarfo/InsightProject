Project title
-------------
Analysis and modelling of City of Toronto traffic and transportation network data

Description
------------
The Big Data Innovation Team is creating models to predict traffic volumes in order to understand congestion in Toronto. They are currently productionizing models that enable them fill gaps and predict observed vehicle volumes (number of vehicles over a period of time) at traffic monitoring stations throughout the city, and to estimate values for road segments without monitoring stations. In order to understand congestion from the perspective of all road users, they wish to expand this work to active transportation modes - pedestrians and cyclists - as well. The team believes, however, that these are much more sensitive to factors like weather conditions, land use, and access to road infrastructure (eg. sidewalks and cycling lanes), than vehicles, and that any predictive model would need to incorporate these data.

Description of data
--------------------
A csv dump of data detailing the pedestrian and cyclist volumes observed at approximately 20 intersections in downtown Toronto between May and August 2019 inclusive have been provided. The sampling frequency at each intersection is 5 minutes, each intersection is monitored 24 hours a day, and volumes are disaggregated by direction of travel. In total, this is approximately 600,000 rows by three columns (intersection ID, timestamp, direction).

Expected deliverable:
A prototype model that can gap-fill and extrapolate observed pedestrian and cyclist volumes, as well as estimate volumes at intersections with only short-term data (a few days’ worth) is required. Additionally, corresponding testing documentation on how error metrics (eg. mean square or mean absolute error) change with hyperparameter or model architecture choices is desired.

Method
-------
The above problem requires that the prototype model is able to do the following: 1) forecast pedestrian/ cyclist traffic at intersections with monitoring stations; 2) gap-fill the pedestrian/ cyclist traffic at intersections with monitoring stations; 3) estimate pedestrian/ cyclist traffic at intersections without monitoring stations.

For the purpose of gap-filling the data at given intersections, the presence of missing chunks of data presents the problem of identifying a continuous sequence of traffic data long enough to accurately learn the characteristics of the time-series. Thus, this greatly limits the application of classical time-series forecasting methods such as ARIMA, which requires continuous sequence of data to identify the stationarity of the data and learn the autoregressive and moving average parameters as well as the seasonal parameters. In fact, this problem is not particular to ARIMA only, but to other autoregressive models as well, among which is classical recurrent neural networks or long short term memory networks (LSTM), since the presence of missing data at arbitrary instances greatly limits the amount of useful training data that can be collated to train the models. One might think of training bidirectional LSTMs, so that their forward and backward predictions might be averaged to gap-fill the missing intervals. Apart from the computational complexity involved, training bidirectional LSTMs would only likely work satisfactorily if there are only a handful of missing chunks of data.

Gaussian process regression is a non-parametric alternative that is well-suited for this task. For one thing, it does not require a continuous stream of data, and in this sense, is non-autoregressive... to be continued

Instructions
------------
The webapp can be assessed at: torontotraffic.live:8866

The main script is TrafficForecast.ipynb, and can be found under /web_app. This script implements Gaussian process regression forecasting. Example inputs and expected outputs are already set up in this notebook, and can be easily seen by running all the cells in this notebook, once all required packages are installed.

The following packages are required to run the code: voila, folium, plotly, ipywidgets, numpy, pandas. These can be installed via regular pip or conda commands.

Unfortunately, other saved files that are required for this notebook may not be available due to their size.

The training of the Gaussian process regression models are done in the file scripts/trainGPR.py. A squared exponential kernel is used for the training, and the hyperparameters are optimised during fitting using BFGS. Other kernel functions as well as optimisation methods may be used in this script.
