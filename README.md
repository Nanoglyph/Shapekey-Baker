# ShapeKey Baker

Ever want to edit a mesh after you've made shape keys without messing the other shape keys up? Or apply your current shape key mix as your new basis while propogating that change down through all your shape keys?

Then welcome to Shape Key Baker!

(There's also an option to alphabetize the shape keys).

## Options

The addon has a couple utilities:

1. **Bake to ShapeKeys:** Apply the current blend of shape keys to the base shape, and propogate to all shape keys. If you wanted to edit your Basis, you would make new shapekey(s) for those edits then run this option. It'll work even if the base shape isn't named *Basis* (but it will rename it to *Basis*).
2. **Bake and Delete ShapeKeys:** Applies the current shape to the mesh and deletes all shape keys. Obviously, don't use it on a figure with shape keys for expressions or corrective shape keys.
3. **Alphabetize ShapeKeys:** Alphabetizes shape keys. Carefully programmed not to move the base shape at the top of the stack, even if it is not named *Basis*. Not really essential for the shapekey baking stuff, but still a useful utility, so I threw it in.
