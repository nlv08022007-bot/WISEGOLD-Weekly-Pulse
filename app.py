import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from logic_phantich import analyze_correlation, calculate_forecast, load_data

# ==========================================
# 0. CONFIG & DARK PURPLE FULL BACKGROUND + LIGHT GREEN SIDEBAR
# ==========================================
st.set_page_config(
    page_title="SJC Gold Analytics - Dark Purple",
    page_icon="🔱",
    layout="wide",
)

st.markdown(
    """
    <style>
    /* 1. NỀN TOÀN TRANG MÀU ĐEN TÍM PHỦ TRÀN */
    .stApp {
        background: linear-gradient(135deg, #0d0714 0%, #160d29 50%, #0a0512 100%);
        background-attachment: fixed;
        color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* 2. BANNER INVESTING STYLE */
    .investing-banner {
        background: linear-gradient(90deg, rgba(15, 10, 28, 0.95) 0%, rgba(20, 13, 38, 0.82) 50%, rgba(15, 10, 28, 0.6) 100%),
                    url('https://images.unsplash.com/photo-1610375461246-83df859d849d?q=80&w=1920&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        border: 1px solid rgba(168, 85, 247, 0.4);
        border-radius: 20px;
        padding: 50px;
        margin-bottom: 30px;
        backdrop-filter: blur(8px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.7), 0 0 25px rgba(168, 85, 247, 0.2);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .badge-investing {
        background: #10b981;
        color: #0b0f19;
        font-weight: 800;
        font-size: 0.85rem;
        padding: 7px 16px;
        border-radius: 20px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 18px;
        box-shadow: 0 0 12px rgba(16, 185, 129, 0.5);
    }

    .hero-title-glow {
        font-size: 3.3rem;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 15px;
        line-height: 1.15;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.9), 0 0 35px rgba(192, 132, 252, 0.8);
    }

    .hero-sub-text {
        color: #e9d5ff;
        font-size: 1.15rem;
        max-width: 650px;
        margin-bottom: 28px;
        line-height: 1.5;
        text-shadow: 0 2px 4px rgba(0,0,0,0.8);
    }

    .btn-orange {
        background: #f97316;
        color: #ffffff;
        padding: 12px 28px;
        border-radius: 10px;
        font-weight: 800;
        font-size: 1rem;
        display: inline-block;
        margin-right: 12px;
        box-shadow: 0 4px 15px rgba(249, 115, 22, 0.5);
    }

    .btn-outline {
        border: 1px solid rgba(255, 255, 255, 0.4);
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        padding: 12px 24px;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1rem;
        display: inline-block;
        backdrop-filter: blur(4px);
    }

    .banner-mockup {
        background: rgba(20, 13, 38, 0.88);
        border: 1px solid rgba(192, 132, 252, 0.4);
        border-radius: 16px;
        padding: 22px;
        width: 380px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        backdrop-filter: blur(10px);
    }

    .mockup-item {
        display: flex;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        font-size: 0.92rem;
    }

    /* 3. METRIC CARDS */
    [data-testid="stMetric"] {
        background: rgba(22, 14, 41, 0.85) !important;
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
        border-radius: 14px;
        padding: 18px;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    }
    [data-testid="stMetricLabel"] {
        color: #c084fc !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    /* 4. TIÊU ĐỀ MỤC */
    .section-title {
        border-left: 5px solid #a855f7;
        padding-left: 14px;
        font-size: 1.3rem;
        font-weight: 800;
        color: #ffffff;
        margin: 30px 0 15px 0;
        text-shadow: 0 0 10px rgba(168, 85, 247, 0.4);
    }

    /* 5. TÙY CHỈNH EXPANDER (KHUNG CHI TIẾT TƯƠNG QUAN) */
    div[data-testid="stExpander"] {
        background-color: rgba(22, 14, 41, 0.9) !important;
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }
    div[data-testid="stExpander"] details summary {
        background-color: rgba(30, 18, 55, 0.95) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
    }
    div[data-testid="stExpander"] details summary p {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* 6. BẢNG DỮ LIỆU ĐEN TÍM */
    [data-testid="stDataFrame"] {
        background-color: rgba(22, 14, 41, 0.85) !important;
        border-radius: 14px;
        border: 1px solid rgba(168, 85, 247, 0.3);
        padding: 12px;
    }

    /* 7. SIDEBAR - MÀU XANH LÁ CHUỐI NON TƯƠI SÁNG */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #132a13 0%, #1f401b 100%) !important;
        border-right: 2px solid #aacc00 !important; 
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* Tiêu đề mục Sidebar: */
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #ccff00 !important; /* Màu chuối non phát sáng */
        text-shadow: 0 0 10px rgba(204, 255, 0, 0.4);
    }

    /* Ô Khung thời gian: */
    div[data-baseweb="input"], div[data-baseweb="base-input"] {
        background-color: rgba(10, 25, 10, 0.85) !important;
        border: 1.5px solid #aacc00 !important;
        border-radius: 10px !important;
        box-shadow: 0 0 8px rgba(170, 204, 0, 0.2);
    }

    div[data-baseweb="input"] input {
        color: #d8f3dc !important; 
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        -webkit-text-fill-color: #d8f3dc !important;
    }

    /* Màu chữ các mục Checkbox & Radio */
    [data-testid="stSidebar"] .stCheckbox p, 
    [data-testid="stSidebar"] .stRadio p {
        color: #e9ff70 !important; 
        font-weight: 600 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# --- LOAD DỮ LIỆU ---
@st.cache_data(ttl=3600)
def get_cached_data():
    return load_data()


df_raw = get_cached_data()

# ==========================================
# 1. HERO BANNER
# ==========================================
st.markdown(
    """
    <div class="investing-banner">
        <div style="flex: 1; padding-right: 30px;">
            <span class="badge-investing">SALE THÁNG 8 • AI ANALYTICS 2026</span>
            <div class="hero-title-glow">Thị trường chưa bao giờ ngơi nghỉ</div>
            <div class="hero-sub-text">
                Nhưng bạn hoàn toàn có thể. Hãy để AI thay bạn theo dõi biến động Giá vàng SJC, vàng Thế giới & Tỷ giá USD/VND trực quan liên tục theo thời gian thực.
            </div>
            <div>
                <span class="btn-orange">Trải nghiệm miễn phí</span>
                <span class="btn-outline">Giảm 55%</span>
            </div>
        </div>
        <div class="banner-mockup">
            <div style="font-weight: 800; color: #10b981; font-size: 1.1rem; margin-bottom: 12px;">
                📈 SJC/VND Trend +189.1%
            </div>
            <div class="mockup-item">
                <span style="color: #cbd5e1;">🥇 Giá vàng SJC</span>
                <span style="color: #fbbf24; font-weight: 700;">142.94 Triệu/Lượng</span>
            </div>
            <div class="mockup-item">
                <span style="color: #cbd5e1;">🌐 TG quy đổi</span>
                <span style="color: #38bdf8; font-weight: 700;">142.87 Triệu/Lượng</span>
            </div>
            <div class="mockup-item">
                <span style="color: #cbd5e1;">💵 Tỷ giá USD/VND</span>
                <span style="color: #c084fc; font-weight: 700;">26,099 VNĐ</span>
            </div>
            <div style="font-size: 0.75rem; color: #a78bfa; margin-top: 10px; text-align: right;">
                *Cập nhật tự động bởi thuật toán AI
            </div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. SIDEBAR BỘ LỌC & CẤU HÌNH (XANH LÁ NHẸ)
# ==========================================
st.sidebar.markdown("<h2 style='color:#34d399; font-size:1.4rem; font-weight:800; margin-bottom:20px;'> BỘ LỌC & CẤU HÌNH</h2>", unsafe_allow_html=True)

min_date = df_raw.index.min().date()
max_date = df_raw.index.max().date()

start_date, end_date = st.sidebar.date_input(
    "Khung thời gian:",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date,
)

mask = (df_raw.index.date >= start_date) & (df_raw.index.date <= end_date)
df = df_raw.loc[mask].copy()

if df.empty:
    st.error("Không có dữ liệu trong khoảng thời gian này!")
    st.stop()

# --- TÍNH TOÁN DƯỜNG MA BỔ SUNG CHO BIỂU ĐỒ ---
df["MA7"] = df["SJC_Price"].rolling(window=7).mean()
df["MA30"] = df["SJC_Price"].rolling(window=30).mean()

# --- BỔ SUNG BỘ LỌC CHỈ BÁO KỸ THUẬT NGHỆ THUẬT ---
st.sidebar.markdown("<br><h3 style='color:#6ee7b7; font-size:1.1rem; font-weight:700;'> CHỈ BÁO KỸ THUẬT (MA)</h3>", unsafe_allow_html=True)
show_ma7 = st.sidebar.checkbox("Hiển thị MA 7 Ngày (Lướt sóng)", value=True)
show_ma30 = st.sidebar.checkbox("Hiển thị MA 30 Ngày (Trung hạn)", value=True)

latest = df.iloc[-1]
prev = df.iloc[-2] if len(df) > 1 else latest

# ==========================================
# 3. THẺ METRIC CHỈ SỐ
# ==========================================
c1, c2, c3, c4 = st.columns(4)
with c1:
    delta_sjc = latest["SJC_Price"] - prev["SJC_Price"]
    st.metric(
        "🥇 Giá vàng SJC (Triệu/Lượng)",
        f"{latest['SJC_Price']:.2f} triệu",
        f"{delta_sjc:+.2f}",
    )
with c2:
    delta_conv = latest["Gold_Converted"] - prev["Gold_Converted"]
    st.metric(
        "🌐 TG quy đổi (USD -> Triệu/Lượng)",
        f"{latest['Gold_Converted']:.2f} triệu ",
        f"{delta_conv:+.2f}",
    )
with c3:
    delta_spread = latest["Spread"] - prev["Spread"]
    st.metric(
        "⚖️ Chênh lệch (SJC - TG)",
        f"{latest['Spread']:.2f} triệu",
        f"{delta_spread:+.2f}",
        delta_color="inverse",
    )
with c4:
    delta_usd = latest["USDVND=X"] - prev["USDVND=X"]
    st.metric(
        "💵 Tỷ giá USD/VND",
        f"{latest['USDVND=X']:,.0f} USD",
        f"{delta_usd:+.0f}",
    )

# ==========================================
# 4. BIỂU ĐỒ DIỄN BIẾN GIÁ VÀNG (CÓ TRUNG BÌNH TRƯỢT MA)
# ==========================================
st.markdown(
    '<div class="section-title"> 1. Biến động Giá vàng SJC, Thế giới & Trung bình trượt (Rolling 7/30 ngày)</div>',
    unsafe_allow_html=True,
)

fig_main = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.08,
    row_heights=[0.7, 0.3],
    specs=[[{"secondary_y": True}], [{"secondary_y": False}]],
)

# Đường SJC Thực tế
fig_main.add_trace(
    go.Scatter(
        x=df.index,
        y=df["SJC_Price"],
        name="SJC Thực tế",
        line=dict(color="#fbbf24", width=2.5),
    ),
    row=1,
    col=1,
)

# Đường MA7 (Nếu tích chọn)
if show_ma7:
    fig_main.add_trace(
        go.Scatter(
            x=df.index,
            y=df["MA7"],
            name="MA 7 Ngày",
            line=dict(color="#34d399", width=1.5),
        ),
        row=1,
        col=1,
    )

# Đường MA30 (Nếu tích chọn)
if show_ma30:
    fig_main.add_trace(
        go.Scatter(
            x=df.index,
            y=df["MA30"],
            name="MA 30 Ngày",
            line=dict(color="#f43f5e", width=1.5, dash="dash"),
        ),
        row=1,
        col=1,
    )

# Đường TG Quy Đổi
fig_main.add_trace(
    go.Scatter(
        x=df.index,
        y=df["Gold_Converted"],
        name="TG quy đổi",
        line=dict(color="#38bdf8", width=1.8, dash="dot"),
    ),
    row=1,
    col=1,
    secondary_y=True,
)

# Đường Chênh lệch Vùng
fig_main.add_trace(
    go.Scatter(
        x=df.index,
        y=df["Spread"],
        name="Chênh lệch (Vùng)",
        fill="tozeroy",
        fillcolor="rgba(168, 85, 247, 0.2)",
        line=dict(color="#c084fc", width=1.5),
    ),
    row=2,
    col=1,
)

fig_main.update_layout(
    height=500,
    hovermode="x unified",
    paper_bgcolor="rgba(22, 14, 41, 0.85)",
    plot_bgcolor="rgba(22, 14, 41, 0.85)",
    font=dict(color="#ffffff"),
    margin=dict(l=10, r=10, t=20, b=20),
    legend=dict(
        orientation="h",
        y=1.05,
        x=0.5,
        xanchor="center",
        yanchor="bottom",
        font=dict(color="#ffffff", size=13),
        bgcolor="rgba(0,0,0,0)",
    ),
)
fig_main.update_xaxes(gridcolor="rgba(168, 85, 247, 0.15)")
fig_main.update_yaxes(gridcolor="rgba(168, 85, 247, 0.15)")

st.plotly_chart(fig_main, use_container_width=True)

# ==========================================
# 5. DỰ BÁO HOÀN CHỈNH & PHÂN TÍCH CHI TIẾT
# ==========================================
st.markdown(
    '<div class="section-title"> 2. Mô hình dự báo hồi quy tuyến tính (90 ngày)</div>',
    unsafe_allow_html=True,
)
df_forecast, future_dates, y_future_pred, upper_bound, lower_bound = (
    calculate_forecast(df)
)

fig_fc = go.Figure()
fig_fc.add_trace(
    go.Scatter(
        x=df_forecast.index,
        y=df_forecast["SJC_Price"],
        name="Lịch sử",
        line=dict(color="#fbbf24"),
    )
)
fig_fc.add_trace(
    go.Scatter(
        x=future_dates,
        y=y_future_pred,
        name="Dự báo",
        line=dict(color="#ef4444", dash="dash"),
    )
)
fig_fc.add_trace(
    go.Scatter(
        x=np.concatenate([future_dates, future_dates[::-1]]),
        y=np.concatenate([upper_bound, lower_bound[::-1]]),
        fill="toself",
        fillcolor="rgba(239, 68, 68, 0.18)",
        line=dict(color="rgba(255,255,255,0)"),
        name="Khoảng tin cậy 95%",
    )
)

fig_fc.update_layout(
    height=350,
    paper_bgcolor="rgba(22, 14, 41, 0.85)",
    plot_bgcolor="rgba(22, 14, 41, 0.85)",
    font=dict(color="#ffffff"),
    margin=dict(l=10, r=10, t=10, b=10),
    legend=dict(font=dict(color="#ffffff")),
)
fig_fc.update_xaxes(gridcolor="rgba(168, 85, 247, 0.15)")
fig_fc.update_yaxes(gridcolor="rgba(168, 85, 247, 0.15)")
st.plotly_chart(fig_fc, use_container_width=True)

# --- PHẦN PHÂN TÍCH CHI TIẾT NGUYÊN NHÂN TĂNG/GIẢM BỞI MÔ HÌNH ---
start_val = y_future_pred[0]
end_val = y_future_pred[-1]
diff_val = end_val - start_val

if diff_val < 0:
    trend_direction = " **XU HƯỚNG DỰ BÁO: GIẢM**"
    trend_reason = f"Mô hình hồi quy tuyến tính xác định xu hướng chủ đạo trong khoảng thời gian đã chọn là **đi xuống** (tổng mức giảm dự báo khoảng **{abs(diff_val):.2f} triệu VNĐ/lượng** trong 90 ngày tới). Điều này xảy ra do áp lực giảm từ chuỗi dữ liệu quá khứ chiếm ưu thế hơn so with các nhịp hồi phục ngắn hạn."
else:
    trend_direction = " **XU HƯỚNG DỰ BÁO: TĂNG**"
    trend_reason = f"Mô hình hồi quy tuyến tính xác định xu hướng chủ đạo trong khoảng thời gian đã chọn là **đi lên** (tổng mức tăng dự báo khoảng **{abs(diff_val):.2f} triệu VNĐ/lượng** trong 90 ngày tới). Thuật toán ghi nhận lực mua tích lũy và đà tăng giá từ quá khứ tạo động lực kéo đường dự báo tiếp tục đi lên."

st.markdown(
    f"""
    <div style="background: rgba(22, 14, 41, 0.9); border: 1px solid rgba(168, 85, 247, 0.4); border-radius: 12px; padding: 18px; margin-top: -10px; margin-bottom: 25px;">
        <div style="font-size: 1.1rem; font-weight: 800; color: #f59e0b; margin-bottom: 8px;">
             Phân tích cơ chế Mô hình dự báo:
        </div>
        <div style="font-size: 0.95rem; color: #ffffff; line-height: 1.6;">
            • {trend_direction}: {trend_reason}<br>
            • <b>Khoảng tin cậy 95%:</b> Vùng màu đỏ mờ thể hiện biên độ dao động rủi ro. Giá thực tế hoàn toàn có thể biến động dịch chuyển lên/xuống trong phạm vi này tùy thuộc vào các tin tức vĩ mô bất ngờ.
        </div>
        <div style="background: rgba(239, 68, 68, 0.15); border-left: 4px solid #ef4444; padding: 10px 14px; margin-top: 12px; border-radius: 4px; font-size: 0.88rem; color: #fca5a5;">
            ⚠️ <b>LƯU Ý QUAN TRỌNG:</b> Đây là kết quả tính toán tự động dựa trên thuật toán thống kê hồi quy tuyến tính từ dữ liệu quá khứ. Dự báo mang tính chất tham khảo kỹ thuật và <b>hoàn toàn có thể phát sinh sai sót</b> do các yếu tố thị trường thực tế (chính sách ngân hàng, tỷ giá, địa chính trị) biến động bất ngờ.
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 6. MA TRẬN TƯƠNG QUAN & BOXPLOT
# ==========================================
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown(
        '<div class="section-title"> 3. Ma trận tương quan</div>',
        unsafe_allow_html=True,
    )
    corr_matrix, corr_insights = analyze_correlation(df)

    corr_display = corr_matrix.copy()
    corr_display.columns = ["SJC", "TG (USD)", "USD/VND", "quy đổi"]
    corr_display.index = ["SJC", "TG (USD)", "USD/VND", "quy đổi"]

    fig_heat = px.imshow(
        corr_display,
        text_auto=".2f",
        color_continuous_scale="Blues",
        aspect="auto",
    )

    fig_heat.update_layout(
        height=350,
        paper_bgcolor="rgba(22, 14, 41, 0.85)",
        plot_bgcolor="rgba(22, 14, 41, 0.85)",
        font=dict(color="#ffffff"),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    with st.expander(" Chi tiết đánh giá tương quan", expanded=True):
        for insight in corr_insights:
            st.markdown(
                f"<span style='color: #ffffff;'>• {insight}</span>",
                unsafe_allow_html=True,
            )

with col_right:
    st.markdown(
        '<div class="section-title"> 4. Phân phối biến động theo tháng (Boxplot)</div>',
        unsafe_allow_html=True,
    )

    df_box = df.copy()
    df_box["Year_Month"] = df_box.index.to_period("M").astype(str)

    fig_box = px.box(
        df_box,
        x="Year_Month",
        y="SJC_Price",
        labels={"Year_Month": "Tháng/Năm", "SJC_Price": "Triệu VNĐ/Lượng"},
        color_discrete_sequence=["#c084fc"],
    )

    fig_box.update_layout(
        height=350,
        paper_bgcolor="rgba(22, 14, 41, 0.85)",
        plot_bgcolor="rgba(22, 14, 41, 0.85)",
        font=dict(color="#ffffff"),
        xaxis_tickangle=-45,
        margin=dict(l=10, r=10, t=10, b=10),
    )
    fig_box.update_xaxes(gridcolor="rgba(168, 85, 247, 0.15)")
    fig_box.update_yaxes(gridcolor="rgba(168, 85, 247, 0.15)")
    st.plotly_chart(fig_box, use_container_width=True)

    st.info(
        " **Boxplot:** Mức độ dao động giá trong từng tháng. Hộp càng dài chứng tỏ biến động càng lớn."
    )

# ==========================================
# 7. BẢNG DỮ LIỆU & NÚT TẢI CSV
# ==========================================
st.markdown(
    '<div class="section-title"> 5. Bảng dữ liệu lịch sử chi tiết</div>',
    unsafe_allow_html=True,
)

df_display = df[[
    "SJC_Price",
    "Gold_Converted",
    "Spread",
    "GC=F",
    "USDVND=X",
    "SJC_Daily_Return",
]].copy()

df_display.columns = [
    "Giá SJC (Triệu/Lượng)",
    "TG quy đổi (Triệu/Lượng)",
    "Chênh lệch (Triệu VNĐ)",
    "Vàng TG (USD/Ounce)",
    "Tỷ giá USD/VND",
    "Thay đổi ngày (%)",
]

df_display = df_display.sort_index(ascending=False)

st.dataframe(
    df_display.style.format({
        "Giá SJC (Triệu/Lượng)": "{:.2f}",
        "TG quy đổi (Triệu/Lượng)": "{:.2f}",
        "Chênh lệch (Triệu VNĐ)": "{:.2f}",
        "Vàng TG (USD/Ounce)": "{:.2f}",
        "Tỷ giá USD/VND": "{:,.0f}",
        "Thay đổi ngày (%)": "{:+.2f}%",
    }),
    use_container_width=True,
    height=380,
)

col_dl1, col_dl2 = st.columns([1, 4])
with col_dl1:
    csv_data = df_display.to_csv().encode("utf-8")
    st.download_button(
        label=" Tải Dữ Liệu Chi Tiết (.CSV)",
        data=csv_data,
        file_name="SJC_Gold_Forex_Data.csv",
        mime="text/csv",
        type="primary",
    )