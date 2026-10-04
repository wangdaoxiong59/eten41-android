# 倚天41鍵 Android 輸入法

在 Android 上用**英文字母鍵盤**打注音，背後走**倚天41鍵**對應
（相容 26鍵合併按法）。鍵盤只顯示 A–Z，不顯示注音符號，
憑字母位置盲打——給從倚天／忘形時代走來的老派手指。

2026-10-04 實測評價：「用手機有史以來最順手的注音輸入法」。

## 特色

- 完整 41鍵對應：字母一注音一鍵，`ㄑㄢㄣㄤ` 在 `7 8 9 0`，
  `ㄥㄗㄓㄔㄕㄘㄦ` 在 `- ; , . / ' =`
- 並存 26鍵合併按法：`c`=ㄕ/ㄒ、`m`=ㄢ、`p`/`y`=ㄡ…手機單點更快
- 單字支援聲調：`1=˙ 2=ˊ 3=ˇ 4=ˋ`（一聲不標），例：`ge4`=記
- 約 74 萬詞條，繁體中文詞庫（源自 libchewing-data，LGPL-2.1-or-later）

## 下載現成碼表

不想自己轉碼的話，直接下載打包好的 v0.6
（含 `eten26.conf`＋`eten26.txt`＋Rime 版＋攻略篇）：

[Google Drive：倚天41鍵輸入法 v0.6](https://drive.google.com/drive/folders/1HbJ_24qfa2JYnSGtk6xMMkkDMj2XfE8c)

## 安裝（小企鵝輸入法碼表版，推薦）

1. Play 商店安裝「Fcitx5 for Android」（搜英文 **Fcitx5**）。
2. 下載 `eten26.conf` 和 `eten26.txt` 傳到手機（見上方 Drive 連結）。
3. 小企鵝 App → 附加元件 → 碼表右側齒輪 → 管理碼表輸入法 → `+` 匯入兩檔。
4. 首頁 → 輸入法 → `+` → 加入「倚天26鍵」。
5. 系統設定 → 語言與輸入 → 啟用小企鵝並設為預設。

## 自行轉碼

碼表本體（`eten26.txt`、`eten26.dict.yaml`）由 `src/convert.py`
從 libchewing 詞庫生成；13MB 的生成檔不進 git，有需要自己跑：

```bash
# 先取得 libchewing-data 的 tsi.csv 與 word.csv
python3 src/convert.py tsi.csv word.csv
# 產生 eten26.dict.yaml（Rime 用）與 eten26.txt（小企鵝碼表用）
```

## 打法範例

| 輸入 | 結果 |
|---|---|
| `nehz` | 你好 |
| `te8`（或 `tem`） | 天 |
| `ge4` | 記（四聲） |
| `/4`（或 `c4`） | 是 |
| `gxlhxamenvxo` | 中華民國 |

空白鍵上第一候選字；數字 `8` 等是長按字母鍵（`i`）叫出。

## 備用：Rime 版

`rime/` 目錄有 Rime 方案（同文輸入法／小企鵝＋Rime 插件用），
詳見[攻略篇](攻略篇.md)。

## 開發故事

詳見 [攻略篇.md](攻略篇.md)——從撞牆、被維基誤導、
到靠使用者的手指破案，最後修掉 fcitx5 引擎綁走數字鍵的坑。

## 授權

- 詞庫衍生自 [libchewing-data](https://github.com/chewing/libchewing-data)（LGPL-2.1-or-later）
- 對應表與轉換腳本：MIT（歡迎 fork 改良）
