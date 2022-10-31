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

Tests as of 2022-10-31T16:29:41+0:00

```
BIG SHOT (8): 4.115615173217203
Fly me to the moon (5): 1.9212268355661932
Freedom Dive (10): 20.25539628814488
Friday Night (6): 2.9372382285545635
Gourmet Race (8): 7.889309366286308
Megalovania (Trombone Champ Remix) (10): 9.01770788203087
Meikaruza (Instrumental) (10): 10.102187190659391
Rick AStley - Never Gonna Give You Up (7): 2.2188284340056206
Rainbow Tylenol (19): 7.197992624657065
RuneScapeSeaShanty2 (6): 6.767920196237722
Through the Fire and Flames (10): 9.948409479564312
We Are Number One (6): 4.820307625487056
```
