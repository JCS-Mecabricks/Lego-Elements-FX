bl_info = {
    "name": "LEGO ElementsFX",
    "author": "JCS",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > LEGO ElementsFX",
    "description": "Adds element effects to LEGO pieces",
    "category": "Object",
}

import bpy
import os


def append_object(blend_path, obj_name):
    inner_path = "Object"
    directory = os.path.join(blend_path, inner_path) + os.sep
    if obj_name not in bpy.data.objects:
        bpy.ops.wm.append(
            filepath=os.path.join(directory, obj_name),
            directory=directory,
            filename=obj_name,
            link=False
        )
    return bpy.data.objects.get(obj_name)


class WaterOperator(bpy.types.Operator):
    bl_idname = "water.1"
    bl_label = "Water Operator"

    def execute(self, context):
        selected = context.selected_objects
        if not selected:
            self.report({'ERROR'}, "No objects selected")
            return {'CANCELLED'}

        blend_path = os.path.join(os.path.dirname(bpy.data.filepath), "assets", "element_assets.blend")
        obj_ref = append_object(blend_path, "Raindrop")
        if obj_ref is None:
            self.report({'ERROR'}, "Could not load Raindrop")
            return {'CANCELLED'}

        for obj in selected:
            bpy.context.view_layer.objects.active = obj
            psys = obj.modifiers.new(name="ParticleSystem", type='PARTICLE_SYSTEM').particle_system
            old_settings = psys.settings
            new_settings = bpy.data.particles.new(name=f"{obj.name}_RaindropSettings")
            psys.settings = new_settings
            bpy.data.particles.remove(old_settings)

            s = psys.settings
            s.type = 'HAIR'
            s.distribution = 'RAND'
            s.render_type = 'OBJECT'
            s.instance_object = obj_ref

        return {'FINISHED'}


class FireOperator(bpy.types.Operator):
    bl_idname = "fire.1"
    bl_label = "Fire Operator"

    def execute(self, context):
        selected = context.selected_objects
        if not selected:
            self.report({'ERROR'}, "No objects selected")
            return {'CANCELLED'}

        blend_path = os.path.join(os.path.dirname(bpy.data.filepath), "assets", "element_assets.blend")
        obj_ref = append_object(blend_path, "Fireflies")
        if obj_ref is None:
            self.report({'ERROR'}, "Could not load Fireflies")
            return {'CANCELLED'}

        for obj in selected:
            bpy.context.view_layer.objects.active = obj
            psys = obj.modifiers.new(name="ParticleSystem", type='PARTICLE_SYSTEM').particle_system
            old_settings = psys.settings
            new_settings = bpy.data.particles.new(name=f"{obj.name}_FirefliesSettings")
            psys.settings = new_settings
            bpy.data.particles.remove(old_settings)

            s = psys.settings
            s.physics_type = 'NEWTON'
            s.type = 'EMITTER'
            s.count = 80
            s.frame_start = 1
            s.frame_end = 1
            s.lifetime = 50
            s.particle_size = 0.22
            s.render_type = 'OBJECT'
            s.instance_object = obj_ref

        return {'FINISHED'}


class EarthOperator(bpy.types.Operator):
    bl_idname = "earth.1"
    bl_label = "Earth Operator"

    def execute(self, context):
        selected = context.selected_objects
        if not selected:
            self.report({'ERROR'}, "No objects selected")
            return {'CANCELLED'}

        blend_path = os.path.join(os.path.dirname(bpy.data.filepath), "assets", "element_assets.blend")
        obj_ref = append_object(blend_path, "Leaf")
        if obj_ref is None:
            self.report({'ERROR'}, "Could not load Leaf")
            return {'CANCELLED'}

        for obj in selected:
            bpy.context.view_layer.objects.active = obj
            psys = obj.modifiers.new(name="ParticleSystem", type='PARTICLE_SYSTEM').particle_system
            old_settings = psys.settings
            new_settings = bpy.data.particles.new(name=f"{obj.name}_LeafSettings")
            psys.settings = new_settings
            bpy.data.particles.remove(old_settings)

            s = psys.settings
            s.physics_type = 'NEWTON'
            s.type = 'EMITTER'
            s.count = 10
            s.particle_size = 0.45
            s.frame_start = 1
            s.frame_end = 1
            s.lifetime = 50
            s.render_type = 'OBJECT'
            s.instance_object = obj_ref

        return {'FINISHED'}


def append_object(blend_path, obj_name):
    if obj_name in bpy.data.objects:
        return bpy.data.objects.get(obj_name)

    with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
        if obj_name in data_from.objects:
            data_to.objects = [obj_name]
        else:
            return None

    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj)
    return data_to.objects[0] if data_to.objects else None



class AirOperator(bpy.types.Operator):
    bl_idname = "air.1"
    bl_label = "Air Operator"

    def execute(self, context):
        selected = context.selected_objects
        if not selected:
            self.report({'ERROR'}, "No objects selected")
            return {'CANCELLED'}
        blend_path = os.path.join(
            os.path.dirname(bpy.data.filepath),
            "assets",
            "element_assets.blend"
        )

        collection_ref = append_collection(blend_path, "Dust Particles")
        if not collection_ref:
            self.report({'ERROR'}, "Could not load Dust Particles")
            return {'CANCELLED'}
        for obj in selected:
            bpy.context.view_layer.objects.active = obj
            psys = obj.modifiers.new(name="ParticleSystem", type='PARTICLE_SYSTEM').particle_system
            old_settings = psys.settings
            new_settings = bpy.data.particles.new(name=f"{obj.name}_DustSettings")
            psys.settings = new_settings
            bpy.data.particles.remove(old_settings)

            s = psys.settings
            s.type = 'EMITTER'
            s.emit_from = 'VOLUME'
            s.count = 200
            s.particle_size = 1
            s.frame_start = 1
            s.frame_end = 1
            s.lifetime = 250
            s.lifetime_random = 0.6
            s.rotation_factor_random = 0.1
            s.use_dynamic_rotation = True
            s.size_random = 1
            s.effector_weights.gravity = 0
            s.render_type = 'COLLECTION'
            s.instance_collection = collection_ref
        return {'FINISHED'}

def append_collection(blend_path, collection_name):
    if collection_name in bpy.data.collections:
        return bpy.data.collections.get(collection_name)

    with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
        if collection_name in data_from.collections:
            data_to.collections = [collection_name]
        else:
            return None

    for coll in data_to.collections:
        if coll is not None:
            bpy.context.scene.collection.children.link(coll)
    return data_to.collections[0] if data_to.collections else None





class WaterPanel(bpy.types.Panel):
    bl_label = "Raindrop Settings"
    bl_idname = "Water"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "LEGO ElementsFX"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator(WaterOperator.bl_idname, text="Add Raindrops", icon="HOLDOUT_OFF")
        obj = context.object
        if obj and obj.particle_systems:
            for psys in obj.particle_systems:
                if "RaindropSettings" in psys.settings.name:
                    s = psys.settings
                    row = layout.row()
                    row.label(text="Amount", icon='LINENUMBERS_ON')
                    row.prop(s, "count", text="")
                    row = layout.row()
                    row.label(text="Scale", icon='CURVE_NCIRCLE')
                    row.prop(s, "particle_size", text="")
                    row = layout.row()
                    row.label(text="Scale Randomness", icon='SURFACE_NCIRCLE')
                    row.prop(s, "size_random", text="")
                    row = layout.row()
                    row.label(text="Seed", icon='CURVES_DATA')
                    row.prop(psys, "seed", text="")


class FirePanel(bpy.types.Panel):
    bl_label = "Firefly Settings"
    bl_idname = "Fire"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "LEGO ElementsFX"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator(FireOperator.bl_idname, text="Add Fireflies", icon="PARTICLE_POINT")
        obj = context.object
        if obj and obj.particle_systems:
            for psys in obj.particle_systems:
                if "FirefliesSettings" in psys.settings.name:
                    s = psys.settings
                    row = layout.row()
                    row.label(text="Amount", icon='LINENUMBERS_ON')
                    row.prop(s, "count", text="")
                    row = layout.row()
                    row.label(text="Scale", icon='CURVE_NCIRCLE')
                    row.prop(s, "particle_size", text="")
                    row = layout.row()
                    row.label(text="Scale Randomness", icon='SURFACE_NCIRCLE')
                    row.prop(s, "size_random", text="")
                    row = layout.row()
                    row.label(text="Seed", icon='CURVES_DATA')
                    row.prop(psys, "seed", text="")
                    row = layout.row()
                    row.label(text="Separation", icon='MOD_LENGTH')
                    row.prop(s, "normal_factor", text="", slider=True)


class EarthPanel(bpy.types.Panel):
    bl_label = "Leaf Settings"
    bl_idname = "Earth"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "LEGO ElementsFX"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator(EarthOperator.bl_idname, text="Add Leaves", icon="RNDCURVE")
        obj = context.object
        if obj and obj.particle_systems:
            for psys in obj.particle_systems:
                if "LeafSettings" in psys.settings.name:
                    s = psys.settings
                    row = layout.row()
                    row.label(text="Amount", icon='LINENUMBERS_ON')
                    row.prop(s, "count", text="")
                    row = layout.row()
                    row.label(text="Scale", icon='CURVE_NCIRCLE')
                    row.prop(s, "particle_size", text="")
                    row = layout.row()
                    row.label(text="Scale Randomness", icon='SURFACE_NCIRCLE')
                    row.prop(s, "size_random", text="")
                    row = layout.row()
                    row.label(text="Seed", icon='CURVES_DATA')
                    row.prop(psys, "seed", text="")
                    row = layout.row()
                    row.label(text="Separation", icon='MOD_LENGTH')
                    row.prop(s, "normal_factor", text="", slider=True)
                    row = layout.row()
                    row.label(text="Rotation", icon='DECORATE_OVERRIDE')
                    row.prop(s, "rotation_factor_random", text="", slider=True)


class AirPanel(bpy.types.Panel):
    bl_label = "Dust Settings"
    bl_idname = "Air"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "LEGO ElementsFX"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        layout.operator(AirOperator.bl_idname, text="Add Dust", icon="OUTLINER_DATA_POINTCLOUD")
        row = layout.row()
        row.label(text = r"𝘜𝘴𝘦 𝘋𝘰𝘍 𝘰𝘳 𝘉𝘰𝘬𝘦𝘩 for better results", icon='ERROR')
        obj = context.object
        if obj and obj.particle_systems:
            for psys in obj.particle_systems:
                if "DustSettings" in psys.settings.name:
                    s = psys.settings
                    row = layout.row()
                    row.label(text="Amount", icon='LINENUMBERS_ON')
                    row.prop(s, "count", text="")
                    row = layout.row()
                    row.label(text="Scale", icon='CURVE_NCIRCLE')
                    row.prop(s, "particle_size", text="")
                    row = layout.row()
                    row.label(text="Scale Randomness", icon='SURFACE_NCIRCLE')
                    row.prop(s, "size_random", text="")
                    row = layout.row()
                    row.label(text="Seed", icon='CURVES_DATA')
                    row.prop(psys, "seed", text="")
                    row = layout.row()
                    row.label(text="Separation", icon='MOD_LENGTH')
                    row.prop(s, "normal_factor", text="", slider=True)
                    row = layout.row()
                    row.label(text="Rotation", icon='DECORATE_OVERRIDE')
                    row.prop(s, "rotation_factor_random", text="", slider=True)


_classes = [
    WaterPanel, WaterOperator,
    FirePanel, FireOperator,
    EarthPanel, EarthOperator,
    AirPanel, AirOperator,
]


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
