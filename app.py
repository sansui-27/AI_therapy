import streamlit as st
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import io, requests, os

# 1. 字体与配置
FONT_URL = "https://github.com/googlefonts/noto-cjk/raw/main/Sans/SubsetOTF/SC/NotoSansCJKsc-Regular.otf"
FONT_PATH = "font.otf"

@st.cache_resource
def load_font():
    if not os.path.exists(FONT_PATH):
        try:
            r = requests.get(FONT_URL)
            with open(FONT_PATH, "wb") as f: f.write(r.content)
        except: return None
    return FONT_PATH

# 2. 高级感 CSS：自定义“绒绒”雪花动画
def trigger_soft_snow():
    st.markdown("""
        <style>
        .snowflake { color: #fff; font-size: 1.2em; font-family: Arial; text-shadow: 0 0 5px #fff; opacity: 0.8; }
        @-webkit-keyframes snowflakes-fall{0%{top:-10%}100%{top:100%}}
        @-webkit-keyframes snowflakes-shake{0%{-webkit-transform:translateX(0px);transform:translateX(0px)}50%{-webkit-transform:translateX(80px);transform:translateX(80px)}100%{-webkit-transform:translateX(0px);transform:translateX(0px)}}
        @keyframes snowflakes-fall{0%{top:-10%}100%{top:100%}}
        @keyframes snowflakes-shake{0%{transform:translateX(0px)}50%{transform:translateX(80px)}100%{transform:translateX(0px)}}
        .snowflake{position:fixed;top:-10%;z-index:9999;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none;cursor:default;-webkit-animation-name:snowflakes-fall,snowflakes-shake;-webkit-animation-duration:10s,3s;-webkit-animation-timing-function:linear,ease-in-out;-webkit-animation-iteration-count:infinite,infinite;-webkit-animation-play-state:running,running;animation-name:snowflakes-fall,snowflakes-shake;animation-duration:10s,3s;animation-timing-function:linear,ease-in-out;animation-iteration-count:infinite,infinite;animation-play-state:running,running}
        .snowflake:nth-of-type(0){left:1%;-webkit-animation-delay:0s,0s;animation-delay:0s,0s}
        .snowflake:nth-of-type(1){left:10%;-webkit-animation-delay:1s,1s;animation-delay:1s,1s}
        .snowflake:nth-of-type(2){left:20%;-webkit-animation-delay:6s,.5s;animation-delay:6s,.5s}
        .snowflake:nth-of-type(3){left:30%;-webkit-animation-delay:4s,2s;animation-delay:4s,2s}
        .snowflake:nth-of-type(4){left:40%;-webkit-animation-delay:2s,2s;animation-delay:2s,2s}
        .snowflake:nth-of-type(5){left:50%;-webkit-animation-delay:8s,3s;animation-delay:8s,3s}
        .snowflake:nth-of-type(6){left:60%;-webkit-animation-delay:6s,2s;animation-delay:6s,2s}
        .snowflake:nth-of-type(7){left:70%;-webkit-animation-delay:2.5s,1s;animation-delay:2.5s,1s}
        .snowflake:nth-of-type(8){left:80%;-webkit-animation-delay:1s,0s;animation-delay:1s,0s}
        .snowflake:nth-of-type(9){left:90%;-webkit-animation-delay:3s,1.5s;animation-delay:3s,1.5s}
        /* 绒绒感：模糊粒子 */
        .fluff { width: 8px; height: 8px; background: white; border-radius: 50%; filter: blur(3px); display: inline-block; }
        </style>
        <div class="snowflakes" aria-hidden="true">
          <div class="snowflake"><div class="fluff"></div></div>
          <div class="snowflake"><div class="fluff"></div></div>
          <div class="snowflake"><div class="fluff" style="width:12px;height:12px;filter:blur(5px);"></div></div>
          <div class="snowflake"><div class="fluff"></div></div>
          <div class="snowflake"><div class="fluff" style="width:6px;height:6px;filter:blur(2px);"></div></div>
          <div class="snowflake"><div class="fluff"></div></div>
          <div class="snowflake"><div class="fluff" style="width:10px;height:10px;filter:blur(4px);"></div></div>
          <div class="snowflake"><div class="fluff"></div></div>
          <div class="snowflake"><div class="fluff"></div></div>
          <div class="snowflake"><div class="fluff"></div></div>
        </div>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="情绪状态签", page_icon="🌙")

# 3. AI 逻辑与提示词升级
client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")

st.title("🌙 情绪状态签")
st.caption("认知觉醒 · 去病理化 · 灵魂重建")

user_input = st.text_area("此刻你的内心波澜...", placeholder="描述越详细，语义分析越精准...", height=120)

if st.button("生成状态签 🔮"):
    if not user_input:
        st.warning("请投入你的情绪碎片。")
    else:
        with st.spinner("🧠 正在进行多维度语义建模..."):
            try:
                # 提示词：要求包含 emoji、专业术语、分列排版
                prompt = f"""
                用户内容：'{user_input}'
                请生成一份【情绪状态签】。要求：
                1. [今日标签]：4字以内 + 2个意境Emoji。
                2. [心理维度]：使用1个核心心理学术语（如：防御机制、习得性无助、格式塔、认知失调等），并从‘认知觉醒’角度给出高级感解析。
                3. [音频疗愈]：推荐一首适合歌曲名，并提供一个‘[去听歌]’的文字说明，链接网易云搜索。
                4. [电影处方]：推荐一部高分治愈电影。
                5. [状态语词]：用Emoji分行排列，给出3个情绪状态词。
                """
                
                res = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "system", "content": "你是一位拥有资深背景的心理咨询师，语言温柔但充满洞见，善于使用Emoji辅助表达。"},
                              {"role": "user", "content": prompt}]
                )
                text = res.choices[0].message.content
                
                # 触发自定义“绒绒”雪花
                trigger_soft_snow()

                # 界面展示
                st.markdown(f"""
                <div style="background: #1c1f26; padding: 25px; border-radius: 20px; border: 1px solid #4facfe; color: white; line-height: 1.8;">
                    {text.replace('[', '<span style="color:#4facfe; font-weight:bold;">[').replace(']', ']</span>')}
                </div>
                """, unsafe_allow_html=True)

                # 4. 海报生成
                f_path = load_font()
                img = Image.new('RGB', (600, 1000), color='#121212')
                draw = ImageDraw.Draw(img)
                draw.rectangle([20, 20, 580, 980], outline="#4facfe", width=2)
                
                try:
                    t_font = ImageFont.truetype(f_path, 45) if f_path else ImageFont.load_default()
                    c_font = ImageFont.truetype(f_path, 22) if f_path else ImageFont.load_default()
                    
                    draw.text((300, 100), "情绪状态签", font=t_font, fill="#4facfe", anchor="mm")
                    
                    y = 200
                    for line in text.split('\n'):
                        line = line.strip()
                        if not line: continue
                        color = "#4facfe" if "[" in line else "#ffffff"
                        for i in range(0, len(line), 18):
                            draw.text((60, y), line[i:i+18], font=c_font, fill=color)
                            y += 42
                        y += 10
                except: pass

                st.image(img, use_container_width=True)
                
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.download_button("📥 保存这张卡片", buf.getvalue(), "soul_card.png", "image/png")

            except Exception as e:
                st.error(f"分析中断：{e}")

st.markdown("<br><center style='color:#555;'>✦ 万物皆有裂痕，那是光照进来的地方 ✦</center>", unsafe_allow_html=True)