# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========

from camel.agents.chat_agent import ChatAgent
from camel.configs.qwen_config import QwenConfig
from camel.data_collector import AlpacaDataCollector
from camel.models.model_factory import ModelFactory
import os
from camel.types.enums import ModelPlatformType, ModelType
from camel.load_config import config
from camel.load_config import logger
import time
from camel.schemas import QwenSchemaConverter

"""
把回复变成结构化数据 用qwen模型
{'instruction': "您是个乐于助人的助手 无论输入语言如何， 您必须以 typing.Optional[ForwardRef('zh-cn')]回复.", 
'input': '', 
'output': 'PUBG（《绝地求生》）的正式发布日期是2017年12月20日。这款游戏由韩国公司蓝洞（Bluehole）开发，最初在PC平台上发布，随后扩展到其他平台如Xbox One、PlayStation 4和移动设备。PUBG（《绝地求生：大逃杀》）的发布日期因平台而异，以下是各平台的具体发布时间：", "1. **PC版（Steam平台）**", " - **抢先体验版**：2017年3月23日。", " - **正式版**：2017年12月20日。", "2. **Xbox One版**", " - **抢先体验版**：2017年12月12日。", " - **正式版**：2018年9月4日。", "3. **PlayStation 4版**", " - **正式版**：2018年12月7日。", "4. **移动版（PUBG Mobile）**", " - **iOS/Android版**：2018年3月19日。", "PUBG由韩国公司蓝洞（Bluehole，现更名为Krafton）开发，是一款大逃杀类型的多人在线游戏。它迅速成为全球现象级游戏，吸引了数亿玩家，并推动了“大逃杀”游戏类型的流行。"]'}

"""
# QWEN_API_KEY
os.environ['QWEN_API_KEY'] = config("default_llm", "api_key")
model_config_dict = QwenConfig(
    temperature=0.0,
).as_dict()

model = ModelFactory.create(
    model_platform=ModelPlatformType.QWEN,
    model_type=ModelType.DEEPSEEK_V3,
    model_config_dict=model_config_dict,
)

agent = ChatAgent(system_message="您是个乐于助人的助手", model=model)

usr_msg = "视频游戏PUBG的发布日期是什么时候?"

# 创建一个数据收集器
collector = AlpacaDataCollector().record(agent).start()

# 用户输入
resp = agent.step(usr_msg)

# 记录用户输入
collector.step(role="user", message=usr_msg, )
# logger.info(resp.msgs[-1].role_name,collector.history[-1].message)

# 收集模型输出
collector.step(role=resp.msgs[-1].role_name, name=resp.msgs[-1].role_name, message=resp.msgs[0].content)
logger.info(f"{resp.msgs[-1].role_name},{collector.history[-1].message}")

# 用户二次输入
usr_msg2 = "请帮我详细介绍一下PUBG的发布日期"
resp = agent.step(usr_msg2)
# 收集用户输入
collector.step(role="user", message=usr_msg2, )

# 收集模型输出
collector.step(role=resp.msgs[-1].role_name, name=resp.msgs[-1].role_name, message=resp.msgs[0].content)
# Automatically record the message
logger.info(f"""collector message:{collector.data, len(collector.history)}""")

# Convert>>>
print(collector.convert())

# history内结构
# id: UUID,
#         name: str,
#         role: Literal["user", "assistant", "system", "tool"],
#         message: Optional[str] = None,
#         function_call: Optional[Dict[str, Any]] = None,

# collector.step("user", "Tools calling operator", usr_msg) #deepseek 不能用tools
logger.info(f"resp message:{resp.msgs[0].content}")
time.sleep(5)
logger.info(f"collector message:{collector.data, collector.history}")
collector.step("assistant", "Tools calling operator", resp.msgs[0].content)

print(collector.llm_convert(converter=QwenSchemaConverter()))
{'instruction': "您是个乐于助人的助手 无论输入语言如何， 您必须以 typing.Optional[ForwardRef('zh-cn')]回复.",
 'input': '',
 'output': 'PUBG（《绝地求生》）的正式发布日期是2017年12月20日。这款游戏由韩国公司蓝洞（Bluehole）开发，最初在PC平台上发布，随后扩展到其他平台如Xbox One、PlayStation 4和移动设备。PUBG（《绝地求生：大逃杀》）的发布日期因平台而异，以下是各平台的具体发布时间：", "1. **PC版（Steam平台）**", " - **抢先体验版**：2017年3月23日。", " - **正式版**：2017年12月20日。", "2. **Xbox One版**", " - **抢先体验版**：2017年12月12日。", " - **正式版**：2018年9月4日。", "3. **PlayStation 4版**", " - **正式版**：2018年12月7日。", "4. **移动版（PUBG Mobile）**", " - **iOS/Android版**：2018年3月19日。", "PUBG由韩国公司蓝洞（Bluehole，现更名为Krafton）开发，是一款大逃杀类型的多人在线游戏。它迅速成为全球现象级游戏，吸引了数亿玩家，并推动了“大逃杀”游戏类型的流行。"]'}

collector.reset()

# Manually record the message
collector.step("user", "Tools calling operator", usr_msg)

collector.step("assistant", "Tools calling operator", resp.msgs[0].content)

print(collector.convert())

# ruff: noqa: E501
"""
{'instruction': 'You are a helpful assistantWhen is the release date of the video game Portal?', 'input': '', 'output': 'The video game "Portal" was released on October 10, 2007. It was developed by Valve Corporation and is part of the game bundle known as "The Orange Box," which also included "Half-Life 2" and its episodes.'}
2025-01-19 19:26:09,140 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
{'instruction': 'You are a helpful assistant When is the release date of the video game Portal?', 'input': '', 'output': 'The video game "Portal" was released on October 10, 2007. It was developed by Valve Corporation and is part of the game bundle known as "The Orange Box," which also included "Half-Life 2" and its episodes.'}
{'instruction': 'You are a helpful assistantWhen is the release date of the video game Portal?', 'input': '', 'output': 'The video game "Portal" was released on October 10, 2007. It was developed by 
"""
