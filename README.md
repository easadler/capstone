# Pronto! Predicted

Hello! 

My name is Evan and I am going to tell you about Pronto! Predicted, my capstone project for the Galvanize Data Science Immersive program.

A few months a go I returned to where I had locked My bike on the street only to find... a single tire! I no longer wanted to worry about my bike getting stolen, so I decided to give Seattle's cycle share, Pronto, a try. 

It turns out that Pronto was a rather cheap solution. It only costs $10 a month for UNLIMITED 30 minute rentals between stations. Given that Pronto has 50 stations around the city, I was able to find a station close enough to my destination. For the most part, it was a great solution, except that I was consistently walking across empty stations. 

I struck up a conversation with one of the dispatchers responsible for reshuffling the bikes. It turned out they have one person on duty at a time who is constantly reacting to the bike traffic. With so many stations, it was hard to develop intuition past "bikes go down hill in the morning, and don't really come up".

After talking to their dispatcher, I realized that I could build a tool using predictive analytics to help Pronto with their reshuffling problem. 

Pronto released a data set containing every trip from their first year of business, with the following format and variables. Since they contained, the date-time, starting station, and ending station, I could effectively model supply and demand by applying the following transformations: 

1. Grouping by datetime & station leaving for demand (or station entering for supply)
2. Imputting all times there were no bikes rented
3. Getting hourly weather data and elevations
4. Adding various lags for different data-time related averages

For both supply and demand, I first predict whether an number of bikes are rented or dropped off. This is to deal with the unbalanced classes. 

I then pipe the stations predicted to have a ride into a model that will predict the actual number. My results are as follows:

1. Classification AUC
 * demand: 0.86
 * supply: 0.82
2. actual number Accuracy for 4 classes:
 * demand: 0.616
 * supply 0.614

Consistantely most important variables:

* Lagged hour Average
* Lagged day-of-week Average
* Lagged month Average
* Temperature 
* Wind speed
* Cloud coverage
* Dew point

For both supply and demand, an actual value of zero is correctly predicted 80% of the time (specificity). On the other hand, an actual value of one or more is correctly labeled as such 75% of the time (recall). Once a value is labeled 'one or more', placing it in one of the four bins has an accuracy of around 62%. Since these models are independently, I can take the product of 61.5% & 75% and say values greater than one are correctly predicted around 46% of the time. Considering that around 40% of misclassifications for second models were placing 3-4 bikes into the 1-2 bikes bucket and that there are 50% more 3 bikes, the majority of errors were only off by one bicycle. 














