import asyncio
import random

async def slow_drip(name):
    print(f"{name} is slipping in... let's see what you can handle.")
    await asyncio.sleep(random.randrange(1,7))
    print(f"{name}... oh, that was nice.")

async def main():
    print("Ready")
    await asyncio.gather(
        slow_drip("A"),
        slow_drip("B"),
        slow_drip("C"),
    )
    
asyncio.run(main())