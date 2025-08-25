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
    page_title="Next Action BI",
    layout="wide",
    page_icon="🛠️"
)

import base64

# Load the image and convert to base64
with open("titanLogo.png", "rb") as f:
    data = f.read()
    encoded = base64.b64encode(data).decode()

# Title with logo
st.markdown(
    f"""
    <div style="width: 100%; display: flex; align-items: center; gap: 18px; margin-bottom: 8px;">
        <div style="background-color: white; width: 65px; height: 65px; border-radius: 10%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
            <img src="data:image/png;base64,{encoded}" style="width: 50px; height: 50px;"/>
        </div>
        <div>
            <div style="font-size: 2.2rem; font-weight: 800; color: white; line-height: 1.2;">
                Immediate Next Action Plan
            </div>
            <div style="font-size: 1rem; color: #ddd; line-height: 1.4;">
                Insights & action assignments with email notifications.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Custom CSS for popover button
st.markdown(
    """
    <style>
    /* Force styling for the popover button */
    [data-testid="stPopover"] > div > button {
        background: transparent !important;
        border: 1.5px solid #ff4d4d !important;   /* Red border */
        color: #ff4d4d !important;                /* Red text */
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 8px 16px !important;
        transition: all 0.2s ease-in-out;
    }

    /* Hover effect */
    [data-testid="stPopover"] > div > button:hover {
        background: #ff4d4d20 !important;  /* light red background */
        color: #ff4d4d !important;
        border-color: #ff1a1a !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
        "✦ Immediate Next Action by Purchase Quantity",
        "✦ Immediate Next Action by Weight",
        "✦ Immediate Next Action by Making Charges",
        "✦ Immediate Next Action Based On Stone Value"
    ],
    "Based On Qualitative Analysis": [
        "✦ Immediate Next Action For Each Brand",
        "✦ Immediate Next Action from Daily Discount Insights"
    ],
    "Based On Multivariate Analysis": [
        "✦ Maximize Revenue from High Value Buyers",
        "✦ Optimize Discount Strategy to Protect Margin & Luxury Perception"
    ],
    "Based On Time Series Analysis": [
        "✦ Reducing Returns & Key Focus Areas",
        "✦ Immediate Next Action - Saturday Sales Push"
    ]
}

card_colors = [
    "linear-gradient(90deg, #BF82D9, #9333EA)",  # Purple gradient
    "linear-gradient(135deg, #f87171, #ef4444)",
    "linear-gradient(90deg, #F6BB4D, #F59E0B)",  # Orange gradient
    "linear-gradient(90deg, #85B4D4, #3B82F6)"   # Teal/Blue gradient
]

example_actions = {
    '✦ Immediate Next Action by Purchase Quantity': [
        "✦ Instead of discounting core items, we can offer “Buy any gold or diamond piece and get 15 to 20% off on studs, pendants, or chains.”",
        "✦ We can cross sell with deals like “Buy this necklace, get 15% off matching bangles.”",
        "✦ This will increase the quantity of jewelry they purchase as well as the total bill value."
    ],
    '✦ Immediate Next Action by Weight': [
       "✦ Currently, Heavy (10–20g) and Very Heavy (>20g) jewelry get the highest discounts at 6.7%, while Medium (5–10g) averages 6.2%.",
       "✦ Shifting Medium to 6.5% and trimming Heavy/Very Heavy to 6.3% makes Medium the clear “best value,” creating a decoy effect that nudges Light/Very Light buyers (5.5–6.0%) to upgrade and positions Medium as the smartest choice."
    ],
    "✦ Immediate Next Action by Making Charges" : [
        "✦ In our data, 835 items had Making Charges above ₹50,000. By introducing a Good, Better, & Best choice with ₹3.0L with ₹52k MC, ₹3.3L with ₹65k MC and ₹4.0L with ₹85k MC, customers are naturally nudged toward the middle or premium option. Even if 30% move to “Better” and 10% to “Best,” this simple decoy pricing approach can unlock nearly ₹50L additional revenue without increasing discounts, purely by guiding customers toward designs with higher Making Charges.",
        "✦ No single bill should get more than ₹1,00,000 discount. In past data, 142 bills crossed ₹1,00,000 in discounts. These very deep cuts directly eat into profit. A hard cap stops uncontrolled losses.",
        "✦ We can test it for 2 weeks and review it. This short trial makes sure it doesn’t hurt overall sales while protecting profit. After 2 weeks, stakeholders can measure and adjust it."
    ],
    "✦ Immediate Next Action Based On Stone Value" : [
        "✦ DIA and GIS are our mid range stone categories, and together they account for 6,281 transactions with average stone values between ₹25,000 and ₹50,000. That’s nearly 2/3 of all our sales. This means even a small adjustment in how we manage discounts here by just 2–3% can have the biggest impact on our overall margins. So, this segment needs careful control on discounts, supported by value added offers like vouchers.",
        "✦ For discounts above ₹50,000, we can split it. For example we can give ₹30,000 off now + ₹20,000 shopping voucher for the next purchase. In past data, 371 bills had discounts over ₹50,000. If part of it is a voucher, customers must come back, which boosts future sales and reduces instant profit loss."
    ],
    
    "✦ Immediate Next Action For Each Brand" : [
        "✦ ZOYA – Achieved ₹2.25 Cr sales from just 43 orders but with an extremely high average discount of ₹69k. This risks diluting luxury positioning so shift from heavy discounts to exclusivity perks like private previews and customization.",
        "✦ TANISHQ – Delivered ₹92.9 Cr sales from 8203 orders with avg discount of ₹10.6k, but 349 returns hurt margins. Focus on reducing returns through better sizing guidance, quality checks, and clearer product info.",
        "✦ MIA – ₹5.1 Cr sales from 1652 orders with an average discount of just ₹2.5k shows that customers like the brand at mid-level pricing. But with 68 returns, there’s a gap between what customers expect and what they actually receive. To fix this, MIA should improve product descriptions, images, and try-on/AR options so buyers feel more confident before purchasing, which will reduce returns and increase trust.",
        "✦ ECOM – ₹45 L sales from 102 orders, zero returns, avg discount just ₹195 shows stable performance. We need to expand reach with stronger digital marketing and targeted acquisition."
    ],
        "✦ Immediate Next Action from Daily Discount Insights" : [
        """✦ Observation:
            During the 'Festival of Diamonds' campaign, customers were willing to make big purchases, but their buying decisions were driven mainly by substantial discounts, typically between ₹15k and ₹23k. This group is both aspirational and price-conscious, they desire luxury items, but only when it feels like they are getting a great deal.""",
        """✦ Why It Matters:
            If we continue to throw raw discounts at them, we’ll train them to wait only for mega sales.
            Instead, if we flip their psychology and make them feel like special members and not bargain hunters, they’ll shop even without big discounts, stick with us, spend more on premium pieces, stay engaged, and recommend us to others."""
    ],
    "✦ Maximize Revenue from High Value Buyers" : [
        "✦ Experiences create stronger memories than money saved. A ₹50k discount is forgotten but a luxury photoshoot becomes a story they tell. For customers spending ₹5L+, replace the ₹50k discount with a professional couple’s photoshoot (worth ₹50k) featuring their new jewelry. This costs the same to us, but delivers 2x perceived value, boosts social sharing, and can generate 3 to 5 organic referrals per customer.",
        "✦ People hate missing out more than they love getting a deal, so when luxury is offered for a limited time, the urgency feels real and natural. Tanishq can run a “Design of the Week”, a necklace or earring sold only for 5 days and then retire it, creating urgency that pushes faster buying decisions and can lift sales by 10-15%, especially around occasions like Akshaya Tritiya."
    ],
    "✦ Optimize Discount Strategy to Protect Margin & Luxury Perception" : [
        "✦ Zoya's discounts are way higher than than Tanishq and Mia. In South 3 it even hits 12.18%. We should pull this back closer to 8% which saves margin and keeps the luxury image intact.",
        "✦ Ecom is giving 11.3% discounts, almost twice the stores. It is better to run short flash sales under 8% which keeps urgency alive without making customers expect big cuts every time."
    ],
    "✦ Reducing Returns & Key Focus Areas" : [
        "✦ Out of 420 returns, about 170 (40%) are diamonds. If we double check stone quality and size before shipping, we can avoid at least 40 returns every month, saving around ₹25–30 lakh.",
        "✦ Returns shoot up on sale days that trigger the most returns. On the 13th (22 returns), 25th (27), and 30th (31), returns spiked due to offers. If we fix the products and offers on those days, we can cut around 50 returns monthly, worth ₹35–40 lakh.",
        "✦ Tanishq is a major source of returns: 118 out of 420 (28%) come from Tanishq, mainly diamonds and GIS. If we make customers try these in-store before buying, we can cut 40–45 returns a month, saving ₹25–30 lakh."
    ],
    "✦ Immediate Next Action - Saturday Sales Push" : [
        "✦ Weekends run at 5.94% average discount vs 5.57% on weekdays, but with fewer transactions (3,356 vs 6,182). If we balance weekend offers better, we can lift sales by 10–12% without cutting margins.",
        "✦ Monday (6.40%) and Thursday (6.36%) have the steepest discounts but not the highest sales (1,055 and 1,506 txns). Trimming just 0.5% discount here saves ₹15–20 lakh monthly without hurting volumes.",    
        "✦ Sunday is at 1,947 sales with 6.03% discount, while Saturday is only 1,409 at 5.84%. That’s 40% more sales on Sunday for just 0.2% higher discount. Pushing offers and campaigns on Saturday can add ~500 sales weekly without extra discount."
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
    padding: 1.2em;
    border-radius: 1.2em;
    font-size: 1em;
    font-weight: 600;
    text-align: center;
    color: #fff;
    margin-bottom: 1em;
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
                        st.markdown(
                            f"""
                            <div class="custom-card" style="background:linear-gradient(90deg,#BF82D9,#9333EA); text-align:left; font-size:0.95em;">
                                {bullet}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    st.markdown("---")
                    action_text = st.text_area(
                        "Add further specific instructions or planned steps:",
                        placeholder="E.g. Assign tasks, request weekly update, etc.",
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

# Reference Link
st.markdown(
    """
    <style>
    .header-container {
        display: flex;
        justify-content: flex-end;  /* Align only to right */
        margin-top: 8px;
        margin-bottom: 15px;
    }
    .yellow-line {
        border: none;
        border-top: 3px solid #FFD700; /* Yellow line */
        margin: 15px 0;
    }
    .dashboard-link {
        display: block;
        padding: 14px 22px;
        border-radius: 12px;
        text-align: center;
        font-size: 16px;
        font-weight: 600;
        color: white !important;
        background: linear-gradient(90deg, #BF82D9, #9333EA);
        text-decoration: none !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.25), 
                    inset 0 1px 6px rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    .dashboard-link:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 12px 28px rgba(0,0,0,0.35), 
                    inset 0 1px 8px rgba(255,255,255,0.25);
        text-decoration: none !important;
        color: white !important;
    }
    .dashboard-link span {
        display: block;
        font-size: 13px;
        font-weight: 400;
        margin-top: 4px;
        opacity: 0.9;  
        color: white !important;
    }
    </style>

    <!-- Yellow line under title -->
    <hr class="yellow-line">

    <div class="header-container">
        <a class="dashboard-link" href="https://discount-analysis-dashboard.streamlit.app/" target="_blank">
            🌐 Open Discount Analysis Dashboard
            <span>Explore AI-Powered Analytics With Chatbot Assistance</span>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)







