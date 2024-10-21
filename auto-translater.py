# -*- coding: utf-8 -*-
import os
import openai  # pip install openai
import sys
import re
import yaml  # pip install PyYAML
from env import *
import json
import logging
from datetime import datetime
import requests

# 设置 OpenAI API Key 和 API Base 参数，通过 env.py 传入
openai.api_key = os.environ.get("CHATGPT_API_KEY")
openai.api_base = os.environ.get("CHATGPT_API_BASE")

# Ollama设置
USE_OLLAMA = os.environ.get("USE_OLLAMA", "false").lower() == "true"
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL")

# 设置最大输入字段，超出会拆分输入，防止超出输入字数限制
max_length = 2500

# 设置翻译的路径
dir_to_translate = "testdir/to-translate"
dir_translated = {
    "zh": "testdir/docs/zh" 
}

# 不进行翻译的文件列表
exclude_list = ["index.md", "Contact-and-Subscribe.md", "WeChat.md"]
# 已处理的 Markdown 文件名的列表，会自动生成
processed_list = "processed_list.txt"

# 由 ChatGPT 翻译的提示
tips_translated_by_chatgpt = {
    "zh": "\n\n> 本文是使用AI翻译的，如有遗漏请[**反馈**]( )。"
}
# 文章使用中文撰写的提示，避免本身为中文的文章被重复翻译
marker_written_in_zh = "\n> 本文原始语言为中文。\n"
# 即使在已处理的列表中，仍需要重新翻译的标记
marker_force_translate = "\n[translate]\n"

# 在文件开头添加以下代码来读取 JSON 文件
def load_replace_rules(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['replace_rules'], data['front_matter_replace_rules']

# 替换原有的 replace_rules 和 front_matter_replace_rules 定义
replace_rules, front_matter_replace_rules = load_replace_rules('replace_rules.json')

def front_matter_replace(value, lang):
    for rule in front_matter_replace_rules:
        if value == rule["orginal_text"]:
            return rule["replaced_text"][lang]
    return value  # 如果没有匹配的规则，返回原始值

# Front Matter 处理规则
front_matter_translation_rules = {
    # 调用 ChatGPT 自动翻译
    "title": lambda value, lang: translate_text(value, lang, "front-matter"),
    "description": lambda value, lang: translate_text(value, lang, "front-matter"),
    
    # 使用固定的替换规则
    "categories": lambda value, lang: front_matter_replace(value, lang),
    "tags": lambda value, lang: front_matter_replace(value, lang),
    
    # 未添加的字段将默认不翻译
}

def split_content_and_codeblocks(text):
    pattern = r'(```[\s\S]*?```)'
    parts = re.split(pattern, text)
    return [{'type': 'code' if i % 2 else 'text', 'content': part.strip()} for i, part in enumerate(parts) if part.strip()]

# 定义调用 ChatGPT API 翻译的函数
def translate_text(text, lang, type):
    logging.info(f"开始翻译文本，语言：{lang}，类型：{type}")
    target_lang = {
        "zh": "Chinese"
    }[lang]
    
    logging.info(f"输入文本：\n{text}")
    
    if type == "front-matter":
        system_content = "You are a professional translation engine, please translate the text into a colloquial, professional, elegant and fluent content, without the style of machine translation. You must only translate the text content, never interpret it."
    elif type == "main-body":
        system_content = "You are a professional translation engine, please translate the text into a colloquial, professional, elegant and fluent content, without the style of machine translation. You must maintain the original markdown format. You must not translate the `[to_be_replace[x]]` field.You must only translate the text content, never interpret it."
    
    logging.info(f"系统提示：\n{system_content}")
    
    user_content = f"Translate into {target_lang}:\n\n{text}\n"
    
    logging.info(f"用户提示：\n{user_content}")
    
    if USE_OLLAMA:
        try:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": f"{system_content}\n\n{user_content}",
                    "stream": False
                }
            )
            response.raise_for_status()
            output_text = response.json()["response"]
        except requests.RequestException as e:
            logging.error(f"Ollama API调用失败：{str(e)}")
            raise
    else:
        completion = openai.ChatCompletion.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ],
        )
        output_text = completion.choices[0].message.content
    
    logging.info(f"AI 输出：\n{output_text}")
    logging.info("翻译完成")
    return output_text

# Front Matter 处理规则
def translate_front_matter(front_matter, lang):
    translated_front_matter = {}
    for key, value in front_matter.items():
        if key in front_matter_translation_rules:
            processed_value = front_matter_translation_rules[key](value, lang)
        else:
            # 如果在规则列表内，则不做任何翻译或替换操作
            processed_value = value
        translated_front_matter[key] = processed_value
    return translated_front_matter

# 定义文章拆分函数
def split_text(text, max_length):
    # 根据段落拆分文章
    paragraphs = text.split("\n\n")
    output_paragraphs = []
    current_paragraph = ""

    for paragraph in paragraphs:
        if len(current_paragraph) + len(paragraph) + 2 <= max_length:
            # 如果当前段落加上新段落的长度不超过最大长度，就将它们合并
            if current_paragraph:
                current_paragraph += "\n\n"
            current_paragraph += paragraph
        else:
            # 否则将当前段落添加到输出列表中，并重新开始一个新段落
            output_paragraphs.append(current_paragraph)
            current_paragraph = paragraph

    # 将最后一个段落添加到输出列表中
    if current_paragraph:
        output_paragraphs.append(current_paragraph)

    # 将输出段落合并为字符串
    output_text = "\n\n".join(output_paragraphs)

    return output_text

def translate_and_append(chunk, lang, output_paragraphs):
    if chunk:
        # 分割文本和代码块
        parts = split_content_and_codeblocks(chunk)
        translated_parts = []
        for part in parts:
            if part['type'] == 'text':
                translated_text = translate_text(part['content'].strip(), lang, "main-body")
                translated_parts.append(translated_text)
            else:  # 代码块
                translated_parts.append(part['content'])
        
        translated_chunk = "\n\n".join(translated_parts)
        output_paragraphs.append(translated_chunk)

# 定义翻译文的函数
def translate_file(input_file, filename, lang):
    logging.info(f"开始翻译文件：{filename}，目标语言：{lang}")
    sys.stdout.flush()

    # 定义输出文件
    if lang in dir_translated:
        output_dir = dir_translated[lang]
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = os.path.join(output_dir, filename)

    # 读取输入文件内容
    with open(input_file, "r", encoding="utf-8") as f:
        input_text = f.read()

    # 创建一个字典来存储占位词和对应的替换文本
    placeholder_dict = {}

    # 使用 for 循环应用替换规则，并将匹配的文本替换为占位词
    for i, rule in enumerate(replace_rules):
        find_text = rule["orginal_text"]
        replace_with = rule["replaced_text"][lang]
        placeholder = f"[to_be_replace[{i + 1}]]"
        input_text = input_text.replace(find_text, placeholder)
        placeholder_dict[placeholder] = replace_with

    # 删除译文中指示强制翻译的 marker
    input_text = input_text.replace(marker_force_translate, "")

    # 使用正则表达式来匹配 Front Matter
    front_matter_match = re.search(r'---\n(.*?)\n---', input_text, re.DOTALL)
    if front_matter_match:
        front_matter_text = front_matter_match.group(1)
        # 使PyYAML加载YAML格式的数据
        front_matter_data = yaml.safe_load(front_matter_text)

        # 按照前文规则对 Front Matter 进行翻译
        front_matter_data = translate_front_matter(front_matter_data, lang)

        # 将处理完的数据转换回 YAML
        front_matter_text_processed = yaml.dump(
            front_matter_data, allow_unicode=True, default_style=None, sort_keys=False)

        # 暂时删除未处理的 Front Matter
        input_text = input_text.replace(
            "---\n"+front_matter_text+"\n---\n", "")

    # 拆分文章
    paragraphs = input_text.split("\n\n")
    output_paragraphs = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) + 2 <= max_length:
            if current_chunk:
                current_chunk += "\n\n"
            current_chunk += paragraph
        else:
            # 如果当前块不为空，先翻译它
            translate_and_append(current_chunk, lang, output_paragraphs)
            
            # 检查当前段落是否超过最大长度
            if len(paragraph) > max_length:
                # 如果单个段落超过最大长度，按句子拆分
                sentences = re.split(r'(?<=[.!?])\s+', paragraph)
                current_sentence_chunk = ""
                for sentence in sentences:
                    if len(current_sentence_chunk) + len(sentence) <= max_length:
                        current_sentence_chunk += sentence + " "
                    else:
                        # 翻译当前句子块
                        translate_and_append(current_sentence_chunk, lang, output_paragraphs)
                        current_sentence_chunk = sentence + " "
                
                # 处理最后一个句子块
                translate_and_append(current_sentence_chunk, lang, output_paragraphs)
            else:
                # 如果段落没有超过最大长度，直接作为新的当前块
                current_chunk = paragraph

    # 处理最后一个块
    translate_and_append(current_chunk, lang, output_paragraphs)

    # 合并相邻的短块
    merged_paragraphs = []
    temp_chunk = ""
    for paragraph in output_paragraphs:
        if len(temp_chunk) + len(paragraph) + 2 <= max_length:
            if temp_chunk:
                temp_chunk += "\n\n"
            temp_chunk += paragraph
        else:
            if temp_chunk:
                merged_paragraphs.append(temp_chunk)
            temp_chunk = paragraph
    
    if temp_chunk:
        merged_paragraphs.append(temp_chunk)

    # 将输出段落合并为字符串
    output_text = "\n\n".join(merged_paragraphs)

    if front_matter_match:
        # 加Front Matter
        output_text = "---\n" + front_matter_text_processed + "---\n\n" + output_text

    # 最后，将占位词替换为对应的替换文本
    for placeholder, replacement in placeholder_dict.items():
        output_text = output_text.replace(placeholder, replacement)

    # 写入输出文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_text)

    logging.info(f"翻译后的内容已写入文件：{output_file}")

    logging.info(f"文件翻译完成：{filename}")

# 添加日志设置函数
def setup_logging():
    log_dir = "log"
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"translation_log_{current_time}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

# 在主程序开始之前调用 setup_logging 函数
setup_logging()

# 在主程序开始前添加Ollama使用提示
if USE_OLLAMA:
    logging.info(f"使用Ollama本地模型：{OLLAMA_MODEL}")
else:
    logging.info("使用OpenAI API")

# 主程序
try:
    logging.info("开始执行翻译脚本")
    # 按文件名称顺序排序
    file_list = os.listdir(dir_to_translate)
    sorted_file_list = sorted(file_list)

    # 创建一个外部列表文件，存放已处理的 Markdown 文件名列表
    if not os.path.exists(processed_list):
        with open(processed_list, "w", encoding="utf-8") as f:
            print("processed_list created")
            sys.stdout.flush()

    # 遍历目录下的所有.md文件，并进行翻译
    for filename in sorted_file_list:
        if filename.endswith(".md"):
            logging.info(f"处理文件：{filename}")
            input_file = os.path.join(dir_to_translate, filename)

            # 读取 Markdown 文件的内容
            with open(input_file, "r", encoding="utf-8") as f:
                md_content = f.read()

            # 读取processed_list内容
            with open(processed_list, "r", encoding="utf-8") as f:
                processed_list_content = f.read()

            if marker_force_translate in md_content or filename not in processed_list_content:
                # 翻译为中文
                translate_file(input_file, filename, "zh")
            elif filename in exclude_list:  # 不进行翻译
                print(f"Pass the post in exclude_list: {filename}")
                sys.stdout.flush()
            else:  # 不进行翻译
                print(f"Pass the post in processed_list: {filename}")
                sys.stdout.flush()

            # 将处理完成的文件名加到列表，下次跳过不处理
            if filename not in processed_list_content:
                print(f"Added into processed_list: {filename}")
                with open(processed_list, "a", encoding="utf-8") as f:
                    f.write("\n")
                    f.write(filename)

            # 强制将缓冲区中的数据刷新到终端中，使用 GitHub Action 时方便实时查看过程
            sys.stdout.flush()
            
    logging.info("所有文件处理完成")
    logging.info("Congratulations! All files processed done.")
    sys.stdout.flush()

except Exception as e:
    logging.error(f"发生错误：{str(e)}", exc_info=True)
    raise SystemExit(1)  # 1 表示非正常退出，可以根据需要更改退出码

