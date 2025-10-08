# 由 LLM 生成的 Minecraft 命令行界面工具集合

For English version, see `[README.md](https://github.com/difficult-to-have-name/llm-mc-tools)` under the same directory.

这是一个由大型语言模型（LLMs）协助开发的与 Minecraft 相关的命令行界面工具集合。这些工具可能在某些时候派得上用场。

## 目录概览
- `log2msg.py`: 解析 Minecraft 日志文件并提取聊天消息，将其以干净的文本格式保存。非常适合过滤日志文件中的噪音，专注于聊天内容。
- `asset_extractor.py`: 从 Minecraft 游戏主体提取资源文件。
- 工作进行中 未来将添加更多（由 LLM 生成的）工具

## 如何运行

每个工具都是一个独立的 Python 脚本。你可以从命令行运行它们。确保你的系统上安装了 Python3。此外，你需要安装一些列在 `requirements.txt` 中的依赖项。使用命令 `pip install -r requirements.txt` 来安装这些依赖项。

例如，要运行 `log2msg.py` 工具，你可以使用如下命令：

```bash
python3 log2msg.py -i path/to/minecraft/logs/latest.log -o path/to/output/clean_chat.txt
```

这会读取指定的 Minecraft 日志文件，并将清理后的聊天消息输出到指定的文本文件中。

## 许可证
本项目根据 MIT 许可证进行许可——DeepSeek 做出了这个选择。有关详细信息，请参阅 `LICENSE` 文件。

## 致谢
嗯……我想我应该感谢那些帮助我编写这些工具的 LLM。没有它们，我可能仍然困在 Minecraft 的世界里，试图弄清楚如何手动提取文件。

- DeepSeek 编写了大部分代码。
- GitHub Copilot 帮助编写了 README 文件并修复了一些小问题。
- 我提出了利用 LLM 来协助开发这些工具的想法。