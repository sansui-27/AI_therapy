import streamlit as st
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import io, requests, os

# 1. 自动处理字体（解决海报方块字）
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

# 2. 界面配置
st.set_page_config(page_title="情绪魔法实验室", page_icon="🧪")
st.markdown("""
    <style>
    .stTextArea textarea {border-radius:15px; border: 1px solid #4A90E2;}
    .stButton button {background: linear-gradient(45deg, #6a11cb, #2575fc); color:white; border-radius:25px; font-weight:bold; width: 100%;}
    .prescription-box {background-color:#1e1e32; padding:20px; border-radius:15px; border-left: 5px solid #4A90E2; color: white;}
    </style>
""", unsafe_allow_html=True)

st.title("🧪 情绪魔法实验室")
st.caption("将碎掉的情绪，炼成电影与音乐的诗")

# 3. AI 逻辑
client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
user_input = st.text_area("此刻的心情碎语...", placeholder="比如：窗外在下雨，想起了一些往事...")

if st.button("开始炼制魔法药水 🔮"):
    if not user_input:
        st.warning("药炉还是空的哦。")
    else:
        with st.spinner("✨ 正在检索光影与乐章..."):
            try:
                # 强化版提示词
                prompt = f"""
                用户心情：'{user_input}'
                请以此炼制药方，严格遵守格式：
                [标签]：4个字的诗意短语。
                [电影]：推荐一部治愈此情绪的电影名及一句话推荐。
                [音乐]：推荐一首适合此时听的歌曲名及氛围描述。
                [寄语]：一句温柔的短句。
                """
                
                res = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "system", "content": "你是一位文艺的情绪疗愈师，擅长用电影和音乐治愈人心。"},
                              {"role": "user", "content": prompt}]
                )
                content = res.choices[0].message.content
                
                st.snow()
                st.success("药水炼制成功！")
                st.markdown(f'<div class="prescription-box">{content}</div>', unsafe_allow_html=True)

                # 4. 绘制海报
                f_path = load_font()
                img = Image.new('RGB', (600, 850), color='#121212')
                draw = ImageDraw.Draw(img)
                draw.rectangle([20, 20, 580, 830], outline="#4A90E2", width=2)
                
                try:
                    t_font = ImageFont.truetype(f_path, 40) if f_path else ImageFont.load_default()
                    c_font = ImageFont.truetype(f_path, 22) if f_path else ImageFont.load_default()
                    
                    draw.text((300, 100), "情绪处方清单", font=t_font, fill="#4A90E2", anchor="mm")
                    
                    y = 180
                    for line in content.split('\n'):
                        line = line.strip()
                        if not line: continue
                        color = "#FFCC00" if "[" in line else "#FFFFFF"
                        # 自动换行
                        for i in range(0, len(line), 18):
                            draw.text((60, y), line[i:i+18], font=c_font, fill=color)
                            y += 40
                        y += 10
                    
                    draw.text((300, 780), "✦ 每一阵风都有它的节奏 ✦", font=c_font, fill="#555555", anchor="mm")
                except:
                    draw.text((100, 400), "Poster Font Error", fill="white")

                st.image(img, caption="专属情绪海报")
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.download_button("📥 下载海报", buf.getvalue(), "poster.png", "image/png")
                
            except Exception as e:
                st.error(f"失败了: {e}")