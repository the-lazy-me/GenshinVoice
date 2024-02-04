# GenshinVoice

[QChatGPT](https://github.com/RockChinQ/QChatGPT)的插件，生成原神语音，调用这个网站的接口https://v2.genshinvoice.top/

> 我没学过python，代码大量依赖于AI生成，难免有不合理不正确之处，不过，代码和人有一个能跑就行😋

## 介绍

本插件调用了[genshinvoice](https://v2.genshinvoice.top/)的接口，用于将QChatGPT返回的内容转换为原神语音

速度快，免费，效果好

## 使用

### 下载

克隆此项目，放到plugins的文件夹下

```bash
git clone https://github.com/the-lazy-me/GenshinVoice.git
```

或下载源码压缩包，解压后放到plugins的文件夹下

打开GenshinVoice文件夹，命令行执行

```bash
pip install -r requirements.txt
```

速度太慢可以执行

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```

### 前置工作

参考此教程，安装ffmpeg

教程：https://zhuanlan.zhihu.com/p/118362010

### 配置

打开GenshinVoice的config文件夹下的`config.yml`，内容如下所示

```yml
data:
  character: "派蒙_ZH"
  # 选择默认的角色，可选的参考同目录的 角色列表.txt，也可以在对话中调整
  audio_speed: 1 # 语音播放速度
  #这几个不懂不用调
  ns: 0.5
  nsw: 0.9
  sdp_radio: 0.2
  timeout: 30
  emotion: "Happy"
  weight: 0.7

# 是否默认开启语音功能，默认为False，即不开启，True为默认开启，看你喜好
voice_switch: False

```

### 指令

管理员向机器人发送下面指令，私聊直接发指令，群里@后面加指令

- `!ysvoice on`：开启原神语音
- `!ysvoice off`：关闭原神语音
- `!ysvoice switch <角色名>`：切换语音声线，把`<角色名>`替换为config文件夹下的`角色列表.txt`里面的角色
- `!ysvoice list`：查看角色列表