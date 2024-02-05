import base64
import os

import mirai
import yaml

from pkg.plugin.host import EventContext, PluginHost
from pkg.plugin.models import *

from plugins.GenshinVoice.pkg.generate_voice import AudioGenerator

# 读取配置文件
with open(os.path.join(os.path.dirname(__file__), 'config/config.yml'), 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

user_character = None
enable = config['voice_switch']


# 发送消息函数，文本或语音
def send_msg(kwargs, msg):
    host: pkg.plugin.host.PluginHost = kwargs["host"]
    host.send_person_message(kwargs["launcher_id"], [msg]) if kwargs[
                                                                  "launcher_type"] == "person" else host.send_group_message(
        kwargs["launcher_id"], [msg])


# 注册插件
@register(name="GenshinVoice", description="一个生成原神语音的插件", version="1.0", author="the-lazy-me")
class GenshinVoicePlugin(Plugin):

    # 插件加载时触发
    # plugin_host (pkg.plugin.host.PluginHost) 提供了与主程序交互的一些方法，详细请查看其源码
    def __init__(self, plugin_host: PluginHost):
        pass

    # 当消息回复时触发
    @on(NormalMessageResponded)
    def text_to_voice(self, event: EventContext, **kwargs):
        global enable
        global user_character
        # 如果语音开关开启
        if enable:
            # 输出调试信息
            # logging.debug("hello, {}".format(kwargs['sender_id']))

            logging.info("回复的文本消息是：{}".format(kwargs["response_text"]))
            send_msg(kwargs, kwargs["prefix"] + kwargs["response_text"])
            res_text = kwargs["response_text"]

            audio_generator = AudioGenerator(config['data'], character=user_character or None)

            logging.info(
                "使用角色“" + user_character + "”进行语音合成" if user_character else "使用默认角色" + config["data"][
                    "character"] + "进行语音合成")

            result = audio_generator.generate_audio(res_text)

            if result:
                # 将silk进行base64编码，返回base64编码后的字符串
                with open(result, 'rb') as f:
                    result = f.read()

                # 发送语音消息
                voice_msg = mirai.Voice(base64=base64.b64encode(result).decode('utf-8'))
                send_msg(kwargs, voice_msg)
            event.prevent_default()
            event.prevent_postorder()

    # 当收到个人/群消息时触发
    @on(PersonCommandSent)
    @on(GroupCommandSent)
    def open_text_to_voice(self, event: EventContext, **kwargs):
        global enable
        global user_character
        command = kwargs["command"]
        params = kwargs["params"]
        if command == "ysvoice":
            if params[0] == "help":
                event.add_return("reply", ["ysvoice switch [角色名] - 切换角色",
                                           "ysvoice on - 开启语音生成",
                                           "ysvoice off - 关闭语音生成",
                                           "ysvoice status - 查看原神语音插件开关状态",
                                           "ysvoice list - 查看角色列表"])
                event.prevent_default()
                event.prevent_postorder()
            elif params[0] == "on":
                enable = True
                event.add_return("reply", ["原神语音生成已开启"])
                event.prevent_default()
                event.prevent_postorder()
                
            elif params[0] == "off":
                enable = False
                event.add_return("reply", ["原神语音生成已关闭"])
                event.prevent_default()
                event.prevent_postorder()

            elif params[0] == "status":
                if enable:
                    if user_character:
                        event.add_return("reply", ["原神语音生成已开启，当前角色：" + user_character])
                    else:
                        event.add_return("reply", ["原神语音生成已开启，当前角色（默认）：" + config["data"]["character"]])
                    event.prevent_default()
                    event.prevent_postorder()

                else:
                    if user_character:
                        event.add_return("reply", ["原神语音生成已关闭，当前角色：" + user_character])
                    else:
                        event.add_return("reply", ["原神语音生成已关闭，当前角色（默认）：" + config["data"]["character"]])
                    event.prevent_default()
                    event.prevent_postorder()

                    
        if command == "ysvoice" and kwargs["is_admin"]:
            if params[0] == "switch":
                # 读取角色列表txt
                with open(os.path.join(os.path.dirname(__file__), 'config/角色列表.txt'), "r",
                          encoding='UTF-8') as file:
                    characters = file.read().splitlines()
                if params[1] in characters:
                    user_character = params[1]
                    event.add_return("reply", ["角色已切换为：" + user_character])
                    event.prevent_default()
                    event.prevent_postorder()
                else:
                    event.add_return("reply", ["角色不存在"])
                    event.prevent_default()
                    event.prevent_postorder()

        if command == "ysvoice" and kwargs["is_admin"]:
            if params[0] == "list":
                # 读取角色列表txt的每一行
                with open(os.path.join(os.path.dirname(__file__), 'config/角色列表.txt'), "r",
                          encoding='UTF-8') as file:
                    characters = file.read().splitlines()
                reply = "角色列表：\n"
                for character in characters:
                    reply += character + "\n"
                event.add_return("reply", [reply])
                event.prevent_default()
                event.prevent_postorder()


# 插件卸载时触发
def __del__(self):
    pass
