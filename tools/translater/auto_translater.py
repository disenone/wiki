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
import argparse
import copy
try:
	import env	# noqa
except:
	pass

translater_folder = os.path.dirname(__file__)

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

Tips = '此帖子是使用 ChatGPT 翻译的，请在[**反馈**](https://github.com/disenone/wiki_blog/issues/new)中指出任何遗漏之处。'

# region 增加新语言需要改这些内容

Translate_Into = {
	# 繁体中文
	'zh-Hant': {
		'name': 'Traditional Chinese',
		'replace_rules': {
			'--8<-- "footer.md"': '--8<-- "footer_tc.md"',
		},
	},

	# 英语
	'en': {
		'name': 'English',
		'replace_rules': {
			'--8<-- "footer.md"': '--8<-- "footer_en.md"',
		},
	},

	# 西班牙语
	'es': {
		'name': 'Spanish',
		'replace_rules': {
			'--8<-- "footer.md"': '--8<-- "footer_es.md"',
		},
	},

	# 日本语
	'ja': {
		'name': 'Japanese',
		'replace_rules': {
			'--8<-- "footer.md"': '--8<-- "footer_ja.md"',
		},
	},

	# 德语
	'de': {
		'name': 'German',
		'replace_rules': {
			'--8<-- "footer.md"': '--8<-- "footer_de.md"',
		},
	},

	# 法语
	'fr': {
		'name': 'French',
		'replace_rules': {
			'--8<-- "footer.md"': '--8<-- "footer_fr.md"',
		},
	},

	# 阿拉伯语
	'ar': {
		'name': 'Arabic',
		'replace_rules': {
			'--8<-- "footer.md"': '--8<-- "footer_ar.md"',
		},
	},

	# 韩语
	'ko': {
		'name': 'Korean',
		'replace_rules': {
			'--8<-- "footer.md"': '--8<-- "footer_ko.md"',
		},
	},
}

# endregion 增加新语言需要改这些内容

TranslateType_MainBody = 1
TranslateType_FrontMater = 2

TranslateType_Config = {
	TranslateType_MainBody: {
		'model': 'gpt-3.5-turbo',
		'messages': [
			{"role": "system", "content": "You are a professional translation engine, please translate the text into a colloquial, professional, elegant and fluent content, without the style of machine translation. You must only translate the text content, never interpret it. Keep all the characters that you cannot translate. Do not say anything else. Do not explain them."},	# noqa
			{"role": "user", "content": "Translate these text into {lang_name} language:\n\n{text}\n"},
		]
	},

	# Front Matter 与正文内容使用不同的 prompt 翻译
	TranslateType_FrontMater: {
		'model': 'gpt-3.5-turbo',
		'messages': [
			{"role": "system", "content": "You are a professional translation engine, please translate the text into a colloquial, professional, elegant and fluent content, without the style of machine translation. You must maintain the original markdown format. You must only translate the text content, never interpret it. Keep all the characters that you cannot translate. Do not say anything else. Do not add any other character. Do not explain them. Keep the original meaning, Do not add any hint or warning or error, do not add any markdown code snippets. You must translate the punctuation."},	# noqa
			{"role": "user", "content": "Translate these text into {lang_name} language:\n\n{text}\n"},
		]
	}
}

# 不进行翻译的文件列表
exclude_list = ['baidu_verify_codeva-S4d2IcuRUu.html']  # 不进行翻译的文件列表

# 已处理的 Markdown 文件名的列表，会自动生成，格式 {{file_name: {modify_time:xxx, git_ref:xxx}}}，优先判断 git_ref，如果没有 git_ref，则判断修改时间
processed_dict_file = os.path.join(translater_folder, "processed_dict.txt")

# 强制指定翻译的文件，其他文件都不翻译，方便对某文件测试
only_list = [
	# 'test2.md',
	# 'cpp-C和Cpp宏编程解析.md',
	# 'cpp-编写Windows下的MemoryLeakDetector.md',
	# 'test3.md',
	# 'ue-使用路径形式扩展菜单.md',
]
code_flag = '```'
skip_line_startswith = [code_flag, '<detail>', '</detail>', '<meta property']  # 跳过以这些字符开始的行，简单复制粘贴到结果中

# 文章使用英文撰写的提示，避免本身为英文的文章被重复翻译为英文
marker_written_in_en = "\n> This post was originally written in English.\n"
# 即使在已处理的列表中，仍需要重新翻译的标记
marker_force_translate = "\n<!-- translate -->\n"
# 含有这个标记，则不翻译文件
marker_no_translate = '<!-- no translate -->'

# 段落内 begin end 包住的内容不翻译
marker_no_translate_begin = '<!-- no translate begin -->'
marker_no_translate_end = '<!-- no translate end -->'

# 正则匹配链接
marker_link_pattern = re.compile(r'(\[.*?\])(\(.*?\))')

# Front Matter 处理规则
front_matter_translation_rules = {
	# 调用 ChatGPT 自动翻译
	"title": lambda value, lang: translate_text(value, lang, TranslateType_FrontMater),
	"description": lambda value, lang: translate_text(value, lang, TranslateType_FrontMater),

	# 使用固定的替换规则
	"categories": lambda value, lang: front_matter_replace(value, lang),
	"tags": lambda value, lang: front_matter_replace(value, lang),

	# 未添加的字段将默认不翻译
}


# Front Matter 固定字段替换规则。
front_matter_replace_rules = [
	# {
	# 	"orginal_text": "类别 1",
	# 	"replaced_text": {
	# 		"en": "Categories 1",
	# 		"es": "Categorías 1",
	# 		"ar": "الفئة 1",
	# 	}
	# },
	# {
	# 	"orginal_text": "类别 2",
	# 	"replaced_text": {
	# 		"en": "Categories 2",
	# 		"es": "Categorías 2",
	# 		"ar": "الفئة 2",
	# 	}
	# },
	# {
	# 	"orginal_text": "标签 1",
	# 	"replaced_text": {
	# 		"en": "Tags 1",
	# 		"es": "Etiquetas 1",
	# 		"ar": "بطاقة 1",
	# 	}
	# },
	# {
	# 	"orginal_text": "标签 2",
	# 	"replaced_text": {
	# 		"en": "Tags 2",
	# 		"es": "Etiquetas 2",
	# 		"ar": "بطاقة 2",
	# 	}
	# },
]

##############################


def get_output_path(lang):
	return 'docs/' + lang


LOG_CONFIGED = False


def log(*msg, level=logging.INFO):
	global LOG_CONFIGED
	if not LOG_CONFIGED:
		logging.basicConfig(
			level=LOG_LEVEL,
			format='[%(asctime)s] %(message)s',
			datefmt='%Y-%m-%d %H:%M:%S',
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
	if not line:
		return True
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
	if not text:
		return text

	if is_skip_line(text):
		return text

	if text.isspace():
		return text

	if marker_no_translate_begin in text and text.count(marker_no_translate_begin) == text.count(marker_no_translate_end):
		if text.count(marker_no_translate_begin) != text.count(marker_no_translate_end):
			raise RuntimeError('count marker_no_translate_begin != marker_no_translate_end: %s' % text)

		output_text = ''
		while text:
			begin = text.find(marker_no_translate_begin)
			if begin >= 0:
				end = text.find(marker_no_translate_end)
				if end <= begin:
					raise RuntimeError('index marker_no_translate_end <= marker_no_translate_begin: %s' % text)

				output_text += translate_text(text[:begin], lang, type)
				if output_text.endswith('\n') and text[begin - 1] != '\n':
					output_text = output_text[:-1]
				output_text += text[begin:end + len(marker_no_translate_end)]
				text = text[end + len(marker_no_translate_end):]
			else:
				output_text += translate_text(text, lang, type)
				text = ''
		return output_text

	# 链接
	link_match = marker_link_pattern.search(text)
	if link_match:
		link_text = link_match.group(1)
		link_url = link_match.group(2)
		output_text = translate_text(text[:link_match.start() + len(link_text)], lang, type)
		if not output_text.endswith(']'):
			output_text = output_text[:output_text.rfind(']') + 1]
		output_text += link_url
		output_text += translate_text(text[link_match.end():], lang, type)
		return output_text

	# 标题
	if text.startswith('#'):
		return '#' + translate_text(text[1:], lang, type)

	log('translate_text0:', repr(text), lang, type, level=logging.DEBUG)
	lang_name = Translate_Into[lang]['name']

	messages = copy.deepcopy(TranslateType_Config[type]['messages'])
	for message in messages:
		message['content'] = message['content'].format(lang_name=lang_name, text=text)

	completion = openai_client.chat.completions.create(
		model=TranslateType_Config[type]['model'],
		messages=messages,
	)

	log('translate_text1:', completion, level=logging.DEBUG)

	# 获取翻译结果
	output_text = completion.choices[0].message.content
	new_output_text = []
	for line in output_text.split('\n'):
		if not line.startswith(code_flag):
			new_output_text.append(line)
	output_text = '\n'.join(new_output_text)
	if text.startswith('> ') and not output_text.startswith('> '):
		output_text = '> ' + output_text
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
	if lang not in Translate_Into:
		return
	filename = os.path.basename(input_file)
	if only_list and filename not in only_list:
		return

	lang_name = Translate_Into[lang]['name']
	log(f"Translating into [{lang_name}]: {filename}")
	sys.stdout.flush()

	# 定义输出文件
	if lang in Translate_Into:
		output_dir = get_output_path(lang)
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)
		output_file = os.path.join(working_folder, output_dir, filename)

	# 读取输入文件内容
	with open(input_file, "r", encoding="utf-8") as f:
		input_text = f.read()

	# 创建一个字典来存储占位词和对应的替换文本
	placeholder_dict = {}

	# 使用 for 循环应用替换规则
	for origin_text, replace_text in Translate_Into[lang].get('replace_rules', {}).items():
		input_text = input_text.replace(origin_text, replace_text)

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
		input_text = input_text.replace("---\n" + front_matter_text + "\n---\n", "")
	else:
		# log("没有找到front matter，不进行处理。")
		pass

	# log(input_text) # debug 用，看看输入的是什么

	# 拆分文章
	paragraphs = input_text.split("\n")

	input_text = ""
	output_paragraphs = []
	current_paragraph = ""

	next_percent = 10
	for idx, paragraph in enumerate(paragraphs):
		if is_skip_line(paragraph):
			output_paragraphs.append(paragraph)
		else:
			output_paragraphs.append(translate_text(paragraph, lang, TranslateType_MainBody))

		percent = float(idx) / len(paragraphs) * 100
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
			output_paragraphs.append(translate_text(current_paragraph, lang, TranslateType_MainBody))

	# 如果还有未翻译的文本，就将它们添加到输出列表中
	if input_text:
		output_paragraphs.append(translate_text(input_text, lang, TranslateType_MainBody))

	log('progress: 100%%')
	# 将输出段落合并为字符串
	output_text = "\n".join(output_paragraphs)

	if front_matter_match:
		# 加入 Front Matter
		output_text = "---\n" + front_matter_text_processed + "---\n\n" + output_text

	tips = translate_text(Tips, lang, TranslateType_MainBody)
	if tips:
		tips = '\n\n> %s \n' % tips
		output_text += tips

	# 最后，将占位词替换为对应的替换文本
	for placeholder, replacement in placeholder_dict.items():
		output_text = output_text.replace(placeholder, replacement)

	# 写入输出文件
	with open(output_file, "w", encoding="utf-8") as f:
		f.write(output_text)


def GetGitRef(input_file):
	repo = git.Repo('.')
	git_log = repo.git.log(input_file, date='format:%Y%m%d', max_count=1, pretty='format:{"commit":"%h","date":"%cd","summary":"%s"}')	# noqa
	if not git_log:
		return
	log(git_log, level=logging.DEBUG)
	return json.loads(git_log)['commit']


def CreateProcessInfo(input_file):
	info = {}
	git_ref = GetGitRef(input_file)
	if git_ref:
		info['git_ref'] = git_ref
	info['mtime'] = os.stat(input_file).st_mtime
	return info


def NeedProcess(working_folder, precessed_dict, input_file, lang):
	if lang not in Translate_Into:
		return False

	if not input_file.endswith('.md'):
		return False

	filename = os.path.basename(input_file)

	output_filename = os.path.join(working_folder, get_output_path(lang), filename)

	log(f"Checking [{input_file}] to [{lang}], output [{output_filename}]")

	if only_list:
		return filename in only_list

	# 读取 Markdown 文件的内容
	with open(input_file, "r", encoding="utf-8") as f:
		md_content = f.read()

	if marker_no_translate in md_content:
		log(f"Pass the post with content {marker_no_translate}: {filename}")
		sys.stdout.flush()
		return False

	if marker_written_in_en in md_content:  # 翻译为除英文之外的语言
		log(f"Pass the en-en translation: {filename}")
		sys.stdout.flush()
		if lang == 'en':
			return False

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

	elif filename in precessed_dict and os.path.exists(output_filename):
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
		log(f"Pass the post in processed_list [{filename}] to [{lang}]")
		sys.stdout.flush()

	else:  # 翻译为所有语言
		return True


def run(working_folder):
	parser = argparse.ArgumentParser()
	parser.add_argument('--list', action='store_true', default=False, help='only list files, not translate')
	parser.add_argument('--files', type=str, nargs='+', help='translate specific multi files')
	parser.add_argument('--langs', type=str, nargs='+', help='translate files into specific langs', choices=Translate_Into.keys())	# noqa
	args = parser.parse_args()

	# 按文件名称顺序排序
	dir_to_translate_abs = os.path.abspath(os.path.join(working_folder, dir_to_translate))
	file_list = os.listdir(dir_to_translate_abs)
	file_list = sorted(file_list)
	file_list = [os.path.join(dir_to_translate_abs, file) for file in file_list]
	# log(sorted_file_list)

	# 指定文件
	force = False
	if args.files:
		new_file_list = [os.path.join(dir_to_translate_abs, file) for file in args.files]
		for file in new_file_list:
			if file not in file_list:
				raise ValueError('file [%s] not found' % file)
		file_list = new_file_list
		force = True

	# 指定翻译语言
	translate_langs = Translate_Into.keys()
	if args.langs:
		for lang in args.langs:
			if lang not in translate_langs:
				raise ValueError('lang [%s] is not supported' % lang)
		translate_langs = args.langs

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
		has_translated = False
		for lang in translate_langs:
			if force or NeedProcess(working_folder, processed_dict, input_file, lang):
				log('find file translate to [%s]: %s' % (Translate_Into[lang]['name'], input_file))
				log('old processed_info: %s' % (processed_dict.get(os.path.basename(input_file)), ))
				new_info = CreateProcessInfo(input_file)
				log('new processed_info: %s' % (new_info, ))
				if not args.list:
					translate_file(working_folder, input_file, lang)
					has_translated = True

			# 强制将缓冲区中的数据刷新到终端中，使用 GitHub Action 时方便实时查看过程
			sys.stdout.flush()

		if not args.list and has_translated:
			processed_dict[os.path.basename(input_file)] = CreateProcessInfo(input_file)

	if not args.list:
		with open(processed_dict_file, 'wb') as f:
			f.write(json.dumps(processed_dict, indent=2, ensure_ascii=False).encode('utf-8'))

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
