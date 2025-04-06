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


```sudo apt-get install python3-pip```

```sudo pip3 install matplotlib --break-system-packages```

```sudo pip3 install astropy --break-system-packages```

```sudo pip3 install astroquery --break-system-packages```

```sudo pip3 install skyfield --break-system-packages```

```sudo pip3 install pandas --break-system-packages```

```sudo pip3 install suntime --break-system-packages```

```sudo pip3 install pyephem --break-system-packages```

```sudo pip3 install reportlab --break-system-packages```

### Usage

#### Best date and time for DSOs
Adjust the configuration in config.py to your desired location.

Run

```python3 DSO_observation_planning.py --best --dso M30```

or

```python3 DSO_observation_planning.py --best```

on the commandline.

##### Result
The result is a plot which contains graphs for the appearance of the desired
DSO every month of the current year. If no DSO is specified all DSOs from the
list in DSO_observation_planning.py are calculated.
Good months are plotted in darker colours, sub-optimal months in pastel colours.

![M31 in 2025](https://github.com/yetanothergithubaccount/DSObest/blob/main/DSO_M31_2025.png)
![IC434 in 2025](https://github.com/yetanothergithubaccount/DSObest/blob/main/DSO_IC434_2025.png)
![NGC6888 in 2025](https://github.com/yetanothergithubaccount/DSObest/blob/main/DSO_NGC6888_2025.png)


#### Best DSOs tonight
Adjust the configuration in config.py to your desired location.

Run

```python3 DSO_observation_planning.py --tonight```

or

```python3 DSO_observation_planning.py --tonight --moon # consider moon illumination and location during the maximum altitude of a DSO```

on the commandline.

##### Result
The result is a list of DSOs visible during nautical night, visible during astronomical
night and invisible DSOs. Depending on the option the moon's illumnation and
location is considered as well.

```
Find best DSOs for tonight, ordered by their max. altitude...
Nautical night: 23.02.2025 19:09 - 24.02.2025 06:06
  M1: 62.0 in S at 19:10
    TOP: Moon is below the horizon at 23.02.2025 19:10
    Quite good: Moon dir: NW (303.0) , DSO dir: S (191.0)
    Quite nice: Moon illumination is below 50 %: 21.52 %
  M31: 37.0 in WNW at 19:10
    TOP: Moon is below the horizon at 23.02.2025 19:10
    Quite good: Moon dir: NW (303.0) , DSO dir: WNW (293.0)
    Quite nice: Moon illumination is below 50 %: 21.52 %
  M32: 37.0 in WNW at 19:10
    TOP: Moon is below the horizon at 23.02.2025 19:10
    Quite good: Moon dir: NW (303.0) , DSO dir: WNW (293.0)
    Quite nice: Moon illumination is below 50 %: 21.52 %
  M33: 38.0 in W at 19:10
    TOP: Moon is below the horizon at 23.02.2025 19:10
    Quite good: Moon dir: NW (303.0) , DSO dir: W (274.0)
    Quite nice: Moon illumination is below 50 %: 21.52 %
  M34: 56.0 in W at 19:10
    TOP: Moon is below the horizon at 23.02.2025 19:10
    Quite good: Moon dir: NW (303.0) , DSO dir: W (277.0)
    Quite nice: Moon illumination is below 50 %: 21.52 %
  M36: 74.0 in SSW at 19:10
    TOP: Moon is below the horizon at 23.02.2025 19:10
    Quite good: Moon dir: NW (303.0) , DSO dir: SSW (196.0)
    Quite nice: Moon illumination is below 50 %: 21.52 %
  M37: 72.0 in S at 19:10
    TOP: Moon is below the horizon at 23.02.2025 19:10
    Quite good: Moon dir: NW (303.0) , DSO dir: S (184.0)
    Quite nice: Moon illumination is below 50 %: 21.52 %
  M38: 75.0 in SSW at 19:10
    TOP: Moon is below the horizon at 23.02.2025 19:10
    Quite good: Moon dir: NW (303.0) , DSO dir: SSW (203.0)
    Quite nice: Moon illumination is below 50 %: 21.52 %
  M42: 34.0 in S at 19:10
    TOP: Moon is below the horizon at 23.02.2025 19:10
    Quite good: Moon dir: NW (303.0) , DSO dir: S (187.0)
    Quite nice: Moon illumination is below 50 %: 21.52 %
  M43: 34.0 in S at 19:10
    TOP: Moon is below the horizon at 23.02.2025 19:10
    Quite good: Moon dir: NW (303.0) , DSO dir: S (187.0)
    Quite nice: Moon illumination is below 50 %: 21.52 %
  M45: 54.0 in SW at 19:10
    TOP: Moon is below the horizon at 23.02.2025 19:10
    Quite good: Moon dir: NW (303.0) , DSO dir: SW (237.0)
    Quite nice: Moon illumination is below 50 %: 21.52 %
  M74: 28.0 in W at 19:10
    TOP: Moon is below the horizon at 23.02.2025 19:10
    Quite good: Moon dir: NW (303.0) , DSO dir: W (261.0)
    Quite nice: Moon illumination is below 50 %: 21.52 %
  M76: 51.0 in WNW at 19:10
    TOP: Moon is below the horizon at 23.02.2025 19:10
    Quite good: Moon dir: NW (303.0) , DSO dir: WNW (298.0)
    Quite nice: Moon illumination is below 50 %: 21.52 %
  M77: 25.0 in SW at 19:10
    TOP: Moon is below the horizon at 23.02.2025 19:10
    Quite good: Moon dir: NW (303.0) , DSO dir: SW (236.0)
    Quite nice: Moon illumination is below 50 %: 21.52 %
  M78: 40.0 in S at 19:10
    TOP: Moon is below the horizon at 23.02.2025 19:10
    Quite good: Moon dir: NW (303.0) , DSO dir: S (184.0)
    Quite nice: Moon illumination is below 50 %: 21.52 %
  M79: 15.0 in S at 19:10
    TOP: Moon is below the horizon at 23.02.2025 19:10
    Quite good: Moon dir: NW (303.0) , DSO dir: S (188.0)
    Quite nice: Moon illumination is below 50 %: 21.52 %
  M103: 53.0 in NW at 19:10
    TOP: Moon is below the horizon at 23.02.2025 19:10
    Quite nice: Moon illumination is below 50 %: 21.52 %
  M110: 37.0 in WNW at 19:10
    TOP: Moon is below the horizon at 23.02.2025 19:10
    Quite good: Moon dir: NW (303.0) , DSO dir: WNW (294.0)
    Quite nice: Moon illumination is below 50 %: 21.52 %
  M35: 64.0 in S at 19:21
    TOP: Moon is below the horizon at 23.02.2025 19:21
    Quite good: Moon dir: NW (307.0) , DSO dir: S (180.0)
    Quite nice: Moon illumination is below 50 %: 21.44 %
  M4: 13.0 in S at 05:34
    Quite good: Moon dir: SE (141.0) , DSO dir: S (180.0)
    Quite nice: Moon illumination is below 50 %: 26.01 %
  M107: 27.0 in S at 05:43
    Quite good: Moon dir: SE (143.0) , DSO dir: S (180.0)
    Quite nice: Moon illumination is below 50 %: 25.96 %
  M13: 76.0 in S at 05:51
    Quite good: Moon dir: SE (144.0) , DSO dir: S (180.0)
    Quite nice: Moon illumination is below 50 %: 25.93 %
  M12: 38.0 in S at 05:57
    Quite good: Moon dir: SE (145.0) , DSO dir: S (180.0)
    Quite nice: Moon illumination is below 50 %: 25.9 %
  M2: 12.0 in ESE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: ESE (107.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M6: 7.0 in S at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: S (170.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M7: 4.0 in S at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: S (168.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M8: 14.0 in SSE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (164.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M9: 21.0 in S at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: S (174.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M10: 36.0 in S at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: S (180.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M11: 28.0 in SE at 06:06
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M14: 36.0 in S at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: S (167.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M15: 23.0 in E at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: E (99.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M16: 24.0 in SSE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (158.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M17: 21.0 in SSE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (158.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M18: 20.0 in SSE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (159.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M19: 14.0 in S at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: S (178.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M20: 15.0 in SSE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (164.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M21: 16.0 in SSE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (164.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M22: 13.0 in SSE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (156.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M23: 20.0 in SSE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (165.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M24: 19.0 in SSE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (160.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M25: 18.0 in SSE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (156.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M26: 26.0 in SE at 06:06
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M27: 45.0 in ESE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: ESE (110.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M28: 12.0 in SSE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (159.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M29: 52.0 in E at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: E (87.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M39: 47.0 in ENE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: ENE (65.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M52: 40.0 in NE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: NE (38.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M54: 5.0 in SSE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (154.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M55: 1.0 in SE at 06:06
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M56: 57.0 in ESE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: ESE (114.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M57: 63.0 in ESE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: ESE (117.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M62: 10.0 in S at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: S (179.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M69: 5.0 in SSE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (160.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M70: 4.0 in SSE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (157.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M71: 43.0 in ESE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: ESE (115.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M72: 9.0 in ESE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: ESE (122.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M73: 8.0 in ESE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: ESE (121.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M75: 7.0 in SE at 06:06
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M92: 82.0 in SSE at 06:06
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
Astronomical night: 23.02.2025 19:47 - 24.02.2025 05:29
  M41: 19.0 in S at 19:57
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M50: 31.0 in S at 20:15
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M47: 25.0 in S at 20:48
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M46: 25.0 in S at 20:54
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M93: 16.0 in S at 20:55
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M48: 34.0 in S at 21:25
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M44: 59.0 in S at 21:51
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M67: 52.0 in S at 22:03
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M81: 71.0 in N at 23:08
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M82: 71.0 in N at 23:08
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M95: 51.0 in S at 23:55
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M96: 52.0 in S at 23:58
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M105: 52.0 in S at 23:58
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M108: 85.0 in N at 00:23
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M97: 85.0 in N at 00:25
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M65: 53.0 in S at 00:30
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M66: 53.0 in S at 00:31
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M109: 87.0 in N at 01:09
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M98: 55.0 in S at 01:25
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M99: 54.0 in S at 01:29
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M106: 87.0 in S at 01:29
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M61: 44.0 in S at 01:32
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M40: 82.0 in N at 01:33
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M100: 56.0 in S at 01:33
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M84: 53.0 in S at 01:36
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M85: 58.0 in S at 01:36
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M86: 53.0 in S at 01:36
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M49: 48.0 in S at 01:40
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M87: 52.0 in S at 01:42
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M88: 54.0 in S at 01:42
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M89: 52.0 in S at 01:46
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M91: 54.0 in S at 01:46
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M58: 52.0 in S at 01:48
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M90: 53.0 in S at 01:48
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M68: 13.0 in S at 01:50
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M104: 28.0 in S at 01:50
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M59: 51.0 in S at 01:52
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M60: 51.0 in S at 01:53
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M94: 81.0 in S at 02:01
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M64: 61.0 in S at 02:08
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M53: 58.0 in S at 02:24
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M63: 82.0 in S at 02:26
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M51: 87.0 in S at 02:39
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M83: 10.0 in S at 02:48
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M3: 68.0 in S at 02:52
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M101: 86.0 in N at 03:13
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M102: 84.0 in N at 04:16
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M5: 42.0 in S at 04:29
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
  M80: 17.0 in S at 05:27
    Quite good: Moon dir: SE (147.0) , DSO dir: SSE (151.0)
    Quite nice: Moon illumination is below 50 %: 25.86 %
Invisible DSOs:
  M30: -6.0 in ESE at 06:06
```


The optional option --justthetopones in combination with the options --tonight and --moon allows to look at the TOP DSOs of that night only:
```
python3 DSO_observation_planning.py --tonight --moon --justthetopones
```

The optional option -r/--direction in combination with the options --tonight and --moon allows to look at the TOP DSOs of that night which appear in a certain direction (S/W/N/E) only:
```
python3 DSO_observation_planning.py --tonight --moon --justthetopones --direction S
```

The optional option -c/--catalogue Messier|Caldwell allows to select a catalogue of well-known DSOs for tonight's check.
```
python3 DSO_observation_planning.py --tonight --moon --catalogue Messier
```

## Blog

[https://thisisyetanotherblog.wordpress.com/2025/02/22/astrophotography-what-is-the-best-time-to-observe-my-favourite-deep-sky-object/](https://thisisyetanotherblog.wordpress.com/2025/02/22/astrophotography-what-is-the-best-time-to-observe-my-favourite-deep-sky-object/)

[https://thisisyetanotherblog.wordpress.com/2025/02/23/astrophotography-whats-on-the-sky-tonight/](https://thisisyetanotherblog.wordpress.com/2025/02/23/astrophotography-whats-on-the-sky-tonight/)
