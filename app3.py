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

    # ---------- CEO ----------
    nodes.append(Node(
        id="ceo",
        label=wrap_text(org_data["ceo"]),
        shape="box",
        color="#1e88e5",
        font={"color": "white", "size": 14},
        width=220,
        height=65,
        level=0
    ))

    # ---------- CEO Office ----------
    nodes.append(Node(
        id="ceo_office",
        label=wrap_text("مدیریت حوزه مدیرعامل و هماهنگی امور"),
        shape="box",
        color="#455a64",
        font={"color": "white", "size": 12},
        width=260,
        height=60,
        level=1
    ))
    edges.append(Edge("ceo", "ceo_office"))

    # ---------- Two arms ----------
    arms = [
        "مدیریت توسعه کسب و کار",
        "مدیریت برنامه ریزی"
    ]

    for arm in arms:
        arm_id = f"arm_{arm}"
        nodes.append(Node(
            id=arm_id,
            label=wrap_text(arm),
            shape="box",
            color="#2e7d32",
            font={"color": "white", "size": 12},
            width=220,
            height=60,
            level=2
        ))
        edges.append(Edge("ceo_office", arm_id))

    # ---------- Main vertical line continues ----------
    hub_id = "main_hub"
    nodes.append(Node(
        id=hub_id,
        label="",
        shape="dot",
        size=5,
        level=3
    ))
    edges.append(Edge("ceo_office", hub_id))

    # ---------- Deputies ----------
    for dep_name, dep_data in org_data["deputies"].items():
        dep_id = f"dep_{dep_name}"

        nodes.append(Node(
            id=dep_id,
            label=wrap_text(dep_name),
            shape="box",
            color="#4caf50",
            font={"color": "white", "size": 12},
            width=200,
            height=60,
            level=4
        ))
        edges.append(Edge(hub_id, dep_id))

        # ---------- Managers (only if expanded) ----------
        if dep_name in expanded_deputies:
            for mgr_name in dep_data["managers"]:
                mgr_id = f"mgr_{dep_name}_{mgr_name}"

                nodes.append(Node(
                    id=mgr_id,
                    label=wrap_text(mgr_name, max_len=14),
                    shape="box",
                    color="#1976d2",
                    font={"color": "white", "size": 11},
                    width=160,
                    height=55,
                    level=5
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
