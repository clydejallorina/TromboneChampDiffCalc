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

Tests as of 2022-10-31T07:23:15+0:00

```
BIG SHOT (8): 5.251091171147717
Fly me to the moon (5): 3.0599958889675483
Friday Night (6): 4.34950469474435
Gourmet Race (8): 8.188087013764193
Megalovania (Trombone Champ Remix) (10): 8.74623378557948
Meikaruza (Instrumental) (10): 9.157682467728907
Rick AStley - Never Gonna Give You Up (7): 3.4486365721015377
Rainbow Tylenol (19): 8.616013394475639
RuneScapeSeaShanty2 (6): 6.802765318582144
Through the Fire and Flames (10): 9.50882653840689
We Are Number One (6): 5.50876705032371
```
