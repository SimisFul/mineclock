# mineclock

This is a clock meant to be used with Minecraft: Pi Edition. 
It is compatible with the original unmodified version of the game as well as modified versions
which also support the Python API included in Minecraft: Pi Edition.

This clock aims to be fun to look at with multiple different transition animations for every number change.
Unfortunately, this script must be run as root since almost all animations depend on keyboard and mouse inputs 
and root is required to create those virtual devices.

I have made some custom textures to enhance the visual appearance of the clock, making certain blocks
and items more/fully transparent and to hide the hud. 
These textures are not required and the clock will look fine without them.

# Requirements
The following python modules are required: python-uinput minecraftstuff mcpi

The provided glass map is important as it contains small builds that I call "models"
which can be used for transition animations.
