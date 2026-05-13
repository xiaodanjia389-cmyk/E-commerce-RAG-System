# test_model_middleware.py (更新版)
from utils.middleware_utils import (
    model_call_monitor_middleware, 
    dynamic_prompt_middleware
)
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from utils.config_utils import settings

llm = ChatOpenAI(
    model=settings['model_config']['model_name'],
    openai_api_key=settings['model_config']['api_key'],
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# --- 叠加中间件：先切换提示词，再记录日志 ---
monitored_invoke = dynamic_prompt_middleware(
    model_call_monitor_middleware(llm.invoke)
)

def run_test(query):
    print(f"\n>>> 测试问题: {query}")
    # 模拟标准的消息流：[系统提示词, 用户提问]
    msgs = [
        SystemMessage(content="你是一个简单的机器人助手。"),
        HumanMessage(content=query)
    ]
    response = monitored_invoke(msgs)
    print(f"[回答]: {response.content[:150]}...")

if __name__ == "__main__":
    # 场景1：普通问答
    run_test("你好，你是谁？")
    
    # 场景2：触发报告模式
    run_test("请根据我上周的清扫数据，帮我生成一份清扫报告。")