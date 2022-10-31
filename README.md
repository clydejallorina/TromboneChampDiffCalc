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

Result Format: `[Name of Track] ([Mapper-Estimated Difficulty]): [Algorithm-Estimated Difficulty]`

Tests as of 2022-10-31T18:51:05+0:00

```
BIG SHOT (8): 6.038286955906907
Fly me to the moon (5): 3.7201824431972783
Freedom Dive (10): 21.137789604636367
Friday Night (6): 5.150487691155724
Gourmet Race (8): 8.618617539990563
Megalovania (Trombone Champ Remix) (10): 9.4847756839943
Meikaruza (Instrumental) (10): 11.105435258356682
Rick AStley - Never Gonna Give You Up (7): 4.458809456166826
Rainbow Tylenol (19): 10.605794491083223
RuneScapeSeaShanty2 (6): 7.23535349518896
Through the Fire and Flames (10): 10.554195862461635
We Are Number One (6): 5.9445152655941484
```
