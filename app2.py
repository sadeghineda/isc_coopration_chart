import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
# برای محیط واقعی
from database import get_org_data, get_flat_data, get_stats, test_connection

# ===============================
# تنظیمات صفحه
# ===============================
st.set_page_config(
    page_title="چارت سازمانی",
    page_icon="🏢",
    layout="wide"
)



# ===============================
# ساخت نودها با expand / collapse
# ===============================
def build_graph(org_data, expanded_deputies):
    nodes = []
    edges = []

    # ========= CEO =========
    nodes.append(Node(
        id="ceo",
        label=org_data["ceo"],
        shape="box",
        color="#1f4e79",
        font={"color": "white", "size": 14},
        size=35,
        level=0
    ))

    # ========= Spine nodes (نامرئی) =========
    nodes.append(Node(id="spine_1", label="", size=1, level=1))
    nodes.append(Node(id="spine_2", label="", size=1, level=2))
    nodes.append(Node(id="spine_3", label="", size=1, level=3))

    edges.append(Edge("ceo", "spine_1"))
    edges.append(Edge("spine_1", "spine_2"))
    edges.append(Edge("spine_2", "spine_3"))

    # ========= مدیریت حوزه مدیرعامل =========
    ceo_office = "مدیریت حوزه مدیرعامل و هماهنگی امور"

    nodes.append(Node(
    id="ceo_office",
    label=wrap_text(ceo_office),
    shape="box",
    color="#455a64",
    font={"color": "white", "size": 12},
    width=220,
    height=60,
    level=1
))


    edges.append(Edge("spine_1", "ceo_office"))

    # ========= دو بازوی موقت =========
    left_arm = "مدیریت توسعه کسب‌وکار"
    right_arm = "مدیریت برنامه‌ریزی"

    for arm in [left_arm, right_arm]:
        if arm in org_data["deputies"]:
            nodes.append(Node(
    id=f"arm_{arm}",
    label=wrap_text(arm),
    shape="box",
    color="#2e7d32",
    font={"color": "white", "size": 12},
    width=200,
    height=60,
    level=2
))

            edges.append(Edge("spine_2", f"arm_{arm}"))

    # ========= سایر معاونت‌ها (زیر مدیرعامل، از spine اصلی) =========
    for dep_name, dep_data in org_data["deputies"].items():
        if dep_name in [left_arm, right_arm]:
            continue

        dep_id = f"dep_{dep_name}"

        nodes.append(Node(
    id=dep_id,
    label=wrap_text(dep_name),
    shape="box",
    color="#4caf50",
    font={"color": "white", "size": 12},
    width=180,
    height=60,
    level=3
))


        edges.append(Edge("spine_3", dep_id))

        # باز شدن زیرمجموعه‌ها
        if dep_name in expanded_deputies:
            for mgr_name in dep_data["managers"]:
                mgr_id = f"mgr_{dep_name}_{mgr_name}"

                nodes.append(Node(
                    id=mgr_id,
                    label=mgr_name,
                    shape="box",
                    color="#1976d2",
                    font={"color": "white"},
                    size=18,
                    level=4
                ))

                edges.append(Edge(dep_id, mgr_id))

    return nodes, edges

def wrap_text(text, max_len=16):
    words = text.split(" ")
    lines = []
    current = ""

    for w in words:
        if len(current) + len(w) <= max_len:
            current += (" " if current else "") + w
        else:
            lines.append(current)
            current = w

    if current:
        lines.append(current)

    return "\n".join(lines)



# ===============================
# Main
# ===============================
def main():
    st.title("🏢 چارت سازمانی")

    # Test DB connection
    success, msg = test_connection()
    if not success:
        st.error(f"❌ خطا در اتصال به دیتابیس: {msg}")
        return

    org_data = get_org_data()

    # --- state برای معاون‌های باز ---
    if "expanded_deputies" not in st.session_state:
        st.session_state.expanded_deputies = set()

    nodes, edges = build_graph(
        org_data,
        st.session_state.expanded_deputies
    )

    config = Config(
        width="100%",
        height=1000,
        directed=True,
        hierarchical=True,
        physics=False,
        direction="UD",
        levelSeparation=150,
        nodeSpacing=140,
    )


    clicked = agraph(
        nodes=nodes,
        edges=edges,
        config=config
    )

    # --- مدیریت کلیک ---
    if clicked and clicked.startswith("dep_"):
        dep_name = clicked.replace("dep_", "")
        if dep_name in st.session_state.expanded_deputies:
            st.session_state.expanded_deputies.remove(dep_name)
        else:
            st.session_state.expanded_deputies.add(dep_name)

        st.rerun()


if __name__ == "__main__":
    main()
