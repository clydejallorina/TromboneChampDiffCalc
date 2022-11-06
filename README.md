# Trombone Champ Difficulty Calculator

This script is a rough test on how viable is it to automatically determine difficulty of custom Trombone Champ charts.

## Background

As this is going to be calculations for overall difficulty, I think the focus of this system would be on the peaks of difficulty of a chart, and as such the system I have in mind would be designed around the idea that the difficulty of a chart would be more or less determined by its hardest portions. A lot of ideas for this comes from Xexxar's rework of osu!'s Star Rating and PP system in 2021 which I believe is quite close to quantifying difficulty in rhythm properly: https://github.com/ppy/osu/pull/14395

There's going to be around 3 criteria that the system I've had in mind would use to determine the difficulty. (More could be added soon depending on how accurate these criteria are in determining difficulty of a chart)

1. Speed: This corresponds to the speed of toots that must be correctly played by the player. It's harder to tap 10 toots in a bar compared to 1 (more often than not)
For this one, I've simply taken the maximum amount of buttons that would need to be pushed a bar, and multiplied it by the beats per second in order to determine of which toots must be done.

2. Note Spacing / Aim Strain: This corresponds to the cumulative distance between notes in a bar, and how difficult it is to accurately aim notes/sliders. It's harder to toot different pitches of notes (or sliders that go in wave patterns) than those that are the same pitch (or sliders that stay on the same line)

3. Rhythm Complexity: In rhythm games, it's usually easier to tap continuously than in bursts. The system needs to take complex rhythms into account when calculating difficulty.

## Results

```
+-----------------------------+----------+---------------+--------------+------------+-------------+
|          Song Name          | Map Diff | Computed Diff | Speed Rating | Aim Rating |  TT Rating  |
+-----------------------------+----------+---------------+--------------+------------+-------------+
|         A Long Fall         |    6     |      6.851221 |     4.491651 |   8.516486 |   55.483475 |
|          BIG SHOT           |    8     |      6.674674 |     6.726129 |   7.264758 |   79.940545 |
|        Bloody Stream        |    7     |      5.569697 |     3.497254 |   5.599051 |   56.608916 |
|         Bonetrousle         |    5     |      7.028048 |     7.675195 |   7.981899 |   66.956078 |
|         DRAGONLADY          |    9     |     10.549868 |    16.932243 |  18.523426 |  142.168802 |
|     Fly me to the moon      |    5     |      4.396119 |     1.896726 |   3.492072 |   29.320105 |
|        Freedom Dive         |    10    |     19.463868 |   101.940480 |  46.839499 |  628.443496 |
|        Friday Night         |    6     |      5.865078 |     3.725163 |   6.275982 |   52.986667 |
|        Gourmet Race         |    8     |      7.909082 |     6.783741 |  12.817220 |   80.568117 |
|         Megalovania         |    10    |      8.782461 |     7.378212 |  13.995650 |   86.923861 |
|          Meikaruza          |    10    |      9.528541 |    16.735297 |  13.790765 |  148.452639 |
|   Never Gonna Give You Up   |    7     |      5.348760 |     4.307680 |   4.667420 |   57.980852 |
|      Next Color Planet      |    8     |      6.625879 |     4.415193 |   7.894088 |   60.323641 |
|      Night of Knights       |    10    |      9.525699 |    19.196664 |  13.035157 |  160.428881 |
|         penis music         |    6     |      9.143612 |    15.043722 |  12.876661 |  135.736055 |
|       Rainbow Tylenol       |    19    |     11.852446 |    36.379381 |  17.956106 |  258.126933 |
|         Rockefeller         |    7     |      6.332471 |     1.981651 |   7.897931 |   35.401007 |
|        Sea Shanty 2         |    6     |      6.943245 |     5.165613 |   8.572115 |   68.038735 |
|       Thomas The Tank       |    4     |      4.673184 |     3.274363 |   3.925731 |   43.355269 |
|     Thru Fire & Flames      |    10    |     10.116112 |    24.248879 |  13.748660 |  193.920469 |
|      We Are Number One      |    6     |      6.212167 |     5.142399 |   6.521266 |   57.294018 |
|         White Sedan         |    1     |      1.007705 |     0.527501 |   3.313106 |   10.455208 |
+-----------------------------+----------+---------------+--------------+------------+-------------+
Report generated at Thu Nov  3 15:12:42 2022
Generated in 1.779353 seconds
```
