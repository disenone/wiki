# -*- coding: utf-8 -*-
import os
from openai import OpenAI
import sys
import re
import yaml  # pip install PyYAML
import json
import git
import logging
import functools
try:
    import env
except:
    pass

# 日志
LOG_LEVEL = logging.INFO

# 设置 OpenAI API Key 和 API Base 参数，通过 env.py 传入
openai_client = OpenAI(
    api_key=os.environ.get("CHATGPT_API_KEY"),
    base_url=os.environ.get("CHATGPT_API_BASE"),
)

# 设置最大输入字段，超出会拆分输入，防止超出输入字数限制
max_length = 1800

# 设置翻译的路径
dir_to_translate = "docs/zh"
dir_translate_to = {"en": "docs/en", }

# 不进行翻译的文件列表
exclude_list = ["index.md", "contact-and-subscribe.md", "WeChat.md"]  # 不进行翻译的文件列表
processed_dict_file = "tools/processed_dict.txt"  # 已处理的 Markdown 文件名的列表，会自动生成，格式 {{file_name: {modify_time:xxx, git_ref:xxx}}}，优先判断 git_ref，如果没有 git_ref，则判断修改时间
only_list = [         # 强制指定翻译的文件，其他文件都不翻译，方便对某文件测试
    # 'test2.md',
    # 'cpp-C和Cpp宏编程解析.md',
    # 'cpp-编写Windows下的MemoryLeakDetector.md',
    # 'test3.md',
]
code_flag = '```'
skip_line_startswith = [code_flag, '<detail>', '</detail>', '<meta property']  # 跳过以这些字符开始的行，简单复制粘贴到结果中


# 由 ChatGPT 翻译的提示
tips_translated_by_chatgpt = {
    "en": "\n\n> This post is translated using ChatGPT, please [**feedback**](https://github.com/disenone/wiki/issues/new) if any omissions.\n",
    "es": "\n\n> Este post está traducido usando ChatGPT, por favor [**feedback**](https://github.com/disenone/wiki/issues/new) si hay alguna omisión.\n",
    "ar": "\n\n> تمت ترجمة هذه المشاركة باستخدام ChatGPT، يرجى [**تزويدنا بتعليقاتكم**](https://github.com/disenone/wiki/issues/new) إذا كانت هناك أي حذف أو إهمال.\n"
}

# 文章使用英文撰写的提示，避免本身为英文的文章被重复翻译为英文
marker_written_in_en = "\n> This post was originally written in English.\n"
# 即使在已处理的列表中，仍需要重新翻译的标记
marker_force_translate = "\n[translate]\n"

# Front Matter 处理规则
front_matter_translation_rules = {
    # 调用 ChatGPT 自动翻译
    "title": lambda value, lang: translate_text(value, lang,"front-matter"),
    "description": lambda value, lang: translate_text(value, lang,"front-matter"),
    
    # 使用固定的替换规则
    "categories": lambda value, lang: front_matter_replace(value, lang),
    "tags": lambda value, lang: front_matter_replace(value, lang),
    
    # 未添加的字段将默认不翻译
}

# 固定字段替换规则。文章中一些固定的字段，不需要每篇都进行翻译，且翻译结果可能不一致，所以直接替换掉。
replace_rules = [
    {
        # 版权信息手动翻译
        "orginal_text": "> 原文地址：<https://disenone.github.io/wiki>",
        "replaced_text": {
            "en": "> Original: <https://disenone.github.io/wiki>",
            "es": "> Dirección original del artículo: <https://disenone.github.io/wiki>",
            "ar": "> عنوان النص: <https://disenone.github.io/wiki>",
        }
    },
    {
        # 版权信息手动翻译
        "orginal_text": "> 本篇文章受 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh) 协议保护，转载请注明出处。",
        "replaced_text": {
            "en": "> This post is protected by [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by/4.0/deed.en) agreement, should be reproduced with attribution.",
            "es": "> Este artículo está protegido por la licencia [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh). Si desea reproducirlo, por favor indique la fuente.",
            "ar": "> يتم حماية هذا المقال بموجب اتفاقية [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh)، يُرجى ذكر المصدر عند إعادة النشر.",
        }
    },
    {
        # snippet
        "orginal_text": '--8<-- "footer.md"',
        "replaced_text": {
            "en": '--8<-- "footer_en.md"'
        }
    }
]

# Front Matter 固定字段替换规则。
front_matter_replace_rules = [
    {
        "orginal_text": "类别 1",
        "replaced_text": {
            "en": "Categories 1",
            "es": "Categorías 1",
            "ar": "الفئة 1",
        }
    },
    {
        "orginal_text": "类别 2",
        "replaced_text": {
            "en": "Categories 2",
            "es": "Categorías 2",
            "ar": "الفئة 2",
        }
    },
    {
        "orginal_text": "标签 1",
        "replaced_text": {
            "en": "Tags 1",
            "es": "Etiquetas 1",
            "ar": "بطاقة 1",
        }
    },
    {
        "orginal_text": "标签 2",
        "replaced_text": {
            "en": "Tags 2",
            "es": "Etiquetas 2",
            "ar": "بطاقة 2",
        }
    },
]

##############################


LOG_CONFIGED = False
def log(*msg, level=logging.INFO):
    global LOG_CONFIGED
    if not LOG_CONFIGED:
        logging.basicConfig(
            level    = LOG_LEVEL,
            format   = '[%(asctime)s] %(message)s',
            datefmt  = '%Y-%m-%d %H:%M:%S',
        )
        LOG_CONFIGED = True

    if len(msg) > 1:
        msg = ' '.join([str(m) for m in msg])
    else:
        msg = msg[0]
    logging.log(level, msg)


# 对 Front Matter 使用固定规则替换的函数
def front_matter_replace(value, lang):
    for index in range(len(value)):
        element = value[index]
        # log(f"element[{index}] = {element}")
        for replacement in front_matter_replace_rules:
            if replacement["orginal_text"] in element:
                # 使用 replace 函数逐个替换
                element = element.replace(
                    replacement["orginal_text"], replacement["replaced_text"][lang])
        value[index] = element
        # log(f"element[{index}] = {element}")
    return value


def retry_except(times=3):
    def _retry(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times - 1):
                try:
                    return func(*args, **kwargs)
                except:
                    continue
            return func(*args, **kwargs)
        return wrapper
    return _retry
        

def is_skip_line(line):
    if line.isspace():
        return False
    if line.isascii():
        return True
    for skip in skip_line_startswith:
        if line.startswith(skip):
            return True
    return False


# 定义调用 ChatGPT API 翻译的函数
@retry_except(3)
def translate_text(text, lang, type):    
    if is_skip_line(text):
        return text
    
    if text.isspace():
        return text
    
    log('translate_text0:', repr(text), level=logging.DEBUG)
    target_lang = {
        "en": "English",
        "es": "Spanish",
        "ar": "Arabic"
    }[lang]
    
    # Front Matter 与正文内容使用不同的 prompt 翻译
    # 翻译 Front Matter。
    if type == "front-matter":
        completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional translation engine, please translate the text into a colloquial, professional, elegant and fluent content, without the style of machine translation. You must only translate the text content, never interpret it. Keep all the characters that you cannot translate. Do not say anything else. Do not explain them."},
                {"role": "user", "content": f"Translate these text into {target_lang} language:\n\n{text}\n"},
            ],
        )  
    # 翻译正文
    elif type== "main-body":
        completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional translation engine, please translate the text into a colloquial, professional, elegant and fluent content, without the style of machine translation. You must maintain the original markdown format. You must not translate the `[to_be_replace[x]]` field. You must only translate the text content, never interpret it. Keep all the characters that you cannot translate. Do not say anything else. Do not add any other character. Do not explain them. Keep the original meaning, Do not add any hint or warning or error, do not add any markdown code snippets."},
                {"role": "user", "content": f"Translate these text into {target_lang} language:\n\n{text}\n"},
            ],
        )

    log('translate_text1:', completion, level=logging.DEBUG)

    # 获取翻译结果
    output_text = completion.choices[0].message.content
    new_output_text = []
    for line in output_text.split('\n'):
        if not line.startswith(code_flag):
            new_output_text.append(line)
    output_text = '\n'.join(new_output_text)
    log('translate_text2:', repr(output_text), level=logging.DEBUG)

    sys.stdout.flush()
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
        # log(key, ":", processed_value)
    return translated_front_matter


# 定义翻译文件的函数
def translate_file(working_folder, input_file, lang):
    if lang not in dir_translate_to:
        return
    filename = os.path.basename(input_file)
    if only_list and filename not in only_list:
        return
    
    log(f"Translating into {lang}: {filename}")
    sys.stdout.flush()

    # 定义输出文件
    if lang in dir_translate_to:
        output_dir = dir_translate_to[lang]
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = os.path.join(working_folder, output_dir, filename)

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

    # 删除其他出英文外其他语言译文中的 marker_written_in_en
    if lang != "en":
        input_text = input_text.replace(marker_written_in_en, "")

    # 使用正则表达式来匹配 Front Matter
    front_matter_match = re.search(r'---\n(.*?)\n---', input_text, re.DOTALL)
    if front_matter_match:
        front_matter_text = front_matter_match.group(1)
        # 使用PyYAML加载YAML格式的数据
        front_matter_data = yaml.safe_load(front_matter_text)

        # 按照前文的规则对 Front Matter 进行翻译
        front_matter_data = translate_front_matter(front_matter_data, lang)

        # 将处理完的数据转换回 YAML
        front_matter_text_processed = yaml.dump(
            front_matter_data, allow_unicode=True, default_style=None, sort_keys=False)

        # 暂时删除未处理的 Front Matter
        input_text = input_text.replace(
            "---\n"+front_matter_text+"\n---\n", "")
    else:
        # log("没有找到front matter，不进行处理。")
        pass

    # log(input_text) # debug 用，看看输入的是什么

    # 拆分文章
    paragraphs = input_text.split("\n")

    input_text = ""
    output_paragraphs = []
    current_paragraph = ""

    translate_idx = 0
    next_percent = 10
    for idx, paragraph in enumerate(paragraphs):
        if is_skip_line(paragraph):
            translate_idx = idx
            current_paragraph and output_paragraphs.append(translate_text(current_paragraph, lang,"main-body"))
            output_paragraphs.append(paragraph)
            current_paragraph = ''
        elif len(current_paragraph) + len(paragraph) + 2 <= max_length:
            # 如果当前段落加上新段落的长度不超过最大长度，就将它们合并
            if current_paragraph:
                current_paragraph += "\n"
            current_paragraph += paragraph
        else:
            # 否则翻译当前段落，并将翻译结果添加到输出列表中
            translate_idx = idx
            output_paragraphs.append(translate_text(current_paragraph, lang,"main-body"))
            current_paragraph = paragraph
        percent = float(translate_idx) / len(paragraphs) * 100
        if percent >= next_percent:
            log('progress: %.1f%%' % percent)
            next_percent = int(percent) - int(percent) % 10 + 10

    # 处理最后一个段落
    if current_paragraph:
        if input_text and len(current_paragraph) + len(input_text) <= max_length:
            # 如果当前段落加上之前的文本长度不超过最大长度，就将它们合并
            input_text += "\n" + current_paragraph
        else:
            # 否则翻译当前段落，并将翻译结果添加到输出列表中
            output_paragraphs.append(translate_text(current_paragraph, lang,"main-body"))

    # 如果还有未翻译的文本，就将它们添加到输出列表中
    if input_text:
        output_paragraphs.append(translate_text(input_text, lang,"main-body"))

    log('progress: 100%%')
    # 将输出段落合并为字符串
    output_text = "\n".join(output_paragraphs)

    if front_matter_match:
        # 加入 Front Matter
        output_text = "---\n" + front_matter_text_processed + "---\n\n" + output_text

    # 加入由 ChatGPT 翻译的提示
    if lang == "en":
        output_text = output_text + tips_translated_by_chatgpt["en"]
    elif lang == "es":
        output_text = output_text + tips_translated_by_chatgpt["es"]
    elif lang == "ar":
        output_text = output_text + tips_translated_by_chatgpt["ar"]

    # 最后，将占位词替换为对应的替换文本
    for placeholder, replacement in placeholder_dict.items():
        output_text = output_text.replace(placeholder, replacement)

    # 写入输出文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_text)


def GetGitRef(input_file):
    repo = git.Repo('.')
    git_log = repo.git.log(input_file, date='format:%Y%m%d', max_count=1, pretty='format:{"commit":"%h","date":"%cd","summary":"%s"}')
    if not git_log:
        return
    return json.loads(git_log)['commit']
    

def CreateProcessInfo(input_file):
    info = {}
    git_ref = GetGitRef(input_file)
    if git_ref:
        info['git_ref'] = git_ref
    info['mtime'] = os.stat(input_file).st_mtime
    return info

def NeedProcess(precessed_dict, input_file, lang):
    if lang not in dir_translate_to:
        return False

    if not input_file.endswith('.md'):
        return False

    filename = os.path.basename(input_file)

    if only_list:
        return filename in only_list
    
    # 读取 Markdown 文件的内容
    with open(input_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    if marker_force_translate in md_content:  # 如果有强制翻译的标识，则执行这部分的代码
        if marker_written_in_en in md_content:  # 翻译为除英文之外的语言
            log("Pass the en-en translation: ", filename)
            sys.stdout.flush()
            if lang != 'en':
                return True
            
        else:  # 翻译为所有语言
            return True

    elif filename in exclude_list:  # 不进行翻译
        log(f"Pass the post in exclude_list: {filename}")
        sys.stdout.flush()
        return False

    elif filename in precessed_dict:  
        # 以前翻译过，判断是否有更新
        # 优先判断 git_ref，如果没有 git_ref，则判断修改时间 
        processed_info = precessed_dict[filename]
        git_ref = GetGitRef(input_file)
        if git_ref:
            if git_ref != processed_info.get('git_ref'):
                return True
        else:
            mtime = os.stat(input_file).st_mtime
            if mtime != processed_info.get('mtime'):
                return True
        log(f"Pass the post in processed_list: {filename}")
        sys.stdout.flush()
        
    elif marker_written_in_en in md_content:  # 翻译为除英文之外的语言
        log(f"Pass the en-en translation: {filename}")
        sys.stdout.flush()
        if lang != 'en':
            return True
            
    else:  # 翻译为所有语言
        return True
 

def run(working_folder):
    # 按文件名称顺序排序
    dir_to_translate_abs = os.path.abspath(os.path.join(working_folder, dir_to_translate))
    file_list = os.listdir(dir_to_translate_abs)
    file_list = sorted(file_list)
    file_list = [os.path.join(dir_to_translate_abs, file) for file in file_list]
    # log(sorted_file_list)
    
    # 创建一个外部列表文件，存放已处理的 Markdown 文件名列表
    if not os.path.exists(processed_dict_file):
        with open(processed_dict_file, "w", encoding="utf-8") as f:
            f.write(json.dumps({}))
            log("processed_dict created")
            sys.stdout.flush()

    # 读取processed_dict内容
    with open(processed_dict_file, "r", encoding="utf-8") as f:
        processed_dict_content = f.read()
        processed_dict = json.loads(processed_dict_content)

    # 遍历目录下的所有.md文件，并进行翻译
    for input_file in file_list:
        for lang in dir_translate_to.keys():
            if NeedProcess(processed_dict, input_file, lang):
                translate_file(working_folder, input_file, lang)
                processed_dict[os.path.basename(input_file)] = CreateProcessInfo(input_file)
            # 强制将缓冲区中的数据刷新到终端中，使用 GitHub Action 时方便实时查看过程
            sys.stdout.flush()

    with open(processed_dict_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(processed_dict, indent=2))

    # 所有任务完成的提示
    log("Congratulations! All files processed done.")
    sys.stdout.flush()
    

def main(working_folder='.'):
    try:
        run(working_folder)

    except Exception as e:
        # 捕获异常并输出错误信息
        sys.excepthook(*sys.exc_info())
        log(f"An error has occurred: {e}")
        sys.stdout.flush()
        raise SystemExit(1)  # 1 表示非正常退出，可以根据需要更改退出码
        # os.remove(input_file)  # 删除源文件


if __name__ == '__main__':
    main()
    