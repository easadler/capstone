# Pronto! Predicted
## Galvanize Capstone Project
### January 2016
### Evan Sadler

Pronto! Predicted was built to help Seattle's cycle sharing program better reshuffle there bicycles. They have been having a difficult time and after hearing they do not use predictive analytics from an employee, I set out to make the single dispatcher's life a little easier using the power of data science!

## Pronto! Predicting

Let's see how the application works. Using Pronto's JSON feed to get the number of available bikes at each station and scraping hourly weather forecasts, Pronto! Predicted is already prepared to predict the future as soon as it loads. 

When you arrive on the website, you will have the option to look four time periods ahead. Then click "Go!".

![Pronto! Predicted Viz](https://raw.githubusercontent.com/easadler/capstone/master/presentation/images/visualization.png)

After you click "Go!" the circles will shift according to there predicted size. 

### Interpreting the Map
The circles represent a unique station and the sizes of the circles represent the number of bikes currently docked at a station. They are comparable across all stations, no matter the number of docks at a station. On the other hand, the colors represent how full each station is relative to the number of viable available docks. The colors mean as follows:
* Blue: Full
* Green: 50% full
* Red: empty

The color scale slides between the colors, so use blended colors to indicate between the three states above. At anytime, hover on a circle to get the station ID and predicted count.

## How it works


### Forecasting Inventory
![Forecasting Method](https://raw.githubusercontent.com/easadler/capstone/master/presentation/images/forcastingmodel.png =100x20)

### Predictive Model
![Predictive Model](https://raw.githubusercontent.com/easadler/capstone/master/presentation/images/predictivemodel.png =100x20)


