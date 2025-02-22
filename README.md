# DSObest
Some deep space objects (DSOs) are not visible all year round. They appear
seasonally only.

This tool helps to find out about the best time and date to observe a DSO.
Not only the observers location is considered, but also the moon's phase,
illumination, direction and altitude is taken into account as well.

## How does it work?
The idea behind is to check a DSO every first of a month in the current year.
The maximum altitude during the astronomical night is determined. The moon's
phase, illumination, altitude and direction is also checked.
Simple rules like 'DSO maximum altitude reached during the astronomical night',
moon below the horizon', 'moon in a different direction', 'moon illumination <
50%' allow to make a recommendation for good observation conditions.

## Software
### Requirements
- Python3 and a few modules


```sudo apt install python3-pip```

```sudo pip3 install matplotlib --break-system-packages```

```sudo pip3 install astropy --break-system-packages```

```sudo pip3 install astroquery --break-system-packages```

```sudo pip3 install skyfield --break-system-packages```

```sudo pip3 install pandas --break-system-packages```

```sudo pip3 install suntime --break-system-packages```

```sudo pip3 install pyephem --break-system-packages```

### Usage

Run

```python3 DSO_observation_planning.py --best --dso M30```

on the commandline.

## Result
The result is a plot which contains graphs for the appearance of the desired
DSO every month of the current year.
Good months are plotted in darker colours, sub-optimal months in pastel colours.
