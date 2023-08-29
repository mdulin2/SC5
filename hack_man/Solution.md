# hack-man: solution

There are many ways to solve this problem. For example, you could get rid of collisions, so that you float through the middle wall.

However, the intended approach was to put a breakpoint inside the player's position update logic, then to set the player's position to the location of the chest. In particular, line 993 of `index.js` (using the browser's development console), which is inside of the `update` function of the player object. This gets called by the game engine whenever the player object's position is updated.

The relevant code is here:
```
update:function(){
    var coord = this.coord;
    if(!coord.offset){
        ... <omitted for brevity's sake> ...
```

Once the program breaks at that point, update the player's position to where the chest is.

Overall, here are the steps:

1. Start the game by pressing enter.

2. Move towards the chest in the middle. Position yourself such that you are on the left side of the box in the middle, facing the chest. You should not be moving at this point since you are facing a wall.

3. Pause the game once you're near the chest by pressing space.

4. Open the browser's dev tools. Put a breakpoint on line 993.

5. On the right (in Chrome), click "Closure" in the scope tab and select `player`. Then, scroll down to the `x` field and set it to 315.

6. Get rid of the breakpoint.

7. Resume the game by pressing space again.

8. At this point, the flag is revealed.

It may be easier to eat the powerup so that the ghosts run away, especially while trying to move towards the chest.
