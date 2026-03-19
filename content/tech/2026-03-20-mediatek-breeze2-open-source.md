---
title: "聯發科一口氣開源 3 款台灣 AI 模型：繁中多模態 Llama-Breeze2 + 台灣口音語音合成 BreezyVoice"
date: 2026-03-20T07:50:00+08:00
description: "聯發創新基地開源 Llama-Breeze2-3B 和 8B 兩款繁中多模態模型，支援看圖、函式呼叫、手機端運行。同步釋出台灣口音語音合成模型 BreezyVoice，只需 5 秒範例音訊即可生成擬真語音。三款模型均含權重與程式碼，Apache 2.0 授權。"
categories: ["科技"]
tags: ["聯發科", "MediaTek", "Llama-Breeze2", "BreezyVoice", "開源AI", "繁體中文", "台灣AI"]
image: "images/tech/2026-03-20-mediatek-breeze2.jpg"
readingTime: 4
draft: false
faq:
  - q: "Llama-Breeze2 是什麼？"
    a: "聯發創新基地（MediaTek Research）基於 Meta Llama 3.2 優化的繁體中文多模態語言模型，有 3B（手機版）和 8B（PC 版）兩個版本，支援繁中理解、圖像分析和函式呼叫功能。"
  - q: "BreezyVoice 有什麼特色？"
    a: "BreezyVoice 是專為繁體中文訓練的語音合成模型，特色是只需 5 秒的範例音訊就能生成擬真的台灣口音語音。可在筆電上運行，也能結合任何 LLM 或語音轉文字架構。"
  - q: "這些模型可以商用嗎？"
    a: "模型權重和執行程式碼均已在 HuggingFace 和 GitHub 上開源，具體商用授權需參考聯發科的釋出條款與 Llama 基礎模型的授權規範。"
  - q: "Llama-Breeze2-3B 可以在手機上跑嗎？"
    a: "可以。聯發科同步開源了以 Llama-Breeze2-3B 驅動的 Android App，可直接部署到手機作為 AI 助理，支援即時翻譯、景點推薦、語音生成等功能。"
---

台灣半導體龍頭聯發科，這次不是發晶片，是發 AI 模型——而且一次三款，全部開源。

## 三款模型一次到位

聯發創新基地（MediaTek Research）一口氣開源了三款專為台灣打造的 AI 模型：

| 模型 | 參數量 | 目標裝置 | 核心能力 |
|------|--------|---------|---------|
| **Llama-Breeze2-3B** | 30 億 | 手機 | 繁中 + 看圖 + 函式呼叫 |
| **Llama-Breeze2-8B** | 80 億 | 個人電腦 | 繁中 + 看圖 + 函式呼叫 |
| **BreezyVoice** | — | 筆電+ | 台灣口音語音合成 |

所有模型的權重和程式碼都已釋出：
- 📦 [HuggingFace 模型庫](https://huggingface.co/collections/MediaTek-Research/breeze-2-family-67863158443a06a72dd29900)
- 📱 [Android App 原始碼](https://github.com/mtkresearch/Breeze2-android-demo)
- 🗣️ [BreezyVoice 模型](https://huggingface.co/MediaTek-Research/BreezyVoice)

## Llama-Breeze2：真正懂台灣的多模態模型

基於 Meta 的 Llama 3.2 優化，Llama-Breeze2 有三大特色：

### 1. 繁中能力大幅領先原版

聯發科做了一個直球對決的測試：讓兩個模型各寫一篇台灣夜市短文。

| 模型 | 提到的夜市 | 正確性 |
|------|-----------|--------|
| **Llama-Breeze2-3B** | 士林夜市、饒河街夜市、羅東夜市 | ✅ 全部正確 |
| Llama 3.2-3B | 士林夜市、「電信夜市」、「世貿夜市」 | ❌ 幻覺兩個 |

這就是用繁中資料微調的威力——不會再看到 AI 捏造不存在的台灣地標。

### 2. 多模態：不只讀文字，還能看圖

Llama-Breeze2 整合了視覺語言模型，能理解：
- 📊 **圖表**：直接看圖算數據
- 📝 **OCR**：辨識圖片中的文字
- 🏛️ **景點照片**：識別地點並提供資訊

實測範例：
> **使用者**：請問前三名總共可獲得多少錢？  
> **Llama-Breeze2-8B**：根據圖片，第一名獎金為 30 萬元、第二名 20 萬元、第三名 15 萬元。前三名獎金總和為 **65 萬元整**。

### 3. 函式呼叫：連接真實世界

模型具備 Function Calling 能力，能調用外部 API。例如問天氣時，模型會自動呼叫天氣 API 取得即時資訊再回答——不是用過時的訓練數據瞎猜。

## BreezyVoice：5 秒就能複製你的台灣口音

這可能是台灣開發者最期待的一款。

**BreezyVoice** 是專為繁體中文加強訓練的語音合成模型，核心賣點：

- 🎤 **只需 5 秒範例音訊**即可生成擬真語音
- 🇹🇼 **台灣口音**：不是對岸普通話，是正港台灣腔
- 💻 **筆電就能跑**：輕量架構，無需 GPU 伺服器
- 🔌 **可結合任何 LLM**：接上 ChatGPT、Llama 或任何模型當語音輸出

應用場景：
- AI 語音助理（台灣口音版 Siri）
- 智慧導航語音
- Podcast 自動生成
- 客服語音機器人

## Android App：手機上的台灣 AI 助理

聯發科不只開源模型，還直接做了一個 [Android App](https://github.com/mtkresearch/Breeze2-android-demo)：

- 以 Llama-Breeze2-3B 驅動
- 可作為手機端 AI 助理
- 支援即時翻譯、景點推薦
- 內建語音生成功能
- 完整原始碼開源

## 對台灣 AI 生態的意義

這次開源的重要性，不只是模型本身：

1. **降低繁中 AI 開發門檻**：台灣開發者不再需要從零訓練繁中模型
2. **端側 AI 普及**：3B 模型能在手機上跑，意味著離線 AI 助理成為可能
3. **語音合成突破**：BreezyVoice 是目前少數專為台灣口音優化的開源 TTS
4. **生態系建設**：聯發科作為硬體廠商投入 AI 軟體開源，帶動上下游發展

對於正在開發繁中 AI 應用的團隊來說，這三款模型值得立刻試用。

---

*原文來源：[iThome](https://www.ithome.com.tw/news/167427) | [聯發科官方部落格](https://www.mediatek.tw/blog/聯發創新基地全面開源-breeze2)*
