# Fz-sDatapackImporter
一个用于将stats数据同步到Fz-sDatapack记分版的 MCDR 插件
适用于未在开服时未及时安装 Fz-sDatapack 但希望能够同步数据的场景

本插件支持 从 usercache.json 或 whitelist.json 中载入玩家 uuid

## 安装方法
丢进 MCDR 插件文件夹, 插件会在启动时自动生成配置文件

## 设置方法
会在插件同目录下生成配置文件夹, 编辑config.json
|设置选项|描述|默认值|可选择的值|
|-----|-----|-----|-----|
|global.mode|同步数据使用的 uuid 来源|whitelist|whitelist, usercache|
|commandPermissions.help|!!fdi help 命令权限|0|0,1,2,3,4|
|commandPermissions.refresh|!!fdi refresh 命令权限|3|0,1,2,3,4|
|commandPermissions.process|!!fdi process 命令权限|3|0,1,2,3,4|

## 使用方法

### 命令
|命令|描述|
|-----|-----|
|!!fdi help| 插件帮助信息|
|!!fdi refresh| 刷新 uuid 缓存|
|!!fdi process [榜单]| 执行刷新|

### 榜单可用的值
|参数|描述|
|-----|-----|
|kill|击杀榜|
|dig|挖掘榜|
|death|死亡榜|
|trading|PY榜|
|fishing|钓鱼榜|
|damage|奥利给榜|
|activation|活跃度排行|

## 下一步计划
1. 优化冗余代码
2. 将服务端路径添加到配置文件
