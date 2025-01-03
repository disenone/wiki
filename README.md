# wiki

My Blog Built with MkDocs

[wiki.disenone.site](https://wiki.disenone.site/)

Currently Support Three Languages: 中文/English/Español

![wiki](https://github.com/user-attachments/assets/b7f16993-7054-4b87-b359-feec4436e895)

## tools

### translater

使用 AI 自动翻译文章，目前把中文翻译成英文和西班牙文

auto translate article into other languages, currently zh -> en, es

#### 增加语言支持

* 在 tools/auto_translater.py 中的 `Translate_Into` 加上新语言的设置

* 在 mkdocs.yml 的 languages/git-revision-date-localized 字段加上新语言的设置

### push_baidu

自动推送新的文章地址到百度索引

auto push new site into baidu webconsole
