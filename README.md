# Solar Battery Management System

So our house now has panels plugged into a Growatt Inverter, going to a GivEnergy Battery+Inverter. 
Our energy provider is Octopus.
Neither GivEnergy nor Octopus have a satisfactory system of buying and selling from/to the grid so i'm implementing it myself.



Intended system design: maximise profit by selling when the price is highest.

The system must answer a few questions:

1. How much excess energy will i generate today? Excess energy is energy that cannot be stored because the battery will be full. For our situation, we will target 50% full for this calc.
-- how long will it take to sell this at max power of 3.3kW? Therefore how many charge intervals do i need?
NB we can use 3.3kWh per hour, so 40%

2. How can I sell this excess energy most profitably? what are the N most profitable charge intervals

3. how much energy will i generate and need in the next 24 hours?

To do all of this, we will use `crontab` to manage the process.

## System v1
Identify the 3 most profitable intervals in the day, and set crontab to set mode 4 for those intervals.
Steps:
1. Get prices
2. Get 3 most profitable intervals
3. Set crontab for mode 4 for those intervals

