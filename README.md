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
+-----------------------------+----------+---------------+--------------+------------+
|          Song Name          | Map Diff | Computed Diff | Speed Rating | Aim Rating |
+-----------------------------+----------+---------------+--------------+------------+
|         A Long Fall         |    6     |      6.851221 |     4.491651 |   8.516486 |
|          BIG SHOT           |    8     |      6.675562 |     6.726129 |   7.264758 |
|         DRAGONLADY          |    9     |     10.643551 |    16.932243 |  18.523426 |
|     Fly me to the moon      |    5     |      4.396899 |     1.896726 |   3.492072 |
|        Freedom Dive         |    10    |     19.463868 |   101.940480 |  46.839499 |
|        Friday Night         |    6     |      5.936264 |     3.725163 |   6.275982 |
|        Gourmet Race         |    8     |      8.407158 |     6.783741 |  12.817220 |
|         Megalovania         |    10    |      8.782543 |     7.378212 |  13.995650 |
|          Meikaruza          |    10    |      9.528542 |    16.735297 |  13.790765 |
|   Never Gonna Give You Up   |    7     |      5.348764 |     4.307680 |   4.667420 |
|      Next Color Planet      |    8     |      6.625879 |     4.415193 |   7.894088 |
|      Night of Knights       |    10    |      9.544479 |    19.196664 |  13.035157 |
|       Rainbow Tylenol       |    19    |     11.874849 |    36.379381 |  17.956106 |
|         Rockefeller         |    7     |      6.333868 |     1.981651 |   7.897931 |
|        Sea Shanty 2         |    6     |      6.946442 |     5.165613 |   8.572115 |
|     Thru Fire & Flames      |    10    |     10.116112 |    24.248879 |  13.748660 |
|      We Are Number One      |    6     |      6.213166 |     5.142399 |   6.521266 |
|         White Sedan         |    1     |      4.044058 |     0.527501 |   3.313106 |
+-----------------------------+----------+---------------+--------------+------------+
Report generated at Tue Nov  1 11:30:47 2022
Generated in 1.663024 seconds
```
