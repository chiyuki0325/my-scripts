#!/usr/bin/env python3
import pulsectl
import sys
from math import ceil, floor
import subprocess
import time

# Volume control utility for dickful Redmi Buds 3


def notify_send(right, left):
    global notify_id
    subprocess.run(
        [
            "notify-send",
            " 新音量:",
            f"真实音量:{right}%\n(左耳:{left}%)",
            "-i",
            "pavucontrol",
            "-a",
            "新音量:",
            "-e",
            "-t",
            "1000",
            '-r',
            # timestamp
            str(int(int(time.time())/5))[2:],
        ],
    )


pulse = pulsectl.Pulse("volume-control")

for card in pulsectl.Pulse("volume-control").card_list():
    if card.profile_active.name == "a2dp-sink-sbc":
        card_id = card.name.split(".")[1]
        for sink in pulse.sink_list():
            if card_id in sink.name:
                current_right_volume = ceil(floor(sink.volume.values[1] * 100) / 5) * 5
                match sys.argv[1]:
                    case "up":
                        new_right_volume = current_right_volume + 5
                    case "down":
                        new_right_volume = current_right_volume - 5
                new_left_volume = new_right_volume * 2
                sink.volume.values = (new_left_volume / 100, new_right_volume / 100)
                pulse.volume_set(sink, sink.volume)
                notify_send(new_right_volume, new_left_volume)
