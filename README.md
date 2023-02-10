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
|          Song Name          | Map Diff | Computed Diff |  Tap Rating  | Aim Rating |  TT Rating  |
+-----------------------------+----------+---------------+--------------+------------+-------------+
|      1 2 Gourmet Race       |    7     |      2.623433 |     3.942420 |   1.963940 |   38.958087 |
|  21st century schizoid man  |    10    |      5.654925 |     3.757545 |   6.603616 |  228.352238 |
|   A Cruel Angel's Thesis    |    10    |      3.669300 |     3.853736 |   3.577081 |   77.954928 |
|           Africa            |    6     |      2.610957 |     3.525593 |   2.153638 |   38.627880 |
|   All I Want 4 Xmas Is U    |    7     |      2.396299 |     2.487482 |   2.350708 |   33.262816 |
|      Aquatic Ambience       |    7     |      4.248129 |     5.170422 |   3.786982 |  113.199565 |
|      A Thousand Miles       |    4     |      2.031104 |     3.066801 |   1.513255 |   25.402155 |
|           Aurora            |    10    |      6.113902 |     7.434926 |   5.453389 |  275.152192 |
|        Axe to Grind         |    9     |      2.350327 |     2.784938 |   2.133021 |   32.188736 |
|          Baby Park          |    8     |      5.601315 |     5.898887 |   5.452529 |  223.185367 |
|          Bad Apple          |    7     |      4.097202 |     6.044389 |   3.123609 |  103.336916 |
|         Baka Mitai          |    5     |      1.603362 |     1.855713 |   1.477186 |   17.933844 |
|            DotA             |    7     |      4.757907 |     6.531245 |   3.871238 |  150.054139 |
|      Battlerock Galaxy      |    7     |      1.675878 |     2.189641 |   1.418996 |   19.083692 |
|       Beethoven Virus       |    10    |      7.021021 |     7.181626 |   6.940718 |  381.315348 |
|   better call saul theme    |    8     |      2.486345 |     2.195192 |   2.631921 |   35.441911 |
|          BIG SHOT           |    8     |      3.694013 |     3.789247 |   3.646396 |   79.317560 |
|         Big Enough          |    8     |      2.565921 |     2.732529 |   2.482616 |   37.453090 |
|     Bill Nye (Chinese)      |    5     |      2.257602 |     3.025617 |   1.873595 |   30.098925 |
|           Blend W           |    7     |      3.010719 |     3.236143 |   2.898006 |   50.293342 |
|        Bloody Stream        |    7     |      2.686908 |     2.872217 |   2.594254 |   40.670529 |
|      Blue (Da Ba Dee)       |    6     |      3.173092 |     4.774299 |   2.372489 |   55.713911 |
|      Bohemian Rhapsody      |    7     |      2.736004 |     3.636763 |   2.285625 |   42.032859 |
|       Bomb Rush Blush       |    9     |      4.561058 |     6.437493 |   3.622840 |  135.172493 |
|         Breakout v2         |    8     |      4.299066 |     4.985765 |   3.955717 |  116.635894 |
|         BRODYQUEST          |    9     |      3.890844 |     3.254082 |   4.209225 |   90.621521 |
|    Calamari Inkantation     |    5     |      3.554186 |     3.592843 |   3.534857 |   71.773967 |
|        Cantina Band         |    6     |      3.424782 |     2.744504 |   3.764920 |   65.151445 |
|       Caramelldansen        |    6     |      3.126851 |     3.974585 |   2.702985 |   54.127733 |
| Carol of the Bells (metal)  |    5     |      3.714494 |     5.568490 |   2.787496 |   80.456368 |
|      Chariots Of Fire       |    5     |      1.975963 |     2.331527 |   1.798180 |   24.341417 |
|     Chemical Plant Zone     |    9     |      4.518580 |     4.727285 |   4.414227 |  132.068763 |
|       Chug Jug With U       |    7     |      3.239614 |     3.480213 |   3.119315 |   58.056602 |
|    The Dance of Eternity    |    10    |     11.314443 |    15.212331 |   9.365498 | 1141.468076 |
|        Dancing Queen        |    6     |      2.090154 |     3.237610 |   1.516425 |   26.573025 |
| Dedicated to MoonlightHard  |    10    |      5.278529 |     7.245156 |   4.295216 |  193.391180 |
|      Deja Vu (Vocals)       |    7     |      3.534771 |     4.558287 |   3.023013 |   70.758445 |
|          Densmore           |    9     |      6.358215 |     6.181477 |   6.446585 |  301.948710 |
|          Detonate           |    6     |      3.100408 |     4.695366 |   2.302928 |   53.236010 |
|  Ding Dong Merrily on High  |    10    |      1.728888 |     1.315802 |   1.935432 |   19.952576 |
|      dont stop me now       |    8     |      2.799459 |     3.589606 |   2.404385 |   43.843518 |
|         Double-Tap          |    3     |      1.144161 |     1.729754 |   0.851365 |   11.570603 |
|         dragonborn          |    7     |      2.175477 |     3.284818 |   1.620807 |   28.330795 |
|     Dragonroost Island      |    8     |      2.168983 |     2.481055 |   2.012947 |   28.194209 |
|       Drop Pop Candy        |    5     |      3.140505 |     4.713425 |   2.354045 |   54.592521 |
|    Escape From The City     |    5     |      2.345705 |     3.016402 |   2.010357 |   32.082174 |
|     Every Time We Touch     |    7     |      2.824879 |     4.111987 |   2.181326 |   44.584937 |
|Everybody Knows That You're I|    8     |      3.192041 |     5.122565 |   2.226779 |   56.373866 |
|Exit This Earth's Atomosphere|    10    |      6.132864 |    10.158991 |   4.119800 |  277.184889 |
|      Eye of the Tiger       |    5     |      2.198633 |     3.090857 |   1.752521 |   28.821639 |
|       Feel Good Inc.        |    4     |      2.915089 |     4.208534 |   2.268366 |   47.291717 |
|       Final Countdown       |    7     |      2.072469 |     2.696310 |   1.760548 |   26.218511 |
|          Firework           |    5     |      2.332461 |     3.512436 |   1.742473 |   31.778187 |
|         Flock Step          |    6     |      2.907634 |     3.423103 |   2.649899 |   47.063493 |
|        GALAXY DRIVE         |    10    |      5.728779 |     6.901615 |   5.142361 |  235.572390 |
|       GoPro Trombone        |    7     |      3.061745 |     4.299927 |   2.442654 |   51.952129 |
|      Grass Skirt Chase      |    6     |      2.535776 |     3.080990 |   2.263169 |   36.681608 |
|        Gravity Falls        |    4     |      2.322103 |     1.934995 |   2.515657 |   31.541911 |
|        Guile's Theme        |    6     |      2.674841 |     3.145744 |   2.439390 |   40.340778 |
|Harder, Better, Faster, Stron|    8     |      4.295105 |     4.702688 |   4.091313 |  116.366689 |
|           Hey Ya!           |    7     |      2.663837 |     3.891337 |   2.050088 |   40.041803 |
|Hide And Seek (Player Vocoder|    4     |      1.682882 |     1.825326 |   1.611660 |   19.197101 |
|         Hole In One         |    5     |      1.728280 |     1.917723 |   1.633559 |   19.942473 |
|        Hopes&Dreams         |    8     |      4.334760 |     4.564935 |   4.219673 |  119.076323 |
|      Little White Pony      |    8     |      3.986325 |     5.935246 |   3.011864 |   96.394634 |
| I'll Make a Man Out Of You  |    5     |      2.088771 |     2.617081 |   1.824616 |   26.545190 |
|        Industry Baby        |    7     |      2.161301 |     3.584734 |   1.449584 |   28.033234 |
|         In The End          |    5     |      2.543919 |     4.573639 |   1.529059 |   36.888840 |
|     Jump Up Super Star      |    7     |      2.992569 |     3.683977 |   2.646865 |   49.713010 |
|         Kass' Theme         |    5     |      2.130007 |     2.561025 |   1.914498 |   27.384198 |
|    Katamari on the Rocks    |    8     |      2.721586 |     3.889850 |   2.137454 |   41.629312 |
|            kids             |    6     |      1.928523 |     2.288237 |   1.748667 |   23.453395 |
|        Killer Queen         |    8     |      2.696773 |     2.839710 |   2.625305 |   40.941587 |
|       Checker Knights       |    8     |      3.546600 |     4.107588 |   3.266107 |   71.376283 |
|     Koi no Disco Queen      |    6     |      2.480699 |     1.646895 |   2.897601 |   35.302305 |
|          Leekspin           |    6     |      2.718134 |     2.966001 |   2.594201 |   41.533130 |
|  Life Will Change (inst.)   |    7     |      1.941216 |     2.899995 |   1.461827 |   23.688799 |
|        Live & Learn         |    9     |      2.141544 |     2.396468 |   2.014082 |   27.622235 |
|     Lonely Rolling Star     |    5     |      1.940660 |     2.082521 |   1.869729 |   23.678449 |
|          Loonboon           |    6     |      3.372220 |     3.191809 |   3.462426 |   62.946162 |
|      Mass Destruction       |    5     |      2.625808 |     2.434204 |   2.721609 |   39.021170 |
|        Mortal Kombat        |    7     |      4.488869 |     5.359362 |   4.053623 |  129.920569 |
|  Hall of the Mountain King  |    9     |      3.862510 |     5.501484 |   3.043024 |   88.944840 |
|        Mr. Blue Sky         |    7     |      2.233657 |     2.965627 |   1.867671 |   29.575484 |
|      Mystic Cave Zone       |    6     |      3.008912 |     3.801905 |   2.612415 |   50.235337 |
|          Nautilus           |    8     |      4.078750 |     5.370689 |   3.432780 |  102.163765 |
|      Night of Knights       |    10    |      6.743476 |     6.166113 |   7.032158 |  346.888930 |
|          Nightmare          |    7     |      2.453723 |     3.044033 |   2.158568 |   34.640787 |
|    Omori GOLDENVENGEANCE    |    8     |      2.159931 |     3.474966 |   1.502413 |   28.004598 |
|       Omori Stardust        |    6     |      1.631396 |     2.340975 |   1.276607 |   18.373171 |
|         Outro Song          |    5     |      1.854988 |     2.283106 |   1.640929 |   22.120423 |
|          Peer Gynt          |    8     |      3.978321 |     5.316772 |   3.309096 |   95.903404 |
|        Pink Dinosaur        |    6     |      3.310390 |     4.321233 |   2.804969 |   60.629405 |
|       Pink Yesterday        |    9     |      3.963570 |     3.612314 |   4.139198 |   95.001564 |
|       Waterfall Cave        |    6     |      2.644625 |     2.838506 |   2.547684 |   39.523748 |
|   Pokemon RSE Wild Battle   |    7     |      2.714030 |     2.474062 |   2.834014 |   41.418983 |
|        Remix 10 WII         |    8     |      3.591847 |     3.573632 |   3.600954 |   73.766076 |
|         Rockefeller         |    7     |      2.529460 |     4.036319 |   1.776031 |   36.521470 |
|       Samba do Brasil       |    4     |      2.722992 |     2.575656 |   2.796660 |   41.668545 |
|       Team Fortress 2       |    7     |      2.229162 |     2.222266 |   2.232610 |   29.477967 |
|         Buddy Holly         |    6     |      2.305862 |     2.979109 |   1.969239 |   31.173987 |
|        Sea Shanty 2         |    6     |      3.267888 |     3.439180 |   3.182241 |   59.074348 |
|Six Degrees Of Inner Turbulen|    10    |      5.661379 |     5.659754 |   5.662191 |  228.978423 |
|         SSBB Theme          |    3     |      1.628781 |     1.843186 |   1.521578 |   18.331909 |
|       Station Square        |    6     |      2.133561 |     2.458704 |   1.970990 |   27.457376 |
|     Still Alive (Radio)     |    6     |      2.389272 |     2.705484 |   2.231166 |   33.096984 |
|      Stop the Cavalry       |    6     |      2.990271 |     4.590393 |   2.190210 |   49.639879 |
|       End Theme - SMW       |    7     |      2.436292 |     3.621574 |   1.843651 |   34.218189 |
|         Take On Me          |    5     |      2.665484 |     3.646753 |   2.174850 |   40.086448 |
|         Tambourine          |    5     |      1.927604 |     2.330096 |   1.726358 |   23.436409 |
|           Tetris            |    6     |      2.435670 |     3.237039 |   2.034985 |   34.203175 |
|        The Airbuster        |    10    |      5.389548 |     7.117358 |   4.525643 |  203.384616 |
|I Really Really Really Like T|    6     |      2.030961 |     3.299511 |   1.396686 |   25.399360 |
|          Toot Toot          |    1     |      0.589689 |     0.804199 |   0.482434 |    5.481497 |
|     U.N. Owen was Her?      |    9     |      5.706817 |     6.850083 |   5.135184 |  233.412935 |
|Under the Sea (Instrumental) |    8     |      2.712478 |     3.282433 |   2.427500 |   41.375878 |
|        VOID Recorder        |    10    |      2.100290 |     1.630677 |   2.335096 |   26.777712 |
|             WAP             |    3     |      1.645665 |     2.559264 |   1.188866 |   18.599277 |
|      We Like To Party       |    4     |      4.436930 |     6.958313 |   3.176238 |  126.209852 |
|      We're Not Alright      |    7     |      3.138904 |     4.953559 |   2.231576 |   54.537864 |
|        Witch Doctor         |    8     |      4.139459 |     6.060643 |   3.178868 |  106.050271 |
|          yesterday          |    4     |      1.560797 |     1.927629 |   1.377381 |   17.279077 |
|         Yume Hanabi         |    9     |      4.499669 |     5.827846 |   3.835580 |  130.699270 |
+-----------------------------+----------+---------------+--------------+------------+-------------+
Report generated at Fri Feb 10 12:51:03 2023
Generated in 84.332202 seconds
```

> **NOTE:** Generation time has significantly increased from previous iteration due to chart generation. Chart generation does not happen server-side.

> **NOTE:** `TT Rating` is the base rating one would get for a play that is at **80%** of the chart's **maximum possible** score.

Charts are obtained from the [Trombone Champ Modding Discord](https://discord.gg/KVzKRsbetJ)

Join us in developing this algorithm further at the [TootTally Discord](https://discord.gg/9jQmVEDVTp)
