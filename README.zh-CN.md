# Codex 研究工作流 Skills

[English](README.md)

这是一套面向机器学习、遥感与地理空间科研的 Codex 工作流 Skills。它把研究问题一致性、数据泄漏、地理空间数据质量、实验执行、实验复核和科研结论审查连接为可追溯的 Gate 链，帮助研究者避免协议漂移、测试集泄漏，以及将 smoke 或探索性结果误写为正式科研结论。

适合需要冻结实验协议、按事件、区域或时间分组评估，或需要保留配置、随机种子、数据划分、日志与指标证据的研究项目。

## 包含的 Skills

### 研究完整性与可复现性

- research-question-audit — 检查计划或已完成的实验是否仍然回答冻结的研究问题。
- data-leakage-audit — 检查训练集、验证集和测试集之间的时间、空间、分组、预处理、目标、oracle 以及评估泄漏。
- geospatial-data-qc — 检查地理空间数据的 CRS、基准、单位、网格对齐、nodata 和时间兼容性。
- experiment-runner — 只有在必要的研究审计 Gate 通过后才执行可复现实验。
- experiment-audit — 独立复核实验的协议合规性、产物完整性、可复现性和评估完整性。
- research-evidence-review — 判断经过验证的实验是否足以支持提出的科研结论。

### 文化解释与表达

- fengshui-cultural-analysis — 使用可复现的 GIS 指标解释传统风水空间概念，但不预测确定吉凶。
  - 明确分离客观空间指标与传统文化解释。
  - 支持地形、水文、水系关系、围合度、启发式指数、敏感性、不确定性和限制说明。
  - 缺少可选数据时，尽可能只降级受影响的指标。
- catgirl-research-companion — 使用 gentle、tsundere 或 sarcastic 风格渲染已有的结构化研究结果，但不改变事实。
  - 只负责自然语言表达。
  - 结构化结果、指标、Gate、证据等级、不确定性、限制和结论保持 immutable。
  - 自动测试验证不同风格可以产生不同文本，但抽取后的结构化事实完全一致。

## Gate 链

对于受研究协议约束的工作，使用以下顺序。前一个 Gate 未解决时，后续状态不得将其升级为通过。

```text
research-question-audit PASS
        + data-leakage-audit PASS
        + geospatial-data-qc PASS
                    ↓
       experiment-runner RUN_COMPLETE
                    ↓
        experiment-audit VALID
                    ↓
 research-evidence-review claim classification
```

RUN_COMPLETE 只表示批准的运行及其产物已经完成。VALID 只表示运行具有足够证据并符合协议。两者都不能单独证明科研结论成立。

## 安装

将 Skill 目录复制到 Codex 全局 Skills 目录：

```text
<CODEX_HOME>/skills/<skill-name>/
```

重新启动 Codex 或开始新的任务，使新的 Skill 元数据被发现。对于高影响的 Gate，建议显式调用 Skill，例如：

```text
$data-leakage-audit Audit the proposed experiment before execution and return one gate decision.
```

## 包含的辅助工具

- data-leakage-audit/scripts/check_split_overlap.py — 检查 CSV 清单中的精确 ID、可选分组以及四舍五入坐标重叠候选。该脚本只读运行，不能单独证明空间独立性。
- geospatial-data-qc/scripts/inspect_raster_metadata.py — 读取 GeoTIFF 元数据并将候选栅格与参考栅格比较。需要 rasterio，且不能单独证明垂直基准、语义或时间兼容性。
- experiment-runner/references/e2e-gate-chain.md — 展示完整的协议约束型准入、执行、实验复核和证据审查流程。

## 可运行的合成样例

examples/ 目录包含极小的完全合成输入、预期摘要和验证器，展示一个划分重叠问题和一个栅格网格不一致问题，不使用真实科研数据。

```text
python examples/verify_examples.py --split-only
python -m pip install rasterio
python examples/verify_examples.py
```

参见 [examples/README.md](examples/README.md)，了解直接运行命令、预期退出码和解释边界。

## 范围与限制

这些内容是工作流说明和轻量级证据辅助工具，不能替代冻结的研究协议、领域审查或独立统计验证。它们保留原始数据，并要求基于证据作出判断。

fengshui-cultural-analysis 提供的是空间模式的可复现文化解释，不是占卜、科学因果模型或确定吉凶预测。catgirl-research-companion 只改变表达方式，不得修改结构化研究事实。

## 许可证

MIT，详见 [LICENSE](LICENSE)。
