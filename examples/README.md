# Runnable synthetic examples

这些样例用于展示仓库内两个只读辅助脚本的输入、预期结果和解释边界。所有 CSV 与 GeoTIFF 都是人为构造的极小合成数据，不能用于科学结论、精度比较或模型训练。

`expected-summary.json` 记录稳定的关键字段，而不是完整原始输出；这样文件路径和运行系统的差异不会造成无意义的比对失败。

## 一键验证

在仓库根目录运行：

```text
python examples/verify_examples.py --split-only
```

这会验证 CSV 划分重叠样例，不依赖第三方库。要同时验证 GeoTIFF 样例，先安装 `rasterio`：

```text
python -m pip install rasterio
python examples/verify_examples.py
```

验证器本身会把两个“预期发现问题”的辅助脚本退出码 `2` 视为通过，并只在输出与预期摘要不一致时失败。

## 1. Split-overlap sample

目录：[`split-overlap/`](split-overlap/)

- `train.csv`、`validation.csv`、`test.csv`：每个文件仅两行。
- `test.csv` 与训练集共享 `sample_id=t2`。
- 验证集与训练集在将坐标舍入到 6 位小数后共享一个坐标。
- `event_id` 没有精确重叠，说明“没有发现组重叠”不等于整个划分安全。

直接运行：

```text
python data-leakage-audit/scripts/check_split_overlap.py --train examples/split-overlap/train.csv --validation examples/split-overlap/validation.csv --test examples/split-overlap/test.csv --id-column sample_id --group-column event_id --x-column x --y-column y --fail-on-overlap
```

预期：输出 `CANDIDATE_OVERLAP_FOUND`，并以退出码 `2` 结束。这是正确的保护性行为；它只是重叠候选证据，仍需结合冻结协议确认泄漏边界。

## 2. Raster-alignment sample

目录：[`raster-alignment/`](raster-alignment/)

- 三个文件均为 2×2、EPSG:4326、float32 的合成 GeoTIFF。
- `matching.tif` 与 `reference.tif` 网格元数据一致。
- `shifted.tif` 的仿射变换平移 0.5 个单位，因此与参考栅格不兼容。

直接运行（需要 `rasterio`）：

```text
python geospatial-data-qc/scripts/inspect_raster_metadata.py examples/raster-alignment/reference.tif examples/raster-alignment/matching.tif examples/raster-alignment/shifted.tif --reference examples/raster-alignment/reference.tif --strict
```

预期：`matching.tif` 为 `MATCH`，`shifted.tif` 为 `DIFFERENT`，整体为 `DIFFERENCES_FOUND`，并以退出码 `2` 结束。该检查只比较有限元数据，不能证明垂直基准、语义、时间或覆盖范围兼容。
