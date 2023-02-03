# Trombone Champ Difficulty Calculator

This script is a rough test on how viable is it to automatically determine difficulty of custom Trombone Champ charts.

This is being used to calculate chart difficulty in [TootTally](https://toottally.com/)

> **NOTE:** This branch will be live on TootTally through the [API](https://toottally.com/api/songs/), and will be used in the future as the basis for the global leaderboard.

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
|   Nyanyanyanyanyanyanya!    |    14    |      8.007589 |     3.025852 |  10.501112 |  517.779538 |
|  You Were Wrong. Go Back.   |    5     |      3.388232 |     3.382500 |   3.411297 |   63.556800 |
|       Rush E (Nerfed)       |    10    |      7.245009 |    10.690906 |   5.522401 |  410.360208 |
|Under the Sea (Instrumental) |    8     |      3.031271 |     3.561510 |   2.766159 |   50.956603 |
|             666             |    10    |      7.239203 |     9.302196 |   6.209193 |  409.593031 |
|         Gymnopédie          |    5     |      1.644792 |     2.285621 |   1.324425 |   18.585394 |
|    The Dance of Eternity    |    10    |      9.585156 |    12.176005 |   8.289732 |  782.734668 |
|     Bill Nye (Chinese)      |    5     |      2.501889 |     3.523677 |   2.302883 |   35.828384 |
|         You Say Run         |    8     |      4.048001 |     5.043452 |   3.550275 |  100.224648 |
|       Trombone Skyze        |    4     |      1.809138 |     2.041377 |   1.693123 |   21.315327 |
|Reality Check Through The Sku|    10    |      5.296985 |     6.776825 |   4.557066 |  195.034138 |
|           Dummy!            |    10    |      5.939867 |     7.461402 |   5.179228 |  256.864456 |
|        GALAXY DRIVE         |    10    |      6.130740 |     7.088208 |   5.652035 |  276.956820 |
|     U.N. Owen was Her?      |    9     |      6.742135 |     7.199608 |   6.514379 |  346.726816 |
|        Viva La Vida         |    7     |      2.431333 |     3.394814 |   1.949593 |   34.098649 |
|Song That Might Play When You|    9     |      6.786230 |     4.841938 |   7.930820 |  352.079793 |
|             666             |    10    |      7.239203 |     9.302196 |   6.209193 |  409.593031 |
|         Zarathustra         |    1     |      1.021456 |     1.199923 |   0.939453 |   10.099002 |
|        Remix 10 WII         |    8     |      3.913946 |     3.801751 |   3.970043 |   92.000939 |
|          Toot Toot          |    1     |      0.628088 |     0.945750 |   0.607385 |    5.863401 |
|         Rum n' Bass         |    10    |      5.065833 |     5.733825 |   4.731846 |  174.985614 |
|  Rainbow Tylenol (Nerfed)   |    8     |      6.217529 |     4.628399 |   7.015043 |  286.357411 |
|        Disco Descent        |    7     |      2.652924 |     2.966906 |   2.495939 |   39.746923 |
|        The Airbuster        |    10    |      5.324411 |     7.094460 |   4.439386 |  197.489039 |
|          Densmore           |    9     |      6.527421 |     6.297844 |   6.642211 |  321.280419 |
|          Baby Park          |    8     |      5.781515 |     6.036801 |   5.653873 |  240.800709 |
|          Bangarang          |    10    |      8.587160 |     7.130205 |   9.315639 |  608.353974 |
|       Waterfall Cave        |    6     |      3.194851 |     3.259371 |   3.170961 |   56.472220 |
|     Bill Nye (Chinese)      |    5     |      2.501889 |     3.523677 |   2.302883 |   35.828384 |
|      We're Not Alright      |    7     |      3.567681 |     5.239064 |   2.732011 |   72.484461 |
|           Warm-Up           |    1     |      1.323517 |     2.038077 |   0.983521 |   13.882296 |
|        The Airbuster        |    10    |      5.324411 |     7.094460 |   4.439386 |  197.489039 |
|      Renai Circulation      |    6     |      3.846101 |     3.844684 |   3.846861 |   87.981405 |
|Harder, Better, Faster, Stron|    8     |      4.614861 |     4.894195 |   4.475195 |  139.158465 |
|Exit This Earth's Atomosphere|    10    |      6.107982 |     9.651418 |   4.336264 |  274.519235 |
|            Taps             |    3     |      0.896038 |     1.301089 |   0.769650 |    8.675848 |
|    Green Hornet (Theme)     |    10    |      7.846443 |     7.760211 |   7.890144 |  493.973278 |
|       Hello BPM 2021        |    10    |     47.649291 |    21.202555 |  60.875485 |30147.814729 |
|         Holdin' On          |    10    |      6.072891 |     2.861464 |   7.678604 |  270.782869 |
|        Kyouki Ranbu         |    10    |     10.596278 |    11.929050 |   9.930033 |  983.645529 |
|         Vs. Lancer          |    10    |      5.759061 |     6.163438 |   5.556873 |  238.567133 |
|           Maniac            |    7     |      4.377990 |     3.956538 |   4.588715 |  122.067816 |
|        Murine Corps         |    10    |      4.412081 |     4.257551 |   4.489346 |  124.454682 |
|       Nightmare King        |    5     |      3.907593 |     5.726333 |   2.998243 |   91.620541 |
|   Nyanyanyanyanyanyanya!    |    14    |      8.007589 |     3.025852 |  10.501112 |  517.779538 |
|          O ma gad           |    10    |      0.359078 |     0.255551 |   0.495759 |    3.271055 |
|      One Winged Angel       |    9     |      4.577409 |     4.118733 |   4.806747 |  136.377351 |
|     Penny Battle Theme      |    5     |      2.528859 |     3.219251 |   2.183708 |   36.506260 |
|  Potion Seller Soundtrack   |    10    |      2.662301 |     4.712109 |   1.637400 |   40.000203 |
|       ロミオとシンデレラ       |    8     |      5.052177 |     5.148679 |   5.006003 |  173.837047 |
|Reality Check Through The Sku|    10    |      5.296985 |     6.776825 |   4.557066 |  195.034138 |
|      Renai Circulation      |    6     |      3.846101 |     3.844684 |   3.846861 |   87.981405 |
|         Rum n' Bass         |    10    |      5.065833 |     5.733825 |   4.731846 |  174.985614 |
|       Rush E (Nerfed)       |    10    |      7.245009 |    10.690906 |   5.522401 |  410.360208 |
|           Rush E            |    10    |      8.888882 |     7.193989 |   9.736733 |  658.600004 |
|          Sandstorm          |    10    |      6.500679 |    12.199771 |   3.651133 |  318.182854 |
|          S.S. Aqua          |    10    |      8.448375 |     5.942291 |   9.705898 |  585.955524 |
|      Strike the Earth!      |    9     |      5.511940 |     4.667253 |   5.934734 |  214.710158 |
|            Taps             |    3     |      0.896038 |     1.301089 |   0.769650 |    8.675848 |
|       Trombone Skyze        |    4     |      1.809138 |     2.041377 |   1.693123 |   21.315327 |
|     Thru Fire & Flames      |    10    |      8.128091 |     5.980225 |   9.202024 |  535.971661 |
|Under the Sea (Instrumental) |    8     |      3.031271 |     3.561510 |   2.766159 |   50.956603 |
|      Unwelcome School       |    10    |      9.755201 |    10.764343 |   9.252370 |  814.801439 |
|      VANESSA (Busted)       |    10    |     10.685799 |     9.875745 |  11.119178 | 1002.627639 |
|        VOID Recorder        |    10    |      1.852056 |     1.666257 |   1.944955 |   22.068341 |
|           Warm-Up           |    1     |      1.323517 |     2.038077 |   0.983521 |   13.882296 |
|      We're Not Alright      |    7     |      3.567681 |     5.239064 |   2.732011 |   72.484461 |
|        YO-KAI Disco         |    10    |      5.407931 |     5.281818 |   5.470989 |  205.065000 |
|         You Say Run         |    8     |      4.048001 |     5.043452 |   3.550275 |  100.224648 |
+-----------------------------+----------+---------------+--------------+------------+-------------+
Report generated at Fri Feb  3 16:49:12 2023
Generated in 34.585277 seconds
```

> **NOTE:** `TT Rating` is the base rating one would get for a play that is at **80%** of the chart's **maximum possible** score.

Charts are obtained from the [Trombone Champ Modding Discord](https://discord.gg/KVzKRsbetJ)

Join us in developing this algorithm further at the [TootTally Discord](https://discord.gg/9jQmVEDVTp)
