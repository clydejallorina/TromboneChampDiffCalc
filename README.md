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
|         A Long Fall         |    6     |      7.549592 |     4.212697 |   8.903877 |   65.411263 |
|          BIG SHOT           |    8     |      8.000478 |     6.188884 |   9.268064 |   85.421460 |
|        Bloody Stream        |    7     |      6.549469 |     3.433295 |   7.113361 |   59.702735 |
|         Bonetrousle         |    5     |      7.420655 |     7.457787 |   6.936047 |   85.295888 |
|         Buddy Holly         |    6     |      5.603539 |     2.724089 |   6.334692 |   47.292032 |
|         DRAGONLADY          |    9     |     11.529786 |    16.978353 |  22.235120 |  172.448261 |
|      Eine (CHAMP MIX)       |    10    |      8.710814 |     6.336351 |  11.830792 |   88.773170 |
|     Fly me to the moon      |    5     |      3.047780 |     1.868634 |   4.921383 |   29.310744 |
|        Freedom Dive         |    10    |     17.518167 |   101.910407 |  41.165224 |  763.514883 |
|        Friday Night         |    6     |      7.258847 |     3.669228 |   8.480179 |   62.111977 |
|        Gourmet Race         |    8     |      8.714653 |     6.780292 |  12.157588 |   91.632756 |
|       Ludicolo Dance        |    8     |      6.030363 |     3.482060 |   9.085493 |   53.951919 |
|         Megalovania         |    10    |      8.927254 |     7.142566 |  12.257412 |   95.255351 |
|          Meikaruza          |    10    |      9.546798 |    16.489748 |  10.418748 |  165.614457 |
|   Never Gonna Give You Up   |    7     |      6.632865 |     4.206098 |   6.836728 |   64.552604 |
|      Next Color Planet      |    8     |      8.004620 |     4.301213 |  10.224373 |   69.991286 |
|      Night of Knights       |    10    |     10.298142 |    19.100259 |  13.140083 |  185.689724 |
|         penis music         |    6     |     10.069630 |    15.277566 |  13.763573 |  158.208073 |
|       Rainbow Tylenol       |    19    |     12.831882 |    35.757221 |  22.801046 |  307.510179 |
|         Rockefeller         |    7     |      7.006140 |     1.913286 |   8.717570 |   45.289249 |
|        Sea Shanty 2         |    6     |      7.282526 |     4.914535 |   7.858388 |   72.461035 |
|            Taps             |    3     |      0.347625 |     0.531644 |   1.806494 |    7.769931 |
|       EUROBEAT THOMAS       |    10    |      8.264161 |    10.439273 |  11.767886 |  110.958987 |
|       Thomas The Tank       |    4     |      5.719888 |     3.196779 |   6.228680 |   51.246611 |
|     Thru Fire & Flames      |    10    |     10.596543 |    23.178374 |  12.824312 |  216.362475 |
|           Warm-Up           |    1     |      2.169397 |     0.732002 |   4.610134 |   17.448106 |
|      We Are Number One      |    6     |      7.099576 |     5.175448 |   7.293433 |   70.480933 |
|         White Sedan         |    1     |      1.712565 |     0.528105 |   4.669855 |   13.208178 |
+-----------------------------+----------+---------------+--------------+------------+-------------+
Report generated at Sun Dec 25 07:48:18 2022
Generated in 2.677114 seconds
```

Charts are obtained from the [Trombone Champ Modding Discord](https://discord.gg/KVzKRsbetJ)
