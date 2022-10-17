# Epidemic-Sim
An agent-based model designed to model epidemics with varying degrees of infectivity, lethality, vaccination rates, mask-wearing, hand-washing. Written in Python. Started Oct 2022.

## How to run
Download the repo into a single folder, open a terminal in that folder, then type:
```
pip3 install requirements.txt
python3 simulation.py
```

## System Design
<img src="/sysdesign/EpidemicSim Mindmap.png" alt="Mindmap showing system design" title="Sysdesign Mindmap">

## Introduction
This package allows you to model the course of an epidemic whilst altering settings such as virus infectivity and lethality, population size, vaccination rates, mask-wearing rates, hand-washing rates etc.

The effectiveness of each 'prevention measure' will be determined using data from peer-reviewed studies on their efficacy in order to increase the accuracy of the model in controlled conditions.

## The Model
This model simulates the spread of an infectious disease through a population of people. At the beginning the user will choose the size of the population and the number of infected people at the outset, as well as other settings pertaining to the disease and prevention measures used by the population.

Each 'day', people gather in locations with other people. The number of people per location will depend upon the population size, number of locations, and social distancing measures in place.

The model then calculates the 'infectivity' of the location from the sum of the infectivity of each infected person in it. If there are no infected people in the location, the infectivity will be 0.

The model calculates the susceptibility of each uninfected, non-immune person who is in a location with at least 1 infected person based upon their prevention measures such as mask-wearing.

For each infected person who shares a room with at least one non-infected, non-immune person, the model calculates the infected person's infecitivity based upon their personal prevention measures and the overall infectivity of the disease.

We then use the above data to determine whether a given person will become infected. Some variance can be added to the duration of their infection as well as the period of immunity they gain post-recovery.

## Settings
Note: all settings can be changed after the simulation starts unless stated otherwise.

### Number of people
The total population at the beginning of the simulation. This cannot be changed after the simulation begins.

### Number of infected
The number of infected people at the beginning of the simulaiton. This cannot be changed after the simulation begins.

### Number of locations
The number of locations in which the population can gather.

### Virus infectivity
The basic infectivity of the disease. Higher numbers are more infectious.

### Infection duration
The period for which in infected person stays infected.

### Infection duration variance
The amount of randomness of the infection duration.

### Mortality rate
The percentage of cases which will result in death.

### Post-recovery immunity period
The length of time for which a person who has recovered has immunity to re-infection.

### Post-recovery immunity period variance
The amount of randomness applied to the period of immunity granted after recovery.

### Vaccinations
Switches on/off vaccinations.

### Daily vaccination chance (%)
Determines how likely each unvaccinated person is to be vaccinated each day.

### Masks
Switches on/off mask usage.

### Mask usage (%)
Determines how many people will use a mask as a percentage of the population. This will also have some slight variance for realism.

### Days to simulate
How many days to simulate. This can be changed and repeated to move in smaller or larger steps.

## Studies on prevention method efficacy
Below is a list of papers I have used to determine the efficacy of given prevention methods. This list will be updated as more data is used.

## Limitations
- The real world is chaotic and extremely difficult to accurately model. This model should be used for demonstration purposes.
- This package is computationally expensive and where fast simulation times are important, has a maximum population size of approximately 100,000 and no more than 300,000. Larger populations significantly slow down the model. There are various code improvements that can increase the speed of the model which will be regularly tested and applied. The popultion list will be pruned to remove dead people, which will speed up the processing for a disease which has killed many people over time.
