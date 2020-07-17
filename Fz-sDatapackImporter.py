import json
import os
import time

config = {}

class fzsDatapackImporter():
    def loadJson(self, filePath):
        with open(filePath, 'r') as f:
            return json.load(f)

    def saveJson(self, filePath, configObject):
        with open(filePath, 'w') as f:
            json.dump(configObject, f, ensure_ascii = False, indent = 4)
    
    def saveDefaultConfig(self):
        defaultConfig = {
            'global': {
                'mode': 'whitelist'
            },
            'commandPermissions': {
                'help': 0,
                'refresh': 3,
                'process': 3,
            }
        }
        self.saveJson('./plugins/{}/config.json'.format(self.getSelfName()), defaultConfig)

    def getSelfName(self):
        return os.path.basename(__file__).replace(".py", "")

    def getPlayerStatsData(self, uuid, classification, target):
        uuidFilePath = './server/world/stats/{}.json'.format(uuid)
        if (os.path.isfile(uuidFilePath)):
            data = self.loadJson(uuidFilePath)
            if ('minecraft:{}'.format(classification) in data['stats']):
                if ('minecraft:{}'.format(target) in data['stats']['minecraft:{}'.format(classification)]):
                    return data['stats']['minecraft:{}'.format(classification)]['minecraft:{}'.format(target)]
        return None

    def refreshUUID(self):
        for i in {'usercache', 'whitelist'}:
            t = self.loadJson('./server/{}.json'.format(i))
            r = {}
            for k in t: 
                r[k['name']] =  k['uuid']
            self.saveJson('./plugins/{}/uuid/{}.json'.format(self.getSelfName(), i), r)
    
    def checkConfig(self):
        if (not os.path.isdir('./plugins/{}'.format(self.getSelfName()))):
            os.makedirs('./plugins/{}/uuid'.format(self.getSelfName()))
        if (not os.path.isfile('./plugins/{}/config.json'.format(self.getSelfName()))):
            self.saveDefaultConfig()
        self.refreshUUID()

    def loadUUID(self):
        config = self.loadJson('./plugins/{}/config.json'.format(self.getSelfName()))
        if (config['global']['mode'] in {'usercache', 'whitelist'}):
            t = self.loadJson('./plugins/{}/uuid/{}.json'.format(self.getSelfName(), config['global']['mode']))
            return t 
        else:
            return None

    def syncKillCounter(self, server):
        r = self.loadUUID()
        if (r):
            total = 0
            for i in r:
                data = 0
                for k in {'mob_kills', 'player_kills'}:
                    if(self.getPlayerStatsData(r[i], 'custom', k)):
                        data += self.getPlayerStatsData(r[i], 'custom', k)
                server.execute('scoreboard players set {} {} {}'.format(i, 'killCounter', data))
                total = total + data
            server.execute('scoreboard players set {} {} {}'.format('总击杀数', 'totalList', total))
            return True
        else:
            return False

    def syncDigCounter(self, server):
        r = self.loadUUID()
        if (r):
            total = 0
            for i in r:
                data = 0
                for k in {'diamond_axe', 'diamond_pickaxe', 'diamond_shovel', 'iron_axe', 'iron_pickaxe', 'iron_shovel', 'stone_axe', 'stone_pickaxe', 'stone_shovel'}:
                    if(self.getPlayerStatsData(r[i], 'used', k)):
                        data += self.getPlayerStatsData(r[i], 'used', k)
                server.execute('scoreboard players set {} {} {}'.format(i, 'digCounter', data))
                total = total + data
            server.execute('scoreboard players set {} {} {}'.format('总挖掘数', 'totalList', total))
            return True
        else:
            return False

    def syncDeathCounter(self, server):
        r = self.loadUUID()
        if (r):
            total = 0
            for i in r:
                data = 0
                for k in {'deaths'}:
                    if(self.getPlayerStatsData(r[i], 'custom', k)):
                        data += self.getPlayerStatsData(r[i], 'custom', k)
                server.execute('scoreboard players set {} {} {}'.format(i, 'deathCounter', data))
                total = total + data
            server.execute('scoreboard players set {} {} {}'.format('总死亡数', 'totalList', total))
            return True
        else:
            return False

    def syncTradingCounter(self, server):
        r = self.loadUUID()
        if (r):
            total = 0
            for i in r:
                data = 0
                for k in {'traded_with_villager'}:
                    if(self.getPlayerStatsData(r[i], 'custom', k)):
                        data += self.getPlayerStatsData(r[i], 'custom', k)
                server.execute('scoreboard players set {} {} {}'.format(i, 'tradingCounter', data))
                total = total + data
            server.execute('scoreboard players set {} {} {}'.format('总交易数', 'totalList', total))
            return True
        else:
            return False
    
    def syncFishingCounter(self, server):
        r = self.loadUUID()
        if (r):
            total = 0
            for i in r:
                data = 0
                for k in {'fish_caught'}:
                    if(self.getPlayerStatsData(r[i], 'custom', k)):
                        data += self.getPlayerStatsData(r[i], 'custom', k)
                server.execute('scoreboard players set {} {} {}'.format(i, 'fishingCounter', data))
                total = total + data
            server.execute('scoreboard players set {} {} {}'.format('总钓鱼数', 'totalList', total))
            return True
        else:
            return False   

    def syncDamageTaken(self, server):
        r = self.loadUUID()
        if (r):
            total = 0
            for i in r:
                data = 0
                for k in {'damage_taken'}:
                    if(self.getPlayerStatsData(r[i], 'custom', k)):
                        data += self.getPlayerStatsData(r[i], 'custom', k)
                server.execute('scoreboard players set {} {} {}'.format(i, 'damageTaken', data))
                total = total + data
            server.execute('scoreboard players set {} {} {}'.format('总受伤害量', 'totalList', total))
            return True
        else:
            return False

    def syncActCounter(self, server):
        r = self.loadUUID()
        if (r):
            total = 0
            for i in r:
                data = 0
                for k in {'play_one_minute'}:
                    if(self.getPlayerStatsData(r[i], 'custom', k)):
                        data += self.getPlayerStatsData(r[i], 'custom', k)
                server.execute('scoreboard players set {} {} {}'.format(i, 'actCounter', data % 72000))
                server.execute('scoreboard players set {} {} {}'.format(i, 'activation', data // 72000))
                total = total + data // 72000
            server.execute('scoreboard players set {} {} {}'.format('总活跃时间', 'totalList', total))
            return True
        else:
            return False

def on_info(server, info):
    p = fzsDatapackImporter()
    p.checkConfig()
    config = p.loadJson('./plugins/{}/config.json'.format(p.getSelfName()))
    args = info.content.split(' ')
    arglen = len(args)
    if (args[0] == '!!fdi'):
        if (arglen > 1 and args[1] in config['commandPermissions']):
            if (server.get_permission_level(info) < config['commandPermissions'][args[1]]):
                server.reply(info, '§aFDI §7>> §c你没有使用该命令的权限!')
                return
            
            elif (args[1] == 'help' and arglen == 2):
                server.reply(info, '§a!!fdi help §7- §e获取帮助')
                server.reply(info, '§a!!fdi refresh §7- §e刷新uuid缓存')
                server.reply(info, '§a!!fdi process [榜单] §7- §e执行同步')
                
            elif (args[1] == 'refresh' and arglen == 2):
                p.refreshUUID()
                server.reply(info, '§aFDI §7>> §bUUID缓存刷新完成!')
                
                
            elif (args[1] == 'process' and arglen >= 2 and arglen <= 3):
                if((arglen == 3 and args[2] == 'kill') or arglen == 2):
                    if (p.syncKillCounter(server)):
                        server.reply(info, '§aFDI §7>> §b击杀榜同步完成!')
                    else:
                        server.reply(info, '§aFDI §7>> §c击杀榜同步失败!')
                    time.sleep(1)
                if((arglen == 3 and args[2] == 'dig') or arglen == 2):
                    if (p.syncDigCounter(server)):
                        server.reply(info, '§aFDI §7>> §b挖掘榜同步完成!')
                    else:
                        server.reply(info, '§aFDI §7>> §c挖掘榜同步失败!')
                    time.sleep(1)
                if((arglen == 3 and args[2] == 'death') or arglen == 2):
                    if (p.syncDeathCounter(server)):
                        server.reply(info, '§aFDI §7>> §b死亡榜同步完成!')
                    else:
                        server.reply(info, '§aFDI §7>> §c死亡榜同步失败!')
                    time.sleep(1)
                if((arglen == 3 and args[2] == 'trading') or arglen == 2):
                    if (p.syncTradingCounter(server)):
                        server.reply(info, '§aFDI §7>> §bPY榜同步完成!')
                    else:
                        server.reply(info, '§aFDI §7>> §cPY榜同步失败!')
                    time.sleep(1)
                if((arglen == 3 and args[2] == 'fishing') or arglen == 2):
                    if (p.syncFishingCounter(server)):
                        server.reply(info, '§aFDI §7>> §b钓鱼榜同步完成!')
                    else:
                        server.reply(info, '§aFDI §7>> §c钓鱼榜同步失败!')
                    time.sleep(1)
                if((arglen == 3 and args[2] == 'damage') or arglen == 2):
                    if (p.syncDamageTaken(server)):
                        server.reply(info, '§aFDI §7>> §b奥利给榜同步完成!')
                    else:
                        server.reply(info, '§aFDI §7>> §c奥利给榜同步失败!')
                    time.sleep(1)
                if((arglen == 3 and args[2] == 'activation') or arglen == 2):
                    if (p.syncActCounter(server)):
                        server.reply(info, '§aFDI §7>> §b活跃度排行同步完成!')
                    else:
                        server.reply(info, '§aFDI §7>> §c活跃度排行同步失败!')
                    time.sleep(1)
                        
        else:
            server.reply(info, '§aFDI §7>> §b未知指令, 请输入 !!fdi help 来获取帮助!')
        return

def on_load(server, old_module):
    fzsDatapackImporter().checkConfig()
    server.add_help_message('!!fdi help', '哈尔威数据包积分榜数据同步')