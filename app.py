import streamlit as st
from openai import OpenAI
import random

# 1. 界面与 Secrets 配置
st.set_page_config(page_title="Echoes of Soul", page_icon="🌑", layout="centered")

try:
    ds_key = st.secrets["DEEPSEEK_API_KEY"]
except:
    st.error("密钥缺失，请检查 Secrets 中的 DEEPSEEK_API_KEY")
    st.stop()

# 2. 视觉动效逻辑
def apply_visual_effect(mood_type):
    if mood_type == "fireflies":
        st.markdown("""<style>.firefly { position: fixed; background: #ccff00; width: 4px; height: 4px; border-radius: 50%; box-shadow: 0 0 10px #ccff00; z-index: 9999; opacity: 0; animation: drift 10s infinite, flash 3s infinite; } @keyframes drift { 0% { transform: translate(0, 0); } 50% { transform: translate(100px, -100px); } 100% { transform: translate(-50px, -200px); } } @keyframes flash { 0%, 100% { opacity: 0; } 50% { opacity: 0.6; } }</style>""" + "".join([f'<div class="firefly" style="left:{random.randint(5,95)}%; top:{random.randint(10,90)}%; animation-delay:{random.randint(0,10)}s;"></div>' for _ in range(15)]), unsafe_allow_html=True)
    elif mood_type == "balloons":
        st.markdown("""<style>.balloon { position: fixed; bottom: -10%; width: 18px; height: 24px; background: rgba(173, 216, 230, 0.2); border-radius: 50%; z-index: 9999; animation: rise 15s infinite ease-in; } @keyframes rise { 0% { bottom: -10%; opacity: 0; } 20% { opacity: 0.5; } 100% { bottom: 110%; transform: translateX(50px); opacity: 0; } }</style>""" + "".join([f'<div class="balloon" style="left:{random.randint(5,95)}%; animation-delay:{random.randint(0,10)}s;"></div>' for _ in range(8)]), unsafe_allow_html=True)
    else:
        st.markdown("""<style>.snowflake { position: fixed; top: -10%; z-index: 9999; animation: fall 12s infinite linear; } .fluff { width: 8px; height: 8px; background: white; border-radius: 50%; filter: blur(3px); opacity: 0.4; } @keyframes fall { 0% { top: -10%; opacity: 0; } 10% { opacity: 0.4; } 100% { top: 110%; transform: translateX(30px); opacity: 0; } }</style>""" + "".join([f'<div class="snowflake" style="left:{random.randint(5,95)}%; animation-delay:{random.randint(0,12)}s;"><div class="fluff"></div></div>' for _ in range(10)]), unsafe_allow_html=True)

# 3. 全局样式：纯粹神秘感
st.markdown("""
    <style>
    .main { background-color: #0a0b10; color: #d1d1d1; }
    .stTextArea textarea { background-color: #161821; color: #ececec; border: 1px solid #2d3142; border-radius: 4px; font-size: 1.1rem; }
    .stButton button { width: 100%; border-radius: 2px; background: #161821; color: #555; border: 1px solid #2d3142; letter-spacing: 4px; transition: 1s; padding: 12px; }
    .stButton button:hover { border-color: #4facfe; color: #fff; background: #1a1d26; }
    .result-card { background: #161821; padding: 40px; border-radius: 2px; border-left: 1px solid #4facfe; line-height: 2.2; margin-top: 30px; letter-spacing: 1.5px; }
    .label-style { font-style: italic; color: #4facfe; font-size: 1.3rem; margin-bottom: 25px; display: block; border-bottom: 1px solid #222; padding-bottom: 10px; }
    .insight-style { color: #aaa; font-size: 1.05rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🌑 Echoes of Soul")
st.markdown("<p style='color: #333; font-style: italic; letter-spacing: 2px;'>“于静默处，听见冰山下的回响。”</p>", unsafe_allow_html=True)

# 4. 核心逻辑
client = OpenAI(api_key=ds_key, base_url="https://api.deepseek.com")
user_input = st.text_area("", placeholder="描述那些无法言说的瞬息...", height=150)

if st.button("EXCAVATE"):
    if not user_input:
        st.info("深渊需要回声。")
    else:
        with st.spinner("潜入深处..."):
            try:
                # 提示词强化：要求 AI 进行文学化的互文解读
                prompt = f"""
                用户自白：'{user_input}'
                请作为一名具备极高文学素养和存在主义色彩的心理分析师进行解析。
                要求：
                1. [MOOD]：'sad'、'peaceful' 或 'happy'。
                2. [刻印]：4字以内文学标签。
                3. [灵魂嘴替]：
                   - 结合一部经典电影或名曲，用文学化的语言描述用户的心情。
                   - 语气示例：“此时此刻你的心情就如《重庆森林》中的...你迷惘，彷徨，你在找一个影子...”
                   - 必须包含1个心理学专业术语进行“冰山下”的深度剖析。
                4. [秘语]：一句充满神秘感、直击核心的话。
                """
                
                res = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "system", "content": "你是一位不满足于平庸解读的灵魂捕手，擅长光影隐喻。"},
                              {"role": "user", "content": prompt}]
                )
                raw_content = res.choices[0].message.content
                
                # 判定动效
                mood_tag = raw_content.lower()[:50]
                mood_type = "balloons" if "happy" in mood_tag else ("fireflies" if "peaceful" in mood_tag else "snow")
                apply_visual_effect(mood_type)

                # 格式化输出内容
                lines = raw_content.split('\n')
                display_html = ""
                for line in lines:
                    if "[MOOD]" in line: continue
                    if "[刻印]" in line:
                        display_html += f'<span class="label-style">🔖 {line.replace("[刻印]：", "")}</span>'
                    elif "[" in line:
                        display_html += f'<p><b style="color:#4facfe;">{line[:line.find("]")+1]}</b><span class="insight-style">{line[line.find("]")+1:]}</span></p>'
                    elif line.strip():
                        display_html += f'<p class="insight-style">{line}</p>'

                st.markdown(f'<div class="result-card">{display_html}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"连接断开，请重试: {e}")

st.markdown("<br><br><p style='text-align: center; color: #222; font-size: 0.7em;'>V 9.0 | Silence is a mirror.</p>", unsafe_allow_html=True)