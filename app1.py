"""
Organization Chart Application - Streamlit
چارت سازمانی تعاملی (Graphviz)
"""

import streamlit as st
import graphviz
import pandas as pd
import streamlit.components.v1 as components
import os
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"



# ==============================
# Database imports
# ==============================
# برای تست
# from database_test import get_org_data, get_flat_data, get_stats, test_connection

# برای محیط واقعی
from database import get_org_data, get_flat_data, get_stats, test_connection


# ==============================
# Page config
# ==============================
st.set_page_config(
    page_title="چارت سازمانی",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
.block-container {
    padding-top: 0.5rem;
    padding-bottom: 0;
    padding-left: 0;
    padding-right: 0;
    max-width: 100% !important;
}
</style>
""", unsafe_allow_html=True)



# ==============================
# Custom CSS
# ==============================
st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 1.5rem;
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    color: white;
    border-radius: 10px;
    margin-bottom: 2rem;
}
.stats-box {
    background: #f0f2f6;
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# ==============================
# Graphviz Org Chart
# ==============================
def create_org_chart_graphviz(org_data, show_groups=True):
    # dot = graphviz.Digraph(
    #     engine="dot",
    #     graph_attr={
    #         "rankdir": "TB",
    #         "splines": "ortho",
    #         "nodesep": "0.4",
    #         "ranksep": "0.6"
    #     }
    # )
    dot = graphviz.Digraph(
    engine="dot",
    format="svg",   # 👈 مهم
    graph_attr={
        "rankdir": "TB",
        "splines": "ortho",
        "nodesep": "0.4",
        "ranksep": "0.6"
    }
)


    dot.attr(
        "node",
        shape="box",
        style="filled,rounded",
        fontname="Tahoma",
        fontsize="10"
    )

    # ================= CEO =================
    dot.node("CEO", org_data["ceo"], fillcolor="#1e3c72", fontcolor="white")

    # ================= Deputies =================
    for dep_name, dep_data in org_data["deputies"].items():
        dep_id = f"DEP_{dep_name}"
        dot.node(dep_id, dep_name, fillcolor="#6f42c1", fontcolor="white")
        dot.edge("CEO", dep_id)

        # ================= Managers =================
        for mgr_name, mgr_data in dep_data["managers"].items():
            mgr_id = f"MGR_{dep_name}_{mgr_name}"
            dot.node(mgr_id, mgr_name, fillcolor="#0d6efd", fontcolor="white")
            dot.edge(dep_id, mgr_id)

            # ================= Groups (VERTICAL) =================
            if show_groups and mgr_data["groups"]:
                previous_group_id = None

                for idx, grp in enumerate(mgr_data["groups"]):
                    grp_id = f"GRP_{mgr_name}_{idx}"

                    dot.node(
                        grp_id,
                        grp,
                        fillcolor="#198754",
                        fontcolor="white",
                        fontsize="9"
                    )

                    # فقط گروه اول به مدیر وصل می‌شود
                    if idx == 0:
                        dot.edge(mgr_id, grp_id)
                    else:
                        # اتصال نامرئی برای عمودی شدن
                        dot.edge(
                            previous_group_id,
                            grp_id,
                            style="invis"
                        )

                    previous_group_id = grp_id

    return dot

def render_svg_with_zoom(svg_content, height=1600):
    html = f"""
    <html>
    <head>
      <script src="https://unpkg.com/svg-pan-zoom@3.6.1/dist/svg-pan-zoom.min.js"></script>
      <style>
        html, body {{
          margin: 0;
          padding: 0;
          width: 100%;
          height: 100%;
          overflow: hidden;
        }}
        #svg-container {{
          width: 100vw;
          height: 100vh;
        }}
        svg {{
          width: 100% !important;
          height: 100% !important;
        }}
      </style>
    </head>
    <body>
      <div id="svg-container">
        {svg_content}
      </div>

      <script>
        const svgElement = document.querySelector("svg");

        svgPanZoom(svgElement, {{
          zoomEnabled: true,
          controlIconsEnabled: true,
          fit: true,
          center: true,
          minZoom: 0.2,
          maxZoom: 20
        }});
      </script>
    </body>
    </html>
    """
    components.html(html, height=height, scrolling=False)




# ==============================
# Main App
# ==============================
def main():

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏢 چارت سازمانی</h1>
        <p>نمایش ساختار سازمانی شرکت</p>
    </div>
    """, unsafe_allow_html=True)

    # Test DB connection
    success, msg = test_connection()
    if not success:
        st.error(f"❌ خطا در اتصال به دیتابیس: {msg}")
        return

    # Load data
    try:
        org_data = get_org_data()
        flat_data = get_flat_data()
        stats = get_stats()
    except Exception as e:
        st.error(f"❌ خطا در دریافت داده‌ها: {e}")
        return

    # ==============================
    # Sidebar
    # ==============================
    with st.sidebar:
        st.header("⚙️ تنظیمات")

        show_groups = st.checkbox("نمایش گروه‌ها", value=True)

        st.markdown("---")
        st.header("📊 آمار")

        st.metric("معاونین", stats["deputies_count"])
        st.metric("مدیران", stats["managers_count"])
        st.metric("گروه‌ها", stats["groups_count"])

        st.markdown("---")
        st.info("💡 چارت قابل اسکرول و زوم است")

    # ==============================
    # Tabs
    # ==============================
    tab1, tab2 = st.tabs(["📊 چارت سازمانی", "📋 جدول داده‌ها"])

    # ---- Chart Tab
    with tab1:
        dot = create_org_chart_graphviz(org_data, show_groups)
        svg = dot.pipe().decode("utf-8")
        # render_svg_with_zoom(svg, height=1200)
        render_svg_with_zoom(svg, height=2000)



    # ---- Table Tab
    with tab2:
        df = pd.DataFrame(flat_data, columns=["مدیرعامل", "معاون", "مدیر", "گروه"])

        search = st.text_input("🔍 جستجو")
        if search:
            df = df[df.apply(
                lambda r: r.astype(str).str.contains(search, case=False).any(),
                axis=1
            )]

        st.dataframe(df, use_container_width=True, height=500)

        csv = df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            "📥 دانلود CSV",
            csv,
            "org_chart.csv",
            "text/csv"
        )


# ==============================
# Run
# ==============================
if __name__ == "__main__":
    main()
