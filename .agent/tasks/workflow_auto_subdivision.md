# 🔄 自動細分工作流整合文檔

## 概述

本文檔說明如何將自動細分邏輯整合到 Ingest 和 Sort Garden 工作流中，確保知識庫結構隨著內容增長自動優化。

## 核心原則

### 分類大小閾值
- **小型** (< 10 篇): 保持單一資料夾
- **中型** (10-20 篇): 保持單一資料夾，監控
- **大型** (> 20 篇): 建議細分
- **超大型** (> 30 篇): 強烈建議細分

### 細分策略
- 每個類別最多 4 個子類別（避免過度碎片化）
- 每個子類別最少 3 篇筆記（避免過小類別）
- 使用語義聚類，非字母排序
- 保留所有 WikiLinks（必要時更新路徑）

## 工作流整合

### 1. Ingest 工作流

**觸發**: `@Agent run ingest`

**流程**:
```
1. 處理 00_Inbox 檔案
2. 提取內容 (PDF/Image)
3. 確定類別 (讀取 taxonomy.md)
   ↓
4. 檢查子類別 (NEW)
   - 如果 10_Garden/[Category]/ 有子目錄
   - 分析筆記內容
   - 使用關鍵字匹配路由到最佳子類別
   ↓
5. 建立筆記並移動到正確位置
6. 歸檔原始檔案
   ↓
7. 更新索引 (NEW)
   - 執行 tasks/generate_indices.md
   ↓
8. 檢查類別大小 (NEW)
   - 執行 tasks/subdivide.md
   - 如果類別 > 20 篇，生成細分方案
   - 通知使用者
```

**範例輸出**:
```
✅ Processed 5 files
  - Filed "NVIDIA H200 分析" into AI_Tech/AI_Hardware
  - Filed "投資心理學" into Investment

📊 Category Status:
  - AI_Tech/AI_Hardware: 20 notes ⚠️ At threshold
  - Investment: 13 notes ✅ Optimal

🔍 No subdivision needed at this time
```

### 2. Sort Garden 工作流

**觸發**: `@Agent sort garden`

**流程**:
```
1. 分析所有筆記
2. 提出分類方案
3. 使用者批准
   ↓
4. 執行遷移 (Deploy Plan)
   - 建立目錄
   - 移動檔案
   - 更新 taxonomy.md
   ↓
5. 生成索引 (NEW)
   - 為每個類別生成 主題索引.md
   ↓
6. 自動檢查細分需求 (NEW)
   - 執行 tasks/subdivide.md
   - 分析每個類別大小
   - 如果 > 20 篇，生成細分方案
   ↓
7. 呈現細分建議
   - 顯示 [Category]_Subdivision_Plan.md
   - 等待使用者批准
```

**範例輸出**:
```
✅ Garden Restructured
  - AI_Tech: 29 notes
  - Investment: 12 notes

📊 Category Analysis:
  - AI_Tech: 29 notes ⚠️ Exceeds threshold (20)
  - Investment: 12 notes ✅ Optimal size

🔍 Subdivision Recommended:
  - AI_Tech → Proposed 3 subcategories
  - See: AI_Tech_Subdivision_Plan.md for details

Action: Reply "@Agent Deploy AI_Tech Split" to execute
```

## 相關檔案

### 任務定義
- `.agent/tasks/ingest.md` - Ingest 工作流（已更新）
- `.agent/tasks/deploy.md` - Deploy 工作流（已更新）
- `.agent/tasks/subdivide.md` - 自動細分邏輯（新增）
- `.agent/tasks/generate_indices.md` - 索引生成

### 輔助腳本
- `.agent/check_category_sizes.py` - 檢查類別大小
- `.agent/analyze_ai_tech_subcats.py` - 分析子類別（範例）
- `.agent/deploy_ai_tech_split.py` - 部署細分（範例）

### 分類規則
- `.agent/taxonomy.md` - 主要分類定義
- `.agent/.agent/taxonomy.md` - 分類規則（已棄用？）

## 使用範例

### 範例 1: Ingest 自動路由到子類別

**情境**: 新增一篇 NVIDIA GPU 分析

```bash
@Agent run ingest
```

**系統行為**:
1. 分析內容 → 確定類別: AI_Tech
2. 檢查 AI_Tech 有子類別: AI_Hardware, AI_Products, AI_Applications
3. 關鍵字匹配: "NVIDIA", "GPU" → 路由到 AI_Hardware
4. 建立筆記: `10_Garden/AI_Tech/AI_Hardware/NVIDIA_GPU_分析.md`
5. 更新索引: `AI_Tech/AI_Hardware/主題索引.md`
6. 檢查大小: AI_Hardware 現有 20 篇（達到閾值）
7. 報告: "⚠️ AI_Hardware at threshold (20 notes)"

### 範例 2: Sort Garden 觸發自動細分

**情境**: 重組後 AI_Tech 有 29 篇筆記

```bash
@Agent sort garden
# ... 使用者批准分類方案 ...
@Agent Deploy Plan
```

**系統行為**:
1. 執行遷移 → AI_Tech: 29 篇
2. 生成索引
3. **自動檢查**: AI_Tech > 20 篇
4. **生成細分方案**: AI_Tech_Subdivision_Plan.md
5. **呈現給使用者**: 
   ```
   🔍 AI_Tech (29 notes) exceeds threshold
   Proposed subdivision:
     - AI_Hardware (19 notes)
     - AI_Products (4 notes)
     - AI_Applications (6 notes)
   
   Review: AI_Tech_Subdivision_Plan.md
   To execute: @Agent Deploy AI_Tech Split
   ```

### 範例 3: 手動檢查類別大小

```bash
@Agent Check Category Sizes
```

**輸出**:
```
📊 CATEGORY SIZE ANALYSIS

📁 AI_Tech (has 3 subcategories)
  ✅ AI_Hardware: 19 notes
  ✅ AI_Products: 4 notes
  ✅ AI_Applications: 6 notes

✅ Investment: 12 notes

RECOMMENDATIONS:
✅ All categories are within optimal size (< 20 notes)
```

## 最佳實踐

### 何時細分
- ✅ 類別 > 20 篇且有明確主題聚類
- ✅ 使用者難以在類別中找到筆記
- ✅ 類別涵蓋多個不同子主題

### 何時不細分
- ❌ 類別 < 20 篇
- ❌ 筆記主題高度相關，難以區分
- ❌ 細分後會產生 < 3 篇的小類別

### 細分後維護
1. 定期檢查子類別大小（每月）
2. 如果子類別 > 30 篇，考慮進一步細分
3. 如果子類別 < 3 篇，考慮合併

## 故障排除

### 問題: Ingest 沒有路由到子類別

**檢查**:
1. 子類別目錄是否存在？
2. 關鍵字匹配是否正確？
3. 查看 `.agent/analyze_*.py` 的關鍵字列表

**解決**: 手動移動檔案或更新關鍵字列表

### 問題: 細分方案不合理

**檢查**:
1. 語義聚類是否正確？
2. 子類別分布是否平衡？

**解決**: 修改 `[Category]_Subdivision_Plan.md` 後再執行

### 問題: WikiLinks 失效

**檢查**:
1. 相對路徑是否正確？
2. 檔案是否已移動？

**解決**: 更新 WikiLinks 或使用絕對路徑

## 未來改進

### 短期
- [ ] 自動更新 WikiLinks 路徑
- [ ] 支援更多語義分析方法（TF-IDF, embeddings）
- [ ] 細分歷史追蹤

### 長期
- [ ] 機器學習自動分類
- [ ] 動態閾值（根據使用頻率調整）
- [ ] 視覺化知識圖譜

---

**最後更新**: 2026-01-09  
**版本**: 1.0  
**狀態**: ✅ 已整合到工作流
