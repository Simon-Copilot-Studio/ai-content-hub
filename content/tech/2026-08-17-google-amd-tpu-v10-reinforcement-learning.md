---
title: "Google 傳聯手 AMD 打造第十代 TPU：整合 CPU 核心攻克強化學習與 AI Agent 算力瓶頸，半導體架構迎來什麼巨變？"
date: "2026-08-17 06:00:00"
description: "半導體研究機構 SemiAnalysis 披露，Google 正在與 AMD 洽談合作開發第十代 TPU，計畫首次將 TPU 算力晶片與 AMD CPU 核心、HBM 透過先進封裝技術緊密整合在單一封裝內。本文深入解析這項傳聞背後的 AI 工作負載轉變——從純預訓練（Pre-training）的矩陣運算走向強化學習（Reinforcement Learning）與智慧代理（AI Agent）所需的通用與張量混合運算，並剖析其對 NVIDIA、台積電與全球晶片供應鏈的深遠影響。"
categories:
  - tech
  - ai
  - semiconductor
tags:
  - Google
  - AMD
  - TPU
  - AI Chips
  - Reinforcement Learning
  - AI Agent
  - TSMC
  - Advanced Packaging
  - SoIC
image: "https://images.unsplash.com/photo-1591488320449-011701bb6704?auto=format&fit=crop&w=1200&q=80"
readingTime: "12 min read"
FAQ:
  - question: "Google 為什麼傳出要在第十代 TPU 中聯手 AMD 並整合 CPU 核心？"
  - answer: "隨著 AI 發展從大規模預訓練（Pre-training）過渡到以強化學習（Reinforcement Learning）和 AI Agent 代理式推理為核心的階段，運算需求發生了根本性質變。強化學習和樹狀搜尋（Tree Search）在產生動態決策時，不僅需要龐大的張量運算（Tensor Core），更需要密集的通用運算（General-purpose CPU Compute）。Google 透過將 AMD 的高效能 CPU 核心、HBM 與自家 TPU 張量晶片透過先進封裝（如 SoIC）整合在同一封裝內，能徹底消除傳統 PCIe 匯流排的延遲與頻寬瓶頸，實現零時差的異質協同運算。"

  - question: "這項合作對 NVIDIA 的主導地位會造成實質衝擊嗎？"
  - answer: "短期內，NVIDIA 憑藉強大的 CUDA 軟體生態系與 Blackwell/Rubin 硬體架構，在通用 AI 訓練市場仍處於絕對壟斷地位。然而，這項發展象徵著全球頂級雲端服務商（CSP）正全面深化「專屬運算架構（Custom ASIC）」的佈局。當 Google 結合 AMD 的 IP 打造出針對特定 AI 工作負載（如強化學習與 Agent 推理）極致優化的晶片時，將瓜分高階推理與自研運算市場，削弱 NVIDIA 在整個 AI 軟硬體生態圈的議價權。"

  - question: "這對全球半導體供應鏈（如台積電與先進封裝）有何啟示？"
  - answer: "這再次凸顯了「先進封裝（Advanced Packaging）」與「異質整合（Heterogeneous Integration）」已成為決定 AI 晶片成敗的兵家必爭之地。無論是 AMD 的 Instinct MI300A 混合架構經驗，還是未來 Google 與 AMD 的合作，所有高階晶片最終都離不開台積電（TSMC）的 CoWoS 與 SoIC 先進封裝產能。半導體產業正從單純的「製程微縮（Process Node）」轉向「封裝架構創新（Packaging Architecture Innovation）」的新紀元。"
---

**Google 傳聯手 AMD 打造第十代 TPU：整合 CPU 核心攻克強化學習與 AI Agent 算力瓶頸，半導體架構迎來什麼巨變？**

在 2026 年 8 月中旬的全球半導體與人工智慧（AI）界，一則由權威研究機構 SemiAnalysis 披露的產業內幕引發了軒然大波：**搜尋引擎巨頭 Google 正在與超微（AMD）進行一項高度敏感的戰略洽談，計畫在即將到來的第十代 TPU（TPU v10）專案中攜手合作，首次將 Google 自研的張量運算晶片與 AMD 的高效能 CPU 核心及 HBM（高頻寬記憶體）透過先進封裝技術緊密整合在單一封裝內。**

這項傳聞如果成真，不僅將成為 AMD 歷史上首次實質參與頂級雲端大廠（CSP）的客製化 AI ASIC 專案，更標誌著全球 AI 硬體架構正迎來一場深刻的典範轉移——從過去幾年單純追求「暴力擴張矩陣運算」的預訓練時代，正式跨入「通用計算與張量運算高度交織」的強化學習（Reinforcement Learning）與 AI Agent 代理新紀元。

本文將為讀者深度解構這項傳聞背後的技術邏輯、AI 工作負載的結構性轉變，以及其對 NVIDIA、台積電與全球晶片產業鏈的深遠震撼。

---

### 一、 算力瓶頸的轉折點：為什麼 Google 需要在 TPU 中整合 CPU？

過去數年間，全球大模型（LLM）的競賽核心在於「預訓練（Pre-training）」。在預訓練階段，AI 模型需要吞噬海量的網頁資料、書籍與程式碼，進行超大规模的矩陣乘法運算。此時，NVIDIA 的 GPU 與 Google 早期的 TPU 扮演了純粹的「平行運算怪獸」，只要提供源源不絕的 FLOPS（浮點運算次數），模型就能不斷膨脹。

然而，進入 2026 年，AI 應用的主流已經發生了根本性位移：
1. **AI Agent 與代理式推理崛起：** 使用者不再滿足於單純的文本問答，而是期望 AI Agent 能夠自主規劃任務、呼叫工具、執行 Python 程式碼、進行多步驟推理（Multi-step Reasoning）。
2. **強化學習（Reinforcement Learning）成為模型智力躍升的關鍵：** 像是 OpenAI 的 o 系列、Anthropic 的進階推理模型以及 Google 的 Gemini 深度思考版本，皆高度依賴「推理時計算（Inference-time Compute）」與強化學習中的樹狀搜尋（Tree Search / Monte Carlo Tree Search）。

在這些新工作負載下，運算特性出現了巨大轉變：**模型在每產生一個 token 或執行下一步決策前，都需要大量的「通用運算（General-purpose CPU Compute）」來處理控制邏輯、狀態檢查、演算法搜尋與環境互動。**

事實上，Google 在其 TPU 架構的演進中早已見微知著：
* **TPU 7 代：** 伺服器配置比例大約是每 4 顆 TPU 搭配 1 顆 Intel Xeon「Emerald Rapid」處理器。
* **TPU 8i（推理專用系統）：** 比例迅速提升至每 2 顆 TPU 搭配 1 顆 Google 自研的 Axion CPU。

然而，當系統對 CPU 運算的需求比例逼近甚至達到「1 比 1」時，傳統主機板上透過 PCIe 匯流排連接 TPU 與 CPU 的架構，會暴露出嚴重的**頻寬瓶頸與通訊延遲**。兩者之間頻繁交換狀態資料所產生的等待時間，成為拖累 AI 推理速度與反應靈敏度的隱形殺手。

將 CPU 核心與 TPU 張量晶片直接透過先進封裝（Advanced Packaging）融為一體，消弭實體距離，成為了突破算力天花板的唯一解方。

---

### 二、 為什麼是 AMD？異質整合（Heterogeneous Integration）的強強聯手

如果 Google 決定將 CPU 核心直接整合進 TPU 封裝中，尋找外部合作夥伴便成了最務實的選擇。為什麼 Google 會挑中 AMD？

1. **豐富的異質晶片經驗（如 MI300A）：** AMD 在資料中心等級的處理器設計上擁有世界級的功力。其旗艦產品 Instinct MI300A 已經成功將 x86 CPU 核心、GPU 加速器晶片（Chiplet）以及 HBM 記憶體，透過先進的 3D 封裝技術（如 TSMC SoIC）完美融合在單一封裝內。這種「APU（加速處理單元）」設計理念，與 Google 對 TPU v10 的想像不謀而合。
2. **頂尖的 IP 儲備與先進封裝實力：** AMD 不僅擁有高效能的 Zen 系列 CPU IP，更在晶片互連（Infinity Fabric）、高速介面與晶圓級先進封裝領域深耕多年。對於 Google 而言，與其從零開始自主研發高效能 CPU 晶片並解決龐大的功耗與散熱難題，直接引入 AMD 的成熟 IP 與架構設計經驗，是最具成本效益且能快速落地的捷徑。
3. **軟硬體生態的戰略互補：** 半導體分析師指出，AMD 雖然在 AI 軟體生態（ROCm vs CUDA）上持續追趕 NVIDIA，但其在高效能運算（HPC）與資料中心硬體架構上的深厚底蘊，使其成為雲端巨頭打造專屬硬體（Custom ASIC）時最理想的無代工廠（Fabless）盟友。

---

### 三、 產業格局巨變：NVIDIA 的護城河正遭受「客製化夾擊」

這項傳聞如果最終成為現實，將對全球 AI 硬體生態產生極具指標性的意義：

* **CSP 廠的「去單一供應商化」浪潮：** 繼微軟、Meta、Amazon、OpenAI 與 Anthropic 相繼投入自研晶片或客製化 ASIC 之後，連一向擁有最強大自研能力的 Google，也開始引入外部頂尖晶片設計巨頭（AMD）的 IP 來強化其 TPU 家族。這證明了「通用 GPU 統治一切」的時代正在加速過去，取而代之的是針對特定演算法、特定工作負載（如強化學習、Agent 推理）量身訂做的「百花齊放特種晶片時代」。
* **NVIDIA 的因應之道：** 面對來自 CSP 自研 ASIC 與混合晶片架構的蠶鯨，NVIDIA 的核心優勢在於其不可動搖的 CUDA 軟體生態系與 Blackwell/Rubin 平台的極致系統級整合能力。然而，當運算焦點從「訓練時的巨量平行吞吐」轉向「推理時的低延遲、高靈活性與具身智能互動」時，NVIDIA 也必須推出更具彈性的架構來迎戰。

---

### 四、 台積電與先進封裝供應鏈的絕對贏家地位

無論這場由 Google、AMD、NVIDIA 甚至是各大 AI 新創主演的晶片大戰如何演變，全球半導體供應鏈的核心贏家已然底定——**台積電（TSMC）及其帶動的先進封裝生態系。**

無論是 Google 的 TPU 張量晶片、AMD 的 Zen CPU 核心、NVIDIA 的 Rubin 晶片，抑或是博通（Broadcom）協助雲端大廠設計的各種 ASIC，其最終的生產與製造，都高度依賴台積電的 3 奈米/2 奈米先進製程，以及 CoWoS、SoIC 等先進封裝產能。

這也解釋了為什麼全球半導體設備與封裝材料廠在 2026 年依然保持著空前的景氣熱度。當晶片設計從「單一晶片微縮」轉向「異質晶片拼接（Chiplet & 3D Packaging）」，封裝技術本身就成為了決定 AI 運算極限的決定性戰場。

---

### 結語：迎向 AI 算力的下半場

Google 傳出聯手 AMD 開發第十代 TPU 的消息，向市場發出了清晰無誤的信號：人工智慧的硬體競賽已經走出了「盲目追求規模」的上半場，正式進入「講求極致性價比、軟硬體深度協同、為特定代理與強化學習演算法量身打造」的下半場。

對於台灣的半導體與科技產業而言，這波架構變革既是機遇也是挑戰。隨著 AI Agent 深入各行各業、運算架構朝向異質整合狂奔，誰能掌握先進封裝與高效能運算的關鍵節點，誰就握有了下一個十年的科技話語權。

---

### 常見問題（FAQ）

- **question: "Google 為什麼傳出要在第十代 TPU 中聯手 AMD 並整合 CPU 核心？"**
  - **answer: "隨著 AI 發展從大規模預訓練（Pre-training）過渡到以強化學習（Reinforcement Learning）和 AI Agent 代理式推理為核心的階段，運算需求發生了根本性質變。強化學習和樹狀搜尋（Tree Search）在產生動態決策時，不僅需要龐大的張量運算（Tensor Core），更需要密集的通用運算（General-purpose CPU Compute）。Google 透過將 AMD 的高效能 CPU 核心、HBM 與自家 TPU 張量晶片透過先進封裝（如 SoIC）整合在同一封裝內，能徹底消除傳統 PCIe 匯流排的延遲與頻寬瓶頸，實現零時差的異質協同運算。"**

- **question: "這項合作對 NVIDIA 的主導地位會造成實質衝擊嗎？"**
  - **answer: "短期內，NVIDIA 憑藉強大的 CUDA 軟體生態系與 Blackwell/Rubin 硬體架構，在通用 AI 訓練市場仍處於絕對壟斷地位。然而，這項發展象徵著全球頂級雲端服務商（CSP）正全面深化「專屬運算架構（Custom ASIC）」的佈局。當 Google 結合 AMD 的 IP 打造出針對特定 AI 工作負載（如強化學習與 Agent 推理）極致優化的晶片時，將瓜分高階推理與自研運算市場，削弱 NVIDIA 在整個 AI 軟硬體生態圈的議價權。"**

- **question: "這對全球半導體供應鏈（如台積電與先進封裝）有何啟示？"**
  - **answer: "這再次凸顯了「先進封裝（Advanced Packaging）」與「異質整合（Heterogeneous Integration）」已成為決定 AI 晶片成敗的兵家必爭之地。無論是 AMD 的 Instinct MI300A 混合架構經驗，還是未來 Google 與 AMD 的合作，所有高階晶片最終都離不開台積電（TSMC）的 CoWoS 與 SoIC 先進封裝產能。半導體產業正從單純的「製程微縮（Process Node）」轉向「封裝架構創新（Packaging Architecture Innovation）」的新紀元。"**
