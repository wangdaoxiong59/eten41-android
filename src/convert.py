#!/usr/bin/env python3
"""將 libchewing 詞庫 (tsi.csv / word.csv) 轉換為 Rime 倚天26鍵(忘形)字典.

倚天26鍵對應 (字母 -> 注音), 依維基百科「注音輸入法」條目之倚天26鍵對應表:
  a:ㄚ b:ㄅ c:ㄕ/ㄒ d:ㄉ/˙ e:ㄧ f:ㄈ/ˊ g:ㄓ/ㄐ h:ㄏ/ㄦ i:ㄞ j:ㄖ/ˇ
  k:ㄎ/ˋ l:ㄌ/ㄥ m:ㄇ/ㄢ n:ㄋ/ㄣ o:ㄛ p:ㄆ/ㄡ q:ㄗ/ㄟ r:ㄜ s:ㄙ
  t:ㄊ/ㄤ u:ㄩ v:ㄍ/ㄑ w:ㄘ/ㄝ x:ㄨ y:ㄔ/ㄡ z:ㄠ

反查 (注音 -> 字母) 幾乎是一對一, 唯一例外是 ㄡ 同時在 p 鍵與 y 鍵上,
因此含 ㄡ 的音節會產生兩種編碼 (還原真實忘形行為: 兩個鍵都能打出該字).
聲調在本方案 v1 省略 (手機注音多半不打聲調).
"""
import csv
import itertools
import sys

# 注音 -> 倚天26鍵字母 (ㄡ 有兩種)
# 注音 -> 按鍵：倚天26鍵字母 ＋ 倚天41鍵字母/數字/符號，全相容
# 探長的手指證實為 41鍵 派（ㄢ=8、ㄡ=Y），故以 41鍵 為主，並收 26鍵 的合併按法：
# 41鍵字母（一注音一鍵）：A:ㄚ B:ㄅ C:ㄒ D:ㄉ E:ㄧ F:ㄈ G:ㄐ H:ㄏ I:ㄞ J:ㄖ K:ㄎ L:ㄌ
#   M:ㄇ N:ㄋ O:ㄛ P:ㄆ Q:ㄟ R:ㄜ S:ㄙ T:ㄊ U:ㄩ V:ㄍ W:ㄝ X:ㄨ Y:ㄡ Z:ㄠ
# 41鍵數字/符號列：7:ㄑ 8:ㄢ 9:ㄣ 0:ㄤ -:ㄥ ;:ㄗ ,:ㄓ .:ㄔ /:ㄕ ':ㄘ =:ㄦ
# 26鍵合併按法（加收）：C:ㄕ G:ㄓ H:ㄦ L:ㄥ M:ㄢ N:ㄣ P:ㄡ Q:ㄗ T:ㄤ V:ㄑ W:ㄘ Y:ㄔ
BOPOMOFO_TO_KEY = {
    'ㄅ': 'b', 'ㄆ': 'p', 'ㄇ': 'm', 'ㄈ': 'f',
    'ㄉ': 'd', 'ㄊ': 't', 'ㄋ': 'n', 'ㄌ': 'l',
    'ㄍ': 'v', 'ㄎ': 'k', 'ㄏ': 'h',
    'ㄐ': 'g', 'ㄑ': ('v', '7'), 'ㄒ': 'c',
    'ㄓ': ('g', ','), 'ㄔ': ('y', '.'), 'ㄕ': ('c', '/'), 'ㄖ': 'j',
    'ㄗ': ('q', ';'), 'ㄘ': ('w', "'"), 'ㄙ': 's',
    'ㄧ': 'e', 'ㄨ': 'x', 'ㄩ': 'u',
    'ㄚ': 'a', 'ㄛ': 'o', 'ㄜ': 'r', 'ㄝ': 'w',
    'ㄞ': 'i', 'ㄟ': 'q', 'ㄠ': 'z', 'ㄡ': ('p', 'y'),
    'ㄢ': ('m', '8'), 'ㄣ': ('n', '9'), 'ㄤ': ('t', '0'),
    'ㄥ': ('l', '-'), 'ㄦ': ('h', '='),
}
# fcitx5 碼表用的合法按鍵（字母＋數字＋符號；數字 1-4 為聲調，7-0 為 41鍵注音）
KEYS_FCITX5 = 'abcdefghijklmnopqrstuvwxyz1234567890,./;\'' + '-='
TONES = set('ˉˊˇˋ˙')
# 聲調 -> 41鍵數字（1=輕聲 2=二聲 3=三聲 4=四聲；一聲不標記）
TONE_TO_DIGIT = {'ˉ': '', '˙': '1', 'ˊ': '2', 'ˇ': '3', 'ˋ': '4'}

def parse_syllable(syllable):
    """回傳 (字母碼選項 list, 聲調數字 str)。含非法字元時回傳 ([], '')。"""
    tone = ''
    chars = []
    for ch in syllable:
        if ch in TONE_TO_DIGIT:
            tone = TONE_TO_DIGIT[ch]
        else:
            chars.append(ch)
    if not chars:
        return [], ''
    options = []
    for ch in chars:
        key = BOPOMOFO_TO_KEY.get(ch)
        if key is None:
            return [], ''
        options.append((key,) if isinstance(key, str) else key)
    letter_codes = [''.join(combo) for combo in itertools.product(*options)]
    return letter_codes, tone

def entry_to_codes(phones, with_tone):
    """整詞音節串 -> 所有可能的完整編碼。
    with_tone=True 時每音節尾加聲調數字（單字用）；False 則無聲調（詞語用）。"""
    parsed = [parse_syllable(s) for s in phones.split()]
    if not parsed or any(not codes for codes, _ in parsed):
        return []
    if with_tone:
        syl_options = [[lc + tone for lc in codes] for codes, tone in parsed]
    else:
        syl_options = [codes for codes, _ in parsed]
    return [''.join(combo) for combo in itertools.product(*syl_options)]

def load_csv(path):
    rows = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(',')
            if len(parts) != 3:
                continue
            word, freq, phones = parts
            try:
                freq = int(freq)
            except ValueError:
                continue
            rows.append((word, freq, phones))
    return rows

def main():
    if len(sys.argv) != 4:
        print(f'usage: {sys.argv[0]} tsi.csv word.csv out.dict.yaml', file=sys.stderr)
        sys.exit(1)
    tsi_path, word_path, out_path = sys.argv[1:4]

    best = {}  # (word, code) -> max weight
    skipped = 0
    for path in (tsi_path, word_path):
        for word, freq, phones in load_csv(path):
            if not word:
                skipped += 1
                continue
            # 單字加聲調數字，詞語無聲調
            codes = entry_to_codes(phones, with_tone=(len(word) == 1))
            if not codes:
                skipped += 1
                continue
            weight = freq if freq > 0 else 1
            for code in set(codes):
                key = (word, code)
                if weight > best.get(key, 0):
                    best[key] = weight

    entries = sorted(best.items(), key=lambda kv: -kv[1])
    print(f'entries: {len(entries)}, skipped: {skipped}', file=sys.stderr)

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('# Rime dictionary\n')
        f.write('# encoding: utf-8\n')
        f.write('# 倚天26鍵(忘形)注音輸入字典, v1 (無聲調)\n')
        f.write('# 詞庫來源: libchewing-data (LGPL-2.1-or-later), 轉碼: 阿喵\n')
        f.write('---\n')
        f.write('name: eten26\n')
        f.write('version: "0.1"\n')
        f.write('sort: by_weight\n')
        f.write('use_preset_vocabulary: false\n')
        f.write('...\n')
        for (word, code), weight in entries:
            f.write(f'{word}\t{code}\t{weight}\n')
    print(f'wrote {out_path}', file=sys.stderr)

if __name__ == '__main__':
    main()
