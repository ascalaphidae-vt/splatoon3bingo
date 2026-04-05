import copy
import hashlib
import html
import random
import unicodedata
from typing import Dict, Optional

import streamlit as st

st.set_page_config(page_title="スプラビンゴ", page_icon="🎯", layout="wide")

# =========================
# お題データ
# =========================
level1_topics = [
    'フデで「勝つ」',
    'ストリンガーで「勝つ」',
    'シューターで「勝つ」',
    'ブラスターを「使う」',
    'ワイパーを「使う」',
    'スロッシャーで「勝つ」',
    'ローラーで「勝つ」',
    'スプラシューターでキルとアシスト合計5以上',
    '52ガロンで4デス以下',
    'わかばシューターで1000ポイント以上塗る',
    'N-ZAP85(黒ZAP)でSP4回以上使う',
    '1200ポイント以上塗る',
    'リザルトでキルかアシストを合計10以上',
    '5デス以下',
    '1試合でスペシャル5回以上',
    'ダイナモ、リッター、エクスのいずれかを「使う」',
    'ハイドラ、キャンシェル、フルイドのいずれかを「使う」',
    'スパイガジェットソレーラかワイドローラーを「使う」',
    'クラッシュブラスターネオかガエンFFを「使う」',
    'カニタンクを使って１キル以上する',
    'テイオウイカを使って１キル以上する',
    '(スペシャル名)NO.1の表彰を得る',
    'ギア・スタートダッシュを付けて「勝つ」',
    'ギア・復活ペナルティアップを付けて「勝つ」',
    'ギア・受け身術を付けて「勝つ」',
]

level2_topics = [
    '相手チームの誰よりも多いキルとアシスト数の合計',
    '相手チームの誰よりも少ないデス数',
    '相手チームの誰よりも多い塗りポイント',
    '相手チームの誰よりも多いSP使用回数',
    '全体で2番目に少ないキルとアシスト数の合計',
    '全体で2番目に多いデス数',
    '全体で2番目に少ない塗りポイント',
    '全体で2番目に少ないSP使用回数',
    'キルとアシスト数の合計とデス数が同じ',
    'デス数とSP使用数が同じ',
    'キルとアシスト数の合計とSP使用数が同じ',
    'リッター系統でキルとアシスト合計5以上',
    'ダイナモローラー系統で4デス以下',
    'エクスプロッシャー系統で1000ポイント以上塗る',
    'ハイドラント系統でSP4回以上使う',
    'スパイガジェット系統でキルとアシスト合計8以上',
    'ラピッドブラスターエリート系統で2デス以下',
    'ケルビン525系統で800ポイント以上塗る',
    'プロモデラー系統でSP7回以上使う',
    'イグザミナー系統でキルかアシスト合計10以上',
    '14式竹筒銃系統で3デス以下',
    'LACT系統で1500ポイント以上塗る',
    'R-PEN系統でSP6回以上使う',
    'ラインマーカーでキルする',
    'カーリングボムでキルする',
    'トリプルトルネードでキルする',
    'ショクワンダーの突撃でキルする',
    'ウルトラハンコ投げでキルする(自己申告)',
    'フデかローラーでコロコロキルする',
    'イカニンでイカ速0のダイナモテスラを「使う」',
    'ペナルティアップを付けたもみじシューターを「使う」',
    '逆境、イカニン、対物アップを同時に「使う」',
    'メインギアパワーをインク回復力アップのみにする',
    'メインギアパワーをサブ影響軽減のみにする',
    'メインギアパワーをスペシャル減少量ダウンのみにする',
    '注目された時間NO.1と塗りポイントNO.1の表彰を同時に得る',
    '塗りポイントNO.1とバトルNO.1の表彰を同時に得る',
    '注目された時間NO.1とバトルNO.1の表彰を同時に得る',
    'シェルターで「勝つ」',
    'チャージャーで「勝つ」',
    'スクイックリンβを「使う」',
    'パブロ・ヒューを「使う」',
    'H3リールガンDを「使う」',
    'ソイチューバーカスタムを「使う」',
    'スピナーで「勝つ」',
    'マニューバーで「勝つ」',
]

level3_topics = [
    'キルとアシスト合計15回以上で「勝つ」',
    '1デス以下で「勝つ」',
    '1500ポイント以上塗って「勝つ」',
    'スペシャルを7回以上使って「勝つ」',
    'キルとアシスト数より多いデス数で「勝つ」',
    'トラップで１キル以上する',
    'アメフラシで１キル以上する',
    'スミナガシートで１キル以上する',
    'トライストリンガー系統で金表彰3つ',
    'キャンシェル系統で金表彰3つ',
    'オフロ無印でキルかアシスト10以上',
    'フィンセント無印で2デス以下',
    'Sブラ91で塗りポイント1000以上',
    '金ノーチラスでSP5回以上使う',
    '張替傘乙(和傘乙)を使って勝利する',
    'ボルネオを使って勝利する',
    '塗りポイントNO.1と移動した距離NO.1の表彰を同時に得る',
    'バトルNO.1と耐えたダメージNO.1の表彰を同時に得る',
    '注目された時間NO.1とアシスト数NO.1の表彰を同時に得る',
    'H3Dで3点バーストキルをする(自己申告)',
    '一人が1試合中スペシャルを使わない',
]

level4_topics = [
    'スペースシューターでトドメNO.1を得る',
    'カーボンローラー無印でアシストNO.1を得る',
    'ジャイロオフで「勝つ」',
    'スティックとジャイロ感度-5で「勝つ」',
    'カニタンクの球体モードで1キル以上する',
    '3キル3デス3スペシャルで「勝つ」',
    '●●をたおした‼が3つ表示されているときにスクショを撮る',
    'フルイドVカスタムでピチュンキルをする(自己申告)',
    'デンタルワイパーミントで1振りで同時に2人斬る(自己申告)',
    'キルかアシスト合計1回以下で「勝つ」',
    '塗りポイント400ポイント以下で「勝つ」',
]

center_topics = [
    'ビンゴプレイヤーで同じブキにそろえる',
    '互いの持ちブキを交換',
    '互いのいつものギア(見た目)を交換',
    'おそろいのギアにする',
    '開幕ナイスをする',
]

ROWS = ['1', '2', '3', '4', '5']
COLS = ['A', 'B', 'C', 'D', 'E']
CENTER_POS = 'C-3'
MAX_HISTORY = 5

COLOR_MAP = {
    'pink': '#ffd7e2',
    'green': '#daf5da',
    'blue': '#dceeff',
    'lightyellow': '#fff7c8',
    'lightpurple': '#ead9ff',
    'white': '#ffffff',
}

COLOR_LABELS = {
    'pink': 'Lv1枠',
    'green': 'Lv2枠',
    'blue': 'Lv3枠',
    'lightpurple': 'Lv4枠',
    'lightyellow': '中央枠',
    'white': 'クリア済み',
}

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 1.0rem;
        max-width: 1480px;
    }
    .app-title {
        font-size: 2rem;
        font-weight: 700;
        margin-top: 0.1rem;
        margin-bottom: 0.2rem;
        line-height: 1.25;
    }
    .app-sub {
        color: #666;
        margin-bottom: 1.0rem;
    }
    .seed-note {
        font-size: 0.92rem;
        color: #666;
        margin-top: -0.2rem;
        margin-bottom: 0.8rem;
    }
    .bingo-cell {
        border: 1px solid rgba(49, 51, 63, 0.14);
        border-radius: 12px;
        padding: 0.42rem 0.48rem;
        min-height: 96px;
        margin-bottom: 0.24rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
        overflow: hidden;
    }
    .bingo-pos {
        font-size: 0.68rem;
        font-weight: 700;
        color: #222222;
        opacity: 0.9;
        margin-bottom: 0.18rem;
    }
    .bingo-topic {
        font-size: 0.76rem;
        line-height: 1.24;
        color: #111111;
        word-break: break-word;
        overflow-wrap: anywhere;
        white-space: pre-wrap;
        font-weight: 600;
    }
    .done-badge {
        display: inline-block;
        padding: 0.14rem 0.42rem;
        border-radius: 999px;
        background: rgba(0, 0, 0, 0.08);
        color: #111111;
        font-size: 0.66rem;
        font-weight: 700;
        margin-top: 0.4rem;
    }
    .legend-chip {
        display: inline-block;
        padding: 0.22rem 0.56rem;
        border-radius: 999px;
        margin: 0.1rem 0.18rem 0.1rem 0;
        font-size: 0.78rem;
        border: 1px solid rgba(49, 51, 63, 0.12);
        color: #111111;
        font-weight: 600;
    }
    div[data-testid="column"] {
        padding-left: 0.14rem;
        padding-right: 0.14rem;
    }
    div[data-testid="stButton"] > button {
        padding-top: 0.28rem;
        padding-bottom: 0.28rem;
        font-size: 0.88rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def init_state() -> None:
    if 'bingo_card' not in st.session_state:
        st.session_state.bingo_card = None
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'current_level' not in st.session_state:
        st.session_state.current_level = 1
    if 'last_seed_text' not in st.session_state:
        st.session_state.last_seed_text = ""

def text_to_seed(text: str, max_value: Optional[int] = None) -> int:
    normalized = unicodedata.normalize("NFC", text)
    digest = hashlib.sha256(normalized.encode("utf-8")).digest()
    seed = int.from_bytes(digest[:8], byteorder="big", signed=False)
    if max_value is not None:
        if max_value <= 0:
            raise ValueError("max_value は 1 以上である必要があります。")
        seed %= max_value
    return seed

def make_random_from_text(text: str) -> random.Random:
    return random.Random(text_to_seed(text))

def generate_bingo_card(level: int, seed_text: str) -> Dict[str, Dict[str, str]]:
    rng = make_random_from_text(f"level:{level}|seed:{seed_text}")

    if level == 1:
        topics_level1 = rng.sample(level1_topics, 14)
        topics_level2 = rng.sample(level2_topics, 10)
        topics = topics_level1 + topics_level2
        colors = ['pink'] * 14 + ['green'] * 10
    elif level == 2:
        topics_level1 = rng.sample(level1_topics, 10)
        topics_level2 = rng.sample(level2_topics, 12)
        topics_level3 = rng.sample(level3_topics, 2)
        topics = topics_level1 + topics_level2 + topics_level3
        colors = ['pink'] * 10 + ['green'] * 12 + ['blue'] * 2
    elif level == 3:
        topics_level1 = rng.sample(level1_topics, 7)
        topics_level2 = rng.sample(level2_topics, 13)
        topics_level3 = rng.sample(level3_topics, 3)
        topics_level4 = rng.sample(level4_topics, 1)
        topics = topics_level1 + topics_level2 + topics_level3 + topics_level4
        colors = ['pink'] * 7 + ['green'] * 13 + ['blue'] * 3 + ['lightpurple'] * 1
    elif level == 4:
        topics_level2 = rng.sample(level2_topics, 10)
        topics_level3 = rng.sample(level3_topics, 12)
        topics_level4 = rng.sample(level4_topics, 2)
        topics = topics_level2 + topics_level3 + topics_level4
        colors = ['green'] * 10 + ['blue'] * 12 + ['lightpurple'] * 2
    elif level == 5:
        topics_level2 = rng.sample(level2_topics, 6)
        topics_level3 = rng.sample(level3_topics, 12)
        topics_level4 = rng.sample(level4_topics, 6)
        topics = topics_level2 + topics_level3 + topics_level4
        colors = ['green'] * 6 + ['blue'] * 12 + ['lightpurple'] * 6
    else:
        raise ValueError('レベルは1〜5のみ対応です。')

    combined = list(zip(topics, colors))
    rng.shuffle(combined)
    topics, colors = zip(*combined)
    center_topic = rng.choice(center_topics)

    bingo_card: Dict[str, Dict[str, str]] = {}
    index = 0
    for col in COLS:
        for row in ROWS:
            position = f'{col}-{row}'
            if position == CENTER_POS:
                bingo_card[position] = {'topic': center_topic, 'color': 'lightyellow', 'cleared': False}
            else:
                bingo_card[position] = {'topic': topics[index], 'color': colors[index], 'cleared': False}
                index += 1
    return bingo_card

def push_history() -> None:
    if st.session_state.bingo_card is None:
        return
    st.session_state.history.append(copy.deepcopy(st.session_state.bingo_card))
    if len(st.session_state.history) > MAX_HISTORY:
        st.session_state.history.pop(0)

def clear_cell(position: str) -> None:
    if st.session_state.bingo_card is None:
        return
    cell = st.session_state.bingo_card[position]
    if cell['cleared']:
        return
    push_history()
    cell['topic'] = 'Clear!!'
    cell['color'] = 'white'
    cell['cleared'] = True

def undo() -> None:
    if st.session_state.history:
        st.session_state.bingo_card = st.session_state.history.pop()

def count_cleared(card: Dict[str, Dict[str, str]]) -> int:
    return sum(1 for cell in card.values() if cell.get('cleared'))

def render_legend() -> None:
    chips = []
    for key in ['pink', 'green', 'blue', 'lightpurple', 'lightyellow', 'white']:
        chips.append(
            f"<span class='legend-chip' style='background:{COLOR_MAP[key]}'>{html.escape(COLOR_LABELS[key])}</span>"
        )
    st.markdown(''.join(chips), unsafe_allow_html=True)

def render_cell(position: str, cell: Dict[str, str]) -> None:
    bg = COLOR_MAP.get(cell['color'], '#ffffff')
    body = html.escape(cell['topic']).replace('\n', '<br>')
    done_badge = "<div class='done-badge'>クリア済み</div>" if cell.get('cleared') else ''
    st.markdown(
        f"""
        <div class="bingo-cell" style="background:{bg};">
            <div>
                <div class="bingo-pos">{position}</div>
                <div class="bingo-topic">{body}</div>
            </div>
            {done_badge}
        </div>
        """,
        unsafe_allow_html=True,
    )
    if cell.get('cleared'):
        st.button('クリア済み', key=f'done_{position}', disabled=True, use_container_width=True)
    else:
        if st.button(f'{position} をクリア', key=f'clear_{position}', use_container_width=True):
            clear_cell(position)
            st.rerun()

init_state()

st.markdown("<div class='app-title'>🎯 スプラビンゴ</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='app-sub'>レベル別5x5ビンゴを生成して、達成したマスを手動でクリアしていく用のStreamlit版です。</div>",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header('設定')
    selected_level = st.radio('レベルを選ぶ', [1, 2, 3, 4, 5], index=st.session_state.current_level - 1, horizontal=False)
    seed_text = st.text_input("シード文字列", value=st.session_state.last_seed_text)
    st.caption("同じ文字列なら同じビンゴシートになります。空欄でも生成できますが、その場合は毎回同じ「空欄用シート」になります。")

    if st.button('新しいビンゴを生成', use_container_width=True):
        st.session_state.current_level = selected_level
        st.session_state.last_seed_text = seed_text
        st.session_state.bingo_card = generate_bingo_card(selected_level, seed_text)
        st.session_state.history = []
        st.rerun()

    undo_disabled = len(st.session_state.history) == 0
    if st.button('1手もどす', use_container_width=True, disabled=undo_disabled):
        undo()
        st.rerun()

    if st.session_state.bingo_card is not None:
        cleared = count_cleared(st.session_state.bingo_card)
        st.metric('クリア済みマス', f'{cleared} / 25')
        st.caption(f'戻せる履歴: {len(st.session_state.history)} / {MAX_HISTORY}')
        shown_seed = st.session_state.last_seed_text if st.session_state.last_seed_text != "" else "（空欄）"
        st.caption(f'現在のシード: {shown_seed}')

    st.divider()
    st.write('使い方')
    st.caption('1. レベルとシード文字列を入れて新規生成')
    st.caption('2. 同じレベル・同じ文字列なら同じ盤面になる')
    st.caption('3. 中央マスもシードに応じて再現可能に変わる')
    st.caption('4. 達成したマスだけ「◯-◯ をクリア」を押す')
    st.caption('5. 間違えたら「1手もどす」を使う')

if st.session_state.bingo_card is None:
    st.info('左のサイドバーでレベルとシード文字列を入力して「新しいビンゴを生成」を押してください。')
    st.stop()

header_left, header_right = st.columns([1.2, 0.8])
with header_left:
    st.subheader(f'レベル {st.session_state.current_level} ビンゴ')
with header_right:
    cleared = count_cleared(st.session_state.bingo_card)
    st.write(f'進捗: **{cleared} / 25**')

current_seed_label = st.session_state.last_seed_text if st.session_state.last_seed_text != "" else "（空欄）"
st.markdown(f"<div class='seed-note'>現在のシード文字列: <b>{html.escape(current_seed_label)}</b></div>", unsafe_allow_html=True)

render_legend()
st.write('')

for row in ROWS:
    row_columns = st.columns(5, gap='small')
    for idx, col in enumerate(COLS):
        pos = f'{col}-{row}'
        with row_columns[idx]:
            render_cell(pos, st.session_state.bingo_card[pos])