call .\env\Scripts\activate.bat
@REM python tools\translater\auto_translater.py --files ue-通过插件源码添加插件.md --langs ko
python tools/translater/auto_translater.py --concurrency=16
@REM python tools\translater\auto_translater.py --files ue-插件-AIChatPlus-Usage-Source-Claude.md --langs en
call .\env\Scripts\deactivate.bat
