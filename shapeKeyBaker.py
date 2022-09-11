bl_info = {
    "name": "ShapeKey Baker",
    "author": "Nanoglyph",
    "version": (1, 1),
    "blender": (3, 1, 2),
    "location": "View3D > Toolshelf > Tools",
    "description": "Apply the current blend of shape keys to the basis, and all shapekeys",
    "warning": "",
    "doc_url": "",
    "category": "Mesh",
}

import bpy

"""UI SETUP"""
class SKeyBakerMainPanel(bpy.types.Panel):
    """Creates a Panel"""
    bl_label = 'ShapeKey Baker'
    bl_idname = 'SKEYBAKER_PT_MAINPANEL'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text= 'ShapeKey baking utilities')
        """Bake to Shape Keys"""
        row = layout.row()
        row.operator('shapekey.bakeall_operator')
        
        """Bake And Delete Shape Keys"""
        row = layout.row()
        row.operator('shapekey.bakedelete_operator')
        
        """Alphabetize Shape Keys"""
        row = layout.row()
        row.label(text= 'Other utilities')
        row = layout.row()
        row.operator('shapekey.alphabetize_all_operator')

"""CREATE SHAPEKEY OPERATOR TYPE BAKE ALL"""
class SHAPEKEY_OT_BAKEALL(bpy.types.Operator):
    # Button label and operator ID
    bl_label = 'Bake to ShapeKeys'
    bl_idname = 'shapekey.bakeall_operator'

    def execute(self, context):
        # Get selected object and shapekeys
        ob = bpy.context.object
        try:
            skeys = ob.data.shape_keys.key_blocks
        except:
            print("\nNo shape keys found. Cancelling operation")
            return {'FINISHED'}

        # Terminate if Basis is the only key
        if len(skeys) <= 2:
            print("\nNothing to bake. Cancelling operation\n")
            return {'FINISHED'}

        # Utility variables
        oldBasis = 'OriginalBasis' # New name for orinal Basis
        subD = False
        suffix = '__axpxp'
        count = 0
        currentSK = ob.active_shape_key.name
        
        """PREP WORK"""
        # Rename 'OriginalBasis' if it already exists
        if bool(skeys.get(oldBasis)):
            skeys.get(oldBasis).name = oldBasis + '.Older'
                
        # Disable subdivision for performance, if it exists
        try:
            if ob.modifiers['Subdivision'].show_viewport == True:
                subD = True
                ob.modifiers['Subdivision'].show_viewport = False
        except:
            print('')
            
        # Rename Basis, whether it is at the top of the stack or not
        ob.active_shape_key_index = 0
        ob.active_shape_key.name = oldBasis
        try:
            skeys.get('Basis').name = 'Basis.Older'
        except:
            print('')
        
        """BAKE NEW BASIS FROM MIX"""
        # Create new shape from mix and zero out all shape keys
        ob.shape_key_add(name = str('Basis'), from_mix=True)
        bpy.ops.object.shape_key_clear()
        
        # Enable and set active shape key to index of Basis
        # Then move to index 0
        skeys.get('Basis').value = 1
        ob.active_shape_key_index = skeys.find('Basis')
        bpy.ops.object.shape_key_move(type='TOP')
        bpy.ops.object.shape_key_move(type='UP')
        # Zero out all shape keys
        bpy.ops.object.shape_key_clear()
            
        """ BAKE NEW SHAPE KEYS """
        for key in skeys:
            if  key.name != 'Basis' and key.name != oldBasis:
                    
                # Prevent infinite loop by screening out "__apxpx" shape keys
                if suffix not in key.name:
                    count+=1
                    print("Key " + str(count) + ": " + key.name)
                        
                    # Preserve current value max value
                    # And set max to 1 to ensure new key replicates current behavior
                    kmax = key.slider_max
                    key.slider_max = 1
                        
                    # Enable shape key and create new shape key from mix
                    key.value = 1
                    ob.shape_key_add(name=key.name + suffix, from_mix=True)
                    
                    # Copy min/max rang values
                    skeys.get(key.name + suffix).slider_max = kmax
                    skeys.get(key.name + suffix).slider_min = key.slider_min

                    # Zero out all shape keys
                    bpy.ops.object.shape_key_clear()    

        """ CLEAN UP """
        # Delete original keys and remove temp suffix from new keys
        for key in skeys:
            if  key.name != 'Basis' and key.name != oldBasis:
                if suffix not in key.name:
                    ob.active_shape_key_index = skeys.find(key.name)
                    bpy.ops.object.shape_key_remove()
                else:
                    key.name = key.name.replace(suffix,'')

        # Set Old Basis relative to new Basis
        skeys.get(oldBasis).relative_key = skeys.get('Basis')
            
        # This is hacky, but for some reason if we don't toggle edit mode
        # the mesh reverts to the original Basis if we don't.
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        try:
            # Go to user's current shapekey
            ob.active_shape_key_index = skeys.find(currentSK)
        except:
            print('')
        
        # Re-enable subdvivision if it had been enabled
        if subD == True:
            ob.modifiers['Subdivision'].show_viewport = True

        return {'FINISHED'}

"""CREATE SHAPEKEY OPERATOR TYPE BAKE AND DELETE"""
class SHAPEKEY_OT_BAKEDELETE(bpy.types.Operator):
    # Button label and operator ID
    bl_label = 'Bake and Delete ShapeKeys'
    bl_idname = 'shapekey.bakedelete_operator'

    def execute(self, context):
        # Get selected object and shapekeys
        ob = bpy.context.object
        try:
            skeys = ob.data.shape_keys.key_blocks
        except:
            print("\nNo shape keys found. Cancelling operation")
            return {'FINISHED'}

        basisName = 'NewBasisNameTempDel'

        """PREP NEW BASIS"""
        # Create new shape from mix
        ob.shape_key_add(name = str(basisName), from_mix=True)
        # Zero out all shape keys
        bpy.ops.object.shape_key_clear()
        
        """MAKE NEW BASIS"""
        # Enable and set active shape key to index of Basis
        # Then move to index 0
        skeys.get(basisName).value = 1
        ob.active_shape_key_index = skeys.find(basisName)
        bpy.ops.object.shape_key_move(type='TOP')
        bpy.ops.object.shape_key_move(type='UP')

        """CLEAN UP"""
        # Toggle edit mode to stick the change
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        # Clear shape keys from mesh
        ob.shape_key_clear()

        return {'FINISHED'}

"""CREATE SHAPEKEY OPERATOR TYPE ALPHABETIZE"""
class SHAPEKEY_OT_ALPHABETIZE(bpy.types.Operator):
    # Button label and operator ID
    bl_label = 'Alphabetize ShapeKeys'
    bl_idname = 'shapekey.alphabetize_all_operator'

    def execute(self, context):     
        ob = bpy.context.object
        try:
            skeys = ob.data.shape_keys.key_blocks
        except:
            print("\nNo shape keys found. Cancelling operation\n")
            return {'FINISHED'}
        basisName = 'Basis'
        currentSK = ob.active_shape_key.name
        
        """"PREP WORK"""
        # Get name of key at top of stack (usually Basis)
        ob.active_shape_key_index = 0
        basisName = ob.active_shape_key.name
        
        """DISABLE SUBDIVISION FOR PERFORMANCE"""
        subD = False
        try:
            if ob.modifiers['Subdivision'].show_viewport == True:
                subD = True
                ob.modifiers['Subdivision'].show_viewport = False
        except:
            print('\n')

        # Sort keys by name
        skey_names = sorted(skeys.keys(), key=lambda v: v.upper())
        
        """ALPHABETIZE SHAPE KEYS"""
        for name in skey_names:
            # Protect Basis' location!
            if  name != basisName:
                index = skeys.keys().index(name)
                ob.active_shape_key_index = index
                bpy.ops.object.shape_key_move(type='BOTTOM')
        
        """CLEAN UP"""
        # Go to user's current shapekey
        ob.active_shape_key_index = skeys.find(currentSK)
        # Re-enable subdvivision if it had been enabled
        if subD == True:
            ob.modifiers['Subdivision'].show_viewport = True
        
        return {'FINISHED'}

        
def register():
    bpy.utils.register_class(SKeyBakerMainPanel)
    bpy.utils.register_class(SHAPEKEY_OT_BAKEALL)
    bpy.utils.register_class(SHAPEKEY_OT_BAKEDELETE)
    bpy.utils.register_class(SHAPEKEY_OT_ALPHABETIZE)

def unregister():
    bpy.utils.unregister_class(SKeyBakerMainPanel)
    bpy.utils.unregister_class(SHAPEKEY_OT_BAKEALL)
    bpy.utils.unregister_class(SHAPEKEY_OT_BAKEDELETE)
    bpy.utils.unregister_class(SHAPEKEY_OT_ALPHABETIZE)

if __name__ == '__main__':
    register()