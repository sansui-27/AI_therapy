import streamlit as st
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import io, requests, os

# 1. 字体处理
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

# 2. 界面样式
st.set_page_config(page_title="情绪魔法实验室", page_icon="🧪")
st.markdown("""
    <style>
    .stTextArea textarea {border-radius:15px; border: 1px solid #4A90E2;}
    .stButton button {background: linear-gradient(45deg, #6a11cb, #2575fc); color:white; border-radius:25px; font-weight:bold;}
    </style>
""", unsafe_allow_html=True)

st.title("🧪 情绪魔法实验室")
st.caption("将碎掉的情绪，炼成电影与音乐的诗")

# 3. AI 逻辑（更新了提示词）
client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
user_input = st.text_area("此刻的心情碎语...", placeholder="比如：窗外在下雨，想起了一些往事...")

if st.button("开始炼制魔法药水 🔮"):
    if not user_input:
        st.warning("药炉还是空的哦，请输入心情。")
    else:
        with st.spinner("✨ 正在检索光影与乐章..."):
            try:
                # 提示词升级：要求电影、音乐和短标签
                prompt = f"""
                用户心情：'{user_input}'
                请以此炼制药方，严格遵守格式：
                1. [标签]：4-6个字的诗意短语。
                2. [电影]：推荐一部治愈此情绪的电影名及一句话推荐。
                3. [音乐]：推荐一首适合此时听的歌曲名及氛围描述。
                4. [寄语]：一句温柔的短句。
                """
                
                res = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "system", "content": "你是一位精通电影和音乐的情绪疗愈师，说话简练且有高级感。"},
                              {"role": "user", "content": prompt}]
                )
                text = res.choices[0].message.content
                st.success("炼制完成")
                st.info(text)

                # 4. 海报绘制优化
                f_path = load_font()
                img = Image.new('RGB', (600, 850), color='#121212')
                draw = ImageDraw.Draw(img)
                
                # 渐变边框效果
                draw.rectangle([15, 15, 585, 835], outline="#3A3A3A", width=1)
                draw.rectangle([25, 25, 575, 825], outline="#4A90E2", width=2)
                
                try:
                    t_font = ImageFont.truetype(f_path, 45) if f_path else ImageFont.load_default()
                    c_font = ImageFont.truetype(f_path, 22) if f_path else ImageFont.load_default()
                    
                    # 写入标题
                    draw.text((300, 100), "情绪处方清单", font=t_font, fill="#4A90E2", anchor="mm")
                    
                    # 自动换行写入
                    y = 200
                    lines = text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line: continue
                        
                        # 为不同的部分上色
                        fill_color = "#FFFFFF"
                        if "[标签]" in line: fill_color = "#FFCC00"
                        elif "[电影]" in line or "[音乐]" in line: fill_color = "#00FFCC"
                        
                        # 简单的自动换行处理（每行约18个汉字）
                        for i in range(0, len(line), 18):
                            draw.text((60, y), line[i:i+18], font=c_font, fill=fill_color)
                            y += 40
                        y += 15 # 段落间距
                    
                    draw.text((300, 780), "✦ 每一阵风都有它的节奏 ✦", font=c_font, fill="#555555", anchor="mm")
                except:
                    draw.text((100, 400), "Poster Error", fill="white")

                st.image(img)
                
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.download_button("📥 保存这张疗愈书签", buf.getvalue(), "healing_card.png", "image/png")
                
            except Exception as e:
                st.error(f"炼制失败：{e}")