# Research Workflow Skills for Codex

Reusable Codex Skills for protocol-governed research, especially machine learning and geospatial experiments.

## 中文简介

这是一套面向机器学习、遥感与地理空间科研的 Codex 工作流 Skills。它把研究问题一致性、数据泄漏、地理空间数据质量、实验执行、实验复核和科研结论审查连接为可追溯的 Gate 链，帮助研究者避免协议漂移、测试集泄漏，以及将 smoke/探索性结果误写为正式科研结论。

适合需要冻结实验协议、按事件/区域/时间分组评估，或需要保留配置、随机种子、数据划分、日志与指标证据的研究项目。

**关键词：** codex-skill · research-workflow · research-integrity · machine-learning · data-leakage · reproducibility · geospatial · remote-sensing · spatial-validation · experiment-tracking · scientific-evidence · 科研工作流 · 数据泄漏 · 可复现研究 · 地理空间数据

## Included Skills

### Research integrity and reproducibility

- research-question-audit — verify that a planned or completed experiment still answers its frozen research question.
- data-leakage-audit — audit train/validation/test, temporal, spatial, group, preprocessing, target, oracle, and evaluation leakage.
- geospatial-data-qc — quality-check geospatial inputs for CRS, datum, units, grid alignment, nodata, and temporal compatibility.
- experiment-runner — run reproducible experiments only after required audit gates pass.
- experiment-audit — independently verify protocol compliance, artifacts, reproducibility, and evaluation integrity.
- research-evidence-review — decide whether a validated experiment supports a proposed scientific claim.

### Cultural interpretation and presentation

- fengshui-cultural-analysis — provide reproducible GIS-based cultural interpretation without definitive auspiciousness predictions.
  - Separates objective spatial metrics from traditional cultural interpretation.
  - Supports terrain, hydrology, water-relationship, enclosure, heuristic scoring, sensitivity, uncertainty, and limitations reporting.
  - Treats missing optional data as a metric-specific degradation where possible.
- catgirl-research-companion — render existing structured research results in gentle, tsundere, or sarcastic styles without changing facts.
  - Presentation-only rendering.
  - Structured results, metrics, gates, evidence levels, uncertainty, limitations, and conclusions remain immutable.
  - Tests verify that prose may differ while structured facts remain identical.

## Gate Chain

For protocol-governed work, use the chain below. A later status must never upgrade an unresolved earlier status.

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

RUN_COMPLETE only means the approved run and its artifacts completed. VALID only means the run is sufficiently evidenced and protocol-compliant. Neither alone proves a scientific claim.

## Installation

Copy a Skill directory into your Codex global Skills directory:

```text
<CODEX_HOME>/skills/<skill-name>/
```

Restart or begin a new Codex task so the new Skill metadata is discovered. For high-consequence gates, invoke the Skill explicitly, for example:

```text
$data-leakage-audit Audit the proposed experiment before execution and return one gate decision.
```

## Included Helpers

- data-leakage-audit/scripts/check_split_overlap.py checks CSV inventories for exact ID, optional group, and rounded-coordinate overlap candidates. It is read-only and does not prove spatial independence.
- geospatial-data-qc/scripts/inspect_raster_metadata.py reads GeoTIFF metadata and compares candidate rasters with a reference. It requires rasterio and does not establish vertical-datum, semantic, or temporal compatibility.
- experiment-runner/references/e2e-gate-chain.md demonstrates a complete protocol-governed admission, execution, audit, and evidence-review sequence.

## Runnable Synthetic Examples

The examples/ directory contains tiny, fully synthetic inputs, expected summaries, and a verifier for two helpers. It demonstrates an expected split-overlap finding and an expected raster-grid mismatch without using any real research data.

```text
python examples/verify_examples.py --split-only
python -m pip install rasterio
python examples/verify_examples.py
```

See [examples/README.md](examples/README.md) for direct commands, expected exit codes, and interpretation limits.

## Scope and Limits

These are workflow instructions and lightweight evidence helpers, not substitutes for a frozen protocol, domain review, or independent statistical validation. They preserve original data and require evidence-backed decisions.

The fengshui-cultural-analysis Skill provides a reproducible cultural interpretation of spatial patterns, not divination, scientific causality, or a definitive auspiciousness prediction. The catgirl-research-companion Skill changes presentation only and must not alter structured research facts.

## License

MIT. See [LICENSE](LICENSE).
