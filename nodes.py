#import torch
import toml
import os
import glob
from server import PromptServer
from aiohttp import web


routes = PromptServer.instance.routes
@routes.post('/mittimi_promptonly_path')
async def my_function(request):
    the_data = await request.post()
    LoadPromptMittimi.handle_my_message(the_data)
    LoadTextMittimi.handle_my_message(the_data)
    return web.json_response({})


my_directory_path = os.path.dirname((os.path.abspath(__file__)))
presets_directory_path = os.path.join(my_directory_path, "presets")
preset_list = []
tmp_list = []
tmp_list += glob.glob(f"{presets_directory_path}/**/*.toml", recursive=True)
for l in tmp_list:
    preset_list.append(os.path.relpath(l, presets_directory_path))
if len(preset_list) > 1: preset_list.sort()


class LoadPromptMittimi:
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "preset": (preset_list,),
                "PositivePrompt": ("STRING", {"multiline": True}),
                "NegativePrompt": ("STRING", {"multiline": True}),
            },
            "hidden": {"node_id": "UNIQUE_ID" }
        }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("positive_prompt_text", "negative_prompt_text", )
    FUNCTION = "loadPrompt"
    CATEGORY = "mittimiTools"

    def loadPrompt(self, PositivePrompt, NegativePrompt, node_id, preset=[], ):
        return(PositivePrompt, NegativePrompt, )
    
    def handle_my_message(d):
        
        preset_data = ""
        preset_path = os.path.join(presets_directory_path, d['message'])
        print(f"preset_path={preset_path}")
        with open(preset_path, 'r') as f:
            preset_data = toml.load(f)
        PromptServer.instance.send_sync("my.custom.message", {"message":preset_data, "node":d['node_id']})


class LoadTextMittimi:
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "preset": (preset_list,),
                "text": ("STRING", {"multiline": True}),
            },
            "hidden": {"node_id": "UNIQUE_ID" }
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("text", )
    FUNCTION = "loadPrompt"
    CATEGORY = "mittimiTools"

    def loadPrompt(self, text, node_id, preset=[], ):
        return(text, )
    
    def handle_my_message(d):
        
        preset_data = ""
        preset_path = os.path.join(presets_directory_path, d['message'])
        with open(preset_path, 'r') as f:
            preset_data = toml.load(f)
        PromptServer.instance.send_sync("my.custom.message", {"message":preset_data, "node":d['node_id']})


NODE_CLASS_MAPPINGS = {
    "LoadPromptMittimi": LoadPromptMittimi,
    "LoadTextMittimi": LoadTextMittimi,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadPromptMittimi": "LoadPrompt",
    "LoadTextMittimi": "LoadText"
}