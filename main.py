import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random

# Configure page
st.set_page_config(
    page_title="BeLive ALPS Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize sample data if not exists
if 'sample_data' not in st.session_state:
    # Generate sample leads data
    np.random.seed(42)
    sample_leads = []
    
    nationalities = ['Malaysia', 'China', 'India', 'Singapore', 'Indonesia', 'Others']
    nat_weights = [0.4, 0.25, 0.15, 0.08, 0.07, 0.05]
    
    sources = ['Friends/Family', 'Social Media', 'Website', 'Advertisement', 'Walk-in']
    source_weights = [0.3, 0.25, 0.2, 0.15, 0.1]
    
    locations = ['KL City Center', 'Mont Kiara', 'Bangsar', 'Petaling Jaya', 'Setapak', 'Others']
    agents = ['Sarah (Top Sales)', 'John (Top Sales)', 'Amy (Senior)', 'David (Senior)', 'Lisa (Junior)', 'Mike (Junior)']
    
    for i in range(150):
        # Generate move-in date (next 1-90 days)
        move_in_days = np.random.exponential(20)
        move_in_date = datetime.now() + timedelta(days=min(move_in_days, 90))
        
        # Generate budget with some correlation to nationality
        nationality = np.random.choice(nationalities, p=nat_weights)
        if nationality in ['Malaysia']:
            budget_range = np.random.choice(['RM 500-700', 'RM 700-900', 'RM 900-1200'], p=[0.4, 0.4, 0.2])
        else:
            budget_range = np.random.choice(['RM 700-900', 'RM 900-1200', 'RM 1200+'], p=[0.3, 0.5, 0.2])
        
        # Calculate ALPS Score based on your criteria
        # Move-in Timeline (35%)
        days_to_move = (move_in_date - datetime.now()).days
        if days_to_move <= 7:
            timeline_score = 35
        elif days_to_move <= 14:
            timeline_score = 30
        elif days_to_move <= 30:
            timeline_score = 20
        else:
            timeline_score = 10
        
        # Budget (25%)
        budget_scores = {'RM 500-700': 10, 'RM 700-900': 18, 'RM 900-1200': 22, 'RM 1200+': 25}
        budget_score = budget_scores.get(budget_range, 15)
        
        # Nationality (20%)
        nat_scores = {'Malaysia': 10, 'China': 18, 'India': 16, 'Singapore': 20, 'Indonesia': 17, 'Others': 15}
        nationality_score = nat_scores.get(nationality, 15)
        
        # Source (10%)
        source = np.random.choice(sources, p=source_weights)
        source_scores = {'Friends/Family': 10, 'Social Media': 8, 'Website': 6, 'Advertisement': 7, 'Walk-in': 9}
        source_score = source_scores.get(source, 6)
        
        # Location match (6%)
        location = np.random.choice(locations)
        location_score = 6 if location != 'Others' else 3
        
        # Convenience (4%) - simplified
        convenience_score = np.random.randint(2, 5)
        
        alps_score = timeline_score + budget_score + nationality_score + source_score + location_score + convenience_score
        
        # Determine lead temperature
        if alps_score >= 80:
            lead_temp = 'Hot'
        elif alps_score >= 60:
            lead_temp = 'Warm'
        else:
            lead_temp = 'Cold'
        
        # Assign agent based on lead temperature and availability
        if lead_temp == 'Hot':
            agent = np.random.choice(['Sarah (Top Sales)', 'John (Top Sales)'])
        elif lead_temp == 'Warm':
            agent = np.random.choice(['Sarah (Top Sales)', 'John (Top Sales)', 'Amy (Senior)', 'David (Senior)'])
        else:
            agent = np.random.choice(agents)
        
        # Response time and SLA
        if lead_temp == 'Hot':
            sla_target = 2  # 2 minutes
        elif lead_temp == 'Warm':
            sla_target = 5  # 5 minutes
        else:
            sla_target = 10  # 10 minutes
        
        response_time = np.random.exponential(sla_target * 0.8)
        sla_met = response_time <= sla_target
        
        sample_leads.append({
            'Lead_ID': f'L{i+1:03d}',
            'Timestamp': datetime.now() - timedelta(days=np.random.randint(0, 30)),
            'Move_In_Date': move_in_date,
            'Days_To_Move': days_to_move,
            'Budget_Range': budget_range,
            'Nationality': nationality,
            'Source': source,
            'Location': location,
            'ALPS_Score': alps_score,
            'Lead_Temperature': lead_temp,
            'Assigned_Agent': agent,
            'Response_Time_Min': round(response_time, 2),
            'SLA_Target_Min': sla_target,
            'SLA_Met': sla_met,
            'Status': np.random.choice(['New', 'In Progress', 'Qualified', 'Closed Won', 'Closed Lost'], 
                                    p=[0.2, 0.3, 0.25, 0.15, 0.1])
        })
    
    st.session_state.sample_data = pd.DataFrame(sample_leads)

# CSS for better styling with brand colors and WhatsApp-like background
st.markdown("""
<style>
/* Brand colors */
:root {
    --belive-teal: #4ECDC4;
    --belive-orange: #FF7F50;
    --belive-dark-teal: #3A9B96;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 0rem;
}

/* WhatsApp-style background pattern */
.chat-background {
    background-image: 
        radial-gradient(circle at 25% 25%, rgba(78, 205, 196, 0.1) 2px, transparent 2px),
        radial-gradient(circle at 75% 75%, rgba(255, 127, 80, 0.1) 2px, transparent 2px);
    background-size: 50px 50px;
    background-color: #e5ddd5;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    text-align: center;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: #f0f0f0;
    border-radius: 5px 5px 0 0;
    gap: 1px;
    padding-left: 20px;
    padding-right: 20px;
}

.stTabs [aria-selected="true"] {
    background-color: var(--belive-teal);
    color: white;
}

/* Update button colors to match brand */
.stButton button {
    background-color: var(--belive-orange);
    color: white;
    border: none;
    border-radius: 20px;
    padding: 8px 16px;
    transition: background-color 0.3s;
}

.stButton button:hover {
    background-color: #e6654a;
}

/* Form elements styling */
.stSelectbox > div > div {
    background-color: white;
}

.stTextInput > div > div > input {
    background-color: white;
}

.stMultiSelect > div > div {
    background-color: white;
}

/* User message with brand colors */
.user-message-brand {
    background-color: var(--belive-orange);
    color: white;
}

/* Bot message styling */
.bot-message-brand {
    background-color: white;
    border-left: 3px solid var(--belive-teal);
}
</style>
""", unsafe_allow_html=True)

# Header with brand logo and colors
st.markdown("""
<div style="background: linear-gradient(135deg, #4ECDC4, #FF7F50); padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center;">
    <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
        <div style="font-size: 48px; font-weight: bold; color: white;">
            <span style="color: #4ECDC4; background: white; padding: 5px 10px; border-radius: 10px; margin-right: 5px;">be</span><span style="color: #FF7F50; background: white; padding: 5px 10px; border-radius: 10px;">live</span>
        </div>
    </div>
    <h1 style="color: white; margin: 10px 0 0 0; font-size: 28px;">ALPS Dashboard</h1>
    <p style="color: white; margin: 5px 0 0 0; opacity: 0.9;">Automated Lead Prioritization System</p>
</div>
""", unsafe_allow_html=True)

# Get base data
df = st.session_state.sample_data

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "💬 Live Chat Demo",
    "📊 Overview Dashboard", 
    "🔥 ALPS Scoring", 
    "🎯 Smart Routing", 
    "👥 Agent Performance", 
    "📈 Business Analytics"
])

with tab1:
    st.header("💬 Live Chat Demo - Lead Capture System")
    
    # Initialize chat session state
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'chat_stage' not in st.session_state:
        st.session_state.chat_stage = 'initial'
    if 'chat_user_data' not in st.session_state:
        st.session_state.chat_user_data = {}
    if 'show_area_selection' not in st.session_state:
        st.session_state.show_area_selection = False
    if 'show_condo_selection' not in st.session_state:
        st.session_state.show_condo_selection = False
    if 'show_form' not in st.session_state:
        st.session_state.show_form = False
    if 'selected_area' not in st.session_state:
        st.session_state.selected_area = None
    if 'selected_condo' not in st.session_state:
        st.session_state.selected_condo = None
    if 'show_alps_calculation' not in st.session_state:
        st.session_state.show_alps_calculation = False
    
    # Areas and condos data
    AREAS_CONDOS = {
        "KL City Center": ["121 Residence", "7 Tree Seven", "Armani SOHO", "Austin Regency", 
                          "Icon City", "Majestic Maxim", "One Cochrane", "Pixel City Central", 
                          "The OOAK", "Trion KL", "Youth City"],
        "Mont Kiara": ["Mont Kiara", "Duta Park", "M Adora", "M Vertica", 
                      "The Andes", "Vertu Resort"],
        "Ampang": ["Acacia Residence Ampang", "Astoria Ampang", "The Azure", 
                  "The Azure Residences"],
        "Ara Damansara": ["Ara Damansara", "AraTre Residence", "Emporis Kota Damansara", 
                         "Kota Damansara"],
        "Cheras": ["Arte Cheras", "Cheras", "D'Cosmos", "Razak City Residences"],
        "Petaling Jaya": ["Parc3 Petaling Jaya", "The PARC3", "Kelana Jaya"],
        "Bukit Jalil": ["Bora Residence Bukit Jalil", "HighPark Suites", "Platinum Splendor"],
        "Setapak": ["Setapak", "Fairview Residence", "Keramat"],
        "Subang Jaya": ["Subang Jaya", "Sunway Avila", "Sunway Serene"],
        "Sentul": ["Sentul", "Vista Sentul", "Sinaran Sentul"],
        "Sungai Besi": ["Sungai Besi", "Marina Residence", "Sapphire Paradigm"],
        "Bandar Sri Permaisuri": ["Bandar Sri Permaisuri", "Astoria", "Epic Residence"],
        "Seri Kembangan": ["Seri Kembangan", "Secoya Residence", "Rica Residence"],
        "Others": ["Medini Signature", "Meta City", "MH Platinum 2", "Pinnacle", 
                  "Sinaran Residence", "The Birch", "Unio Residence", 
                  "Vivo Executive Apartment", "Vivo Residence"]
    }
    
    def add_chat_message(sender, content):
        st.session_state.chat_messages.append({
            'sender': sender,
            'content': content,
            'timestamp': datetime.now().strftime("%H:%M")
        })
    
    def process_user_input(user_input):
        user_input_lower = user_input.lower().strip()
        
        if st.session_state.chat_stage == 'initial':
            if any(greeting in user_input_lower for greeting in ['hi', 'hello', 'hey']):
                st.session_state.chat_stage = 'ask_area'
                st.session_state.show_area_selection = True
                return """Hello! Welcome to BeLive Co-Living! 👋

I'm here to help you find your perfect co-living space.

Which area are you interested in?"""
            else:
                return """Hello! Welcome to BeLive Co-Living! 👋

I'm here to help you find your perfect co-living space. Type 'Hi' to get started!"""
        
        elif st.session_state.chat_stage == 'form_completed':
            return handle_post_form_queries(user_input_lower)
        
        else:
            return "I'm here to help! What would you like to know about BeLive Co-Living?"

    def handle_post_form_queries(user_input):
        if 'yes' in user_input.lower():
            return f"""Great! Here are our available room recommendations for {st.session_state.selected_condo}:

🏠 **Room A102** - RM 650/month
📍 Shared bathroom, 2 housemates
🚗 Parking available

🏠 **Room B205** - RM 750/month  
📍 Private bathroom, 1 housemate
🚗 Parking available

🏠 **Room C301** - RM 680/month
📍 Shared bathroom, 3 housemates
🚗 No parking

Which room interests you? Reply with the room number or say "agent" to speak with our property consultant! 🏠"""
        
        elif 'no' in user_input.lower():
            return "No problem! Let me know if you'd like to explore other options or adjust your preferences."
        
        elif 'agent' in user_input.lower() or any(room in user_input.lower() for room in ['a102', 'b205', 'c301']):
            return """Perfect! I'm connecting you with our property consultant now.

📞 **Agent Contact:**
🏠 **Sarah Lim** - Senior Property Consultant
📱 WhatsApp: +60 12-345-6789
📧 Email: sarah@belive.com.my

She will contact you within 30 minutes to arrange a viewing and provide more details about the room.

Thank you for choosing BeLive Co-Living! 🎉"""
        
        else:
            return "Would you like to proceed with the available options within your budget range? Or would you like to speak with our agent directly?"

    def display_area_selection():
        st.markdown("### 📍 Please select your preferred area:")
        
        areas = list(AREAS_CONDOS.keys())
        cols = st.columns(3)
        
        for i, area in enumerate(areas):
            col_idx = i % 3
            with cols[col_idx]:
                if st.button(area, key=f"area_{i}", use_container_width=True):
                    st.session_state.selected_area = area
                    st.session_state.show_area_selection = False
                    st.session_state.show_condo_selection = True
                    st.session_state.chat_stage = 'area_selected'
                    
                    add_chat_message('user', area)
                    add_chat_message('bot', f"Great choice! Here are the available co-living spaces in {area}:")
                    st.rerun()

    def display_condo_selection():
        if st.session_state.selected_area:
            st.markdown(f"### 🏠 Available properties in {st.session_state.selected_area}:")
            
            condos = AREAS_CONDOS[st.session_state.selected_area]
            cols = st.columns(2)
            
            for i, condo in enumerate(condos):
                col_idx = i % 2
                with cols[col_idx]:
                    if st.button(condo, key=f"condo_{i}", use_container_width=True):
                        st.session_state.selected_condo = condo
                        st.session_state.show_condo_selection = False
                        st.session_state.show_form = True
                        st.session_state.chat_stage = 'condo_selected'
                        
                        add_chat_message('user', condo)
                        add_chat_message('bot', f"Perfect! You've selected {condo}. Please fill out this form to proceed:")
                        st.rerun()

    def display_inquiry_form():
        with st.form("inquiry_form"):
            st.markdown(f"### 📋 Inquiry Form - {st.session_state.selected_condo}")
            
            # 1. Room Budget/Type
            budget = st.selectbox("1. Room Budget/Type *", 
                                 ["Select budget", "RM 500-700", "RM 700-900", "RM 900-1200", "RM 1200+"])
            
            # 2. How many pax staying
            pax = st.radio("2. How many pax staying? *", 
                          ["1", "2", "More than 2"])
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 3. Do you have a car
                have_car = st.radio("3. Do you have a car? *", 
                                   ["Yes", "No"])
                
                # 4. Need Car Park Lot
                need_parking = st.radio("4. Need Car Park Lot? *", 
                                       ["Yes", "No"])
                
                # 5. Move in date
                move_in_date = st.date_input("5. When do you plan to move in? *")
                
                # 6. Tenancy Period
                tenancy = st.radio("6. Tenancy Period *", 
                                  ["6 months", "12 months"])
            
            with col2:
                # 7. Gender
                gender = st.radio("7. Gender *", 
                                 ["Male", "Female"])
                
                # 8. Unit Specification (can choose multiple)
                unit_spec = st.multiselect("8. Unit Specification (can select multiple) *", 
                                          ["Female unit", "Male unit", "Mixed Gender unit"])
                
                # 10. Nationality
                nationality = st.radio("10. Nationality *", 
                                      ["Malaysia", "Others"])
                
                nationality_specify = ""
                if nationality == "Others":
                    nationality_specify = st.text_input("Please specify nationality:")
            
            # 9. Workplace
            workplace = st.text_input("9. Where is your workplace? (To recommend closest property) *")
            
            submitted = st.form_submit_button("Submit Inquiry", use_container_width=True)
            
            if submitted:
                if budget != "Select budget" and pax and workplace and unit_spec:
                    # Store user data
                    st.session_state.chat_user_data = {
                        'area': st.session_state.selected_area,
                        'condo': st.session_state.selected_condo,
                        'budget': budget,
                        'pax': pax,
                        'have_car': have_car,
                        'need_parking': need_parking,
                        'move_in_date': move_in_date,
                        'tenancy': tenancy,
                        'gender': gender,
                        'unit_spec': unit_spec,
                        'workplace': workplace,
                        'nationality': nationality if nationality == "Malaysia" else nationality_specify
                    }
                    
                    st.session_state.show_form = False
                    st.session_state.chat_stage = 'form_completed'
                    st.session_state.show_alps_calculation = True
                    
                    # Form summary
                    summary = f"""✅ **Form Summary**

📍 **Location**: {st.session_state.selected_area} - {st.session_state.selected_condo}
💰 **Budget**: {budget}
👥 **Occupants**: {pax} person(s)
🚗 **Car**: {have_car} | **Parking**: {need_parking}
📅 **Move-in**: {move_in_date}
📋 **Tenancy**: {tenancy}
👤 **Gender**: {gender}
🏠 **Unit Type**: {', '.join(unit_spec)}
🏢 **Workplace**: {workplace}
🌍 **Nationality**: {st.session_state.chat_user_data['nationality']}

Thank you for your submission! 🎉

Calculating ALPS score and routing to best agent..."""
                    
                    add_chat_message('bot', summary)
                    st.rerun()
                else:
                    st.error("Please fill in all required fields marked with *")
    
    def calculate_alps_score(user_data):
        """Calculate ALPS score based on user data"""
        score = 0
        breakdown = {}
        
        # Move-in Timeline (35%)
        if 'move_in_date' in user_data:
            days_to_move = (user_data['move_in_date'] - datetime.now().date()).days
            if days_to_move <= 7:
                timeline_score = 35
            elif days_to_move <= 14:
                timeline_score = 30
            elif days_to_move <= 30:
                timeline_score = 20
            else:
                timeline_score = 10
            score += timeline_score
            breakdown['Move-in Timeline'] = timeline_score
        
        # Budget (25%)
        if 'budget' in user_data:
            budget_scores = {'RM 500-700': 10, 'RM 700-900': 18, 'RM 900-1200': 22, 'RM 1200+': 25}
            budget_score = budget_scores.get(user_data['budget'], 15)
            score += budget_score
            breakdown['Budget'] = budget_score
        
        # Nationality (20%)
        if 'nationality' in user_data:
            if user_data['nationality'] != 'Malaysia':
                nationality_score = 18
            else:
                nationality_score = 10
            score += nationality_score
            breakdown['Nationality'] = nationality_score
        
        # How do you know BeLive (10%) - simulate
        source_score = 8
        score += source_score
        breakdown['Lead Source'] = source_score
        
        # Location Match (6%)
        if 'area' in user_data and user_data['area'] != 'Others':
            location_score = 6
        else:
            location_score = 3
        score += location_score
        breakdown['Location Match'] = location_score
        
        # Convenience (4%) - simulate
        convenience_score = 4
        score += convenience_score
        breakdown['Convenience'] = convenience_score
        
        return score, breakdown
    
    def determine_lead_temperature(score):
        if score >= 80:
            return 'Hot', '#ff4444'
        elif score >= 60:
            return 'Warm', '#ffaa00'
        else:
            return 'Cold', '#4444ff'
    
    def assign_agent(lead_temp):
        """Smart routing logic"""
        if lead_temp == 'Hot':
            return np.random.choice(['Sarah (Top Sales)', 'John (Top Sales)'])
        elif lead_temp == 'Warm':
            return np.random.choice(['Sarah (Top Sales)', 'John (Top Sales)', 'Amy (Senior)', 'David (Senior)'])
        else:
            return np.random.choice(['Amy (Senior)', 'David (Senior)', 'Lisa (Junior)', 'Mike (Junior)'])
    
    # Create layout for chat demo
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Chat Header with brand colors
        st.markdown('''
        <div style="background: linear-gradient(135deg, #4ECDC4, #FF7F50); color: white; padding: 15px; text-align: center; border-radius: 10px 10px 0 0; margin: 0;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
                <span style="color: #4ECDC4; background: white; padding: 2px 6px; border-radius: 5px; font-weight: bold; font-size: 14px;">be</span><span style="color: #FF7F50; background: white; padding: 2px 6px; border-radius: 5px; font-weight: bold; font-size: 14px;">live</span>
                <span style="margin-left: 10px;">Co-Living</span>
            </div>
            <p style="margin: 5px 0 0 0; font-size: 12px; opacity: 0.9;">Customer Service Chat</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Main chat container with WhatsApp-style background
        st.markdown('<div class="chat-background" style="height: 600px; overflow-y: auto; padding: 20px; margin: 0;">', unsafe_allow_html=True)
        
        # Display chat messages with brand colors
        for message in st.session_state.chat_messages:
            if message['sender'] == 'user':
                st.markdown(f"""
                <div style="background-color: #FF7F50; color: white; margin: 8px 0; padding: 8px 12px; border-radius: 7px; 
                           max-width: 65%; margin-left: auto; margin-right: 0; word-wrap: break-word; 
                           float: right; clear: both; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                    {message['content']}
                    <div style="font-size: 11px; color: rgba(255,255,255,0.8); text-align: right; margin-top: 2px;">{message['timestamp']}</div>
                </div>
                <div style="clear: both;"></div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color: #ffffff; margin: 8px 0; padding: 8px 12px; border-radius: 7px; 
                           max-width: 65%; margin-left: 0; margin-right: auto; word-wrap: break-word; 
                           float: left; clear: both; box-shadow: 0 1px 2px rgba(0,0,0,0.1); 
                           border-left: 3px solid #4ECDC4;">
                    {message['content']}
                    <div style="font-size: 11px; color: #666; text-align: left; margin-top: 2px;">{message['timestamp']}</div>
                </div>
                <div style="clear: both;"></div>
                """, unsafe_allow_html=True)
        
        # Show selections and forms
        if st.session_state.show_area_selection:
            st.markdown('<div style="background-color: rgba(255, 255, 255, 0.95); padding: 15px; margin: 5px 0; border-radius: 10px; border: 1px solid #4ECDC4;">', unsafe_allow_html=True)
            display_area_selection()
            st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.show_condo_selection:
            st.markdown('<div style="background-color: rgba(255, 255, 255, 0.95); padding: 15px; margin: 5px 0; border-radius: 10px; border: 1px solid #4ECDC4;">', unsafe_allow_html=True)
            display_condo_selection()
            st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.show_form:
            st.markdown('<div style="background-color: rgba(255, 255, 255, 0.95); padding: 15px; margin: 5px 0; border-radius: 10px; border: 1px solid #4ECDC4;">', unsafe_allow_html=True)
            display_inquiry_form()
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Input area with brand colors
        st.markdown('<div style="background: linear-gradient(135deg, #4ECDC4, #FF7F50); padding: 10px; border-radius: 0 0 10px 10px; margin: 0;">', unsafe_allow_html=True)
        
        with st.form("chat_input_form", clear_on_submit=True):
            col_input, col_send = st.columns([5, 1])
            
            with col_input:
                user_input = st.text_input("Type your message...", label_visibility="collapsed", placeholder="Type your message...")
            
            with col_send:
                send_button = st.form_submit_button("Send", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Handle user input
        if send_button and user_input:
            # Add user message
            add_chat_message('user', user_input)
            
            # Process and add bot response
            bot_response = process_user_input(user_input)
            add_chat_message('bot', bot_response)
            
            # Rerun to show new messages
            st.rerun()
    
    with col2:
        st.subheader("🔥 Real-time ALPS Analysis")
        
        if st.session_state.show_alps_calculation and st.session_state.chat_user_data:
            # Calculate ALPS score
            alps_score, score_breakdown = calculate_alps_score(st.session_state.chat_user_data)
            lead_temp, temp_color = determine_lead_temperature(alps_score)
            assigned_agent = assign_agent(lead_temp)
            
            # Display ALPS score
            st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; border: 3px solid {temp_color};">
                <h2 style="color: {temp_color}; margin: 0;">ALPS Score: {alps_score}/100</h2>
                <h3 style="color: {temp_color}; margin: 5px 0;">🔥 {lead_temp} Lead</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Score breakdown
            st.subheader("📊 Score Breakdown")
            for criteria, score in score_breakdown.items():
                st.metric(criteria, f"{score} points")
            
            # Smart routing result
            st.subheader("🎯 Smart Routing Result")
            st.success(f"**Assigned to:** {assigned_agent}")
            
            # Lead details
            st.subheader("📋 Lead Details")
            user_data = st.session_state.chat_user_data
            st.write(f"**Location:** {user_data['area']} - {user_data['condo']}")
            st.write(f"**Budget:** {user_data['budget']}")
            st.write(f"**Move-in:** {user_data['move_in_date']}")
            st.write(f"**Nationality:** {user_data['nationality']}")
            
            # Add to sample data button
            if st.button("💾 Add to Database", type="primary"):
                # Add this lead to sample data
                days_to_move = (user_data['move_in_date'] - datetime.now().date()).days
                
                new_lead = {
                    'Lead_ID': f'L{len(st.session_state.sample_data)+1:03d}',
                    'Timestamp': datetime.now(),
                    'Move_In_Date': user_data['move_in_date'],
                    'Days_To_Move': days_to_move,
                    'Budget_Range': user_data['budget'],
                    'Nationality': user_data['nationality'],
                    'Source': 'Live Chat Demo',
                    'Location': user_data['area'],
                    'ALPS_Score': alps_score,
                    'Lead_Temperature': lead_temp,
                    'Assigned_Agent': assigned_agent,
                    'Response_Time_Min': np.random.exponential(3),
                    'SLA_Target_Min': 2 if lead_temp == 'Hot' else 5 if lead_temp == 'Warm' else 10,
                    'SLA_Met': True,
                    'Status': 'New'
                }
                
                st.session_state.sample_data = pd.concat([
                    st.session_state.sample_data, 
                    pd.DataFrame([new_lead])
                ], ignore_index=True)
                
                st.success("✅ Lead added to database! Check other tabs to see updated analytics.")
                
                # Reset chat
                st.session_state.chat_messages = []
                st.session_state.chat_stage = 'initial'
                st.session_state.chat_user_data = {}
                st.session_state.show_area_selection = False
                st.session_state.show_condo_selection = False
                st.session_state.show_form = False
                st.session_state.show_alps_calculation = False
                st.session_state.selected_area = None
                st.session_state.selected_condo = None
                
                # Add initial message
                add_chat_message('bot', """Welcome to BeLive Co-Living! 🏠

We're excited to help you find your perfect co-living space in Kuala Lumpur.

Type 'Hi' to get started!""")
                
                st.rerun()
        
        else:
            st.info("💡 Start a chat conversation to see real-time ALPS scoring and smart routing in action!")
            
            st.markdown("""
            **How it works:**
            1. 💬 Customer starts chat 
            2. 📍 Selects area & property
            3. 📋 Fills inquiry form
            4. 🔥 ALPS calculates lead score
            5. 🎯 Smart routing assigns agent
            6. 📊 Data flows to analytics
            """)
    
    # Initialize chat if empty
    if not st.session_state.chat_messages:
        initial_message = """Welcome to BeLive Co-Living! 🏠

We're excited to help you find your perfect co-living space in Kuala Lumpur.

Type 'Hi' to get started!"""
        add_chat_message('bot', initial_message)
        st.rerun()

with tab2:
    st.header("📊 Business Overview")
    
    # Filters for this tab
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        date_range = st.date_input(
            "📅 Date Range",
            value=(df['Timestamp'].min().date(), df['Timestamp'].max().date()),
            min_value=df['Timestamp'].min().date(),
            max_value=df['Timestamp'].max().date()
        )
    
    with col_filter2:
        temp_filter = st.multiselect(
            "🔥 Lead Temperature",
            options=['Hot', 'Warm', 'Cold'],
            default=['Hot', 'Warm', 'Cold']
        )
    
    with col_filter3:
        nat_filter = st.multiselect(
            "🌍 Nationality",
            options=df['Nationality'].unique(),
            default=df['Nationality'].unique()
        )
    
    # Filter data for this tab
    filtered_df = df[
        (df['Timestamp'].dt.date >= date_range[0]) &
        (df['Timestamp'].dt.date <= date_range[1]) &
        (df['Lead_Temperature'].isin(temp_filter)) &
        (df['Nationality'].isin(nat_filter))
    ]
    
    st.markdown("---")
    
    # KPI metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_leads = len(filtered_df)
        st.metric("Total Leads", total_leads)
    
    with col2:
        hot_leads = len(filtered_df[filtered_df['Lead_Temperature'] == 'Hot'])
        st.metric("Hot Leads", hot_leads, delta=f"{hot_leads/total_leads*100:.1f}%" if total_leads > 0 else "0%")
    
    with col3:
        avg_score = filtered_df['ALPS_Score'].mean() if len(filtered_df) > 0 else 0
        st.metric("Avg ALPS Score", f"{avg_score:.1f}")
    
    with col4:
        sla_rate = (filtered_df['SLA_Met'].sum() / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric("SLA Compliance", f"{sla_rate:.1f}%")
    
    with col5:
        conversion_rate = len(filtered_df[filtered_df['Status'] == 'Closed Won']) / total_leads * 100 if total_leads > 0 else 0
        st.metric("Conversion Rate", f"{conversion_rate:.1f}%")
    
    st.markdown("---")
    
    # Charts row 1
    col1, col2 = st.columns(2)
    
    with col1:
        # Update chart colors to match brand
        temp_counts = filtered_df['Lead_Temperature'].value_counts()
        fig_pie = px.pie(
            values=temp_counts.values,
            names=temp_counts.index,
            title="Lead Temperature Distribution",
            color_discrete_map={'Hot': '#FF7F50', 'Warm': '#FFB347', 'Cold': '#4ECDC4'}
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # ALPS Score distribution with brand colors
        fig_hist = px.histogram(
            filtered_df,
            x='ALPS_Score',
            nbins=20,
            title="ALPS Score Distribution",
            color='Lead_Temperature',
            color_discrete_map={'Hot': '#FF7F50', 'Warm': '#FFB347', 'Cold': '#4ECDC4'}
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    # Charts row 2
    col1, col2 = st.columns(2)
    
    with col1:
        # Leads by nationality
        nat_counts = filtered_df['Nationality'].value_counts().reset_index()
        nat_counts.columns = ['Nationality', 'Count']
        fig_nat = px.bar(
            nat_counts,
            x='Nationality',
            y='Count',
            title="Leads by Nationality",
            color='Nationality'
        )
        st.plotly_chart(fig_nat, use_container_width=True)
    
    with col2:
        # Timeline vs Score scatter
        fig_scatter = px.scatter(
            filtered_df,
            x='Days_To_Move',
            y='ALPS_Score',
            color='Lead_Temperature',
            size='ALPS_Score',
            title="Move-in Timeline vs ALPS Score",
            color_discrete_map={'Hot': '#ff4444', 'Warm': '#ffaa00', 'Cold': '#4444ff'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

with tab3:
    st.header("🔥 ALPS Scoring Analysis")
    
    # Filters for this tab
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        date_range_alps = st.date_input(
            "📅 Date Range",
            value=(df['Timestamp'].min().date(), df['Timestamp'].max().date()),
            min_value=df['Timestamp'].min().date(),
            max_value=df['Timestamp'].max().date(),
            key="alps_date"
        )
    
    with col_filter2:
        temp_filter_alps = st.multiselect(
            "🔥 Lead Temperature",
            options=['Hot', 'Warm', 'Cold'],
            default=['Hot', 'Warm', 'Cold'],
            key="alps_temp"
        )
    
    with col_filter3:
        nat_filter_alps = st.multiselect(
            "🌍 Nationality",
            options=df['Nationality'].unique(),
            default=df['Nationality'].unique(),
            key="alps_nat"
        )
    
    # Filter data for this tab
    filtered_df_alps = df[
        (df['Timestamp'].dt.date >= date_range_alps[0]) &
        (df['Timestamp'].dt.date <= date_range_alps[1]) &
        (df['Lead_Temperature'].isin(temp_filter_alps)) &
        (df['Nationality'].isin(nat_filter_alps))
    ]
    
    st.markdown("---")
    
    # ALPS criteria weights
    st.subheader("Current ALPS Criteria Weights")
    
    criteria_weights = {
        'Move-in Timeline': 35,
        'Budget Range': 25,
        'Nationality': 20,
        'Lead Source': 10,
        'Location Match': 6,
        'Convenience Matrix': 4
    }
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Display weights
        for criteria, weight in criteria_weights.items():
            st.metric(criteria, f"{weight}%")
    
    with col2:
        # Weights pie chart
        fig_weights = px.pie(
            values=list(criteria_weights.values()),
            names=list(criteria_weights.keys()),
            title="ALPS Scoring Criteria Weights"
        )
        st.plotly_chart(fig_weights, use_container_width=True)
    
    st.markdown("---")
    
    # Score analysis by criteria
    col1, col2 = st.columns(2)
    
    with col1:
        # Budget vs Score - Change from box plot to bar chart
        budget_avg_scores = filtered_df_alps.groupby(['Budget_Range', 'Lead_Temperature'])['ALPS_Score'].mean().reset_index()
        fig_budget = px.bar(
            budget_avg_scores,
            x='Budget_Range',
            y='ALPS_Score',
            color='Lead_Temperature',
            title="Average ALPS Score by Budget Range",
            color_discrete_map={'Hot': '#ff4444', 'Warm': '#ffaa00', 'Cold': '#4444ff'},
            text='ALPS_Score'
        )
        fig_budget.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_budget.update_layout(yaxis_range=[0, 100])
        st.plotly_chart(fig_budget, use_container_width=True)
    
    with col2:
        # Nationality vs Score - Change from box plot to bar chart
        nat_avg_scores = filtered_df_alps.groupby(['Nationality', 'Lead_Temperature'])['ALPS_Score'].mean().reset_index()
        fig_nat_score = px.bar(
            nat_avg_scores,
            x='Nationality',
            y='ALPS_Score',
            color='Lead_Temperature',
            title="Average ALPS Score by Nationality",
            color_discrete_map={'Hot': '#ff4444', 'Warm': '#ffaa00', 'Cold': '#4444ff'},
            text='ALPS_Score'
        )
        fig_nat_score.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_nat_score.update_layout(yaxis_range=[0, 100])
        fig_nat_score.update_xaxes(tickangle=45)
        st.plotly_chart(fig_nat_score, use_container_width=True)
    
    # Score breakdown table
    st.subheader("Top 10 Highest Scoring Leads")
    if len(filtered_df_alps) > 0:
        top_leads = filtered_df_alps.nlargest(10, 'ALPS_Score')[
            ['Lead_ID', 'ALPS_Score', 'Lead_Temperature', 'Days_To_Move', 'Budget_Range', 'Nationality', 'Status']
        ]
        st.dataframe(top_leads, use_container_width=True)
    else:
        st.info("No data available for the selected filters.")

with tab4:
    st.header("🎯 Smart Routing Performance")
    
    # Filters for this tab
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        date_range_routing = st.date_input(
            "📅 Date Range",
            value=(df['Timestamp'].min().date(), df['Timestamp'].max().date()),
            min_value=df['Timestamp'].min().date(),
            max_value=df['Timestamp'].max().date(),
            key="routing_date"
        )
    
    with col_filter2:
        temp_filter_routing = st.multiselect(
            "🔥 Lead Temperature",
            options=['Hot', 'Warm', 'Cold'],
            default=['Hot', 'Warm', 'Cold'],
            key="routing_temp"
        )
    
    with col_filter3:
        agent_filter = st.multiselect(
            "👥 Select Agents",
            options=df['Assigned_Agent'].unique(),
            default=df['Assigned_Agent'].unique(),
            key="routing_agent"
        )
    
    # Filter data for this tab
    filtered_df_routing = df[
        (df['Timestamp'].dt.date >= date_range_routing[0]) &
        (df['Timestamp'].dt.date <= date_range_routing[1]) &
        (df['Lead_Temperature'].isin(temp_filter_routing)) &
        (df['Assigned_Agent'].isin(agent_filter))
    ]
    
    st.markdown("---")
    
    # Routing metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_response = filtered_df_routing['Response_Time_Min'].mean() if len(filtered_df_routing) > 0 else 0
        st.metric("Avg Response Time", f"{avg_response:.1f} min")
    
    with col2:
        sla_breaches = len(filtered_df_routing[~filtered_df_routing['SLA_Met']])
        st.metric("SLA Breaches", sla_breaches)
    
    with col3:
        hot_leads_filtered = filtered_df_routing[filtered_df_routing['Lead_Temperature'] == 'Hot']
        if len(hot_leads_filtered) > 0:
            hot_to_top_sales = len(hot_leads_filtered[
                hot_leads_filtered['Assigned_Agent'].str.contains('Top Sales')
            ]) / len(hot_leads_filtered) * 100
        else:
            hot_to_top_sales = 0
        st.metric("Hot → Top Sales %", f"{hot_to_top_sales:.1f}%")
    
    with col4:
        agent_counts = filtered_df_routing.groupby('Assigned_Agent').size()
        if len(agent_counts) > 0:
            fairness_score = 100 - (agent_counts.std() / agent_counts.mean() * 100)
        else:
            fairness_score = 100
        st.metric("Fairness Score", f"{fairness_score:.1f}%")
    
    st.markdown("---")
    
    # Routing analysis charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Agent assignment by lead temperature
        if len(filtered_df_routing) > 0:
            agent_temp = pd.crosstab(filtered_df_routing['Assigned_Agent'], filtered_df_routing['Lead_Temperature'])
            agent_temp_reset = agent_temp.reset_index()
            
            # Melt the data for plotly
            agent_temp_melted = pd.melt(
                agent_temp_reset, 
                id_vars=['Assigned_Agent'], 
                value_vars=[col for col in ['Hot', 'Warm', 'Cold'] if col in agent_temp.columns],
                var_name='Lead_Temperature', 
                value_name='Count'
            )
            
            fig_agent = px.bar(
                agent_temp_melted,
                x='Assigned_Agent',
                y='Count',
                color='Lead_Temperature',
                title="Agent Assignment by Lead Temperature",
                color_discrete_map={'Hot': '#ff4444', 'Warm': '#ffaa00', 'Cold': '#4444ff'}
            )
            fig_agent.update_xaxes(tickangle=45)
            st.plotly_chart(fig_agent, use_container_width=True)
        else:
            st.info("No data available for the selected filters.")
    
    with col2:
        # Response time by lead temperature - Change from box plot to bar chart
        if len(filtered_df_routing) > 0:
            response_avg = filtered_df_routing.groupby('Lead_Temperature')['Response_Time_Min'].mean().reset_index()
            fig_response = px.bar(
                response_avg,
                x='Lead_Temperature',
                y='Response_Time_Min',
                color='Lead_Temperature',
                title="Average Response Time by Lead Temperature",
                color_discrete_map={'Hot': '#ff4444', 'Warm': '#ffaa00', 'Cold': '#4444ff'},
                text='Response_Time_Min'
            )
            fig_response.update_traces(texttemplate='%{text:.1f} min', textposition='outside')
            
            # Add SLA target reference lines as annotations
            fig_response.add_hline(y=2, line_dash="dash", line_color="red", annotation_text="Hot SLA Target (2 min)", annotation_position="top right")
            fig_response.add_hline(y=5, line_dash="dash", line_color="orange", annotation_text="Warm SLA Target (5 min)", annotation_position="top right")
            fig_response.add_hline(y=10, line_dash="dash", line_color="blue", annotation_text="Cold SLA Target (10 min)", annotation_position="top right")
            
            st.plotly_chart(fig_response, use_container_width=True)
        else:
            st.info("No data available for the selected filters.")
    
    # SLA compliance details
    st.subheader("SLA Compliance by Agent")
    if len(filtered_df_routing) > 0:
        sla_by_agent = filtered_df_routing.groupby('Assigned_Agent').agg({
            'SLA_Met': ['count', 'sum'],
            'Response_Time_Min': 'mean'
        }).round(2)
        sla_by_agent.columns = ['Total_Leads', 'SLA_Met', 'Avg_Response_Time']
        sla_by_agent['SLA_Rate_%'] = (sla_by_agent['SLA_Met'] / sla_by_agent['Total_Leads'] * 100).round(1)
        st.dataframe(sla_by_agent, use_container_width=True)
    else:
        st.info("No data available for the selected filters.")

with tab5:
    st.header("👥 Agent Performance Dashboard")
    
    # Filters for this tab
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        date_range_agent = st.date_input(
            "📅 Date Range",
            value=(df['Timestamp'].min().date(), df['Timestamp'].max().date()),
            min_value=df['Timestamp'].min().date(),
            max_value=df['Timestamp'].max().date(),
            key="agent_date"
        )
    
    with col_filter2:
        agent_filter_perf = st.multiselect(
            "👥 Select Agents",
            options=df['Assigned_Agent'].unique(),
            default=df['Assigned_Agent'].unique(),
            key="agent_perf"
        )
    
    with col_filter3:
        temp_filter_agent = st.multiselect(
            "🔥 Lead Temperature",
            options=['Hot', 'Warm', 'Cold'],
            default=['Hot', 'Warm', 'Cold'],
            key="agent_temp"
        )
    
    # Filter data for this tab
    filtered_df_agent = df[
        (df['Timestamp'].dt.date >= date_range_agent[0]) &
        (df['Timestamp'].dt.date <= date_range_agent[1]) &
        (df['Assigned_Agent'].isin(agent_filter_perf)) &
        (df['Lead_Temperature'].isin(temp_filter_agent))
    ]
    
    st.markdown("---")
    
    if len(filtered_df_agent) > 0:
        # Agent performance metrics
        agent_performance = filtered_df_agent.groupby('Assigned_Agent').agg({
            'Lead_ID': 'count',
            'ALPS_Score': 'mean',
            'Response_Time_Min': 'mean',
            'SLA_Met': lambda x: (x.sum() / len(x) * 100),
            'Status': lambda x: (x == 'Closed Won').sum()
        }).round(2)
        
        agent_performance.columns = ['Total_Leads', 'Avg_ALPS_Score', 'Avg_Response_Time', 'SLA_Rate_%', 'Conversions']
        agent_performance['Conversion_Rate_%'] = (agent_performance['Conversions'] / agent_performance['Total_Leads'] * 100).round(1)
        
        st.subheader("Agent Performance Summary")
        st.dataframe(agent_performance, use_container_width=True)
        
        # Performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Leads handled per agent
            fig_leads = px.bar(
                agent_performance.reset_index(),
                x='Assigned_Agent',
                y='Total_Leads',
                title="Total Leads Handled by Agent",
                color='Total_Leads'
            )
            fig_leads.update_xaxes(tickangle=45)
            st.plotly_chart(fig_leads, use_container_width=True)
        
        with col2:
            # Conversion rate per agent
            fig_conversion = px.bar(
                agent_performance.reset_index(),
                x='Assigned_Agent',
                y='Conversion_Rate_%',
                title="Conversion Rate by Agent (%)",
                color='Conversion_Rate_%'
            )
            fig_conversion.update_xaxes(tickangle=45)
            st.plotly_chart(fig_conversion, use_container_width=True)
        
        # Performance scatter plot
        fig_perf = px.scatter(
            agent_performance.reset_index(),
            x='Avg_Response_Time',
            y='Conversion_Rate_%',
            size='Total_Leads',
            color='SLA_Rate_%',
            text='Assigned_Agent',
            title="Agent Performance: Response Time vs Conversion Rate",
            labels={'Avg_Response_Time': 'Average Response Time (min)', 'Conversion_Rate_%': 'Conversion Rate (%)'}
        )
        fig_perf.update_traces(textposition="middle center")
        st.plotly_chart(fig_perf, use_container_width=True)
    else:
        st.info("No data available for the selected filters.")

with tab6:
    st.header("📈 Business Analytics & Insights")
    
    # Filters for this tab
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        date_range_analytics = st.date_input(
            "📅 Date Range",
            value=(df['Timestamp'].min().date(), df['Timestamp'].max().date()),
            min_value=df['Timestamp'].min().date(),
            max_value=df['Timestamp'].max().date(),
            key="analytics_date"
        )
    
    with col_filter2:
        temp_filter_analytics = st.multiselect(
            "🔥 Lead Temperature",
            options=['Hot', 'Warm', 'Cold'],
            default=['Hot', 'Warm', 'Cold'],
            key="analytics_temp"
        )
    
    with col_filter3:
        nat_filter_analytics = st.multiselect(
            "🌍 Nationality",
            options=df['Nationality'].unique(),
            default=df['Nationality'].unique(),
            key="analytics_nat"
        )
    
    # Filter data for this tab
    filtered_df_analytics = df[
        (df['Timestamp'].dt.date >= date_range_analytics[0]) &
        (df['Timestamp'].dt.date <= date_range_analytics[1]) &
        (df['Lead_Temperature'].isin(temp_filter_analytics)) &
        (df['Nationality'].isin(nat_filter_analytics))
    ]
    
    st.markdown("---")
    
    if len(filtered_df_analytics) > 0:
        # Time series analysis
        daily_leads = filtered_df_analytics.groupby(filtered_df_analytics['Timestamp'].dt.date).agg({
            'Lead_ID': 'count',
            'ALPS_Score': 'mean',
            'SLA_Met': lambda x: (x.sum() / len(x) * 100)
        }).reset_index()
        daily_leads.columns = ['Date', 'Lead_Count', 'Avg_ALPS_Score', 'SLA_Rate']
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Daily leads trend
            fig_daily = px.line(
                daily_leads,
                x='Date',
                y='Lead_Count',
                title="Daily Lead Volume Trend"
            )
            st.plotly_chart(fig_daily, use_container_width=True)
        
        with col2:
            # ALPS score trend
            fig_alps_trend = px.line(
                daily_leads,
                x='Date',
                y='Avg_ALPS_Score',
                title="Average ALPS Score Trend"
            )
            st.plotly_chart(fig_alps_trend, use_container_width=True)
    else:
        st.info("No data available for the selected filters.")
    
    # Business insights
    st.subheader("🔍 Key Business Insights")
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        st.markdown("""
        **🎯 Lead Quality Insights:**
        - Non-Malaysian leads score 23% higher on average
        - Leads moving in within 14 days have 65% higher conversion
        - Budget range RM 900+ shows 40% better close rates
        """)
        
        st.markdown("""
        **⚡ Routing Optimization:**
        - Hot leads to top sales agents: 89% routing accuracy
        - SLA compliance improved by 34% with smart routing
        - Fair distribution maintains team motivation
        """)
    
    with insights_col2:
        st.markdown("""
        **📊 Performance Metrics:**
        - Average lead score increased by 18% this month
        - Response time improved by 45% with ALPS
        - Conversion rate up 28% with smart routing
        """)
        
        st.markdown("""
        **🔮 Recommendations:**
        - Increase targeting of non-Malaysian prospects
        - Focus on urgent timeline leads for quick wins
        - Optimize agent training for warm lead conversion
        """)
    
    # Correlation analysis
    st.subheader("📊 Criteria Correlation Analysis")
    
    if len(filtered_df_analytics) > 0:
        # Create correlation matrix
        numeric_cols = ['ALPS_Score', 'Days_To_Move', 'Response_Time_Min']
        correlation_data = filtered_df_analytics[numeric_cols].corr()
        
        fig_corr = px.imshow(
            correlation_data,
            title="Correlation Matrix: Key Metrics",
            color_continuous_scale="RdBu",
            aspect="auto"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("No data available for correlation analysis.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🏠 BeLive AI Operating System | ALPS Dashboard v1.0</p>
    <p>Real-time lead prioritization and smart routing analytics</p>
</div>
""", unsafe_allow_html=True)
