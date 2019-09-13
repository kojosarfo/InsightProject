Project title:
Analysis and modelling of City of Toronto traffic and transportation network data

Description:
The Big Data Innovation Team is creating models to predict traffic volumes in order to understand congestion in Toronto. They are currently productionizing models that enable them fill gaps and predict observed vehicle volumes (number of vehicles over a period of time) at traffic monitoring stations throughout the city, and to estimate values for road segments without monitoring stations. In order to understand congestion from the perspective of all road users, they wish to expand this work to active transportation modes - pedestrians and cyclists - as well. The team believes, however, that these are much more sensitive to factors like weather conditions, land use, and access to road infrastructure (eg. sidewalks and cycling lanes), than vehicles, and that any predictive model would need to incorporate these data.

Description of data:
A csv dump of data detailing the pedestrian and cyclist volumes observed at approximately 20 intersections in downtown Toronto between May and August 2019 inclusive have been provided. The sampling frequency at each intersection is 5 minutes, each intersection is monitored 24 hours a day, and volumes are disaggregated by direction of travel. In total, this is approximately 600,000 rows by three columns (intersection ID, timestamp, direction).

Expected deliverable:
A prototype model that can gap-fill and extrapolate observed pedestrian and cyclist volumes, as well as estimate volumes at intersections with only short-term data (a few days’ worth) is required. Additionally, corresponding testing documentation on how error metrics (eg. mean square or mean absolute error) change with hyperparameter or model architecture choices is desired.
