import streamlit as st
import openai
from PIL import Image, ImageDraw, ImageFont
import io
import random

# --- 1. 页面配置 ---
st.set_page_config(page_title="魔力情绪屋", page_icon="🧪")

# --- 2. 密钥读取 ---
try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except:
    st.error("请在 Secrets 中配置 DEEPSEEK_API_KEY")
    st.stop()

# --- 3. 辅助函数：生成海报 ---
def generate_poster(label, content):
    # 创建一个渐变背景
    img = Image.new('RGB', (800, 1000), color=(30, 30, 50))
    d = ImageDraw.Draw(img)
    
    # 简单的装饰线条
    d.rectangle([20, 20, 780, 980], outline=(100, 100, 250), width=5)
    
    # 写入文字 (这里由于服务器字体限制，默认使用基础字体，部署时可上传自定义中文字体)
    try:
        # 尝试写入标题和标签
        d.text((400, 150), "🌙 灵感疗愈处方", fill=(200, 200, 255), anchor="mm")
        d.text((400, 300), f"【{label}】", fill=(255, 215, 0), anchor="mm")
        
        # 将正文简单分行显示
        margin = 100
        offset = 450
        for line in content[:150] + "...": # 截取部分文字防止溢出
             d.text((margin, offset), line, fill=(255, 255, 255))
             offset += 30
    except:
        d.text((100, 450), "Poster Generated", fill=(255, 255, 255))

    # 转为字节流供下载
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# --- 4. 界面设计 ---
st.title("🧪 情绪魔法实验室")
st.markdown("把你的压力投进烧杯，炼制一份灵魂处方。")

user_input = st.text_area("在此投递你的情绪片段...", placeholder="例如：我想逃离这里，去一个没有信号的森林...")

if st.button("开始炼制魔法药水 🔮"):
    if not user_input:
        st.warning("药炉不能为空哦。")
    else:
        client = openai.OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        
        # 魔法药水加载动画
        status_text = st.empty()
        progress_bar = st.progress(0)
        magic_phases = ["正在研磨忧虑...", "正在加入月光粉末...", "正在搅拌情绪涟漪...", "药水正在沸腾..."]
        
        for i in range(100):
            if i % 25 == 0:
                status_text.text(magic_phases[i//25])
            progress_bar.progress(i + 1)
            import time
            time.sleep(0.02)
        
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一位炼金术士般的心理学导师。给用户一个极简的文学标签（4-8字），然后给出一份三部分的'药方'。"},
                    {"role": "user", "content": user_input}
                ]
            )
            
            result = response.choices[0].message.content
            # 简单假设第一行是标签（这取决于AI的返回格式，你可以进一步微调提示词）
            label = "我的情绪处方" 
            
            # 视觉呈现
            st.snow() # 下雪特效代替气球，更有仪式感
            st.success("药水炼制成功！")
            
            # 使用容器美化输出
            with st.container():
                st.markdown(f"""
                <div style="background-color:#1e1e32; padding:20px; border-radius:15px; border-left: 5px solid #7b61ff">
                    <h2 style="color:#ffcc00">✨ 处方已送达</h2>
                    <p style="color:#ffffff; line-height:1.6">{result}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # --- 5. 海报生成与下载 ---
            st.markdown("### 📸 专属情绪海报")
            poster_data = generate_poster(label, result)
            st.image(poster_data, caption="右键另存为即可分享")
            st.download_button(label="📥 点击下载高清海报", data=poster_data, file_name="my_therapy_poster.png", mime="image/png")

        except Exception as e:
            st.error(f"炼金失败: {e}")

st.markdown("---")
st.caption("“万物皆有裂痕，那是光照进来的地方。”")