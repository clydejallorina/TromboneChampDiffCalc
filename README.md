# Trombone Champ Difficulty Calculator

This script is a rough test on how viable is it to automatically determine difficulty of custom Trombone Champ charts.

This is being used to calculate chart difficulty in [TootTally](https://toottally.com/)

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
|         A Long Fall         |    6     |      7.592946 |     4.491651 |   8.884794 |  129.876478 |
|          BIG SHOT           |    8     |      8.053597 |     6.726129 |   9.173122 |  180.258960 |
|        Bloody Stream        |    7     |      6.562881 |     3.497254 |   7.104281 |  127.912005 |
|         Bonetrousle         |    5     |      7.507284 |     7.675195 |   7.057908 |  149.123018 |
|         Buddy Holly         |    6     |      5.829458 |     2.792928 |   6.475109 |   96.501765 |
|         DRAGONLADY          |    9     |     11.489314 |    16.932243 |  21.971712 |  321.783126 |
|     Fly me to the moon      |    5     |      3.908433 |     1.896726 |   4.914576 |   61.063571 |
|        Freedom Dive         |    10    |     17.483660 |   101.940480 |  40.684321 | 1448.483814 |
|        Friday Night         |    6     |      7.248563 |     3.725163 |   8.426826 |  126.983073 |
|        Gourmet Race         |    8     |      8.713737 |     6.783741 |  12.151981 |  182.415096 |
|       Ludicolo Dance        |    8     |      6.027200 |     3.486178 |   9.072922 |  102.879984 |
|         Megalovania         |    10    |      8.928988 |     7.378212 |  12.146942 |  192.700079 |
|          Meikaruza          |    10    |      9.565933 |    16.735297 |  10.390138 |  319.806220 |
|   Never Gonna Give You Up   |    7     |      6.660987 |     4.307680 |   6.835957 |  132.971424 |
|      Next Color Planet      |    8     |      8.043520 |     4.415193 |  10.294430 |  144.084647 |
|      Night of Knights       |    10    |     10.293069 |    19.196664 |  13.062816 |  352.459587 |
|         penis music         |    6     |     10.007342 |    15.043722 |  13.541115 |  299.248287 |
|       Rainbow Tylenol       |    19    |     12.921512 |    36.379381 |  23.253489 |  580.930661 |
|         Rockefeller         |    7     |      7.115901 |     1.981651 |   8.927771 |   90.589459 |
|        Sea Shanty 2         |    6     |      7.384670 |     5.165613 |   7.990416 |  150.869440 |
|       Thomas The Tank       |    4     |      5.813115 |     3.274363 |   6.273837 |  101.833103 |
|     Thru Fire & Flames      |    10    |     10.774730 |    24.248879 |  13.383213 |  424.638686 |
|      We Are Number One      |    6     |      7.067531 |     5.142399 |   7.237836 |  131.497527 |
|         White Sedan         |    1     |      2.600934 |     0.527501 |   4.665750 |   34.410511 |
+-----------------------------+----------+---------------+--------------+------------+-------------+
Report generated at Fri Dec  2 14:46:50 2022
Generated in 2.019778 seconds
```

Charts are obtained from the [Trombone Champ Modding Discord](https://discord.gg/KVzKRsbetJ)
