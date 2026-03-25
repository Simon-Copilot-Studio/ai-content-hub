---
title: "聯發科 MR Breeze ASR 25 — 專為台灣口音設計的開源語音辨識 AI 模型"
date: 2026-03-20T10:00:00+08:00
description: "聯發創新基地開源的 Breeze ASR 25，基於 Whisper 微調專攻台灣口音，精準度提升 10%、中英混合提升 56%，Apache 2.0 授權可商用，已獲 6400+ 下載，解決 Whisper 聽不懂「花生什麼事」的痛點。"
categories:
  - tech
tags:
  - AI
  - 語音辨識
  - ASR
  - 聯發科
  - MediaTek
  - 開源
  - Whisper
  - 台灣
  - 繁體中文
image: "images/tech/2026-03-20-mediatek-breeze-asr-25.png"
readingTime: 3
draft: false
lang: zh-TW
faq:
  - q: "Breeze ASR 25 跟 OpenAI Whisper 有什麼差別？"
    a: "Breeze ASR 25 基於 Whisper Large V2 微調，專門針對台灣口音、用語和中英混合場景優化。整體精準度比原版 Whisper 提升 10%，中英混合（code-switching）場景更是提升高達 56%，能正確辨識「花生什麼事」這類台式發音。"
  - q: "可以商用嗎？需要付費授權嗎？"
    a: "完全可以。Breeze ASR 25 採用 Apache 2.0 開源授權，無論個人或商業使用都不需要付費，也不需要額外申請授權。你可以直接整合到產品、服務或教育平台中。"
  - q: "這個模型適合裝置端部署嗎？"
    a: "適合。Breeze ASR 25 基於 Whisper Large V2，模型大小約 3GB，可在邊緣裝置、樹莓派或本地伺服器上運行，不需要連網即可執行語音辨識，非常適合隱私敏感場景或離線應用。"
---

如果你曾經用 OpenAI Whisper 轉錄台灣人的對話，可能會發現它把「發生什麼事」聽成「花生什麼事」——不是因為 AI 在開玩笑，而是它沒學過台灣人的講話方式。

聯發創新基地（MediaTek Research）在 2025 年 7 月正式開源了 **MR Breeze ASR 25**，一款專門為台灣口音、用語和中英混合場景微調的語音辨識模型。它不只聽得懂台式中文，還能在商業場景免費使用，目前已經在 HuggingFace 上獲得超過 **6400 次下載**和 **110 個 likes**。

## 為什麼需要台灣專用的語音辨識？

全球主流的語音辨識服務——OpenAI Whisper、Google Speech-to-Text、Azure Speech——都是用海量多語資料訓練出來的，對標準中文（普通話）辨識效果很好，但碰到台灣口音和用語就容易翻車：

- 「花生什麼事」vs.「發生什麼事」
- 「阿不就好棒棒」（諷刺語氣）
- 「欸你等一下」（語氣詞）
- 中英夾雜：「我先 sync 一下 status」

這些細節對在地服務至關重要——無論是客服系統、教育平台還是會議記錄，語音辨識不只要「聽得懂」，還要「聽得對」。

## Breeze ASR 25 做對了什麼？

聯發科的解法很務實：拿 OpenAI 的 **Whisper Large V2** 當基底，用台灣在地語料（包含口音、俚語、中英混合）重新微調。結果：

- **整體精準度提升 10%**（相較原版 Whisper）
- **中英混合場景提升 56%**（code-switching）
- **Apache 2.0 授權**，可商用、可改作、不需付費
- **HuggingFace 開源**：[MediaTek-Research/Breeze-ASR-25](https://huggingface.co/MediaTek-Research/Breeze-ASR-25)
- **論文公開**：[arXiv:2506.11130](https://arxiv.org/abs/2506.11130)

模型於 2025 年 6 月 6 日上架，7 月 1 日正式發布，短短幾個月就累積超過 6400 次下載，證明市場對「在地化 AI」的強烈需求。

## 跟其他語音辨識服務比起來如何？

| 特性 | Breeze ASR 25 | Whisper | Google STT | Azure Speech |
|------|---------------|---------|------------|--------------|
| 台灣口音優化 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 中英混合 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 離線部署 | ✅ | ✅ | ❌ | ❌ |
| 商用授權 | 免費（Apache 2.0） | 免費（MIT） | 付費（API） | 付費（API） |
| 隱私保護 | ✅（本地運行） | ✅ | ⚠️（雲端） | ⚠️（雲端） |

Google STT 和 Azure Speech 在企業場景表現穩定，但需要付費且資料必須上雲；Whisper 免費但對台灣口音支援有限；**Breeze ASR 25 剛好填補了這個空白**——既免費、又本地化、還能離線跑。

## 適合哪些應用場景？

### 1. 教育平台（如 EduSpark）
台灣的線上教育平台可以用 Breeze ASR 25 自動生成課程字幕、筆記，或是做課堂互動辨識——學生說「老師我不懂」，系統能精準捕捉並觸發輔助說明。

### 2. AI 助理與智慧家居（如 OpenClaw）
整合進 AI 助理後，可以用台灣人最自然的說話方式下指令：「幫我查一下明天天氣」「把客廳燈關掉」，不用刻意講標準中文。

### 3. 客服系統
金融、電商、電信客服可以用 Breeze ASR 25 自動轉錄通話內容、分析客戶情緒、產生摘要報告，大幅提升服務效率。

### 4. 會議記錄與字幕生成
遠距會議、podcast 錄音、YouTube 影片字幕——任何需要即時或離線語音轉文字的場景都適用。

## MR Breeze 系列：全套繁中 AI 工具鏈

Breeze ASR 25 只是聯發創新基地 **MR Breeze 系列**的一部分。目前已開源的還包括：

- **Breeze V-LLM**：繁中視覺語言模型
- **Breeze TTS**：繁中語音合成
- **Breeze Function Calling**：繁中工具調用
- **Breeze ASR**：繁中語音辨識

這套工具鏈組合起來，可以打造完全本地化、可離線運行的 AI 應用——從聽（ASR）到想（V-LLM）到說（TTS），全程不需仰賴國外雲端服務。

## 如何開始使用？

最簡單的方式是透過 HuggingFace Transformers：

```python
from transformers import pipeline

asr = pipeline("automatic-speech-recognition", 
               model="MediaTek-Research/Breeze-ASR-25")

result = asr("taiwanese_audio.wav")
print(result["text"])
```

模型大小約 3GB，可以在一般筆電、樹莓派或邊緣裝置上運行，不需要高階 GPU。

## 結論：在地化 AI 的里程碑

聯發科開源 Breeze ASR 25，不只是技術突破，更是「AI 在地化」的重要示範。當全球 AI 巨頭專注在英文和標準中文時，台灣團隊選擇深耕本土需求，用開源方式回饋社群。

對開發者來說，這是一個可以直接拿來用、改來用、商業化的語音辨識方案；對台灣的 AI 生態來說，這是一塊重要的拼圖——我們終於有了「聽得懂台灣話」的開源模型。

如果你正在做教育平台、AI 助理、客服系統或任何需要語音辨識的產品，不妨試試 Breeze ASR 25。它可能就是你一直在找的那個「夠在地」的解決方案。

---

**相關連結**：
- [HuggingFace 模型頁面](https://huggingface.co/MediaTek-Research/Breeze-ASR-25)
- [論文 arXiv:2506.11130](https://arxiv.org/abs/2506.11130)
- [聯發創新基地 MR Breeze 系列](https://huggingface.co/MediaTek-Research)
