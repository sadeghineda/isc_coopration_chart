# import streamlit as st
# from streamlit_agraph import agraph, Node, Edge, Config
# # برای محیط واقعی
# from database import get_org_data, get_flat_data, get_stats, test_connection

# # ===============================
# # تنظیمات صفحه
# # ===============================
# st.set_page_config(
#     page_title="چارت سازمانی",
#     page_icon="🏢",
#     layout="wide"
# )

# st.markdown("""
# <style>
# @font-face {
#     font-family: 'BNazanin';
#     src: url('font/BNazanin.ttf') format('truetype');
# }

# html, body, [class*="css"] {
#     font-family: 'BNazanin', sans-serif;
# }
# </style>
# """, unsafe_allow_html=True)


# # ===============================
# # تنظیمات دو بازو (اینجا رو ویرایش کنید)
# # ===============================
# # نام دقیق دو معاونتی که باید به عنوان بازو نمایش داده شوند:
# LEFT_ARM_NAME = "مدیریت توسعه کسب و کار"  # 👈 نام دقیق را اینجا وارد کنید
# RIGHT_ARM_NAME = "مدیریت برنامه ریزی"  # 👈 نام دقیق را اینجا وارد کنید

# # ===============================
# # تابع کمکی برای شکستن متن
# # ===============================
# def wrap_text(text, max_len=18):
#     """شکستن متن به چند خط"""
#     words = text.split(" ")
#     lines = []
#     current = ""

#     for w in words:
#         if len(current) + len(w) <= max_len:
#             current += (" " if current else "") + w
#         else:
#             lines.append(current)
#             current = w

#     if current:
#         lines.append(current)

#     return "\n".join(lines)


# # ===============================
# # ساخت گراف با expand/collapse
# # ===============================
# def build_graph(org_data, expanded_deputies, expanded_managers, left_arm_name, right_arm_name):
#     nodes = []
#     edges = []

#     # مختصات مرکزی
#     CENTER_X = 0
    
#     # ========= CEO (مدیرعامل) =========
#     nodes.append(Node(
#         id="ceo",
#         label=org_data["ceo"],
#         shape="box",
#         color="#1f4e79",
#         font={"color": "white", "size": 14, "face": "B Nazanin"},
#         size=30,
#         x=CENTER_X,
#         y=0
#     ))

#     # ========= Spine نقاط نامرئی برای خط اصلی =========
#     nodes.append(Node(id="spine_1", label="", size=10, color="#ffffff00", x=CENTER_X, y=120))
#     nodes.append(Node(id="spine_2", label="", size=10, color="#ffffff00", x=CENTER_X, y=280))
#     nodes.append(Node(id="spine_3", label="", size=10, color="#ffffff00", x=CENTER_X, y=440))
#     nodes.append(Node(id="spine_4", label="", size=10, color="#ffffff00", x=CENTER_X, y=600))
    
#     edges.append(Edge("ceo", "spine_1"))
#     edges.append(Edge("spine_1", "spine_2"))
#     edges.append(Edge("spine_2", "spine_3"))
#     edges.append(Edge("spine_3", "spine_4"))

#     # ========= مدیریت حوزه مدیرعامل (کنار خط، در level 1) =========
#     # ceo_office = None

#     # for key in org_data["deputies"].keys():
#     #     if key.startswith("مديريت حوزه مدير عامل و هماهنگي امور"):
#     #         ceo_office = key
#     #         break
    
#     # # بررسی وضعیت expand
#     # is_ceo_office_expanded = ceo_office in expanded_deputies if ceo_office else False
#     # label_text = wrap_text(ceo_office, 20) if ceo_office else ""
    
#     # # اضافه کردن آیکون [+] یا [-]
#     # if ceo_office and ceo_office in org_data["deputies"]:
#     #     if not is_ceo_office_expanded and org_data["deputies"][ceo_office]["managers"]:
#     #         label_text += "\n[+]"
#     #     elif is_ceo_office_expanded:
#     #         label_text += "\n[−]"
    
#     # nodes.append(Node(
#     #     id="ceo_office",
#     #     label=label_text,
#     #     shape="box",
#     #     color="#1f4e79",
#     #     font={"color": "white", "size": 11, "face": "B Nazanin"},
#     #     size=30,
#     #     x=CENTER_X + 350,
#     #     y=120
#     # ))
    
#     # edges.append(Edge("spine_1", "ceo_office"))
#     # is_ceo_office_expanded = ceo_office
#     # # نمایش مدیریت‌های حوزه مدیرعامل (اگر expand شده باشد)
#     # if is_ceo_office_expanded and ceo_office in org_data["deputies"]:
#     #     mgr_list = list(org_data["deputies"][ceo_office]["managers"].keys())
#     #     for idx, mgr_name in enumerate(mgr_list):
#     #         mgr_id = f"mgr_ceo_office_{idx}"
#     #         mgr_full_key = f"{ceo_office}||{mgr_name}"
            
#     #         is_mgr_expanded = mgr_full_key in expanded_managers
#     #         mgr_label = wrap_text(mgr_name, 16)
            
#     #         groups = org_data["deputies"][ceo_office]["managers"][mgr_name]["groups"]
#     #         if groups:
#     #             mgr_label += "\n[+]" if not is_mgr_expanded else "\n[−]"
            
#     #         nodes.append(Node(
#     #             id=mgr_id,
#     #             label=mgr_label,
#     #             shape="box",
#     #             color="#1976d2",
#     #             font={"color": "white", "size": 10, "face": "B Nazanin"},
#     #             size=25,
#     #             x=CENTER_X + (idx * 100),
#     #             y=150
#     #             # y=120 + (idx * 120)
#     #         ))
            
#     #         edges.append(Edge("ceo_office", mgr_id))
            
#     #         # نمایش گروه‌ها (اگر expand شده باشد)
#     #         if is_mgr_expanded and groups:
#     #             for grp_idx, grp_name in enumerate(groups):
#     #                 grp_id = f"grp_ceo_office_{idx}_{grp_idx}"
                    
#     #                 nodes.append(Node(
#     #                     id=grp_id,
#     #                     label=wrap_text(grp_name, 14),
#     #                     shape="box",
#     #                     color="#66bb6a",
#     #                     font={"color": "white", "size": 9, "face": "B Nazanin"},
#     #                     size=15,
#     #                     x=CENTER_X + 950,
#     #                     y=120 + (idx * 120) + (grp_idx * 80)
#     #                 ))
                    
#     #                 edges.append(Edge(mgr_id, grp_id))

#     ceo_office = None

#     for key in org_data["deputies"].keys():
#         if key.startswith("مديريت حوزه مدير عامل و هماهنگي امور"):
#             ceo_office = key
#             break

#     # بررسی وضعیت expand
#     is_ceo_office_expanded = ceo_office in expanded_deputies if ceo_office else False
#     label_text = wrap_text(ceo_office, 20) if ceo_office else ""

#     # اضافه کردن آیکون [+] یا [-]
#     if ceo_office and ceo_office in org_data["deputies"]:
#         if not is_ceo_office_expanded and org_data["deputies"][ceo_office]["managers"]:
#             label_text += "\n[+]"
#         elif is_ceo_office_expanded:
#             label_text += "\n[−]"

#     # موقعیت بلاک اصلی حوزه مدیرعامل
#     ceo_office_x = CENTER_X + 350
#     ceo_office_y = 120

#     nodes.append(Node(
#         id="ceo_office",
#         label=label_text,
#         shape="box",
#         color="#1f4e79",
#         font={"color": "white", "size": 11, "face": "B Nazanin"},
#         size=30,
#         x=ceo_office_x,
#         y=ceo_office_y
#     ))

#     edges.append(Edge("spine_1", "ceo_office"))

#     # نمایش مدیریت‌های حوزه مدیرعامل (اگر expand شده باشد)
#     if is_ceo_office_expanded and ceo_office in org_data["deputies"]:
#         mgr_list = list(org_data["deputies"][ceo_office]["managers"].keys())
#         num_managers = len(mgr_list)
        
#         # تنظیمات برای چیدمان افقی
#         managers_y = ceo_office_y + 80  # فاصله عمودی از بلاک اصلی
#         spacing = 250  # فاصله افقی بین مدیریت‌ها
        
#         for idx, mgr_name in enumerate(mgr_list):
#             mgr_id = f"mgr_ceo_office_{idx}"
#             mgr_full_key = f"{ceo_office}||{mgr_name}"
            
#             is_mgr_expanded = mgr_full_key in expanded_managers
#             mgr_label = wrap_text(mgr_name, 16)
            
#             groups = org_data["deputies"][ceo_office]["managers"][mgr_name]["groups"]
#             if groups:
#                 mgr_label += "\n[+]" if not is_mgr_expanded else "\n[−]"
            
#             # محاسبه موقعیت افقی (یکی چپ، یکی وسط، یکی راست)
#             if num_managers == 1:
#                 mgr_x = ceo_office_x  # فقط یکی وسط
#             elif num_managers == 2:
#                 mgr_x = ceo_office_x + ((idx - 0.5) * spacing)  # دو تا: یکی چپ یکی راست
#             else:
#                 mgr_x = ceo_office_x + ((idx - (num_managers - 1) / 2) * spacing)  # توزیع متقارن
            
#             nodes.append(Node(
#                 id=mgr_id,
#                 label=mgr_label,
#                 shape="box",
#                 color="#1976d2",
#                 font={"color": "white", "size": 10, "face": "B Nazanin"},
#                 size=25,
#                 x=mgr_x,
#                 y=managers_y
#             ))
            
#             edges.append(Edge("ceo_office", mgr_id))
            
#             # نمایش گروه‌ها (اگر expand شده باشد)
#             if is_mgr_expanded and groups:
#                 for grp_idx, grp_name in enumerate(groups):
#                     grp_id = f"grp_ceo_office_{idx}_{grp_idx}"
                    
#                     nodes.append(Node(
#                         id=grp_id,
#                         label=wrap_text(grp_name, 14),
#                         shape="box",
#                         color="#66bb6a",
#                         font={"color": "white", "size": 9, "face": "B Nazanin"},
#                         size=15,
#                         x=mgr_x,  # همان x مدیریت والد
#                         y=managers_y + 120 + (grp_idx * 80)  # زیر مدیریت
#                     ))
                    
#                     edges.append(Edge(mgr_id, grp_id))

#     # ====================================== دو بازو (در level 2 - کنار خط) ===========================================================
#     # # یافتن نام‌های دقیق از دیتابیس
#     # left_arm = LEFT_ARM_NAME
#     # right_arm = RIGHT_ARM_NAME
    
#     # if left_arm_name:
#     #     # استفاده از نام دستی
#     #     if left_arm_name in org_data["deputies"]:
#     #         left_arm = left_arm_name
#     # else:
#     #     # شناسایی خودکار
#     #     for dep_name in org_data["deputies"].keys():
#     #         if "مدیریت توسعه" in dep_name and "کسب  و کار" in dep_name:
#     #             left_arm = dep_name
#     #             break
    
#     # if right_arm_name:
#     #     # استفاده از نام دستی
#     #     if right_arm_name in org_data["deputies"]:
#     #         right_arm = right_arm_name
#     # else:
#     #     # شناسایی خودکار
#     #     for dep_name in org_data["deputies"].keys():
#     #         if "مدیرت برنامه ریزی " in dep_name:
#     #             right_arm = dep_name
#     #             break

#     # planning_key = None

#     # for key in org_data["deputies"]:
#     #     if key.startswith("مديريت برنامه ريزي"):
#     #         planning_key = key
#     #         break
#     # left_arm = planning_key
#     # # بازوی چپ
#     # if left_arm and left_arm in org_data["deputies"]:
#     #     arm_left_id = "arm_left"
        
#     #     is_expanded = left_arm in expanded_deputies
#     #     label_text = wrap_text(left_arm, 18)
#     #     if not is_expanded and org_data["deputies"][left_arm]["managers"]:
#     #         label_text += "\n[+]"
#     #     elif is_expanded:
#     #         label_text += "\n[−]"
        
#     #     nodes.append(Node(
#     #         id=arm_left_id,
#     #         label=label_text,
#     #         shape="box",
#     #         color="#2e7d32",
#     #         font={"color": "white", "size": 11, "face": "B Nazanin"},
#     #         size=25,
#     #         x=CENTER_X - 350,
#     #         y=280
#     #     ))
        
#     #     edges.append(Edge("spine_2", arm_left_id))
        
#     #     # مدیریت‌های بازوی چپ
#     #     if is_expanded:
#     #         mgr_list = list(org_data["deputies"][left_arm]["managers"].keys())
#     #         for idx, mgr_name in enumerate(mgr_list):
#     #             mgr_id = f"mgr_left_{idx}"
#     #             mgr_full_key = f"{left_arm}||{mgr_name}"
                
#     #             is_mgr_expanded = mgr_full_key in expanded_managers
#     #             mgr_label = wrap_text(mgr_name, 16)
                
#     #             groups = org_data["deputies"][left_arm]["managers"][mgr_name]["groups"]
#     #             if groups:
#     #                 mgr_label += "\n[+]" if not is_mgr_expanded else "\n[−]"
                
#     #             nodes.append(Node(
#     #                 id=mgr_id,
#     #                 label=mgr_label,
#     #                 shape="box",
#     #                 color="#1976d2",
#     #                 font={"color": "white", "size": 10, "face": "B Nazanin"},
#     #                 size=20,
#     #                 x=CENTER_X - 600,
#     #                 y=280 + (idx * 120)
#     #             ))
                
#     #             edges.append(Edge(arm_left_id, mgr_id))
                
#     #             # گروه‌ها
#     #             if is_mgr_expanded and groups:
#     #                 for grp_idx, grp_name in enumerate(groups):
#     #                     grp_id = f"grp_left_{idx}_{grp_idx}"
                        
#     #                     nodes.append(Node(
#     #                         id=grp_id,
#     #                         label=wrap_text(grp_name, 14),
#     #                         shape="box",
#     #                         color="#66bb6a",
#     #                         font={"color": "white", "size": 9, "face": "B Nazanin"},
#     #                         size=15,
#     #                         x=CENTER_X - 850,
#     #                         y=280 + (idx * 120) + (grp_idx * 80)
#     #                     ))
                        
#     #                     edges.append(Edge(mgr_id, grp_id))

#     # planning_key = None

#     # for key in org_data["deputies"]:
#     #     if key.startswith("مديريت توسعه كسب و كار"):
#     #         planning_key = key
#     #         break
#     # right_arm = planning_key
#     # # بازوی راست
#     # if right_arm and right_arm in org_data["deputies"]:
#     #     arm_right_id = "arm_right"
        
#     #     is_expanded = right_arm in expanded_deputies
#     #     label_text = wrap_text(right_arm, 18)
#     #     if not is_expanded and org_data["deputies"][right_arm]["managers"]:
#     #         label_text += "\n[+]"
#     #     elif is_expanded:
#     #         label_text += "\n[−]"
        
#     #     nodes.append(Node(
#     #         id=arm_right_id,
#     #         label=label_text,
#     #         shape="box",
#     #         color="#2e7d32",
#     #         font={"color": "white", "size": 11, "face": "B Nazanin"},
#     #         size=25,
#     #         x=CENTER_X + 350,
#     #         y=280
#     #     ))
        
#     #     edges.append(Edge("spine_2", arm_right_id))
        
#     #     # مدیریت‌های بازوی راست
#     #     if is_expanded:
#     #         mgr_list = list(org_data["deputies"][right_arm]["managers"].keys())
#     #         for idx, mgr_name in enumerate(mgr_list):
#     #             mgr_id = f"mgr_right_{idx}"
#     #             mgr_full_key = f"{right_arm}||{mgr_name}"
                
#     #             is_mgr_expanded = mgr_full_key in expanded_managers
#     #             mgr_label = wrap_text(mgr_name, 16)
                
#     #             groups = org_data["deputies"][right_arm]["managers"][mgr_name]["groups"]
#     #             if groups:
#     #                 mgr_label += "\n[+]" if not is_mgr_expanded else "\n[−]"
                
#     #             nodes.append(Node(
#     #                 id=mgr_id,
#     #                 label=mgr_label,
#     #                 shape="box",
#     #                 color="#1976d2",
#     #                 font={"color": "white", "size": 10, "face": "B Nazanin"},
#     #                 size=20,
#     #                 x=CENTER_X + 600,
#     #                 y=280 + (idx * 120)
#     #             ))
                
#     #             edges.append(Edge(arm_right_id, mgr_id))
                
#     #             # گروه‌ها
#     #             if is_mgr_expanded and groups:
#     #                 for grp_idx, grp_name in enumerate(groups):
#     #                     grp_id = f"grp_right_{idx}_{grp_idx}"
                        
#     #                     nodes.append(Node(
#     #                         id=grp_id,
#     #                         label=wrap_text(grp_name, 14),
#     #                         shape="box",
#     #                         color="#66bb6a",
#     #                         font={"color": "white", "size": 9, "face": "B Nazanin"},
#     #                         size=15,
#     #                         x=CENTER_X + 850,
#     #                         y=280 + (idx * 120) + (grp_idx * 80)
#     #                     ))
                        
#     #                     edges.append(Edge(mgr_id, grp_id))

#     # یافتن نام‌های دقیق از دیتابیس
#     left_arm = LEFT_ARM_NAME
#     right_arm = RIGHT_ARM_NAME

#     if left_arm_name:
#         if left_arm_name in org_data["deputies"]:
#             left_arm = left_arm_name
#     else:
#         for dep_name in org_data["deputies"].keys():
#             if "مدیریت توسعه" in dep_name and "کسب  و کار" in dep_name:
#                 left_arm = dep_name
#                 break

#     if right_arm_name:
#         if right_arm_name in org_data["deputies"]:
#             right_arm = right_arm_name
#     else:
#         for dep_name in org_data["deputies"].keys():
#             if "مدیرت برنامه ریزی " in dep_name:
#                 right_arm = dep_name
#                 break

#     planning_key = None
#     for key in org_data["deputies"]:
#         if key.startswith("مديريت برنامه ريزي"):
#             planning_key = key
#             break
#     left_arm = planning_key

#     # بازوی چپ
#     if left_arm and left_arm in org_data["deputies"]:
#         arm_left_id = "arm_left"
#         arm_left_x = CENTER_X - 350
#         arm_left_y = 380  # 100 واحد پایین‌تر (380 + 100)
        
#         is_expanded = left_arm in expanded_deputies
#         label_text = wrap_text(left_arm, 18)
#         if not is_expanded and org_data["deputies"][left_arm]["managers"]:
#             label_text += "\n[+]"
#         elif is_expanded:
#             label_text += "\n[−]"
        
#         nodes.append(Node(
#             id=arm_left_id,
#             label=label_text,
#             shape="box",
#             color="#2e7d32",
#             font={"color": "white", "size": 11, "face": "B Nazanin"},
#             size=25,
#             x=arm_left_x,
#             y=arm_left_y
#         ))
        
#         edges.append(Edge("spine_2", arm_left_id))
        
#         # مدیریت‌های بازوی چپ (افقی)
#         if is_expanded:
#             mgr_list = list(org_data["deputies"][left_arm]["managers"].keys())
#             num_managers = len(mgr_list)
            
#             managers_y = arm_left_y + 150  # فاصله عمودی از بلاک اصلی
#             spacing = 200  # فاصله افقی بین مدیریت‌ها
            
#             for idx, mgr_name in enumerate(mgr_list):
#                 mgr_id = f"mgr_left_{idx}"
#                 mgr_full_key = f"{left_arm}||{mgr_name}"
                
#                 is_mgr_expanded = mgr_full_key in expanded_managers
#                 mgr_label = wrap_text(mgr_name, 16)
                
#                 groups = org_data["deputies"][left_arm]["managers"][mgr_name]["groups"]
#                 if groups:
#                     mgr_label += "\n[+]" if not is_mgr_expanded else "\n[−]"
                
#                 # چیدمان افقی: نصفی چپ، نصفی راست
#                 if idx < num_managers / 2:
#                     # سمت چپ
#                     mgr_x = arm_left_x - (spacing * (1 + (num_managers // 2 - 1 - idx)))
#                 else:
#                     # سمت راست
#                     mgr_x = arm_left_x + (spacing * (1 + (idx - num_managers // 2)))
                
#                 nodes.append(Node(
#                     id=mgr_id,
#                     label=mgr_label,
#                     shape="box",
#                     color="#1976d2",
#                     font={"color": "white", "size": 10, "face": "B Nazanin"},
#                     size=20,
#                     x=mgr_x,
#                     y=managers_y
#                 ))
                
#                 edges.append(Edge(arm_left_id, mgr_id))

#                 # # جایی که Edge ها رو تعریف می‌کنی
#                 # edges.append(Edge(
#                 #     "spine_2", 
#                 #     arm_left_id,
#                 #     smooth={"type": "cubicBezier", "roundness": 0.0}
#                 # ))

                
#                 # گروه‌ها (عمودی زیر هر مدیریت)
#                 if is_mgr_expanded and groups:
#                     for grp_idx, grp_name in enumerate(groups):
#                         grp_id = f"grp_left_{idx}_{grp_idx}"
                        
#                         nodes.append(Node(
#                             id=grp_id,
#                             label=wrap_text(grp_name, 14),
#                             shape="box",
#                             color="#66bb6a",
#                             font={"color": "white", "size": 9, "face": "B Nazanin"},
#                             size=15,
#                             x=mgr_x,
#                             y=managers_y + 100 + (grp_idx * 80)
#                         ))
                        
#                         edges.append(Edge(mgr_id, grp_id))

#     planning_key = None
#     for key in org_data["deputies"]:
#         if key.startswith("مديريت توسعه كسب و كار"):
#             planning_key = key
#             break
#     right_arm = planning_key

#     # بازوی راست
#     if right_arm and right_arm in org_data["deputies"]:
#         arm_right_id = "arm_right"
#         arm_right_x = CENTER_X + 350
#         arm_right_y = 380  # 100 واحد پایین‌تر (280 + 100)
        
#         is_expanded = right_arm in expanded_deputies
#         label_text = wrap_text(right_arm, 18)
#         if not is_expanded and org_data["deputies"][right_arm]["managers"]:
#             label_text += "\n[+]"
#         elif is_expanded:
#             label_text += "\n[−]"
        
#         nodes.append(Node(
#             id=arm_right_id,
#             label=label_text,
#             shape="box",
#             color="#2e7d32",
#             font={"color": "white", "size": 11, "face": "B Nazanin"},
#             size=25,
#             x=arm_right_x,
#             y=arm_right_y
#         ))
        
#         edges.append(Edge("spine_2", arm_right_id))
# #         edges.append(Edge(
# #     "spine_2", 
# #     arm_right_id,
# #     smooth={"type": "cubicBezier", "roundness": 0.0}
# # ))
        
#         # مدیریت‌های بازوی راست (افقی)
#         if is_expanded:
#             mgr_list = list(org_data["deputies"][right_arm]["managers"].keys())
#             num_managers = len(mgr_list)
            
#             managers_y = arm_right_y + 150  # فاصله عمودی از بلاک اصلی
#             spacing = 200  # فاصله افقی بین مدیریت‌ها
            
#             for idx, mgr_name in enumerate(mgr_list):
#                 mgr_id = f"mgr_right_{idx}"
#                 mgr_full_key = f"{right_arm}||{mgr_name}"
                
#                 is_mgr_expanded = mgr_full_key in expanded_managers
#                 mgr_label = wrap_text(mgr_name, 16)
                
#                 groups = org_data["deputies"][right_arm]["managers"][mgr_name]["groups"]
#                 if groups:
#                     mgr_label += "\n[+]" if not is_mgr_expanded else "\n[−]"
                
#                 # چیدمان افقی: نصفی چپ، نصفی راست
#                 if idx < num_managers / 2:
#                     # سمت چپ
#                     mgr_x = arm_right_x - (spacing * (1 + (num_managers // 2 - 1 - idx)))
#                 else:
#                     # سمت راست
#                     mgr_x = arm_right_x + (spacing * (1 + (idx - num_managers // 2)))
                
#                 nodes.append(Node(
#                     id=mgr_id,
#                     label=mgr_label,
#                     shape="box",
#                     color="#1976d2",
#                     font={"color": "white", "size": 10, "face": "B Nazanin"},
#                     size=20,
#                     x=mgr_x,
#                     y=managers_y
#                 ))
                
#                 # edges.append(Edge(arm_right_id, mgr_id))

#                 edges.append(Edge(
#                                 "spine_2",
#                                 arm_right_id,
#                                 smooth={
#                                     "type": "cubicBezier",
#                                     "forceDirection": "vertical"
#                                 }
#                             ))

                
#                 # گروه‌ها (عمودی زیر هر مدیریت)
#                 if is_mgr_expanded and groups:
#                     for grp_idx, grp_name in enumerate(groups):
#                         grp_id = f"grp_right_{idx}_{grp_idx}"
                        
#                         nodes.append(Node(
#                             id=grp_id,
#                             label=wrap_text(grp_name, 14),
#                             shape="box",
#                             color="#66bb6a",
#                             font={"color": "white", "size": 9, "face": "B Nazanin"},
#                             size=15,
#                             x=mgr_x,
#                             y=managers_y + 100 + (grp_idx * 80)
#                         ))
                        
#                         edges.append(Edge(mgr_id, grp_id))

#     # ========= خط افقی برای معاونت‌ها (level 3) =========
#     # نقاط نامرئی برای ساخت خط افقی
#     excluded_arms = [arm for arm in [left_arm, right_arm, ceo_office] if arm is not None]
    
#     other_deputies = [
#         (dep_name, dep_data) 
#         for dep_name, dep_data in org_data["deputies"].items()
#         if dep_name not in excluded_arms
#     ]
    
#     num_deputies = len(other_deputies)
    
#     # محاسبه فاصله‌ها
#     total_width = 1600
#     spacing = total_width / (num_deputies + 1) if num_deputies > 0 else 200
#     start_x = CENTER_X - (total_width / 2)
    
#     # نقاط نامرئی برای خط افقی
#     horizontal_points = []
#     for i in range(num_deputies + 2):  # +2 برای نقاط ابتدا و انتها
#         point_id = f"h_point_{i}"
#         x_pos = start_x + (i * spacing)
        
#         nodes.append(Node(
#             id=point_id,
#             label="",
#             size=1,
#             color="#ffffff00",
#             x=x_pos,
#             y=600
#         ))
        
#         horizontal_points.append(point_id)
        
#         # اتصال نقاط افقی به هم
#         if i > 0:
#             edges.append(Edge(horizontal_points[i-1], point_id))
    
#     # اتصال خط عمودی به وسط خط افقی
#     middle_index = len(horizontal_points) // 2
#     edges.append(Edge("spine_4", horizontal_points[middle_index]))
    
#     # ========= معاونت‌ها (پایین خط افقی) =========
#     deputy_mapping = {}
#     if left_arm:
#         deputy_mapping["arm_left"] = left_arm
#     if right_arm:
#         deputy_mapping["arm_right"] = right_arm
#     if ceo_office:
#         deputy_mapping["ceo_office"] = ceo_office
    
#     manager_mapping = {}
    
#     for i, (dep_name, dep_data) in enumerate(other_deputies):
#         dep_id = f"dep_{i}"
#         deputy_mapping[dep_id] = dep_name
        
#         is_expanded = dep_name in expanded_deputies
#         label_text = wrap_text(dep_name, 18)
#         if not is_expanded and dep_data["managers"]:
#             label_text += "\n[+]"
#         elif is_expanded:
#             label_text += "\n[−]"
        
#         # موقعیت x بر اساس شاخص
#         x_pos = start_x + ((i + 1) * spacing)
        
#         nodes.append(Node(
#             id=dep_id,
#             label=label_text,
#             shape="box",
#             color="#4caf50",
#             font={"color": "white", "size": 11, "face": "B Nazanin"},
#             size=25,
#             x=x_pos,
#             y=750
#         ))
        
#         # اتصال به نقطه متناظر در خط افقی
#         edges.append(Edge(horizontal_points[i + 1], dep_id))
        
#         # مدیریت‌ها
#         if is_expanded:
#             mgr_list = list(dep_data["managers"].keys())
#             for mgr_idx, mgr_name in enumerate(mgr_list):
#                 mgr_id = f"mgr_dep_{i}_{mgr_idx}"
#                 mgr_full_key = f"{dep_name}||{mgr_name}"
#                 manager_mapping[mgr_id] = mgr_full_key
                
#                 is_mgr_expanded = mgr_full_key in expanded_managers
#                 mgr_label = wrap_text(mgr_name, 16)
                
#                 groups = dep_data["managers"][mgr_name]["groups"]
#                 if groups:
#                     mgr_label += "\n[+]" if not is_mgr_expanded else "\n[−]"
                
#                 nodes.append(Node(
#                     id=mgr_id,
#                     label=mgr_label,
#                     shape="box",
#                     color="#1976d2",
#                     font={"color": "white", "size": 10, "face": "B Nazanin"},
#                     size=20,
#                     x=x_pos,
#                     y=900 + (mgr_idx * 120)
#                 ))
                
#                 edges.append(Edge(dep_id, mgr_id))
                
#                 # گروه‌ها
#                 if is_mgr_expanded and groups:
#                     for grp_idx, grp_name in enumerate(groups):
#                         grp_id = f"grp_dep_{i}_{mgr_idx}_{grp_idx}"
                        
#                         nodes.append(Node(
#                             id=grp_id,
#                             label=wrap_text(grp_name, 14),
#                             shape="box",
#                             color="#66bb6a",
#                             font={"color": "white", "size": 9, "face": "B Nazanin"},
#                             size=15,
#                             x=x_pos + (200 if grp_idx % 2 == 0 else -200),
#                             y=900 + (mgr_idx * 120) + (grp_idx * 80)
#                         ))
                        
#                         edges.append(Edge(mgr_id, grp_id))
    
#     # mapping برای مدیران بازوها
#     if left_arm and left_arm in org_data["deputies"] and left_arm in expanded_deputies:
#         for idx, mgr_name in enumerate(org_data["deputies"][left_arm]["managers"].keys()):
#             manager_mapping[f"mgr_left_{idx}"] = f"{left_arm}||{mgr_name}"
    
#     if right_arm and right_arm in org_data["deputies"] and right_arm in expanded_deputies:
#         for idx, mgr_name in enumerate(org_data["deputies"][right_arm]["managers"].keys()):
#             manager_mapping[f"mgr_right_{idx}"] = f"{right_arm}||{mgr_name}"

#     return nodes, edges, deputy_mapping, manager_mapping, left_arm, right_arm


# # ===============================
# # Main
# # ===============================
# def main():
#     st.title("🏢 چارت سازمانی")

#     # Test DB connection
#     success, msg = test_connection()
#     if not success:
#         st.error(f"❌ خطا در اتصال به دیتابیس: {msg}")
#         return

#     org_data = get_org_data()

#     # --- Session state ---
#     if "expanded_deputies" not in st.session_state:
#         st.session_state.expanded_deputies = set()
    
#     if "expanded_managers" not in st.session_state:
#         st.session_state.expanded_managers = set()

#     # --- Sidebar ---
#     with st.sidebar:
#         st.header("🎛️ کنترل‌ها")
        
#         if st.button("🔽 باز کردن همه معاونت‌ها"):
#             st.session_state.expanded_deputies = set(org_data["deputies"].keys())
#             st.rerun()
        
#         if st.button("🔼 بستن همه"):
#             st.session_state.expanded_deputies = set()
#             st.session_state.expanded_managers = set()
#             st.rerun()
        
#         st.markdown("---")
        
#         st.info("""
#         💡 **راهنما:**
#         - روی معاونت کلیک کنید → مدیریت‌ها باز می‌شود
#         - روی مدیریت کلیک کنید → گروه‌ها نمایش داده می‌شود
#         - آیکون [+] = قابل باز شدن
#         - آیکون [−] = باز شده
#         """)
        
#         st.markdown("---")
#         stats = get_stats()
#         st.metric("تعداد معاونت‌ها", stats["deputies_count"])
#         st.metric("تعداد مدیریت‌ها", stats["managers_count"])
#         st.metric("تعداد گروه‌ها", stats["groups_count"])
        
#         st.markdown("---")
#         st.markdown("### 🔍 لیست همه معاونت‌ها")
        
#         # نمایش نام معاونت‌ها
#         with st.expander("کلیک برای مشاهده"):
#             for dep_name in org_data["deputies"].keys():
#                 st.text(f"• {dep_name}")

#     # --- Build graph ---
#     nodes, edges, deputy_mapping, manager_mapping, detected_left, detected_right = build_graph(
#         org_data,
#         st.session_state.expanded_deputies,
#         st.session_state.expanded_managers,
#         LEFT_ARM_NAME,
#         RIGHT_ARM_NAME
#     )
    
#     # نمایش اطلاعات دیباگ
#     if detected_left or detected_right:
#         st.success(f"✅ بازوهای شناسایی شده: چپ={detected_left or 'یافت نشد'} | راست={detected_right or 'یافت نشد'}")
#     else:
#         st.warning("⚠️ دو بازو شناسایی نشدند. لطفاً نام دقیق آنها را در ابتدای کد تنظیم کنید.")

#     config = Config(
#         width="100%",
#         height=1600,
#         directed=True,
#         hierarchical=False,
#         physics=False,
#     )

#     # --- Display graph ---
#     clicked = agraph(
#         nodes=nodes,
#         edges=edges,
#         config=config
#     )

#     # --- مدیریت کلیک ---
#     if clicked:
#         # کلیک روی معاونت
#         if clicked in deputy_mapping:
#             dep_name = deputy_mapping[clicked]
            
#             if dep_name in st.session_state.expanded_deputies:
#                 st.session_state.expanded_deputies.remove(dep_name)
#                 # حذف مدیریت‌های مربوط
#                 st.session_state.expanded_managers = {
#                     m for m in st.session_state.expanded_managers
#                     if not m.startswith(f"{dep_name}||")
#                 }
#             else:
#                 st.session_state.expanded_deputies.add(dep_name)
#             st.rerun()
        
#         # کلیک روی مدیریت
#         elif clicked in manager_mapping:
#             mgr_full_key = manager_mapping[clicked]
            
#             if mgr_full_key in st.session_state.expanded_managers:
#                 st.session_state.expanded_managers.remove(mgr_full_key)
#             else:
#                 st.session_state.expanded_managers.add(mgr_full_key)
#             st.rerun()


# if __name__ == "__main__":
#     main()

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

st.markdown("""
<style>
@font-face {
    font-family: 'BNazanin';
    src: url('font/BNazanin.ttf') format('truetype');
}

html, body, [class*="css"] {
    font-family: 'BNazanin', sans-serif;
}
</style>
""", unsafe_allow_html=True)


# ===============================
# تنظیمات دو بازو (اینجا رو ویرایش کنید)
# ===============================
LEFT_ARM_NAME = "مدیریت توسعه کسب و کار"
RIGHT_ARM_NAME = "مدیریت برنامه ریزی"

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
def build_graph(org_data, expanded_deputies, expanded_managers, left_arm_name, right_arm_name):
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
    nodes.append(Node(id="spine_1", label="", size=10, color="#ffffff00", x=CENTER_X, y=120))
    nodes.append(Node(id="spine_2", label="", size=10, color="#ffffff00", x=CENTER_X, y=280))
    nodes.append(Node(id="spine_3", label="", size=10, color="#ffffff00", x=CENTER_X, y=440))
    nodes.append(Node(id="spine_4", label="", size=10, color="#ffffff00", x=CENTER_X, y=600))
    
    edges.append(Edge("ceo", "spine_1"))
    edges.append(Edge("spine_1", "spine_2"))
    edges.append(Edge("spine_2", "spine_3"))
    edges.append(Edge("spine_3", "spine_4"))

    # ========= مدیریت حوزه مدیرعامل =========
    ceo_office = None

    for key in org_data["deputies"].keys():
        if key.startswith("مديريت حوزه مدير عامل و هماهنگي امور"):
            ceo_office = key
            break

    is_ceo_office_expanded = ceo_office in expanded_deputies if ceo_office else False
    label_text = wrap_text(ceo_office, 20) if ceo_office else ""

    if ceo_office and ceo_office in org_data["deputies"]:
        if not is_ceo_office_expanded and org_data["deputies"][ceo_office]["managers"]:
            label_text += "\n[+]"
        elif is_ceo_office_expanded:
            label_text += "\n[−]"

    ceo_office_x = CENTER_X + 350
    ceo_office_y = 120

    nodes.append(Node(
        id="ceo_office",
        label=label_text,
        shape="box",
        color="#1f4e79",
        font={"color": "white", "size": 11, "face": "B Nazanin"},
        size=30,
        x=ceo_office_x,
        y=ceo_office_y
    ))

    edges.append(Edge("spine_1", "ceo_office"))

    # نمایش مدیریت‌های حوزه مدیرعامل
    if is_ceo_office_expanded and ceo_office in org_data["deputies"]:
        mgr_list = list(org_data["deputies"][ceo_office]["managers"].keys())
        num_managers = len(mgr_list)
        
        managers_y = ceo_office_y + 80
        spacing = 250
        
        for idx, mgr_name in enumerate(mgr_list):
            mgr_id = f"mgr_ceo_office_{idx}"
            mgr_full_key = f"{ceo_office}||{mgr_name}"
            
            is_mgr_expanded = mgr_full_key in expanded_managers
            mgr_label = wrap_text(mgr_name, 16)
            
            groups = org_data["deputies"][ceo_office]["managers"][mgr_name]["groups"]
            if groups:
                mgr_label += "\n[+]" if not is_mgr_expanded else "\n[−]"
            
            if num_managers == 1:
                mgr_x = ceo_office_x
            elif num_managers == 2:
                mgr_x = ceo_office_x + ((idx - 0.5) * spacing)
            else:
                mgr_x = ceo_office_x + ((idx - (num_managers - 1) / 2) * spacing)
            
            nodes.append(Node(
                id=mgr_id,
                label=mgr_label,
                shape="box",
                color="#1976d2",
                font={"color": "white", "size": 10, "face": "B Nazanin"},
                size=25,
                x=mgr_x,
                y=managers_y
            ))
            
            edges.append(Edge("ceo_office", mgr_id))
            
            if is_mgr_expanded and groups:
                for grp_idx, grp_name in enumerate(groups):
                    grp_id = f"grp_ceo_office_{idx}_{grp_idx}"
                    
                    nodes.append(Node(
                        id=grp_id,
                        label=wrap_text(grp_name, 14),
                        shape="box",
                        color="#66bb6a",
                        font={"color": "white", "size": 9, "face": "B Nazanin"},
                        size=15,
                        x=mgr_x,
                        y=managers_y + 120 + (grp_idx * 80)
                    ))
                    
                    edges.append(Edge(mgr_id, grp_id))

    # ========= دو بازو =========
   # ========= دو بازو =========
    left_arm = LEFT_ARM_NAME
    right_arm = RIGHT_ARM_NAME

    if left_arm_name:
        if left_arm_name in org_data["deputies"]:
            left_arm = left_arm_name
    else:
        for dep_name in org_data["deputies"].keys():
            if "مدیریت توسعه" in dep_name and "کسب  و کار" in dep_name:
                left_arm = dep_name
                break

    if right_arm_name:
        if right_arm_name in org_data["deputies"]:
            right_arm = right_arm_name
    else:
        for dep_name in org_data["deputies"].keys():
            if "مدیرت برنامه ریزی " in dep_name:
                right_arm = dep_name
                break

    planning_key = None
    for key in org_data["deputies"]:
        if key.startswith("مديريت برنامه ريزي"):
            planning_key = key
            break
    left_arm = planning_key

    # نقاط میانی برای L-shape
    # نقطه میانی برای بازوی چپ
    nodes.append(Node(
        id="arm_left_mid",
        label="",
        size=1,
        color="#ffffff00",
        x=CENTER_X - 350,
        y=280  # همان y که spine_2 داره
    ))

    # نقطه میانی برای بازوی راست
    nodes.append(Node(
        id="arm_right_mid",
        label="",
        size=1,
        color="#ffffff00",
        x=CENTER_X + 350,
        y=280  # همان y که spine_2 داره
    ))

    # اتصال spine_2 به نقاط میانی (افقی)
    edges.append(Edge("spine_2", "arm_left_mid"))
    edges.append(Edge("spine_2", "arm_right_mid"))

    # بازوی چپ
    if left_arm and left_arm in org_data["deputies"]:
        arm_left_id = "arm_left"
        arm_left_x = CENTER_X - 350
        arm_left_y = 380
        
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
            x=arm_left_x,
            y=arm_left_y
        ))
        
        # اتصال از نقطه میانی به بازو (عمودی)
        edges.append(Edge("arm_left_mid", arm_left_id))
        
        # باقی کد بازوی چپ...
        if is_expanded:
            mgr_list = list(org_data["deputies"][left_arm]["managers"].keys())
            num_managers = len(mgr_list)
            
            managers_y = arm_left_y + 150
            spacing = 200
            
            for idx, mgr_name in enumerate(mgr_list):
                mgr_id = f"mgr_left_{idx}"
                mgr_full_key = f"{left_arm}||{mgr_name}"
                
                is_mgr_expanded = mgr_full_key in expanded_managers
                mgr_label = wrap_text(mgr_name, 16)
                
                groups = org_data["deputies"][left_arm]["managers"][mgr_name]["groups"]
                if groups:
                    mgr_label += "\n[+]" if not is_mgr_expanded else "\n[−]"
                
                if idx < num_managers / 2:
                    mgr_x = arm_left_x - (spacing * (1 + (num_managers // 2 - 1 - idx)))
                else:
                    mgr_x = arm_left_x + (spacing * (1 + (idx - num_managers // 2)))
                
                nodes.append(Node(
                    id=mgr_id,
                    label=mgr_label,
                    shape="box",
                    color="#1976d2",
                    font={"color": "white", "size": 10, "face": "B Nazanin"},
                    size=20,
                    x=mgr_x,
                    y=managers_y
                ))
                
                edges.append(Edge(arm_left_id, mgr_id))
                
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
                            x=mgr_x,
                            y=managers_y + 100 + (grp_idx * 80)
                        ))
                        
                        edges.append(Edge(mgr_id, grp_id))

    planning_key = None
    for key in org_data["deputies"]:
        if key.startswith("مديريت توسعه كسب و كار"):
            planning_key = key
            break
    right_arm = planning_key

    # بازوی راست
    if right_arm and right_arm in org_data["deputies"]:
        arm_right_id = "arm_right"
        arm_right_x = CENTER_X + 350
        arm_right_y = 380
        
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
            x=arm_right_x,
            y=arm_right_y
        ))
        
        # اتصال از نقطه میانی به بازو (عمودی)
        edges.append(Edge("arm_right_mid", arm_right_id))
        
        # باقی کد بازوی راست...
        if is_expanded:
            mgr_list = list(org_data["deputies"][right_arm]["managers"].keys())
            num_managers = len(mgr_list)
            
            managers_y = arm_right_y + 150
            spacing = 200
            
            for idx, mgr_name in enumerate(mgr_list):
                mgr_id = f"mgr_right_{idx}"
                mgr_full_key = f"{right_arm}||{mgr_name}"
                
                is_mgr_expanded = mgr_full_key in expanded_managers
                mgr_label = wrap_text(mgr_name, 16)
                
                groups = org_data["deputies"][right_arm]["managers"][mgr_name]["groups"]
                if groups:
                    mgr_label += "\n[+]" if not is_mgr_expanded else "\n[−]"
                
                if idx < num_managers / 2:
                    mgr_x = arm_right_x - (spacing * (1 + (num_managers // 2 - 1 - idx)))
                else:
                    mgr_x = arm_right_x + (spacing * (1 + (idx - num_managers // 2)))
                
                nodes.append(Node(
                    id=mgr_id,
                    label=mgr_label,
                    shape="box",
                    color="#1976d2",
                    font={"color": "white", "size": 10, "face": "B Nazanin"},
                    size=20,
                    x=mgr_x,
                    y=managers_y
                ))
                
                edges.append(Edge(arm_right_id, mgr_id))
                
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
                            x=mgr_x,
                            y=managers_y + 100 + (grp_idx * 80)
                        ))
                        
                        edges.append(Edge(mgr_id, grp_id))

    # ========= خط افقی برای معاونت‌ها =========
    excluded_arms = [arm for arm in [left_arm, right_arm, ceo_office] if arm is not None]
    
    other_deputies = [
        (dep_name, dep_data) 
        for dep_name, dep_data in org_data["deputies"].items()
        if dep_name not in excluded_arms
    ]
    
    num_deputies = len(other_deputies)
    
    total_width = 1600
    spacing = total_width / (num_deputies + 1) if num_deputies > 0 else 200
    start_x = CENTER_X - (total_width / 2)
    
    horizontal_points = []
    for i in range(num_deputies + 2):
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
        
        if i > 0:
            edges.append(Edge(horizontal_points[i-1], point_id))
    
    middle_index = len(horizontal_points) // 2
    edges.append(Edge("spine_4", horizontal_points[middle_index]))
    
    # ========= معاونت‌ها =========
    deputy_mapping = {}
    if left_arm:
        deputy_mapping["arm_left"] = left_arm
    if right_arm:
        deputy_mapping["arm_right"] = right_arm
    if ceo_office:
        deputy_mapping["ceo_office"] = ceo_office
    
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
        
        edges.append(Edge(horizontal_points[i + 1], dep_id))
        
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
    if left_arm and left_arm in org_data["deputies"] and left_arm in expanded_deputies:
        for idx, mgr_name in enumerate(org_data["deputies"][left_arm]["managers"].keys()):
            manager_mapping[f"mgr_left_{idx}"] = f"{left_arm}||{mgr_name}"
    
    if right_arm and right_arm in org_data["deputies"] and right_arm in expanded_deputies:
        for idx, mgr_name in enumerate(org_data["deputies"][right_arm]["managers"].keys()):
            manager_mapping[f"mgr_right_{idx}"] = f"{right_arm}||{mgr_name}"

    return nodes, edges, deputy_mapping, manager_mapping, left_arm, right_arm


# ===============================
# Main
# ===============================
def main():
    st.title("🏢 چارت سازمانی")

    success, msg = test_connection()
    if not success:
        st.error(f"❌ خطا در اتصال به دیتابیس: {msg}")
        return

    org_data = get_org_data()

    if "expanded_deputies" not in st.session_state:
        st.session_state.expanded_deputies = set()
    
    if "expanded_managers" not in st.session_state:
        st.session_state.expanded_managers = set()

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
        
        st.markdown("---")
        st.markdown("### 🔍 لیست همه معاونت‌ها")
        
        with st.expander("کلیک برای مشاهده"):
            for dep_name in org_data["deputies"].keys():
                st.text(f"• {dep_name}")

    nodes, edges, deputy_mapping, manager_mapping, detected_left, detected_right = build_graph(
        org_data,
        st.session_state.expanded_deputies,
        st.session_state.expanded_managers,
        LEFT_ARM_NAME,
        RIGHT_ARM_NAME
    )
    
    if detected_left or detected_right:
        st.success(f"✅ بازوهای شناسایی شده: چپ={detected_left or 'یافت نشد'} | راست={detected_right or 'یافت نشد'}")
    else:
        st.warning("⚠️ دو بازو شناسایی نشدند. لطفاً نام دقیق آنها را در ابتدای کد تنظیم کنید.")

    # تنظیمات Config با smooth برای خطوط L-shaped
    # config = Config(
    #     width="100%",
    #     height=1600,
    #     directed=True,
    #     hierarchical=False,
    #     physics=False,
    #     # اضافه کردن تنظیمات edges
    #     **{
    #         "edges": {
    #             "smooth": {
    #                 "enabled": True,
    #                 "type": "discrete",
    #                 "forceDirection": "vertical"
    #             }
    #         }
    #     }
    # )


    config = Config(
    width="100%",
    height=1600,
    directed=True,
    hierarchical=False,
    physics=False,
    **{
        "edges": {
            "smooth": {
                "enabled": False
            },
            "arrows": {
                "to": {
                    "enabled": True,
                    "scaleFactor": 0.5
                }
            }
        }
    }
)

    clicked = agraph(
        nodes=nodes,
        edges=edges,
        config=config
    )

    if clicked:
        if clicked in deputy_mapping:
            dep_name = deputy_mapping[clicked]
            
            if dep_name in st.session_state.expanded_deputies:
                st.session_state.expanded_deputies.remove(dep_name)
                st.session_state.expanded_managers = {
                    m for m in st.session_state.expanded_managers
                    if not m.startswith(f"{dep_name}||")
                }
            else:
                st.session_state.expanded_deputies.add(dep_name)
            st.rerun()
        
        elif clicked in manager_mapping:
            mgr_full_key = manager_mapping[clicked]
            
            if mgr_full_key in st.session_state.expanded_managers:
                st.session_state.expanded_managers.remove(mgr_full_key)
            else:
                st.session_state.expanded_managers.add(mgr_full_key)
            st.rerun()


if __name__ == "__main__":
    main()