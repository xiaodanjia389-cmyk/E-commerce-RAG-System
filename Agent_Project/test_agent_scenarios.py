import time
from agent_core import ReActAgent
from utils.logger_utils import logger

def run_scenario_test(scenario_name, query):
    print(f"\n{'='*20} {scenario_name} {'='*20}")
    print(f"用户提问: {query}\n")
    
    agent = ReActAgent()
    print("--- Agent 思考与执行流程 ---")
    
    # 开始流式响应
    full_content = ""
    for chunk in agent.execute_stream(query):
        print(chunk, end="", flush=True)
        full_content += chunk
    
    print(f"\n\n{'='*50}\n")

if __name__ == "__main__":
    # 场景 1：验证 RAG 工具（知识库检索）
    run_scenario_test(
        "测试用例 1：知识库检索", 
        "我家的扫地机器人扫不干净怎么办？"
    )

    # 场景 2：验证多工具串联（天气 + 维护建议）
    run_scenario_test(
        "测试用例 2：多工具串联", 
        "深圳今天的天气如何，顺便说说怎么保养扫地机器人？"
    )

    # 场景 3：验证报告生成全流程（触发动态提示词）
    run_scenario_test(
        "测试用例 3：报告生成", 
        "给我生成我的扫地机器人使用报告"
    )