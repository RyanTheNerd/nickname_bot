import asyncio
from utils import parse_request
import json

class Animation:
    def __init__(self, trigger, frame_delay, frames, iterations, monospaced=False):
        self.monospaced = monospaced
        self.trigger = trigger
        self.frames = frames
        self.frame_delay = frame_delay
        self.iterations = iterations
    
    async def animate(self, channel):
        original = await channel.send(self.frames[0])
        for iteration in range(self.iterations):
            for frame in self.frames:
                if self.monospaced:
                    frame = '```' + frame + '```'
                await original.edit(content = frame)
                await asyncio.sleep(self.frame_delay)

    async def run(self, message):
        user, command, arg = parse_request(message)
        if command == self.trigger:
            await self.animate(message.channel)




smile_wink_frames = [
    ":smiley:",
    ":wink:",
]
sad_cry_frames = [
    ":frowning:",
    ":sob:",
]

with open('anim_frames.json', 'r') as anim_frames_file:
    anim_frames = json.load(anim_frames_file)


animations = [
    Animation("smile", 1, smile_wink_frames, 5),
    Animation("cry", 1, sad_cry_frames, 5),
    Animation("porn", 1, anim_frames, 1, monospaced = True),
]

async def run_animations(message):
    for animation in animations:
        await animation.run(message)


