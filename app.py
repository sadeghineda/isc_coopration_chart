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
# تابع کمکی برای شکستن متن
# ===============================
def wrap_text(text, max_len=18):
    """شکستن متن به چند خط"""
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
# ساخت گراف با expand/collapse
# ===============================
def build_graph(org_data, expanded_deputies, expanded_managers):
    nodes = []
    edges = []

    # مختصات مرکزی
    CENTER_X = 0
    
    # ========= CEO (مدیرعامل) =========
    nodes.append(Node(
        id="ceo",
        label=org_data["ceo"],
        shape="box",
        color="#1f4e79",
        font={"color": "white", "size": 14, "face": "B Nazanin"},
        size=30,
        x=CENTER_X,
        y=0
    ))

    # ========= Spine نقاط نامرئی برای خط اصلی =========
    nodes.append(Node(id="spine_1", label="", size=1, color="#ffffff00", x=CENTER_X, y=120))
    nodes.append(Node(id="spine_2", label="", size=1, color="#ffffff00", x=CENTER_X, y=280))
    nodes.append(Node(id="spine_3", label="", size=1, color="#ffffff00", x=CENTER_X, y=440))
    nodes.append(Node(id="spine_4", label="", size=1, color="#ffffff00", x=CENTER_X, y=600))
    
    edges.append(Edge("ceo", "spine_1"))
    edges.append(Edge("spine_1", "spine_2"))
    edges.append(Edge("spine_2", "spine_3"))
    edges.append(Edge("spine_3", "spine_4"))

    # ========= مدیریت حوزه مدیرعامل (کنار خط، در level 1) =========
    ceo_office = "مدیریت حوزه مدیرعامل و هماهنگی امور"
    
    nodes.append(Node(
        id="ceo_office",
        label=wrap_text(ceo_office, 20),
        shape="box",
        color="#455a64",
        font={"color": "white", "size": 11, "face": "B Nazanin"},
        size=25,
        x=CENTER_X + 400,
        y=120
    ))
    
    edges.append(Edge("spine_1", "ceo_office"))

    # ========= دو بازو (در level 2 - کنار خط) =========
    left_arm = "مدیریت توسعه کسب‌وکار"
    right_arm = "مدیریت برنامه‌ریزی"
    
    # بازوی چپ
    if left_arm in org_data["deputies"]:
        arm_left_id = "arm_left"
        
        is_expanded = left_arm in expanded_deputies
        label_text = wrap_text(left_arm, 18)
        if not is_expanded and org_data["deputies"][left_arm]["managers"]:
            label_text += "\n[+]"
        elif is_expanded:
            label_text += "\n[−]"
        
        nodes.append(Node(
            id=arm_left_id,
            label=label_text,
            shape="box",
            color="#2e7d32",
            font={"color": "white", "size": 11, "face": "B Nazanin"},
            size=25,
            x=CENTER_X - 350,
            y=280
        ))
        
        edges.append(Edge("spine_2", arm_left_id))
        
        # مدیریت‌های بازوی چپ
        if is_expanded:
            mgr_list = list(org_data["deputies"][left_arm]["managers"].keys())
            for idx, mgr_name in enumerate(mgr_list):
                mgr_id = f"mgr_left_{idx}"
                mgr_full_key = f"{left_arm}||{mgr_name}"
                
                is_mgr_expanded = mgr_full_key in expanded_managers
                mgr_label = wrap_text(mgr_name, 16)
                
                groups = org_data["deputies"][left_arm]["managers"][mgr_name]["groups"]
                if groups:
                    mgr_label += "\n[+]" if not is_mgr_expanded else "\n[−]"
                
                nodes.append(Node(
                    id=mgr_id,
                    label=mgr_label,
                    shape="box",
                    color="#1976d2",
                    font={"color": "white", "size": 10, "face": "B Nazanin"},
                    size=20,
                    x=CENTER_X - 600,
                    y=280 + (idx * 120)
                ))
                
                edges.append(Edge(arm_left_id, mgr_id))
                
                # گروه‌ها
                if is_mgr_expanded and groups:
                    for grp_idx, grp_name in enumerate(groups):
                        grp_id = f"grp_left_{idx}_{grp_idx}"
                        
                        nodes.append(Node(
                            id=grp_id,
                            label=wrap_text(grp_name, 14),
                            shape="box",
                            color="#66bb6a",
                            font={"color": "white", "size": 9, "face": "B Nazanin"},
                            size=15,
                            x=CENTER_X - 850,
                            y=280 + (idx * 120) + (grp_idx * 80)
                        ))
                        
                        edges.append(Edge(mgr_id, grp_id))

    # بازوی راست
    if right_arm in org_data["deputies"]:
        arm_right_id = "arm_right"
        
        is_expanded = right_arm in expanded_deputies
        label_text = wrap_text(right_arm, 18)
        if not is_expanded and org_data["deputies"][right_arm]["managers"]:
            label_text += "\n[+]"
        elif is_expanded:
            label_text += "\n[−]"
        
        nodes.append(Node(
            id=arm_right_id,
            label=label_text,
            shape="box",
            color="#2e7d32",
            font={"color": "white", "size": 11, "face": "B Nazanin"},
            size=25,
            x=CENTER_X + 350,
            y=280
        ))
        
        edges.append(Edge("spine_2", arm_right_id))
        
        # مدیریت‌های بازوی راست
        if is_expanded:
            mgr_list = list(org_data["deputies"][right_arm]["managers"].keys())
            for idx, mgr_name in enumerate(mgr_list):
                mgr_id = f"mgr_right_{idx}"
                mgr_full_key = f"{right_arm}||{mgr_name}"
                
                is_mgr_expanded = mgr_full_key in expanded_managers
                mgr_label = wrap_text(mgr_name, 16)
                
                groups = org_data["deputies"][right_arm]["managers"][mgr_name]["groups"]
                if groups:
                    mgr_label += "\n[+]" if not is_mgr_expanded else "\n[−]"
                
                nodes.append(Node(
                    id=mgr_id,
                    label=mgr_label,
                    shape="box",
                    color="#1976d2",
                    font={"color": "white", "size": 10, "face": "B Nazanin"},
                    size=20,
                    x=CENTER_X + 600,
                    y=280 + (idx * 120)
                ))
                
                edges.append(Edge(arm_right_id, mgr_id))
                
                # گروه‌ها
                if is_mgr_expanded and groups:
                    for grp_idx, grp_name in enumerate(groups):
                        grp_id = f"grp_right_{idx}_{grp_idx}"
                        
                        nodes.append(Node(
                            id=grp_id,
                            label=wrap_text(grp_name, 14),
                            shape="box",
                            color="#66bb6a",
                            font={"color": "white", "size": 9, "face": "B Nazanin"},
                            size=15,
                            x=CENTER_X + 850,
                            y=280 + (idx * 120) + (grp_idx * 80)
                        ))
                        
                        edges.append(Edge(mgr_id, grp_id))

    # ========= خط افقی برای معاونت‌ها (level 3) =========
    # نقاط نامرئی برای ساخت خط افقی
    other_deputies = [
        (dep_name, dep_data) 
        for dep_name, dep_data in org_data["deputies"].items()
        if dep_name not in [left_arm, right_arm]
    ]
    
    num_deputies = len(other_deputies)
    
    # محاسبه فاصله‌ها
    total_width = 1600
    spacing = total_width / (num_deputies + 1) if num_deputies > 0 else 200
    start_x = CENTER_X - (total_width / 2)
    
    # نقاط نامرئی برای خط افقی
    horizontal_points = []
    for i in range(num_deputies + 2):  # +2 برای نقاط ابتدا و انتها
        point_id = f"h_point_{i}"
        x_pos = start_x + (i * spacing)
        
        nodes.append(Node(
            id=point_id,
            label="",
            size=1,
            color="#ffffff00",
            x=x_pos,
            y=600
        ))
        
        horizontal_points.append(point_id)
        
        # اتصال نقاط افقی به هم
        if i > 0:
            edges.append(Edge(horizontal_points[i-1], point_id))
    
    # اتصال خط عمودی به وسط خط افقی
    middle_index = len(horizontal_points) // 2
    edges.append(Edge("spine_4", horizontal_points[middle_index]))
    
    # ========= معاونت‌ها (پایین خط افقی) =========
    deputy_mapping = {}
    deputy_mapping["arm_left"] = left_arm
    deputy_mapping["arm_right"] = right_arm
    
    manager_mapping = {}
    
    for i, (dep_name, dep_data) in enumerate(other_deputies):
        dep_id = f"dep_{i}"
        deputy_mapping[dep_id] = dep_name
        
        is_expanded = dep_name in expanded_deputies
        label_text = wrap_text(dep_name, 18)
        if not is_expanded and dep_data["managers"]:
            label_text += "\n[+]"
        elif is_expanded:
            label_text += "\n[−]"
        
        # موقعیت x بر اساس شاخص
        x_pos = start_x + ((i + 1) * spacing)
        
        nodes.append(Node(
            id=dep_id,
            label=label_text,
            shape="box",
            color="#4caf50",
            font={"color": "white", "size": 11, "face": "B Nazanin"},
            size=25,
            x=x_pos,
            y=750
        ))
        
        # اتصال به نقطه متناظر در خط افقی
        edges.append(Edge(horizontal_points[i + 1], dep_id))
        
        # مدیریت‌ها
        if is_expanded:
            mgr_list = list(dep_data["managers"].keys())
            for mgr_idx, mgr_name in enumerate(mgr_list):
                mgr_id = f"mgr_dep_{i}_{mgr_idx}"
                mgr_full_key = f"{dep_name}||{mgr_name}"
                manager_mapping[mgr_id] = mgr_full_key
                
                is_mgr_expanded = mgr_full_key in expanded_managers
                mgr_label = wrap_text(mgr_name, 16)
                
                groups = dep_data["managers"][mgr_name]["groups"]
                if groups:
                    mgr_label += "\n[+]" if not is_mgr_expanded else "\n[−]"
                
                nodes.append(Node(
                    id=mgr_id,
                    label=mgr_label,
                    shape="box",
                    color="#1976d2",
                    font={"color": "white", "size": 10, "face": "B Nazanin"},
                    size=20,
                    x=x_pos,
                    y=900 + (mgr_idx * 120)
                ))
                
                edges.append(Edge(dep_id, mgr_id))
                
                # گروه‌ها
                if is_mgr_expanded and groups:
                    for grp_idx, grp_name in enumerate(groups):
                        grp_id = f"grp_dep_{i}_{mgr_idx}_{grp_idx}"
                        
                        nodes.append(Node(
                            id=grp_id,
                            label=wrap_text(grp_name, 14),
                            shape="box",
                            color="#66bb6a",
                            font={"color": "white", "size": 9, "face": "B Nazanin"},
                            size=15,
                            x=x_pos + (200 if grp_idx % 2 == 0 else -200),
                            y=900 + (mgr_idx * 120) + (grp_idx * 80)
                        ))
                        
                        edges.append(Edge(mgr_id, grp_id))
    
    # mapping برای مدیران بازوها
    if left_arm in org_data["deputies"] and left_arm in expanded_deputies:
        for idx, mgr_name in enumerate(org_data["deputies"][left_arm]["managers"].keys()):
            manager_mapping[f"mgr_left_{idx}"] = f"{left_arm}||{mgr_name}"
    
    if right_arm in org_data["deputies"] and right_arm in expanded_deputies:
        for idx, mgr_name in enumerate(org_data["deputies"][right_arm]["managers"].keys()):
            manager_mapping[f"mgr_right_{idx}"] = f"{right_arm}||{mgr_name}"

    return nodes, edges, deputy_mapping, manager_mapping


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

    # --- Session state ---
    if "expanded_deputies" not in st.session_state:
        st.session_state.expanded_deputies = set()
    
    if "expanded_managers" not in st.session_state:
        st.session_state.expanded_managers = set()

    # --- Sidebar ---
    with st.sidebar:
        st.header("🎛️ کنترل‌ها")
        
        if st.button("🔽 باز کردن همه معاونت‌ها"):
            st.session_state.expanded_deputies = set(org_data["deputies"].keys())
            st.rerun()
        
        if st.button("🔼 بستن همه"):
            st.session_state.expanded_deputies = set()
            st.session_state.expanded_managers = set()
            st.rerun()
        
        st.markdown("---")
        
        st.info("""
        💡 **راهنما:**
        - روی معاونت کلیک کنید → مدیریت‌ها باز می‌شود
        - روی مدیریت کلیک کنید → گروه‌ها نمایش داده می‌شود
        - آیکون [+] = قابل باز شدن
        - آیکون [−] = باز شده
        """)
        
        st.markdown("---")
        stats = get_stats()
        st.metric("تعداد معاونت‌ها", stats["deputies_count"])
        st.metric("تعداد مدیریت‌ها", stats["managers_count"])
        st.metric("تعداد گروه‌ها", stats["groups_count"])

    # --- Build graph ---
    nodes, edges, deputy_mapping, manager_mapping = build_graph(
        org_data,
        st.session_state.expanded_deputies,
        st.session_state.expanded_managers
    )

    config = Config(
        width="100%",
        height=1600,
        directed=True,
        hierarchical=False,
        physics=False,
    )

    # --- Display graph ---
    clicked = agraph(
        nodes=nodes,
        edges=edges,
        config=config
    )

    # --- مدیریت کلیک ---
    if clicked:
        # کلیک روی معاونت
        if clicked in deputy_mapping:
            dep_name = deputy_mapping[clicked]
            
            if dep_name in st.session_state.expanded_deputies:
                st.session_state.expanded_deputies.remove(dep_name)
                # حذف مدیریت‌های مربوط
                st.session_state.expanded_managers = {
                    m for m in st.session_state.expanded_managers
                    if not m.startswith(f"{dep_name}||")
                }
            else:
                st.session_state.expanded_deputies.add(dep_name)
            st.rerun()
        
        # کلیک روی مدیریت
        elif clicked in manager_mapping:
            mgr_full_key = manager_mapping[clicked]
            
            if mgr_full_key in st.session_state.expanded_managers:
                st.session_state.expanded_managers.remove(mgr_full_key)
            else:
                st.session_state.expanded_managers.add(mgr_full_key)
            st.rerun()


if __name__ == "__main__":
    main()