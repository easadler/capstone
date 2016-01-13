# Pronto! Predicted

Hello! 

My name is Evan and I am going to breifly tell you about my capstone project, Pronto! Predicted.

A few months ago, I returned to where I had locked my bike on the street only to find...a single tire! Instead of buying a new bicycle, I decided to give Seattle's cycle share, Pronto, a try. 

It turns out that Pronto was a rather cheap solution. It only costs $10 a month for UNLIMITED 30-minute rentals between stations. Given that Pronto has 50 stations around the city, I was able to find a station close enough to my destination. For the most part, it was a great solution, except that I was consistently walking across empty stations. 

It turns out that the Pronto dispatchers are having a hard time anticipating the flow of bicycles around the city. Seattle is built on a hill and has hard to predict weather, which is unlike many other cities with cycle-sharing programs. After talking to a Pronto dispatcher, I learned their current strategy is reacting to bike traffic. Clearly, this was a great opportunity to apply some data science and create a predictive model. 

Pronto released a data set containing every trip from their first year of business, with the following format and variables. Since they contained, the date-time, starting station, and ending station, I could effectively model supply and demand by applying the following transformations:

1. Aggregate over
 * date
 * [morning, commute to work, afternoon, commute home, night]
 * [starting station (demand), ending station (supply)]
2. Impute date-times where there were no rentals
3. Get features 
 * Weather data (NOAA)
 * Elevations (Google API)
4. Adding lags
 * month avg
 * day-of-week avg
 * hour average

Due to unbalanced classes, I used a data driven approach to bin hours (morning, commute to work,...). This drastically helped, however the counts needed to be binned as well. I first binned by zero bikes and 1 or more. This turned out to be almost 1:1. I then piped the stations predicted to have a ride into a model that will predict if the count is in the following bins: 1-2, 2-4, 5-8, 8-15. Here are my results:

1. Classification AUC
 * demand: 0.87
 * supply: 0.86
2. 4 Class Model Accuracy:
 * demand: 0.616
 * supply 0.614

Most important variables:
* Lagged averages
* Temperature
* Dew Point
* Wind Speed
* Cloud Coverage
* Elevation

For both supply and demand, an actual value of zero is correctly predicted 80% of the time (specificity). On the other hand, an actual value of one or more is correctly labeled as such 75% of the time (recall). Once a value is labeled 'one or more', placing it in one of the four bins has an accuracy of around 62%. Since these models are independently, I can take the product of 61.5% & 75% and say values greater than one are correctly predicted around 46% of the time. Considering that around 40% of misclassifications for second models were placing 3-4 bikes into the 1-2 bikes bucket and that there are 50% more 3 bikes, the majority of errors were only off by one bicycle. 














