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
import os
from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType

from camel.load_config import config
from camel.load_config import logger


# QWEN_API_KEY
os.environ['QWEN_API_KEY'] = config("default_llm", "api_key")
sys_msg = """您是个乐于助人的助手。你的回答使用中文，并且符合markdown格式，并在合适的位置添加emoji表情.
你之回答”篮球“相关的问题，不回答任何和篮球无关的问题，如果问题和篮球无之间关系，请不要回复。
"""
usr_msg = """谁是世界上最好的篮球运动员？ 说说他的事业吧。"""


openai_model = ModelFactory.create(
    model_platform=ModelPlatformType.QWEN,
    model_type=ModelType.DEEPSEEK_R1,
)

openai_agent = ChatAgent(
    system_message=sys_msg,
    model=openai_model,
    output_language="中文",
)
if __name__ == '__main__':
    logger.info('1st')
    response = openai_agent.step(usr_msg)
    print('response:\n', response.msgs[0].content)

# logger.info('2nd')
# response_with_think = openai_agent.step(
#     usr_msg,
#     reason_params=dict(
#         choices=5,
#         threshold=0.6,
#     ),
# )
# print('response_with_think:\n', response_with_think.msgs[0].content)

#
# logger.info('3nd')
# response_with_think2 = openai_agent.step(
#     usr_msg,
#     reason_params=dict(
#         choices=5,
#         threshold=0.1,
#     ),
# )
# print('response_with_think2:\n', response_with_think2.msgs[0].content)
