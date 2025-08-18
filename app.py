import streamlit as st
import time
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="BeLive Co-Living Chat",
    page_icon="🏠",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'chat_stage' not in st.session_state:
    st.session_state.chat_stage = 'initial'
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'show_form' not in st.session_state:
    st.session_state.show_form = False

# Enhanced CSS for better WhatsApp-like styling
st.markdown("""
<style>
/* Hide Streamlit default elements */
.stDeployButton {display: none;}
.stDecoration {display: none;}
header {visibility: hidden;}
.main .block-container {
    padding-top: 0rem;
    padding-bottom: 0rem;
    max-width: 100%;
}

/* Chat container styling */
.chat-container {
    background-color: #e5ddd5;
    height: 70vh;
    overflow-y: auto;
    padding: 20px;
    border-radius: 0;
    margin: 0;
}

/* Message styling */
.user-message {
    background-color: #dcf8c6;
    margin: 10px 0;
    padding: 8px 12px;
    border-radius: 7px 7px 7px 7px;
    max-width: 60%;
    margin-left: auto;
    margin-right: 0;
    word-wrap: break-word;
    position: relative;
    float: right;
    clear: both;
}

.bot-message {
    background-color: #ffffff;
    margin: 10px 0;
    padding: 8px 12px;
    border-radius: 7px 7px 7px 7px;
    max-width: 60%;
    margin-left: 0;
    margin-right: auto;
    word-wrap: break-word;
    position: relative;
    float: left;
    clear: both;
}

.timestamp {
    font-size: 11px;
    color: #666;
    text-align: right;
    margin-top: 2px;
}

.bot-timestamp {
    font-size: 11px;
    color: #666;
    text-align: left;
    margin-top: 2px;
}

/* Header styling */
.chat-header {
    background-color: #075e54;
    color: white;
    padding: 15px;
    text-align: center;
    margin: 0;
    position: sticky;
    top: 0;
    z-index: 100;
}

/* Input area styling */
.input-container {
    background-color: #f0f0f0;
    padding: 10px 20px;
    position: sticky;
    bottom: 0;
    z-index: 100;
}

/* Form styling */
.form-container {
    background-color: #ffffff;
    padding: 15px;
    margin: 10px 0;
    border-radius: 7px;
    border: 1px solid #ddd;
}

/* Clear floats */
.clearfix::after {
    content: "";
    display: table;
    clear: both;
}

/* Streamlit form button styling */
.stButton button {
    background-color: #25d366;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 8px 16px;
}

.stButton button:hover {
    background-color: #128c7e;
}
</style>
""", unsafe_allow_html=True)

def get_current_time():
    return datetime.now().strftime("%H:%M")

def add_message(sender, content, is_form=False):
    st.session_state.messages.append({
        'sender': sender,
        'content': content,
        'timestamp': get_current_time(),
        'is_form': is_form
    })

def process_user_input(user_input):
    user_input_lower = user_input.lower().strip()
    
    if st.session_state.chat_stage == 'initial':
        if any(greeting in user_input_lower for greeting in ['hi', 'hello', 'hey']):
            st.session_state.chat_stage = 'greeting_responded'
            return """Hello! Welcome to BeLive Co-Living! 👋

I'm here to help you find your perfect co-living space.

To get started, could you please fill out this quick form so I can better assist you with your housing needs?"""
        else:
            return """Hello! Welcome to BeLive Co-Living! 👋

I'm here to help you find your perfect co-living space. How can I assist you today?"""
    
    elif st.session_state.chat_stage == 'greeting_responded':
        if any(word in user_input_lower for word in ['ok', 'yes', 'sure', 'okay', 'alright']):
            st.session_state.show_form = True
            st.session_state.chat_stage = 'form_stage'
            return "Great! Please fill out the form below:"
        else:
            return "No problem! Feel free to ask me any questions about our co-living spaces, or let me know when you're ready to fill out the form."
    
    elif st.session_state.chat_stage == 'form_completed':
        return handle_post_form_queries(user_input_lower)
    
    else:
        return "I'm here to help! What would you like to know about BeLive Co-Living?"

def handle_post_form_queries(user_input):
    if any(word in user_input for word in ['price', 'cost', 'rent', 'fee']):
        return f"""Based on your preferences, here are our pricing options:

🏠 **Single Room**: RM 800-1200/month
🏠 **Shared Room**: RM 500-800/month  
🏠 **Premium Room**: RM 1200-1800/month

All prices include:
✅ Utilities (water, electricity, internet)
✅ Cleaning service
✅ Maintenance
✅ 24/7 security

Would you like to schedule a viewing?"""
    
    elif any(word in user_input for word in ['location', 'where', 'area']):
        return f"""We have co-living spaces in several prime locations:

📍 **KL City Center** - Walking distance to LRT
📍 **Mont Kiara** - Expat-friendly area
📍 **Bangsar** - Vibrant neighborhood
📍 **Petaling Jaya** - Great connectivity
📍 **Setapak** - Near universities

Which area interests you most?"""
    
    elif any(word in user_input for word in ['viewing', 'visit', 'see', 'tour']):
        return """Perfect! I'd love to arrange a viewing for you.

Our viewing hours:
🕒 Monday - Friday: 10 AM - 7 PM
🕒 Saturday - Sunday: 10 AM - 5 PM

Please let me know your preferred date and time, and I'll confirm the appointment for you!

You can also call us directly at +60 12-345-6789."""
    
    else:
        return """I'm here to help with any questions about:

🏠 Room types and pricing
📍 Locations and amenities
👥 Community and facilities  
📅 Viewing appointments
📋 Application process

What would you like to know more about?"""

def display_inquiry_form():
    with st.form("inquiry_form"):
        st.markdown("### 📋 BeLive Co-Living Inquiry Form")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *")
            phone = st.text_input("Phone Number *")
            email = st.text_input("Email Address *")
        
        with col2:
            move_in_date = st.date_input("Preferred Move-in Date *")
            budget_range = st.selectbox("Budget Range (RM/month) *", 
                                      ["Select budget range", "500-800", "800-1200", "1200-1800", "1800+"])
            duration = st.selectbox("Stay Duration *", 
                                  ["Select duration", "1-3 months", "3-6 months", "6-12 months", "12+ months"])
        
        room_type = st.selectbox("Preferred Room Type *", 
                                ["Select room type", "Single Room", "Shared Room", "Premium Room", "Any"])
        
        location = st.selectbox("Preferred Location *", 
                               ["Select location", "KL City Center", "Mont Kiara", "Bangsar", "Petaling Jaya", "Setapak", "Any"])
        
        additional_info = st.text_area("Additional Requirements/Questions", 
                                     placeholder="Any specific needs or questions you'd like us to know about...")
        
        submitted = st.form_submit_button("Submit Inquiry", use_container_width=True)
        
        if submitted:
            if name and phone and email and budget_range != "Select budget range":
                st.session_state.user_data = {
                    'name': name,
                    'phone': phone,
                    'email': email,
                    'move_in_date': move_in_date,
                    'budget_range': budget_range,
                    'duration': duration,
                    'room_type': room_type,
                    'location': location,
                    'additional_info': additional_info
                }
                
                st.session_state.show_form = False
                st.session_state.chat_stage = 'form_completed'
                
                response = f"""Thank you {name}! ✨

I've received your inquiry with the following details:
• Budget: RM {budget_range}/month
• Room Type: {room_type}
• Location: {location}
• Move-in: {move_in_date}

Our team will review your requirements and get back to you within 24 hours at {email}.

In the meantime, would you like to:
1. Learn more about our pricing
2. Know about our locations
3. Schedule a viewing
4. Ask any specific questions

How can I help you further?"""
                
                add_message('bot', response)
                st.rerun()
            else:
                st.error("Please fill in all required fields marked with *")

# Header
st.markdown('<div class="chat-header"><h2>🏠 BeLive Co-Living</h2><p>Customer Service Chat</p></div>', unsafe_allow_html=True)

# Main chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    if message['sender'] == 'user':
        st.markdown(f"""
        <div class="user-message">
            {message['content']}
            <div class="timestamp">{message['timestamp']}</div>
        </div>
        <div class="clearfix"></div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-message">
            {message['content']}
            <div class="bot-timestamp">{message['timestamp']}</div>
        </div>
        <div class="clearfix"></div>
        """, unsafe_allow_html=True)

# Show form if triggered
if st.session_state.show_form:
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    display_inquiry_form()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input area
st.markdown('<div class="input-container">', unsafe_allow_html=True)

with st.form("chat_input_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input("Type your message...", label_visibility="collapsed", placeholder="Type your message...")
    
    with col2:
        send_button = st.form_submit_button("Send", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Handle user input
if send_button and user_input:
    # Add user message
    add_message('user', user_input)
    
    # Process and add bot response
    bot_response = process_user_input(user_input)
    add_message('bot', bot_response)
    
    # Rerun to show new messages
    st.rerun()

# Initial greeting if no messages
if not st.session_state.messages:
    initial_message = """Welcome to BeLive Co-Living! 🏠

We're excited to help you find your perfect co-living space in Kuala Lumpur.

Type 'Hi' to get started!"""
    add_message('bot', initial_message)
    st.rerun()
