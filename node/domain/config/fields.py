from node.domain.config.models import TemplateKeyName

# Root templates - used by most of the read/write fields
sequence_root = TemplateKeyName('sequence_root')
shot_root = TemplateKeyName('shot_root')
step_root = TemplateKeyName('shot_task_root')
asset_root = TemplateKeyName('asset_root')
asset_step_root = TemplateKeyName('asset_task_root')

# Maya Shot templates - used by "3D - MtoA Shot" and "Matte - Clarisse Shot"
maya_shot_render_folder = TemplateKeyName(work='Shot_MayaRender_Work_Generic_Name',
                                          publish='Shot_MayaRender_Publish_Generic_Name')
maya_shot_render_layer = TemplateKeyName(work='Shot_MayaRender_Work_Layer', publish='Shot_MayaRender_Publish_Layer')
maya_shot_render_aov = TemplateKeyName(work='Shot_MayaRender_Work_Aov', publish='Shot_MayaRender_Publish_Aov')

maya_shot_render_sequence = TemplateKeyName(work='Shot_MayaRender_Work_Sequence',
                                            publish='Shot_MayaRender_Publish_Sequence')

# Maya Asset templates - used by "3D - MtoA Asset" read fields
maya_asset_render_folder = TemplateKeyName(work='Asset_MayaRender_Work_Generic_Name',
                                           publish='Asset_MayaRender_Publish_Generic_Name')
maya_asset_render_layer = TemplateKeyName(work='Asset_MayaRender_Work_Layer', publish='Asset_MayaRender_Publish_Layer')
maya_asset_render_aov = TemplateKeyName(work='Asset_MayaRender_Work_Aov', publish='Asset_MayaRender_Publish_Aov')

maya_asset_render_sequence = TemplateKeyName(work='Asset_MayaRender_Work_Sequence',
                                             publish='Asset_MayaRender_Publish_Sequence')

# Houdini Shot templates - used by "3D - HtoA Shot" and "Matte - Clarisse Shot" read fields
htoa_shot_render_folder = TemplateKeyName(work='Shot_HoudiniRender_Work_Generic_Name',
                                          publish='Shot_HoudiniRender_Publish_Generic_Name')
htoa_asset_render_folder = TemplateKeyName(work='Asset_HoudiniRender_Work_Generic_Name',
                                           publish='Asset_HoudiniRender_Publish_Generic_Name')
htoa_shot_render_aov = TemplateKeyName(work='Shot_HoudiniRender_Work_Aov', publish='Shot_HoudiniRender_Publish_Aov')
htoa_asset_render_aov = TemplateKeyName(work='Asset_HoudiniRender_Work_Aov', publish='Asset_HoudiniRender_Publish_Aov')

htoa_shot_render_sequence = TemplateKeyName(work='Shot_HoudiniRender_Work_Sequence',
                                            publish='Shot_HoudiniRender_Publish_Sequence')
htoa_asset_render_sequence = TemplateKeyName(work='Asset_HoudiniRender_Work_Sequence',
                                             publish='Asset_HoudiniRender_Publish_Sequence')

# Clarisse Shot templates - unused by fields
clarisse_shot_render_folder = TemplateKeyName(work='Shot_ClarisseRender_Work_Generic_Name',
                                              publish='Shot_ClarisseRender_Publish_Generic_Name')
clarisse_shot_render_image = TemplateKeyName(work='Shot_ClarisseRender_Work_Image',
                                             publish='Shot_ClarisseRender_Publish_Image')
clarisse_shot_render_layer = TemplateKeyName(work='Shot_ClarisseRender_Work_Layer',
                                             publish='Shot_ClarisseRender_Publish_Layer')

clarisse_shot_render_sequence = TemplateKeyName(work='Shot_ClarisseRender_Work_Sequence',
                                                publish='Shot_ClarisseRender_Publish_Sequence')

# Maya Playblast templates - used by "3D - Maya Blast Shot" read fields
mayablast_shot_render_folder = TemplateKeyName(work='Shot_MayaBlast_Work_Generic_Name',
                                               publish='Shot_MayaBlast_Publish_Generic_Name')
mayablast_shot_camera = TemplateKeyName(work='Shot_MayaBlast_Work_Camera', publish='Shot_MayaBlast_Publish_Camera')

mayablast_shot_render_sequence = TemplateKeyName(work='Shot_MayaBlast_Work_Sequence',
                                                 publish='Shot_MayaBlast_Publish_Sequence')

# Hiero templates - used by "Footage - Plate" read fields
footage_root = TemplateKeyName('Hiero_Footage_Root')

footage_render_sequence = TemplateKeyName('Hiero_Footage_Sequence')

# Nuke templates - used by various Nuke read/write fields
nuke_shot_render_folder = TemplateKeyName(work='Shot_NukeRender_Work_Generic_Name',
                                          publish='Shot_NukeRender_Publish_Generic_Name')
nuke_shot_render_sequence = TemplateKeyName(work='Shot_NukeRender_Work_Sequence',
                                            publish='Shot_NukeRender_Publish_Sequence')

nuke_asset_render_folder = TemplateKeyName(work='Asset_NukeRender_Work_Generic_Name',
                                           publish='Asset_NukeRender_Publish_Generic_Name')
nuke_asset_render_sequence = TemplateKeyName(work='Asset_NukeRender_Work_Sequence',
                                             publish='Asset_NukeRender_Publish_Sequence')

nuke_shot_element_render_root = TemplateKeyName('Shot_Element_NukeRender_Root')
nuke_asset_element_render_root = TemplateKeyName('Asset_Element_NukeRender_Root')

nuke_shot_element_render_folder = TemplateKeyName('Shot_Element_NukeRender_Generic_Name')
nuke_shot_element_render_sequence = TemplateKeyName('Shot_Element_NukeRender_Sequence')

nuke_asset_element_render_folder = TemplateKeyName('Asset_Element_NukeRender_Generic_Name')
nuke_asset_element_render_sequence = TemplateKeyName('Asset_Element_NukeRender_Sequence')

# Nuke Scene templates - unused (except part of them as constant string)
nuke_shot_scene = TemplateKeyName(work='Shot_NukeScene_Work', publish='Shot_NukeScene_Publish')
nuke_asset_scene = TemplateKeyName(work='Asset_NukeScene_Work', publish='Asset_NukeScene_PublishArea')
nuke_shot_proxy = TemplateKeyName('Shot_NukeProxy_Work_Sequence')
nuke_asset_proxy = TemplateKeyName('Asset_NukeProxy_Work_Sequence')

# Flame templates - used by "Finish - Flame Shot" read fields
flame_shot_render_folder = TemplateKeyName('Shot_FlameRender_Work_Generic_Name')

flame_shot_render_sequence = TemplateKeyName('Shot_FlameRender_Work_Sequence')

# Photoshop Shot templates - used by "2D - Photoshop Shot" read fields
photoshop_shot_render_sequence = TemplateKeyName(work='Shot_PhotoshopRender_Work_Image',
                                                 publish='Shot_PhotoshopRender_Publish_Image')

# Photoshop Asset templates - used by "2D - Photoshop Asset" read fields
photoshop_asset_render_sequence = TemplateKeyName(work='Asset_PhotoshopRender_Work_Image',
                                                  publish='Asset_PhotoshopRender_Publish_Image')

# Harmony Shot templates - used by "2D - Harmony Shot" read fields
harmony_shot_render_sequence = TemplateKeyName(work='Shot_HarmonyRender_Work_Image',
                                               publish='Shot_HarmonyRender_Publish_Image')

# Harmony Asset templates - used by "2D - Harmony Asset" read fields
harmony_asset_render_sequence = TemplateKeyName(work='Asset_HarmonyRender_Work_Image',
                                                publish='Asset_HarmonyRender_Publish_Image')
