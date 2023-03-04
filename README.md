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
|      1 2 Gourmet Race       |    7     |      2.500715 |     3.510221 |   1.995962 |   35.799079 |
|  21st century schizoid man  |    10    |      4.740608 |     3.372272 |   5.424776 |  148.713397 |
|          2nd Waltz          |    7     |      2.338759 |     3.245158 |   1.885560 |   31.922491 |
|   A Cruel Angel's Thesis    |    10    |      3.363027 |     3.460757 |   3.314161 |   62.597550 |
|   Adventures of Tanukichi   |    4     |      2.469996 |     3.410410 |   1.999790 |   35.038752 |
|           Africa            |    6     |      2.482168 |     3.166076 |   2.140214 |   35.338594 |
|     Alfonso Muskedunder     |    10    |      4.365614 |     5.631102 |   3.732869 |  121.207377 |
|   All I Want 4 Xmas Is U    |    7     |      2.239872 |     2.233825 |   2.242896 |   29.710729 |
|      Good Morning USA       |    5     |      2.448913 |     2.971018 |   2.187860 |   34.523782 |
|      Aquatic Ambience       |    7     |      3.938942 |     4.628461 |   3.594182 |   93.505993 |
|  Astronomia (Coffin Dance)  |    5     |      2.965605 |     4.771035 |   2.062890 |   48.860088 |
|      A Thousand Miles       |    4     |      1.908133 |     2.754068 |   1.485165 |   23.078536 |
|           Aurora            |    10    |      5.595966 |     6.316235 |   5.235831 |  222.673220 |
|       Autumn Mountain       |    2     |      1.600081 |     1.823342 |   1.488450 |   17.882851 |
|        Axe to Grind         |    9     |      2.280579 |     2.500948 |   2.170394 |   30.607382 |
|          Baby Park          |    8     |      5.118471 |     5.119678 |   5.117867 |  179.450195 |
|Bad Apple! (Cosmowave Remix) |    4     |      4.352410 |     6.388841 |   3.334195 |  120.292952 |
|          Bad Apple          |    7     |      3.784194 |     5.428021 |   2.962280 |   84.397001 |
|     Bad Piggies (hard)      |    10    |      5.215884 |     6.589539 |   4.529056 |  187.869244 |
|       Baggy Trousers        |    4     |      3.325425 |     4.805350 |   2.585463 |   61.186770 |
|         Baka Mitai          |    5     |      1.505706 |     1.666480 |   1.425318 |   16.452960 |
|            DotA             |    7     |      4.461427 |     5.833903 |   3.775189 |  127.952915 |
|      Battlerock Galaxy      |    7     |      1.580665 |     1.966356 |   1.387819 |   17.582884 |
|       Beethoven Virus       |    10    |      6.326260 |     6.348872 |   6.314955 |  298.368991 |
|   better call saul theme    |    8     |      2.311296 |     1.971341 |   2.481274 |   31.296740 |
|          BIG SHOT           |    8     |      3.291354 |     3.402844 |   3.235608 |   59.929157 |
|         Big Enough          |    8     |      2.321276 |     2.453884 |   2.254972 |   31.523093 |
|     Bill Nye (Chinese)      |    5     |      2.127572 |     2.717085 |   1.832815 |   27.334139 |
|        Blackout City        |    10    |      5.696584 |     7.166923 |   4.961415 |  232.410331 |
|           Blend W           |    7     |      2.851080 |     2.906142 |   2.823549 |   45.358849 |
|        Bloody Stream        |    7     |      2.564063 |     2.579327 |   2.556431 |   37.405207 |
|      Blue (Da Ba Dee)       |    6     |      2.723998 |     4.003561 |   2.084216 |   41.696617 |
|      Bohemian Rhapsody      |    7     |      2.094805 |     2.722692 |   1.780861 |   26.666815 |
|       Bomb Rush Blush       |    9     |      4.363496 |     5.781039 |   3.654725 |  121.060505 |
|         Breakout v2         |    8     |      3.877809 |     4.331220 |   3.651103 |   89.848091 |
|         BRING IT ON         |    9     |      3.290543 |     4.449979 |   2.710826 |   59.899487 |
|         BRODYQUEST          |    9     |      3.433688 |     2.922252 |   3.689406 |   65.596236 |
|    Calamari Inkantation     |    5     |      3.485403 |     3.226469 |   3.614871 |   68.211041 |
|        Cantina Band         |    6     |      3.192238 |     2.464637 |   3.556039 |   56.380766 |
|       Caramelldansen        |    6     |      2.919756 |     3.569282 |   2.594993 |   47.435037 |
| Carol of the Bells (metal)  |    5     |      3.421974 |     5.000652 |   2.632635 |   65.011563 |
|      Chariots Of Fire       |    5     |      1.851279 |     2.093773 |   1.730032 |   22.054559 |
|     Chemical Plant Zone     |    9     |      4.203833 |     4.245227 |   4.183135 |  110.255496 |
|       Chug Jug With U       |    7     |      3.042288 |     3.125324 |   3.000770 |   51.314849 |
|    Close in the Distance    |    3     |      1.137367 |     1.413283 |   0.999408 |   11.486906 |
|     Cyrus, the Scholar      |    3     |      1.754132 |     1.748485 |   1.756956 |   20.375009 |
|      Daddy! Daddy! Do!      |    5     |      2.561527 |     2.638439 |   2.523070 |   37.339900 |
|    The Dance of Eternity    |    10    |     11.484025 |    15.014492 |   9.718791 | 1180.594128 |
|        Dancing Queen        |    6     |      1.602850 |     2.420723 |   1.193914 |   17.925895 |
| Dedicated to MoonlightHard  |    10    |      3.710579 |     4.878184 |   3.126776 |   80.238003 |
|   Dedicated to Moonlight    |    6     |      2.198596 |     2.800970 |   1.897409 |   28.820845 |
|           Deja Vu           |    7     |      3.324726 |     4.093463 |   2.940357 |   61.160760 |
|      Deja Vu (Vocals)       |    7     |      3.324726 |     4.093463 |   2.940357 |   61.160760 |
|          Densmore           |    9     |      5.912571 |     5.551130 |   6.093292 |  254.056378 |
|          Detonate           |    6     |      2.358085 |     3.435264 |   1.819496 |   32.368211 |
|  Ding Dong Merrily on High  |    10    |      1.270528 |     1.097286 |   1.357149 |   13.178053 |
|        Disco Descent        |    7     |      1.919113 |     1.949140 |   1.904100 |   23.279890 |
|      dont stop me now       |    8     |      2.638924 |     3.223561 |   2.346606 |   39.370991 |
|         Double-Tap          |    3     |      1.077249 |     1.553365 |   0.839191 |   10.757836 |
|      Dracula's Castle       |    5     |      2.253176 |     2.168162 |   2.295683 |   30.001673 |
|         dragonborn          |    7     |      1.992146 |     2.949853 |   1.513293 |   24.649526 |
|     Dragonroost Island      |    8     |      2.069428 |     2.228053 |   1.990115 |   26.157882 |
|       Drop Pop Candy        |    5     |      2.927937 |     4.232781 |   2.275515 |   47.686994 |
|    Escape From The City     |    5     |      2.202594 |     2.708809 |   1.949486 |   28.906192 |
|     Every Time We Touch     |    7     |      2.695546 |     3.692673 |   2.196982 |   40.907798 |
|Everybody Knows That You're I|    8     |      2.779794 |     4.234535 |   2.052424 |   43.276303 |
|Exit This Earth's Atomosphere|    10    |      5.411635 |     8.642121 |   3.796392 |  205.404519 |
|      Eye of the Tiger       |    5     |      2.117198 |     2.775671 |   1.787961 |   27.121614 |
|       Feel Good Inc.        |    4     |      2.738432 |     3.779375 |   2.217960 |   42.101079 |
|  Field of Hopes and Dreams  |    6     |      2.186894 |     2.540467 |   2.010107 |   28.572048 |
|       Final Countdown       |    7     |      1.900467 |     2.421358 |   1.640022 |   22.938656 |
|           Finale            |    7     |      3.647942 |     3.033801 |   3.955013 |   76.787502 |
|          Firework           |    5     |      2.144368 |     3.101942 |   1.665581 |   27.680715 |
|         Flock Step          |    6     |      2.653548 |     3.068901 |   2.445871 |   39.763725 |
|         Fly Or Die          |    10    |      5.186364 |     5.775834 |   4.891629 |  185.296425 |
|     Francis Forever v2      |    2     |      1.563879 |     2.284450 |   1.203593 |   17.325994 |
| Battle! (Galar Gym Leader)  |    9     |      3.654286 |     4.381575 |   3.290641 |   77.133279 |
|        GALAXY DRIVE         |    10    |      5.038457 |     5.747163 |   4.684104 |  172.687105 |
|         Gandalf Sax         |    5     |      2.003163 |     2.354271 |   1.827609 |   24.860778 |
|     Gang-Plank Galleon      |    10    |      4.488715 |     6.558910 |   3.453617 |  129.909458 |
|       GoPro Trombone        |    7     |      2.849306 |     3.861449 |   2.343235 |   45.306140 |
|      Grass Skirt Chase      |    6     |      2.421395 |     2.766810 |   2.248688 |   33.860018 |
|        Gravity Falls        |    4     |      2.092134 |     1.737677 |   2.269362 |   26.612925 |
|    Green Hornet (Theme)     |    10    |      5.332651 |     6.823168 |   4.587393 |  198.229856 |
|        Guile's Theme        |    6     |      2.531103 |     2.824962 |   2.384174 |   36.563083 |
|Harder, Better, Faster, Stron|    8     |      3.707055 |     3.900108 |   3.610529 |   80.041763 |
|          he blåhaj          |    2     |      1.654402 |     1.504565 |   1.729321 |   18.738573 |
|           Hey Ya!           |    7     |      2.474131 |     3.494524 |   1.963935 |   35.140400 |
|Hide And Seek (Player Vocoder|    4     |      1.557791 |     1.634070 |   1.519652 |   17.233386 |
|         Hole In One         |    5     |      1.620409 |     1.722166 |   1.569530 |   18.200220 |
|        Hopes&Dreams         |    8     |      4.123675 |     4.099433 |   4.135796 |  105.032378 |
|      Little White Pony      |    8     |      3.778759 |     5.302983 |   3.016647 |   84.086121 |
|        House of Fun         |    3     |      2.501626 |     3.809672 |   1.847603 |   35.821810 |
| I'll Make a Man Out Of You  |    5     |      1.897435 |     2.246020 |   1.723143 |   22.883488 |
|          Ichibanka          |    4     |      3.037968 |     3.903044 |   2.605430 |   51.174164 |
|        Industry Baby        |    7     |      2.002323 |     3.219187 |   1.393892 |   24.844637 |
|         In The End          |    5     |      1.880668 |     3.298687 |   1.171659 |   22.580007 |
|     Jump Up Super Star      |    7     |      2.587146 |     3.035839 |   2.362799 |   38.003421 |
|         Kass' Theme         |    5     |      1.898183 |     2.299868 |   1.697340 |   22.897079 |
|    Katamari on the Rocks    |    8     |      2.656422 |     3.493188 |   2.238038 |   39.841252 |
|            kids             |    6     |      1.839980 |     2.054898 |   1.732521 |   21.854720 |
|        Killer Queen         |    8     |      2.347334 |     2.381018 |   2.330491 |   32.119692 |
|       Checker Knights       |    8     |      3.295155 |     3.688723 |   3.098371 |   60.068503 |
|         Kiseki knot         |    8     |      2.399557 |     3.407296 |   1.895687 |   33.339902 |
|     Koi no Disco Queen      |    6     |      2.069609 |     1.478955 |   2.364936 |   26.161500 |
|       Kyouki Ranbu v2       |    10    |      8.489228 |    10.160448 |   7.653619 |  592.502277 |
|          Leekspin           |    6     |      2.540463 |     2.663548 |   2.478921 |   36.800795 |
|          Let it Go          |    5     |      1.742576 |     2.175112 |   1.526309 |   20.180929 |
|  Life Will Change (inst.)   |    7     |      1.834639 |     2.604272 |   1.449823 |   21.760686 |
|       Like a Surgeon        |    2     |      1.969368 |     2.253825 |   1.827140 |   24.216636 |
|        Live & Learn         |    9     |      2.002864 |     2.152092 |   1.928250 |   24.855024 |
|     Lonely Rolling Star     |    5     |      1.784286 |     1.870159 |   1.741350 |   20.887081 |
|          Loonboon           |    6     |      3.021473 |     2.866329 |   3.099045 |   50.639611 |
|         lumivoyage          |    8     |      7.063870 |     7.779913 |   6.705848 |  386.784248 |
|      Mass Destruction       |    5     |      2.257602 |     2.185980 |   2.293413 |   30.098910 |
| Moonlight Densetsu TV Size  |    7     |      2.713824 |     3.640664 |   2.250405 |   41.413276 |
|        Mortal Kombat        |    7     |      3.790372 |     4.360986 |   3.505064 |   84.751123 |
|  Hall of the Mountain King  |    9     |      3.562804 |     4.940478 |   2.873967 |   72.227265 |
|        Mr. Blue Sky         |    7     |      2.078452 |     2.647739 |   1.793809 |   26.338084 |
|      Mystic Cave Zone       |    6     |      2.899602 |     3.414211 |   2.642297 |   46.818529 |
|          Nautilus           |    8     |      3.572040 |     4.778617 |   2.968751 |   72.714730 |
|      Night of Knights       |    10    |      6.229989 |     5.537332 |   6.576318 |  287.720706 |
|          Nightmare          |    7     |      2.345529 |     2.733622 |   2.151482 |   32.078106 |
|         Horse Cock          |    5     |      1.964947 |     2.963571 |   1.465635 |   24.133213 |
|         Oh Klahoma          |    6     |      1.966435 |     2.171052 |   1.864126 |   24.161258 |
|           Omoikou           |    8     |      2.479451 |     3.384058 |   2.027148 |   35.271498 |
|    Omori GOLDENVENGEANCE    |    8     |      1.968231 |     3.089287 |   1.407702 |   24.195148 |
|       Omori Stardust        |    6     |      1.504542 |     2.102258 |   1.205684 |   16.435769 |
|      Once Upon A Time       |    3     |      1.532919 |     1.776980 |   1.410889 |   16.858069 |
|          Our House          |    3     |      2.315580 |     3.338111 |   1.804314 |   31.393756 |
|         Outro Song          |    5     |      1.722566 |     2.050290 |   1.558705 |   19.847667 |
|Ov Sacrament and Sincest (Bus|    10    |     12.738751 |    16.439861 |  10.888196 | 1492.498748 |
|         Pathfinder          |    3     |      1.977712 |     2.004111 |   1.964513 |   24.374599 |
|          Peer Gynt          |    8     |      3.706652 |     4.774602 |   3.172677 |   80.019308 |
|         Petit Love          |    8     |      3.356058 |     4.261350 |   2.903411 |   62.334258 |
|            phony            |    7     |      4.311839 |     4.781752 |   4.076882 |  117.506090 |
|        Pink Dinosaur        |    6     |      3.115600 |     3.880582 |   2.733108 |   53.746951 |
|       Pink Yesterday        |    9     |      3.338715 |     3.114156 |   3.450994 |   61.682635 |
|       Waterfall Cave        |    6     |      2.414764 |     2.549054 |   2.347620 |   33.701475 |
|   Pokemon RSE Wild Battle   |    7     |      2.549479 |     2.221773 |   2.713332 |   37.030838 |
|       RED HEART 8-bit       |    7     |      3.250333 |     4.438610 |   2.656195 |   58.440877 |
|        Remix 10 WII         |    8     |      3.198020 |     3.209216 |   3.192422 |   56.583308 |
|      Renai Circulation      |    6     |      2.935565 |     3.138972 |   2.833862 |   47.922843 |
|      Reporting Balloon      |    5     |      0.926515 |     1.596435 |   0.591555 |    9.014684 |
|         Rockefeller         |    7     |      2.419727 |     3.624722 |   1.817229 |   33.820070 |
|      Run Away With Me       |    6     |      2.120317 |     2.733978 |   1.813486 |   27.185390 |
|       Samba do Brasil       |    4     |      2.494759 |     2.313008 |   2.585634 |   35.650722 |
|       Team Fortress 2       |    7     |      2.011544 |     1.995654 |   2.019489 |   25.022325 |
|         Buddy Holly         |    6     |      2.057396 |     2.490007 |   1.841090 |   25.918958 |
|        Sea Shanty 2         |    6     |      2.919433 |     3.088475 |   2.834912 |   47.425106 |
|     Seaside Rendezvous      |    8     |      2.523155 |     3.218498 |   2.175483 |   36.362104 |
|     SHIJOSHUGI ADTRUCK      |    7     |      5.206164 |     6.217395 |   4.700549 |  187.020101 |
|Six Degrees Of Inner Turbulen|    10    |      3.877192 |     3.684169 |   3.973704 |   89.811595 |
|             666             |    10    |      5.872064 |     8.035612 |   4.790290 |  249.919208 |
|         SSBB Theme          |    3     |      1.510588 |     1.655230 |   1.438267 |   16.525220 |
|Stardew Valley OST - Stardew |    3     |      1.309443 |     1.482267 |   1.223032 |   13.693433 |
|       Station Square        |    6     |      2.079226 |     2.207982 |   2.014849 |   26.353581 |
|     Still Alive (Radio)     |    6     |      2.097954 |     2.274761 |   2.009550 |   26.730440 |
|      Stop the Cavalry       |    6     |      2.379487 |     3.442715 |   1.847873 |   32.867061 |
|       End Theme - SMW       |    7     |      2.273281 |     3.206193 |   1.806826 |   30.445232 |
|   Supermassive Black Hole   |    4     |      1.764995 |     2.440792 |   1.427097 |   20.558539 |
|         Take On Me          |    5     |      2.396685 |     3.274881 |   1.957587 |   33.271935 |
|         Tambourine          |    5     |      1.856690 |     2.092488 |   1.738791 |   22.150687 |
|           Tapioca           |    8     |      3.970843 |     5.354481 |   3.279024 |   95.445642 |
|         Terrasphere         |    8     |      4.504542 |     5.305394 |   4.104115 |  131.051418 |
|           Tetris            |    6     |      2.131647 |     2.906947 |   1.743998 |   27.417955 |
|         The Legend          |    7     |      1.892329 |     2.354860 |   1.661064 |   22.790786 |
|        The Airbuster        |    10    |      3.964955 |     4.931605 |   3.481629 |   95.086029 |
|         The Extreme         |    5     |      4.298752 |     5.035986 |   3.930135 |  116.614520 |
|I Really Really Really Like T|    6     |      1.903519 |     2.963048 |   1.373755 |   22.994281 |
| Fantastic Tohno (Touhou 7)  |    7     |      3.576833 |     4.657193 |   3.036653 |   72.968428 |
|          Toot Toot          |    1     |      0.544485 |     0.722192 |   0.455632 |    5.037576 |
|  Triple the Threat (Hard)   |    9     |      3.619462 |     5.383735 |   2.737325 |   75.245365 |
|     U.N. Owen was Her?      |    9     |      4.310099 |     5.096047 |   3.917125 |  117.387378 |
|         Ultraman OP         |    4     |      1.893058 |     2.545952 |   1.566610 |   22.803992 |
|        UltraSeven OP        |    4     |      1.307126 |     1.640866 |   1.140257 |   13.662468 |
|          Undertale          |    4     |      1.793793 |     2.392471 |   1.494454 |   21.050237 |
|Under the Sea (Instrumental) |    8     |      2.540659 |     2.947712 |   2.337133 |   36.805785 |
|      VANESSA (Busted)       |    10    |      9.491906 |     8.694409 |   9.890654 |  765.442840 |
|     Mario Masturbation      |    8     |      3.641107 |     5.711434 |   2.605943 |   76.415861 |
|        VOID Recorder        |    10    |      1.745807 |     1.464391 |   1.886514 |   20.235060 |
|             WAP             |    3     |      1.554491 |     2.266138 |   1.198667 |   17.183301 |
|      We Like To Party       |    4     |      4.091395 |     6.248749 |   3.012718 |  102.966958 |
|      We're Not Alright      |    7     |      2.799256 |     4.367809 |   2.014980 |   43.837643 |
|         Angel Wakes         |    7     |      4.356535 |     3.816202 |   4.626702 |  120.578260 |
|          whiplash           |    9     |      3.563992 |     2.628199 |   4.031889 |   72.289872 |
|         Will Power          |    7     |      2.279185 |     4.306857 |   1.265350 |   30.576373 |
|       Wings of Piano        |    7     |      3.499508 |     3.814412 |   3.342055 |   68.933712 |
|        Witch Doctor         |    8     |      3.677750 |     5.011318 |   3.010965 |   78.419414 |
|   Would You Be Impressed?   |    8     |      3.112811 |     4.016080 |   2.661177 |   53.652895 |
|          yesterday          |    4     |      1.474076 |     1.731062 |   1.345583 |   15.989248 |
|         Yume Hanabi         |    9     |      3.819617 |     4.653737 |   3.402557 |   86.438283 |
|         Yume Hanabi         |    9     |      3.819617 |     4.653737 |   3.402557 |   86.438283 |
+-----------------------------+----------+---------------+--------------+------------+-------------+
Report generated at Sat Mar  4 06:30:09 2023
Generated in 201.917036 seconds
```

> **NOTE:** Generation time has significantly increased from previous iteration due to chart generation. Chart generation does not happen server-side.

> **NOTE:** `TT Rating` is the base rating one would get for a play that is at **80%** of the chart's **maximum possible** score.

Charts are obtained from the [Trombone Champ Modding Discord](https://discord.gg/KVzKRsbetJ)

Join us in developing this algorithm further at the [TootTally Discord](https://discord.gg/9jQmVEDVTp)
