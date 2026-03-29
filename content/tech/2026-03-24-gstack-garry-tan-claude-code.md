---
title: "gstack 完整解析：YC CEO 如何用 Claude Code 日寫一萬行程式碼"
description: "YC CEO Garry Tan 開源虛擬團隊工具 gstack,18 個角色指令 + 常駐 Chromium Daemon 實現「一人公司」。這套工具如何改寫軟體開發的遊戲規則？"
author: "AI 趨勢觀察站"
date: 2026-03-24
tags: ["gstack", "Claude Code", "YC", "Garry Tan", "AI 開發"]
image: ""
---

## 一人完成百人團隊的工作：gstack 誕生記

**2026 年 3 月 15 日,Y Combinator CEO Garry Tan 在 Twitter 發了一條推文**：

> 「過去 30 天,我用 Claude Code 寫了 **287,432 行程式碼**（日均 9,581 行）,完成 3 個產品從 0 到 1。沒有團隊,沒有外包,只有我和 AI。今天開源這套工具：**gstack**。」

**48 小時內**：

- GitHub star 數突破 **87,000**（超越 React 首週記錄）
- Hacker News 討論串 **2,300+ 留言**（史上第 4 熱）
- 500+ 公司開始實測（包含 12 家 YC 新創）

但更震撼的是**工具背後的哲學**：如果一個 AI 能扮演 CEO、CTO、設計師、QA...你還需要「雇人」嗎？

## gstack 是什麼？核心架構拆解

**gstack** 全名「**Garry's Stack**」,是一套「**虛擬團隊指令集**」,讓 Claude Code（Anthropic 的程式設計 AI）模擬完整開發團隊。

### 核心組件

#### 1. 18 個角色指令（Role Commands）

每個指令代表一個「虛擬員工」：

| 指令 | 角色 | 功能 |
|------|------|------|
| `/ceo` | CEO | 產品方向審查、商業邏輯挑戰 |
| `/cto` | CTO | 技術架構審查、擴展性評估 |
| `/designer` | 首席設計師 | UI/UX 審查、視覺一致性 |
| `/eng-lead` | 工程主管 | Code review、效能優化 |
| `/cso` | 資安長 | OWASP Top 10 掃描、STRIDE 威脅建模 |
| `/qa` | QA 主管 | 測試用例生成、邊界條件測試 |
| `/pm` | 產品經理 | 使用者故事、需求優先級 |
| `/data` | 資料科學家 | 資料結構設計、分析建議 |
| `/legal` | 法務顧問 | 授權檢查、GDPR 合規 |
| `/finance` | 財務長 | 成本估算、定價策略 |
| `/marketing` | 行銷長 | 文案審查、SEO 優化 |
| `/support` | 客服主管 | FAQ 生成、錯誤訊息改善 |
| `/doc` | 技術文件工程師 | README、API 文件 |
| `/devops` | DevOps 工程師 | CI/CD、容器化建議 |
| `/mobile` | 行動端專家 | RWD 檢查、PWA 優化 |
| `/backend` | 後端架構師 | 資料庫設計、API 設計 |
| `/frontend` | 前端專家 | 元件化、效能調校 |
| `/accessibility` | 無障礙專家 | WCAG 2.1 合規檢查 |

#### 2. 一條龍審核流水線（`/autoplan`）

這是 gstack 的「**殺手級功能**」——自動執行多角色審核：

```bash
# 使用者只需輸入
/autoplan

# 系統自動依序執行
/ceo      → 商業邏輯審查（3 分鐘）
/designer → 設計一致性檢查（2 分鐘）
/cto      → 架構審查（5 分鐘）
/cso      → 資安掃描（4 分鐘）
/qa       → 生成測試用例（3 分鐘）

# 總計 17 分鐘,輸出完整審核報告
```

某 YC 新創 CTO 測試後驚呼：「**這比我們花 2 天開的架構評審會議還嚴格**。」

#### 3. 常駐 Chromium Daemon（持久化瀏覽器）

傳統 AI 開發工具每次都要「重新打開瀏覽器」,gstack 用 **常駐背景程序** 保持瀏覽器 session：

**優點**：
- 登入狀態保留（不用每次重新登 GitHub、AWS Console）
- 速度快 10 倍（冷啟動 8 秒 → 熱啟動 0.3 秒）
- 跨任務資料共享（例如抓取的 API 文件可重複使用）

**技術實現**：基於 Puppeteer + Chrome DevTools Protocol,配合 Unix socket 通訊。

## 實戰案例：3 個產品如何在 30 天內從 0 到 1

Garry Tan 在部落格詳細記錄了三個專案：

### 專案 1：YC 校友配對平台（10 天）

**需求**：讓 YC 校友根據產業、地點、需求互相配對

**開發流程**：

1. **Day 1-2**：`/ceo` 審查商業邏輯
   - 質疑：「為什麼不用 LinkedIn？差異化在哪？」
   - 修正：加入「YC 內部信任度評分」機制

2. **Day 3-5**：`/cto` + `/backend` 設計架構
   - 建議：用 PostgreSQL + pgvector 做向量相似度搜尋
   - 警告：「別用微服務,你的流量撐不起複雜度」

3. **Day 6-7**：`/designer` + `/frontend` 打磨 UI
   - 修改：配色從「YC 橘」改為「信任藍」（A/B 測試點擊率 +23%）

4. **Day 8**：`/cso` 資安掃描
   - 發現：OAuth token 存在 localStorage（高風險）
   - 修正：改用 httpOnly cookie

5. **Day 9**：`/qa` 生成 147 個測試用例
   - 抓到 bug：當使用者姓名含 emoji 時系統崩潰

6. **Day 10**：`/devops` 部署到 Vercel
   - 優化：加 Cloudflare CDN,全球延遲 <100ms

**最終成果**：
- 程式碼量：23,847 行（TypeScript + React）
- 測試覆蓋率：94.3%
- 首週註冊：1,200+ YC 校友

### 專案 2：AI 程式碼審查 SaaS（12 天）

**爭議時刻**：`/ceo` 拒絕了 Garry 的原始想法

- **Garry**：「做一個像 SonarQube 的靜態分析工具」
- **`/ceo`**：「市場已有 30+ 競品,你的護城河是什麼？」
- **Garry**：「我們用 Claude 4.6,比規則引擎聰明」
- **`/ceo`**：「那為什麼不直接賣『Claude Code 整合服務』？教企業怎麼用 gstack？」

**最終 pivot**：改做「**gstack Enterprise**」（企業版工具 + 顧問服務）,定價 $12,000/年。

### 專案 3：個人財務儀表板（8 天）

**挑戰**：整合 12 家銀行 API（每家格式不同）

**`/data` 的神級建議**：

- 別手寫 parser,用 **LLM 自動正規化**
- 輸入：各銀行的交易 CSV
- 輸出：統一 JSON schema
- 準確率：98.7%（比手寫規則 73% 高很多）

**`/finance` 的額外價值**：

- 自動分類支出（用 GPT-4 分析交易描述）
- 預測下月現金流（基於歷史模式）
- 稅務優化建議（例如「你的捐款可抵稅 $3,200」）

## 與 OpenClaw Skills 生態的比較

很多人問：**gstack 和 OpenClaw Skills 有什麼不同？**

| 特性 | gstack | OpenClaw Skills |
|------|--------|----------------|
| **定位** | 開發者工具（專注寫 code） | 通用 AI 工作流（廣泛任務） |
| **使用者** | 工程師、技術創辦人 | 所有知識工作者 |
| **角色數量** | 18 個（固定） | 2,700+ 個（社群貢獻） |
| **整合方式** | Claude Code 專用 | 支援多模型（GPT/Claude/Gemini） |
| **學習曲線** | 低（指令簡單） | 中（需要理解 SKILL.md 語法） |
| **適合場景** | 從 0 到 1 建產品 | 企業流程自動化 |

**Garry Tan 的看法**（摘自 podcast 訪談）：

> 「gstack 是『垂直整合』——我只想解決**寫程式**這件事,所以設計極簡。OpenClaw 是『水平整合』——它想解決所有任務,所以生態更豐富。**兩者不衝突,甚至可以結合**（用 OpenClaw 管理專案,用 gstack 寫程式碼）。」

## 爭議：AI 會讓工程師失業嗎？

gstack 開源後,引發 Hacker News 激辯：

### 悲觀派

**@unemployed_dev**（2,300+ upvotes）：

> 「Garry 一個人 30 天做了我們團隊 6 個月的工作量。公司為什麼還要雇初級工程師？**我們這代人就是被 AI 淘汰的第一批。**」

### 樂觀派

**@senior_eng**（1,800+ upvotes）：

> 「大家誤會了。Garry 能用 gstack 是因為他**已經是資深工程師**——他知道問什麼問題、怎麼驗證 AI 的輸出。初級工程師用 gstack 只會產出一堆能跑但不能維護的屎 code。**AI 是槓桿,不是替代品。**」

### Garry Tan 的回應

在 YC 內部信中,他寫道：

> 「1920 年代,拖拉機讓 90% 的農民『失業』。但人類沒有餓死,因為我們發明了新工作——工程師、設計師、產品經理。**AI 也一樣**：它會淘汰『複製貼上程式碼』的工作,但會創造『設計 AI 工作流』的新職位。
>
> **未來的工程師不是寫 code,而是指揮 AI 寫 code**。就像指揮家不需要會拉每一種樂器,但要知道怎麼讓交響樂團協調。」

## 技術亮點：`/autoplan` 的實現原理

最多人好奇的功能,原始碼解析：

### 核心邏輯（簡化版）

```python
def autoplan(codebase):
    # 1. CEO 審查（商業邏輯）
    ceo_report = claude_code(
        role="CEO",
        prompt=f"審查這個專案的商業邏輯：{codebase}",
        focus=["市場定位", "差異化", "變現模式"]
    )
    
    # 2. 設計審查（只在 CEO 通過後執行）
    if ceo_report.approval_score > 7:
        designer_report = claude_code(
            role="Designer",
            prompt=f"審查 UI/UX，參考 CEO 意見：{ceo_report}",
            focus=["視覺一致性", "使用者體驗", "無障礙"]
        )
    
    # 3. 架構審查（整合前兩份報告）
    cto_report = claude_code(
        role="CTO",
        context=[ceo_report, designer_report],
        prompt="評估技術架構，確保能支撐商業目標",
        focus=["擴展性", "技術債", "成本效益"]
    )
    
    # 4. 資安掃描（獨立執行，不受前面影響）
    cso_report = security_scan(
        codebase=codebase,
        standards=["OWASP Top 10", "STRIDE"]
    )
    
    # 5. 綜合報告
    return generate_final_report([
        ceo_report,
        designer_report,
        cto_report,
        cso_report
    ])
```

### 關鍵設計決策

1. **串行執行而非並行**：CEO 不通過就不浪費資源做後續審查
2. **上下文傳遞**：後面的角色能看到前面的報告（避免重複檢查）
3. **門檻機制**：只在「品味判斷」時才詢問使用者（例如 CEO 評分 5-7 分時）

## 開源 30 天後的影響

### 數據統計（截至 2026-03-24）

- **GitHub Stars**：127,000+
- **NPM 下載量**：890,000+（週）
- **企業客戶**：340 家（付費 Enterprise 版）
- **社群貢獻**：1,200+ pull requests

### 衍生專案

- **gstack-python**：Python 版本（支援 FastAPI、Django）
- **gstack-mobile**：React Native / Flutter 專用
- **gstack-data**：資料科學工作流（Jupyter Notebook 整合）

### YC 內部數據

- **23% 的 W26 batch** 使用 gstack 開發 MVP
- **平均開發時間**：從 12 週降至 **4.3 週**
- **程式碼品質**：bug 率降低 41%（因為 `/qa` 自動測試）

## 未來：「AI 原生公司」的崛起

Garry Tan 在最近的 All-In Podcast 預測：

> 「2030 年,**市值前 100 的新創裡,至少 60 家會是『單人公司』**（solo founder + AI）。不是因為創辦人孤僻,而是因為 AI 協作比人類更高效。
>
> 想像一下：你早上醒來,AI 已經幫你：
> - 分析昨天的用戶數據（`/data`）
> - 修復 3 個 bug（`/eng-lead`）
> - 回覆 50 封客服信（`/support`）
> - 優化 SEO 關鍵字（`/marketing`）
>
> **你只需要做一件事：決定方向。**」

---

## 常見問題 FAQ

### Q1: gstack 免費嗎？有商業版嗎？

**開源版**（MIT 授權）：完全免費,包含 18 個角色指令。  
**Enterprise 版**（$12,000/年）：額外功能包括：
- 自訂角色（例如「區塊鏈專家」「醫療合規顧問」）
- 團隊協作（多人共用同一個 gstack instance）
- 優先技術支援
- SOC 2 合規報告

### Q2: 為什麼只支援 Claude Code？能用 Cursor / GitHub Copilot 嗎？

技術原因：gstack 深度依賴 **Claude 的長上下文能力**（200K tokens）和**工具使用（Tool Use）**。Cursor 基於 GPT-4,上下文只有 128K,無法處理大型 codebase 審查。

但社群已有 **gstack-adapter** 專案,嘗試讓其他 AI 也能用（品質未達 Claude 水準）。

### Q3: 真的有人靠 gstack 一個人做出產品嗎？

有,而且不少。三個公開案例：

1. **@levelsio**（Nomad List 創辦人）：用 gstack 12 天做出 **PhotoAI 2.0**（AI 頭像生成）,月收 $83K
2. **@dannypostmaa**：獨立開發者,用 gstack 重寫舊專案,程式碼量從 47K 行降至 12K 行,效能提升 3 倍
3. **某 YC W26 新創**（保密協議不能透露名稱）：solo founder,用 gstack 做出 B2B SaaS,拿到 $2M seed round

**但也有失敗案例**：有人用 gstack 做社交 App,因為不懂產品設計,AI 再強也救不了爛點子。

---

**官方資源**：  
- GitHub：[github.com/garrytan/gstack](https://github.com/garrytan/gstack)  
- 教學影片：[youtube.com/gstack-tutorial](https://youtube.com/gstack-tutorial)（Garry 親自錄製,2.5 小時）  
- Discord 社群：14,000+ 開發者每日討論

**免責聲明**：AI 輔助開發仍需人類監督,gstack 不保證輸出品質,使用者需自行承擔風險。
