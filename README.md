

TrafficSeer
-------------
Predicting pedestrian and cyclist traffic in Downtown Toronto

<img src="pedestrianTraffic.jpg"
width="1000" height="300" />

The web app can be assessed [here](https://torontotraffic.live:8866)

Description
-------------
For many people, the above image looks quite familiar, especially during rush hours. Rush hour traffic can get as high as 6000 people in an hour’s interval. Despite this fact, and the level of congestion as shown here, consideration is hardly given to pedestrians or cyclists during road or maintenance work, only to vehicles.

The Big Data Innovation Team at the City of Toronto has only now acquired some historical data for some 14 intersections in Downtown, and I’m consulting with them to predict pedestrian/ cyclist traffic in Downtown -- in order to better optimise traffic signalling,  and better assess the impact of road closures on pedestrian movement.

However, the peculiarities of the problem do not allow a straightforward application of classical forecasting techniques. While we're looking to predict pedestrian/cyclist traffic about two weeks into the future, there are often significant periods of missing data due to ocasional breakdowns of traffic monitors, so that the forecast model should also be capable of gap-filling these intervals of missing data. Furthermore, not all interesections in Downtown have these traffic monitors, and consequently, the model has to be able to provide estimates for those intersections that are not currently monitored.

Data
------

A csv dump of data detailing the pedestrian and cyclist volumes observed at approximately 14 intersections in downtown Toronto between May and August 2019 inclusive has been provided. The sampling frequency at each intersection is 1 to 2 minutes, each intersection is monitored 24 hours a day, and volumes are disaggregated by direction of travel.

Moreover, the Big Data Innovation Team believes that, unlike for vehicular traffic for which they are currently productionising models to predict and gap-fill traffic volumes, pedestrian traffic are much more sensitive to other factors like weather conditions, and that any predictive model would need to incorporate these data. For this reason, I scraped historical weather data for the period over which the traffic data was collected from World Weather Online, and augmented it to the traffic data.

Method
---------
Classical time-series methods such as ARIMA fail, if there are too many chunks of missing data, and in fact, this bottleneck is present in many other autoregressive methods such as time-delayed neural networks (TDNN) or long-short-term-memory networks (LSTMs), since the amount of training data, as well as the length of the history on which the prediction is regressed, becomes limited. Moreover, these models are not well-suited for spatio-temporal regression which is involved in estimating the traffic for intersections not currently monitored.

One non-autoregressive approach to tackling this problem is Gaussian process regression GPR, which, in our case, assumes that the traffic volumes at different intersections are jointly normally distributed, with some constant mean and covariance function. A very common covariance function is the radial basis function kernel, which, being based on the squared Euclidean distance, implies that intersections that are closer together will be more heavily correlated in their traffic volumes than those farther away. This easily provides a Bayesian framework for predicting traffic at locations without historical data, conditioned on the traffic at locations with historical data. More so, one can think of the proximity in the covariance function not just in terms of the spatial co-ordinates of the intersections, but in terms of time as well. For example, all things being equal, the traffic at 8 am today is expected to correlate well with that at 8:00 tomorrow or 7:50 yesterday, so that GPR presents a way of forecasting or gap-filling missing data conditioned on the data at arbitrary spatio-temporal instances.

The training involved in Gaussian process regression is mainly in optimising the length scale parameters of the radial basis function kernel which make up the covariance function, by maximising the marginal likelihood of the data. Being non-parametric, GPR uses the training data for prediction, and is also able to provide the expected value of the test sample as well as the uncertainty of the prediction which is related to the Schur complement.

The main drawback of GPR is that it doesn't scale well with large amounts of training data, since it involves matrix inversion, and thus, its complexity is cubic in terms of the amount of training examples. For this reason, the GPR model, on which the web app is based, is trained on only one month's worth of data to make it feasible to host on an AWS Free Tier instance. Better results may be obtained if more computational power and memory are available.


Instructions
--------------
The main script on which the web app is based is TrafficForecast.ipynb, and can be found under /web_app. This script implements Gaussian process regression. Example inputs and expected outputs are already set up in this notebook, and can be easily seen by running all the cells in this notebook, once all required packages are installed.

The following packages may be required to run the code: voila, folium, plotly, ipywidgets, numpy, pandas. These can be installed via regular pip or conda commands.

Unfortunately, other saved files that are required for this notebook may not be available due to their size.

The training of the Gaussian process regression models are done in the file: scripts/trainGPR.py. A squared exponential kernel is used for the training, and the hyperparameters are optimised during fitting using BFGS. Other kernel functions as well as optimisation methods may be used in this script.
