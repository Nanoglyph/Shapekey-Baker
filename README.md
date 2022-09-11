# ShapeKey Baker

Blender addon: Bake the current blend of shapekeys down to the basis and propogate to all shapekeys.

The addon has a couple utilities:

1. **Bake All:** More or less the same as the script above. Apply the current blend of shape keys to the base shape, and all shapekeys. It'll work even if the base shape isn't named *Basis* but it will rename it to *Basis*.
2. **Bake and delete:** Applies the current shape to the mesh and deletes all shape keys. Obviously, don't use it on a figure with shape keys for expressions or corrective shape keys.
3. **Alphabetize shape keys:** Self-explanatory. Carefully programmed not to move the base shape at the top of the stack, even if it is not named *Basis* anymore. Not really essential for the shapekey baking stuff, but still a useful utility, so I threw it in.
