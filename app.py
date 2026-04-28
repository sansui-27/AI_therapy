import streamlit as st
from openai import OpenAI
import random
import urllib.parse

# 1. 界面配置
st.set_page_config(page_title="Echoes of Soul", page_icon="✨", layout="centered")

# 2. 增强版视觉动效逻辑：增加密度，保持舒缓
def apply_visual_effect(mood_type):
    if mood_type == "fireflies": # 增强版萤火虫：数量增加，明灭更柔和
        st.markdown("""<style>.firefly { position: fixed; background: #ccff00; width: 5px; height: 5px; border-radius: 50%; box-shadow: 0 0 15px #ccff00; z-index: 9999; opacity: 0; animation: drift 15s infinite, flash 4s infinite; } @keyframes drift { 0% { transform: translate(0, 0); } 50% { transform: translate(150px, -150px); } 100% { transform: translate(-80px, -300px); } } @keyframes flash { 0%, 100% { opacity: 0; } 50% { opacity: 0.7; } }</style>""" + "".join([f'<div class="firefly" style="left:{random.randint(2,98)}%; top:{random.randint(10,90)}%; animation-delay:{random.randint(0,15)}s;"></div>' for _ in range(35)]), unsafe_allow_html=True)
    elif mood_type == "balloons": # 增强版气球：更大更梦幻
        st.markdown("""<style>.balloon { position: fixed; bottom: -15%; width: 25px; height: 32px; background: rgba(173, 216, 230, 0.25); border-radius: 50%; z-index: 9999; animation: rise 18s infinite ease-in; } @keyframes rise { 0% { bottom: -15%; opacity: 0; transform: translateX(0); } 20% { opacity: 0.6; } 100% { bottom: 115%; transform: translateX(80px); opacity: 0; } }</style>""" + "".join([f'<div class="balloon" style="left:{random.randint(5,95)}%; animation-delay:{random.randint(0,12)}s;"></div>' for _ in range(15)]), unsafe_allow_html=True)
    else: # 增强版绒雪：覆盖面更广，更密集
        st.markdown("""<style>.snowflake { position: fixed; top: -10%; z-index: 9999; animation: fall 15s infinite linear; } .fluff { width: 10px; height: 10px; background: white; border-radius: 50%; filter: blur(4px); opacity: 0.5; } @keyframes fall { 0% { top: -10%; opacity: 0; } 15% { opacity: 0.5; } 100% { top: 110%; transform: translateX(60px); opacity: 0; } }</style>""" + "".join([f'<div class="snowflake" style="left:{random.randint(2,98)}%; animation-delay:{random.randint(0,15)}s;"><div class="fluff"></div></div>' for _ in range(25)]), unsafe_allow_html=True)

# 3. 全局样式
st.markdown("""
    <style>
    .main { background-color: #0a0b10; color: #d1d1d1; }
    .stTextArea textarea { background-color: #161821; color: #ececec; border: 1px solid #2d3142; border-radius: 4px; font-size: 1.1rem; }
    .guide-text { color: #444; font-size: 0.85rem; margin-top: -10px; margin-bottom: 20px; letter-spacing: 1.5px; }
    .stButton button { width: 100%; border-radius: 2px; background: #161821; color: #777; border: 1px solid #2d3142; letter-spacing: 4px; transition: 1s; padding: 12px; }
    .stButton button:hover { border-color: #4facfe; color: #fff; background: #1a1d26; }
    .result-card { background: #161821; padding: 40px; border-radius: 2px; border-left: 1px solid #4facfe; line-height: 2.2; margin-top: 30px; }
    .label-style { font-style: italic; color: #4facfe; font-size: 1.3rem; margin-bottom: 25px; display: block; border-bottom: 1px solid #222; padding-bottom: 10px; letter-spacing: 3px; }
    /* 音乐按钮样式 */
    .music-btn { display: inline-block; padding: 5px 15px; border: 1px solid #4facfe; color: #4facfe !important; text-decoration: none; border-radius: 20px; font-size: 0.8rem; margin-top: 10px; transition: 0.3s; }
    .music-btn:hover { background: #4facfe; color: #fff !important; }
    </style>
""", unsafe_allow_html=True)

st.title("✨ Echoes of Soul")
st.markdown("<p style='color: #444; font-style: italic; letter-spacing: 2px;'>“于静默处，听见冰山下的回响。”</p>", unsafe_allow_html=True)

# 4. 核心逻辑
client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
user_input = st.text_area("", placeholder="描述那些无法言说的瞬息...", height=150)
st.markdown('<p class="guide-text">✦ 刻印意象 · 意识投影 · 捕捉余音</p>', unsafe_allow_html=True)

if st.button("开启挖掘 EXCAVATE"):
    if not user_input:
        st.info("深渊需要回声。")
    else:
        with st.spinner("正在洗印潜意识底片..."):
            try:
                prompt = f"""
                用户自白：'{user_input}'
                请作为一名具备极高艺术审美和存在主义色彩的心理分析师。
                要求：
                1. [MOOD]：'sad'、'peaceful' 或 'happy'。
                2. [刻印]：4字以内文学标签。
                3. [意识投影]：
                   - 结合一部经典电影描述用户情绪。
                   - 包含1个心理学专业术语。
                4. [共振旋律]：推荐一首氛围感极其对应的歌曲名（含歌手）。
                5. [余音]：一句话直击核心。
                """
                
                res = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "system", "content": "你是一位文字极简、擅长艺术通感的灵魂捕手。"},
                              {"role": "user", "content": prompt}]
                )
                raw_content = res.choices[0].message.content
                
                # 判定动效
                mood_tag = raw_content.lower()[:50]
                mood_type = "balloons" if "happy" in mood_tag else ("fireflies" if "peaceful" in mood_tag else "snow")
                apply_visual_effect(mood_type)

                # 格式化输出
                lines = raw_content.split('\n')
                display_html = ""
                song_name = ""
                
                for line in lines:
                    if "[MOOD]" in line: continue
                    if "[刻印]" in line:
                        display_html += f'<span class="label-style">🔖 {line.replace("[刻印]：", "")}</span>'
                    elif "[共振旋律]" in line:
                        song_name = line.replace("[共振旋律]：", "").strip()
                        search_url = f"https://music.163.com/#/search/m/?s={urllib.parse.quote(song_name)}"
                        display_html += f'<p><b style="color:#4facfe;">【共振旋律】</b><span style="color:#aaa;">{song_name}</span> <a href="{search_url}" target="_blank" class="music-btn">🎵 在网易云开启聆听</a></p>'
                    elif "[" in line:
                        tag = line[line.find("[")+1:line.find("]")]
                        content = line[line.find("]")+1:]
                        display_html += f'<p><b style="color:#4facfe;">【{tag}】</b><span style="color:#aaa;">{content}</span></p>'
                    elif line.strip():
                        display_html += f'<p style="color:#aaa;">{line}</p>'

                st.markdown(f'<div class="result-card">{display_html}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"连接中断: {e}")

st.markdown("<br><br><p style='text-align: center; color: #222; font-size: 0.7em;'>V 14.0 | Silence is a mirror.</p>", unsafe_allow_html=True)