import json, os

class bot_resources:

    async def get_all_data(name):
        if not os.path.exists(f'resources/bot/{name}.json'):
            return 0
        with open(f'resources/bot/{name}.json', 'r') as w:
            return json.load(w)
        
    async def get_user_permissions(id):
        permissions = await bot_resources.get_all_data("user_permissions")
        id = str(id)
        if id not in permissions:
            return ["permission_base"]
        else:
            user_perms = permissions[id]
            user_perms.append("permission_base")
            return user_perms

        
    def get_token():
        with open(f'resources/bot/app.json', 'r') as w:
            return json.load(w)["token"]
    
    async def get_id():
        w = await bot_resources.get_all_data("app")
        w["id"]
        
    async def get_permission(permission):
        permission_data = await bot_resources.get_all_data("permission")
        if permission in permission_data:
            return permission_data[permission]
        else:
            return 0
        
    async def get_feature_config(feature):
        config = await bot_resources.get_all_data("config")
        config = json.load(w)
        config = config["features"]
        if feature in config:
            return config[feature]
        else:
            return 0