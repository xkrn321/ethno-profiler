# EthnoProfiler

一个用于民族药文献探索的 Python 小工具：按药材名称和预设主题向 PubMed 查询题录数量，导出便于初步查看的计数表和热图。

这是一个个人研究原型，适合帮助整理检索线索和讨论下一步查证方向。它不执行系统综述，也不评价研究质量、临床有效性或作用机制。

## 可以做什么

- 按拉丁药材名查询 PubMed 题录数量。
- 按胃肠、炎症、氧化应激、神经调节和黏膜等宽泛主题整理计数。
- 输出结果表和热图，供研究者继续筛选原文。
- 根据需要调整查询式和主题维度。

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
ethno-profiler "Zingiber officinale" --names "干姜" --output counts.tiff
```

也可以从 Python 调用：

```python
from ethno_profiler import Profiler

profiler = Profiler()
result = profiler.profile([("Zingiber officinale", "干姜")])
profiler.print_report(result)
profiler.plot_heatmap(result, "counts.tiff")
```

## 结果怎么读

图表展示的是检索式返回的题录数量，不是“证据强弱”或药效评分。结果会受药材同物异名、拉丁名写法、检索式范围和 PubMed 更新影响。零条结果只表示当前检索式没有找到题录，不能据此推断药材无效或没有研究。

每条线索仍需回到题录和原文核实物种、制备方法、研究对象、实验设计与结果。涉及药理结论时，应由研究团队按预先定义的标准人工筛选和评价。

## 当前边界

- 查询面向 PubMed 题录；目前只做数量检索和可视化，不抓取全文。
- 主题检索式是初步版本，正式研究前应与领域研究者一起修订并记录检索日期。
- 目前没有系统处理药材同义词、复方暴露、重复发表或偏倚风险。
- 网络请求失败时需要检查连接后重新查询；请保存检索日期和实际查询式以便复核。

## 技术

Python、PubMed E-utilities、NumPy、Matplotlib。

## 许可

MIT License，见 [LICENSE](LICENSE)。
