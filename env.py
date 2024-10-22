import os

# 通用设置
USE_OLLAMA = True  # 设置为 True 以使用Ollama，False 以使用OpenAI

# OpenAI配置
CHATGPT_API_KEY = "sk-9abc5a2e428341af80fff39820e26b35"
CHATGPT_API_BASE = "https://api.deepseek.com/v1"
CHATGPT_MODEL = "deepseek-chat"  # 或者您想使用的其他模型名称

# Ollama配置
OLLAMA_BASE_URL = "http://localhost:11434"  # 删除 "/v1"
OLLAMA_MODEL = "qwen2.5:3b"

# 将配置设置为环境变量
os.environ["USE_OLLAMA"] = str(USE_OLLAMA).lower()
os.environ["CHATGPT_API_KEY"] = CHATGPT_API_KEY
os.environ["CHATGPT_API_BASE"] = CHATGPT_API_BASE
os.environ["CHATGPT_MODEL"] = CHATGPT_MODEL
os.environ["OLLAMA_BASE_URL"] = OLLAMA_BASE_URL
os.environ["OLLAMA_MODEL"] = OLLAMA_MODEL

# 其他环境变量...
