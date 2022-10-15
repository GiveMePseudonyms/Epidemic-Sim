# Epidemic-Sim
An agent-based model designed to model epidemics with varying degrees of infectivity, lethality, vaccination rates, mask-wearing, hand-washing. Written in Python. Started Oct 2022.

## System Design
<img src="/sysdesign/EpidemicSim Mindmap.png" alt="Mindmap showing system design" title="Sysdesign Mindmap">

## Introduction
This package allows you to model the course of an epidemic whilst altering settings such as virus infectivity and lethality, population size, vaccination rates, mask-wearing rates, hand-washing rates etc.

The effectiveness of each 'prevention measure' will be determined using data from peer-reviewed studies on their efficacy in order to increase the accuracy of the model in controlled conditions.

## Studies on prevention method efficacy
Below is a list of papers I have used to determine the efficacy of given prevention methods. This list will be updated as more data is used.

## Limitations
- The real world is chaotic and extremely difficult to accurately model. This model should be used for demonstration purposes.
- This package is computationally expensive and where fast simulation times are important, has a maximum population size of approximately 100,000 and no more than 300,000. Larger populations significantly slow down the model. There are various code improvements that can increase the speed of the model which will be regularly tested and applied.
