# COVID Flight Analysis

|     Team Name    |
|------------------|
|Airline with COVID|

| Team Member      | NetId|
|------------------|------|
| Shantanu Tripathi|st3810|
|         Dongzi Qu| dq394|
|        Binghan Li|bl1890|

# Introduction
COVID-19 is spreading widely and rapidly across the globe, from China to Europe, and now to the United States. Within the United State, the deadly virus has infected every state in less than a month. One of the reasons for such insane spreading, on top of the level of contagiousness of COVID-19, is frequent air travel. There are over one million flights happening every day worldwide, it is currently the fastest way for humans to travel to anywhere in the world, unfortunately, it is for the virus as well. Additionally, aircrafts create an environment that is beneficial for COVID-19 to spread, over 100 passengers are in a sealed cabin together for hours without a medical grade ventilation system, if one passenger is infected with the virus, it is highly possible, if not 100 percent, for other passengers to become infected. With this information in everyone’s mind, our team wants to discover how the air travel industry is being affected by COVID-19 within the United States. Furthermore, we want to utilize data to trace the origin of the virus for cities in the United States. Hope you enjoy our project!

# Datasets used

## Raw Data
* **us-counties.csv**: This dataset contains county level COVID-19 information in the United States, and it is updated daily by New York Times. Columns of interest are date, county, state, cases and deaths. This dataset can be viewed and downloaded from [here](https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv).
* **Flights**: This dataset contains worldwide flight information within the first 4 months of 2020, and it consists of 4 data files, each data file contains 1 month of flight information. This dataset is provided by OpenSky Network for combating COVID-19, and it is updated monthly. This dataset can be downloaded [here](https://opensky-network.org/datasets/covid-19/).
* **airports.csv**: This dataset contains information for every airport in the world, and it is provided and maintained daily by OurAirports. This dataset is used for elaborating flight information, such as adding county and state information for destination airport and origin airport for interested flights. This dataset can be downloaded [here](https://ourairports.com/data/airports.csv), and it is also provided in this repo at [here](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Datasets/airports.csv).

## Generated Data

* **disease.csv**: This dataset is generated from [```us-counties.csv```](https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv) using [```construct.py```](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Code/construct.py). This dataset contains COVID-19 information for interested counties, which is listed in [```city_list.csv```](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Datasets/city_list.csv). Generation instruction is provided [here](https://github.com/shantanutrip/covid_flight_analysis/tree/master/Datasets#diseasecsv). Complete dataset can be found [here](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Datasets/disease.csv). Sample dataset is provided below.
```
+--------------------+-----------+------------+    
|     City|      Date|      Cases|      Deaths|
+--------------------+-----------+------------+
|Allegheny|2020-03-14|          1|           0|
|Allegheny|2020-03-15|          3|           0|
|Allegheny|2020-03-16|          5|           0|
|Allegheny|2020-03-17|         10|           0|
+--------------------+-----------+------------+
```

* **merged_flight.csv**: This dataset is generated from all 4 flight data files, it keeps all columns from the original datafiles. This dataset is generated to benefit our analytic models to easily load flight information without having to deal with multiple data files. Generation instruction is provided [here](https://github.com/shantanutrip/covid_flight_analysis/tree/master/Datasets#merged_flightcsv). Complete dataset can be found [here](https://drive.google.com/file/d/1NU0pVbESGXNOVja2vs4yxGaWe9khz728/view?usp=sharing).

* **inter_city_flight_data.csv**: This dataset contains information for every flight between cities listed in [```city_list.csv```](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Datasets/city_list.csv). It is generated from [```merged_flight.csv```](https://drive.google.com/file/d/1NU0pVbESGXNOVja2vs4yxGaWe9khz728/view?usp=sharing) using [```driver.py```](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Code/driver.py). Generation instruction is provided [here](https://github.com/shantanutrip/covid_flight_analysis/tree/master/Code#driverpy-to-generate-the-desired-datasets). Complete dataset can be found [here](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Resultant_Data/inter_city_flight_data.csv). Sample dataset is provided below.
```
+--------------------+------------+---------+----------+----------+             
|           from_city|from_airport|  to_city|to_airport|       day|
+--------------------+------------+---------+----------+----------+
|WILKES-BARRE/SCRA...|        KAVP|CHARLOTTE|      KCLT|2020-02-15|
|WILKES-BARRE/SCRA...|        KAVP|CHARLOTTE|      KCLT|2020-02-17|
|WILKES-BARRE/SCRA...|        KAVP|CHARLOTTE|      KCLT|2020-02-21|
|WILKES-BARRE/SCRA...|        KAVP|CHARLOTTE|      KCLT|2020-02-21|
+--------------------+------------+---------+----------+----------+
```

* **covid_flight_count_data.csv**: This dataset contains information for every city listed in [```city_list.csv```](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Datasets/city_list.csv), for every date since the spread on COVID-19 in that city, the number of COVID-19 cases and deaths, as well as the amount of incoming and outgoing flights. This data is generated from [```merged_flight.csv```](https://drive.google.com/file/d/1NU0pVbESGXNOVja2vs4yxGaWe9khz728/view?usp=sharing), [```airports.csv```](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Datasets/airports.csv) and [```disease.csv```](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Datasets/disease.csv). Generation instruction is provided [here](https://github.com/shantanutrip/covid_flight_analysis/tree/master/Code#driverpy-to-generate-the-desired-datasets). Complete dataset can be found [here](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Resultant_Data/covid_flight_count_data.csv). Sample dataset is provided below.
```
Flight and Covid daily count on merged_flight.csv:
+------+----------+-----+------+---------------------+---------------------+    
|  city|       day|cases|deaths|incoming_flight_count|outgoing_flight_count|
+------+----------+-----+------+---------------------+---------------------+
|BOSTON|2020-02-01|    1|     0|                  341|                  310|
|BOSTON|2020-02-02|    1|     0|                  299|                  293|
|BOSTON|2020-02-03|    1|     0|                  395|                  405|
|BOSTON|2020-02-04|    1|     0|                  423|                  424|
+------+----------+-----+------+---------------------+---------------------+
```
# Data Cleaning

## Challenges
* COVID-19 dataset is county level data, but airports dataset only provides the city name of the location of each airport. For example, “KHOU” is the airport code for William P. Hobby Airport which is located in Houston Texas. However, in COVID-19 dataset, Houston Texas is not an entry because Houston is not a county, instead Harris Texas is used in COVID-19 datasets.
* Inconsistent city naming convention for airports data and COVID-19 data. For example, in airports dataset, "New York" is the city name of JFK, however, in COVID-19 dataset, "New York City" is the name for New York.
* Flight data is provided in four data files with different formats, they need to be merged together for it to be easily loaded for our analytic models.

## Process
* To address the issue of different spatial resolution, we used the geopy library to calculate the county information using each airport’s coordinates.
* To address the issue of different naming conventions, we constructed the [```map_list.csv```](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Datasets/map_list.csv) for the cities listed in [```city_list.csv```](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Datasets/city_list.csv), it contains pairs of names that are different but representing the same city. Beyond the scope of this project, we would have to use geopy to standardize names.  
* To standardize column name in flight data files, [```clean.py```](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Datasets/clean.py) script needs to run for this purpose. Instructions can be found [here](https://github.com/shantanutrip/covid_flight_analysis/tree/master/Datasets#merged_flightcsv)

# Analysis

## COVID-19 Impacts Air Travel Industry:
In this analysis, we aim to find out how the air travel industry is being impacted by COVID-19. As expected, the air travel industry is being negatively impacted by COVID-19. We came to this conclusion by plotting the number flights along with the COVID-19 cases number for each interested city over the course of the pandemic. It clearly shows that the amount of flights decreases dramatically as the number of COVID-19 cases increases. Below is a sample plotting for the city of San Francisco. Complete set of graphs can be found [here](https://github.com/shantanutrip/covid_flight_analysis/tree/master/Analysis/COVID_vs_Flight_Graphs). Reproducible implementation of such a task can be found [here](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Analysis/Analysis_Filght_Covid_Colab.ipynb).
![Sample plotting](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Analysis/COVID_vs_Flight_Graphs/SAN%20FRANCISCO.jpg)

## Air Travel Impacts COVID-19 Spread:
In this analysis, we aim to discover if air travel actually expedited the spread of COVID-19. To do so, we selected several flight attributes and COVID-19 attributes, and plotted each flight attribute with COVID-19 attribute to discover a correlation. Examples for flight attributes are max/min/avg flight count. Examples for COVID-19 attributes are case number and average increase rate. After plotting, we discovered that if a city has more flights, it tends to have more COVID-19 cases and higher increase rate. Below is a sample result for plotting COVID-19 case number with max/min/avg flight count. Complete and reproducible implementation of this task can be found [here](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Analysis/Analysis_Filght_Covid_Colab.ipynb).
![Imgur](https://i.imgur.com/xNz6mlP.png)


## Trace the Origin of COVID-19:
In this analysis, we aim to use available data to determine which cities contributed in the COVID-19 spread in a selected city. To achieve this goal, we took three factors into account: 
1. number of flights within two weeks range prior to the start date of COVID-19 spread in the selected city.
2. day difference between the start date of COVID-19 spread in the selected city and testing city.
3. COVID-19 case number in testing city on the start date of COVID-19 spread in the select city.

We propose that the higher value of the sum of these factors means more significant contribution to the COVID-19 spread in the selected city. Below is a sample result for the city of Dallas. More detailed explanation and reproducible implementation of this task can be found [here](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Analysis/Flight_Impacts_COVID_Basic.ipynb).
![Imgur](https://i.imgur.com/GStwgZQ.png)

## How Possible COVID-19 Spread by Flight
In this analysis, we aim to discover how possible the spread of disease in one target city was resulted from the incoming flights from other "infected" cities (cases appeared earlier). Basiclly, this experiment mainly follows the previous one: tracing the origin of COVID-19 and finding the possiblities, but in more numerical way. To finish this implementation, we mainly focused on these three values:
1. The number of all flights landing to the target city in the past two weeks before the first case in that city. --> (**N_all**)
2. Filter the flights from the **N_all**, choose the flights that the disease has already spreaded out in their source cities. In other words, the start date of disease in these cities should be earlier than the target city. Also the average disease number in these cities should be larger than a threshold. --> (**N_filtered**)
3. The proportion: **Flight_ratio** = **N_filtered** / **N_all**

We propose that the higher value of the **Flight_ratio** means the higher possible for the target city get "infected" via the airlines from other cities. Below is the line chart for the ratio of all the target cities we considered about. More detailed explanation/charts and reproducible implementation of this analysis can be found [here](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Analysis/Flight_Impacts_COVID_Advance.ipynb).

![Imgur](https://github.com/shantanutrip/covid_flight_analysis/blob/master/Archive/line%20chart.png)
