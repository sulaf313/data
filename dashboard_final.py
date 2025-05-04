
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="لوحة تحليل المنشآت", layout="wide")
st.title("📊 لوحة تحليل ومقارنة بيانات المنشآت")

uploaded_files = st.file_uploader("📂 ارفع ملفات CSV (حتى 4)", type="csv", accept_multiple_files=True)

if uploaded_files:
    dfs = []
    for file in uploaded_files:
        df = pd.read_csv(file)
        df['مصدر الملف'] = file.name
        dfs.append(df)
    data = pd.concat(dfs, ignore_index=True)

    st.sidebar.header("🎯 الفلاتر")
    for col in ['باب النشاط', 'قسم النشاط', 'المكتب', 'الربع', 'حجم المنشأة']:
        if col in data.columns:
            options = data[col].dropna().unique()
            selected = st.sidebar.multiselect(f"اختر {col}", options=options, default=options)
            data = data[data[col].isin(selected)]

    st.markdown("## 🧾 عرض أولي للبيانات")
    st.dataframe(data.head(50), use_container_width=True)

    col1, col2 = st.columns(2)
    col1.metric("عدد المنشآت", len(data))
    col2.metric("عدد الملفات", len(uploaded_files))

    if 'باب النشاط' in data.columns:
        st.markdown("### 📌 عدد المنشآت حسب باب النشاط")
        chart1 = data.groupby(['باب النشاط', 'مصدر الملف']).size().reset_index(name='عدد المنشآت')
        fig1 = px.bar(chart1, x='باب النشاط', y='عدد المنشآت', color='مصدر الملف', barmode='group')
        st.plotly_chart(fig1, use_container_width=True)

    if 'حجم المنشأة' in data.columns:
        st.markdown("### 🧱 توزيع المنشآت حسب الحجم")
        chart2 = data.groupby(['حجم المنشأة', 'مصدر الملف']).size().reset_index(name='عدد المنشآت')
        fig2 = px.bar(chart2, x='حجم المنشأة', y='عدد المنشآت', color='مصدر الملف', barmode='group')
        st.plotly_chart(fig2, use_container_width=True)

    if 'الربع' in data.columns:
        st.markdown("### 🕒 مقارنة عدد المنشآت حسب الربع")
        chart4 = data.groupby(['الربع', 'مصدر الملف']).size().reset_index(name='عدد المنشآت')
        fig4 = px.line(chart4, x='الربع', y='عدد المنشآت', color='مصدر الملف', markers=True)
        st.plotly_chart(fig4, use_container_width=True)

    col3, col4 = st.columns(2)

    if 'باب النشاط' in data.columns:
        donut_data = data['باب النشاط'].value_counts().nlargest(7).reset_index()
        donut_data.columns = ['النشاط', 'عدد المنشآت']
        with col3:
            st.markdown("### 🍩 توزيع المنشآت حسب باب النشاط")
            fig = px.pie(donut_data, names='النشاط', values='عدد المنشآت', hole=0.5,
                         color_discrete_sequence=px.colors.qualitative.Bold)
            fig.update_traces(textinfo='label+percent', textfont_size=16, textposition='inside')
            st.plotly_chart(fig, use_container_width=True)

    if 'قسم النشاط' in data.columns:
        top_sections = data['قسم النشاط'].value_counts().nlargest(5).reset_index()
        top_sections.columns = ['قسم النشاط', 'عدد المنشآت']
        with col4:
            st.markdown("### 🧩 أعلى 5 أقسام نشاط")
            for idx, row in top_sections.iterrows():
                st.markdown(f"""<div style='padding:14px; margin-bottom:10px; border-radius:12px;
                                background-color:#d7ecff; box-shadow: 2px 2px 5px #ccc;
                                font-family: "Tahoma", sans-serif; font-size:18px; color:#222'>
                                <b>{row['قسم النشاط']}</b><br> {int(row['عدد المنشآت'])} منشأة
                                </div>""", unsafe_allow_html=True)

else:
    st.info("👈 ارفع ملفات CSV لعرض التحليلات.")
