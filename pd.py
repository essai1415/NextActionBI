import streamlit as st
import pandas as pd
import random
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit_extras.annotated_text import annotated_text
from streamlit_extras.colored_header import colored_header

# ===================
# PAGE CONFIGURATION
# ===================
st.set_page_config(
    page_title="Jewelry Profitability Dashboard",
    layout="wide",
    page_icon="💎"
)

st.title("Suggested Immediate Next Action Plan")
st.write("Insights & action assignments with automatic email notifications.")

# ===================
# DATA LOADING
# ===================
@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_excel("discansamp.xlsx", parse_dates=['docdate'])
    df['day'] = df['docdate'].dt.date
    df['cogs'] = df['goldprice'] + df['stonevalue']
    df['gross_profit'] = df['value'] - df['cogs']
    df['operating_cost'] = 0.05 * df['value']
    df['net_profit'] = df['gross_profit'] - df['discount'] - df['operating_cost']
    df['gross_margin'] = (df['gross_profit'] / df['value']) * 100
    df['net_margin'] = (df['net_profit'] / df['value']) * 100
    return df

df = load_data()

# ===================
# EMAIL SENDING FUNCTION
# ===================
def send_assignment_email(action, team, deadline, personalized_msg=""):
    try:
        sender_email = st.secrets["EMAIL_SENDER"]
        receiver_email = st.secrets["EMAIL_RECEIVER"]
        password = st.secrets["EMAIL_PASSWORD"]
    except KeyError as e:
        st.warning(f"Email credential {e} missing in Streamlit secrets. Please add it to your secrets.toml file.")
        return False

    subject = f"[Assignment Notification] '{action}' assigned to {team}"

    body = f"""
Hello,

You assigned the following action item:

Action: {action}
Assigned To Team: {team}
Deadline: {deadline}

"""

    if personalized_msg.strip():
        body += f"{personalized_msg}\n\n"

    body += "-- BI Team, Titan\n"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# ===================
# ACTION MODULES AND COLORS
# ===================
action_modules = {
    "Based On Quantitative Analysis": [
        "Next Steps by Purchase Quantity",
        "Next Steps by Weight",
    ],
    "Based On Qualitative Analysis": [
        "Next Steps For Each Brand",
        "Next Steps from Daily Discount Insights"
    ],
    "Based On Multivariate Analysis": [
        "Maximize Revenue from High Value Buyers",
        "Optimize product mix where gold content is high"
    ],
    "Based On Time Series Analysis": [
        "Identify dips in weekly net margins for immediate correction",
        "Flag discount spikes around campaign periods"
    ]
}

card_colors = [
    "linear-gradient(90deg, #BF82D9, #9333EA)",  # Purple gradient
    "linear-gradient(135deg, #f9a8d4, #f472b6)",
    "linear-gradient(90deg, #F6BB4D, #F59E0B)",  # Orange gradient
    "linear-gradient(90deg, #85B4D4, #3B82F6)"   # Teal/Blue gradient
]


example_actions = {
    'Next Steps by Purchase Quantity': [
        "Instead of discounting core items, we can offer “Buy any gold or diamond piece and get 20% off on studs, pendants, or chains.”",
        "Cross-sell with deals like “Buy this necklace, get 15% off matching bangles.”",
    ],
    'Next Steps by Weight': [
       "Heavy (10–20g) and Very Heavy (>20g) jewelry get the highest discounts (~6.7%). Reduce them slightly and increase Medium (5–10g) discounts to 6.5% to drive growth.",
       "Encourage Light/Very Light buyers to upgrade by making Medium look like the best value option."
    ],
    "Next Steps For Each Brand" : [
        "ZOYA: Review discounting to protect luxury positioning.",
        "TANISHQ: Focus on reducing high return rates.",
        "MIA: Improve customer satisfaction and retention."
    ],
    "Next Steps from Daily Discount Insights" : [
        "Introduce discount bands (₹5K, ₹10K, ₹20K) for consistency.",
        "Use heavy discount days as anchors in ads.",
        "Segment customers by value and create bundled decoy offers."
    ],
    "Maximize Revenue from High Value Buyers" : [
        "Offer add-ons like studs, chains, or bangles with 15–20% off to top buyers.",
        "Provide loyalty benefits to repeat customers."
    ]
}

def get_next_actions(action):
    return example_actions.get(action, [
        "Define next actions to be taken for this item.",
        "Assign tasks to appropriate team members."
    ])

teams_list = ["Sales", "Marketing", "Finance", "Operations", "Support"]

# === Custom Styling ===
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(145deg, #1f1f2e, #12121a);
    color: #f1f1f1;
    font-family: "Inter", sans-serif;
}

/* Section Header */
h2, .section-header {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid #f6bb4d;
    color: #f6bb4d !important;
}

/* Cards */
.custom-card {
    transition: all 0.3s ease-in-out;
    padding: 1.5em;
    border-radius: 1.2em;
    font-size: 1.1em;
    font-weight: 600;
    text-align: center;
    color: #fff;
    margin-bottom: 1.5em;
    background: rgba(255, 255, 255, 0.07);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}
.custom-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 12px 30px rgba(0,0,0,0.4);
}

/* Global Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6e8efb, #a777e3);
    border: none;
    color: white !important;
    font-weight: 600;
    padding: 0.6rem 1.2rem;
    border-radius: 0.8rem;
    transition: all 0.3s ease;
    cursor: pointer;
}
.stButton > button:hover {
    transform: scale(1.05);
    background: linear-gradient(135deg, #a777e3, #6e8efb);
    box-shadow: 0px 4px 15px rgba(0,0,0,0.25);
}

/* Cancel Button Styling */
.stButton > button[kind="secondary"], 
.stButton > button[title*="Cancel"], 
.stButton > button:has-text("Cancel") {
    background: linear-gradient(135deg, #ff6b6b, #d7385e) !important;
}
.stButton > button[kind="secondary"]:hover, 
.stButton > button[title*="Cancel"]:hover, 
.stButton > button:has-text("Cancel"):hover {
    background: linear-gradient(135deg, #d7385e, #ff6b6b) !important;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.25);
}

/* Popover Styling */
[data-testid="stPopover"] {
    background: rgba(30, 30, 46, 0.85) !important;
    backdrop-filter: blur(10px);
    border-radius: 1rem !important;
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0px 8px 25px rgba(0,0,0,0.4);
    padding: 1.2rem !important;
    color: white !important;
}
[data-testid="stPopover"] h4, 
[data-testid="stPopover"] h3, 
[data-testid="stPopover"] h2 {
    color: #f6bb4d !important;
    font-weight: 700;
}

/* Popover Trigger Button */
.stPopover > button {
    background: linear-gradient(135deg, #6e8efb, #a777e3) !important;
    color: white !important;
    font-weight: 600;
    border-radius: 0.8rem;
    transition: all 0.3s ease;
}
.stPopover > button:hover {
    background: linear-gradient(135deg, #a777e3, #6e8efb) !important;
    transform: scale(1.05);
}

/* Next Actions Heading */
.next-actions-heading {
    font-size: 1.2rem;
    font-weight: 700;
    color: #f6bb4d !important;
    border-bottom: 2px solid #f6bb4d;
    padding-bottom: 0.3rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# === Display Cards ===
for idx, (module_name, actions) in enumerate(action_modules.items()):
    colored_header(module_name, "Key Recommendations", color_name="orange-70")
    cols = st.columns(2)
    for col, action in zip(cols * ((len(actions) + 1) // 2), actions):
        with col:
            color = card_colors[idx % len(card_colors)]
            st.markdown(
                f"""
                <div class="custom-card" style="background:{color};">
                    <b>{action}</b>
                </div>
                """,
                unsafe_allow_html=True
            )
            popup_key = f"popup_{module_name}_{action}"
            if st.button("See Details", key=popup_key):
                current = st.session_state.get(f"show_{popup_key}", False)
                st.session_state[f"show_{popup_key}"] = not current
            if st.session_state.get(f"show_{popup_key}", False):
                with st.popover("Next Actions To Be Taken"):
                    st.markdown('<div class="next-actions-heading">Next Actions to Be Taken</div>', unsafe_allow_html=True)
                    bullets = get_next_actions(action)
                    for bullet in bullets:
                        st.markdown(f"- {bullet}")
                    st.markdown("---")
                    action_text = st.text_area(
                        "Add further specific instructions or planned steps:",
                        placeholder="E.g. Assign regional leads, request weekly update, etc.",
                        height=120,
                        key=f"action_text_{popup_key}"
                    )
                    selected_team = st.selectbox(
                        "Select Team to Assign",
                        teams_list,
                        key=f"team_select_{popup_key}"
                    )
                    c1, c2 = st.columns([1,1])
                    with c1:
                        send_pressed = st.button("Send Action", key=f"send_action_{popup_key}", use_container_width=True)
                    with c2:
                        cancel_pressed = st.button("Cancel", key=f"cancel_action_{popup_key}", use_container_width=True)
                    if send_pressed:
                        st.session_state[f"show_{popup_key}"] = False
                        next_steps = "\n".join(bullets)
                        personalized_msg = f"NEXT ACTIONS:\n{next_steps}\n\nOTHER INSTRUCTIONS:\n{action_text}"
                        success = send_assignment_email(action, selected_team, datetime.date.today(), personalized_msg)
                        if success:
                            st.session_state["assignment_status"] = f"✅ Immediate action sent for '{action}'."
                        else:
                            st.session_state["assignment_status"] = f"⚠️ Failed to send the immediate action for '{action}'. Check your configuration."
                        st.rerun()
                    if cancel_pressed:
                        st.session_state[f"show_{popup_key}"] = False
                        st.rerun()

# Show confirmation messages outside popups
if "assignment_status" in st.session_state:
    st.success(st.session_state["assignment_status"])
    del st.session_state["assignment_status"]
