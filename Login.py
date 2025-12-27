import streamlit as st
import pyrebase

# --------------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------------------------------------
st.set_page_config(
    page_title="Heart Attack App", 
    page_icon=":hearts:", 
    layout="centered"
)

# --------------------------------------------------------------------------------
# 2. OPTIMIZED FIREBASE CONNECTION
# --------------------------------------------------------------------------------
@st.cache_resource
def get_firebase():
    # Load config from Streamlit Secrets (Secure!)
    try:
        firebaseConfig = dict(st.secrets["firebase"])
        # Change 1: Return the whole app, not just auth
        return pyrebase.initialize_app(firebaseConfig)
    except FileNotFoundError:
        st.error("Secrets not found. Please ensure .streamlit/secrets.toml exists.")
        return None

# Initialize the app
firebase = get_firebase()

# Change 2: Extract BOTH Auth and Database tools
if firebase:
    auth = firebase.auth()
    db = firebase.database() # <--- NEW: Get the Database Tool
else:
    auth, db = None, None

# --------------------------------------------------------------------------------
# 3. SESSION STATE MANAGEMENT
# --------------------------------------------------------------------------------
if 'user' not in st.session_state:
    st.session_state.user = None
if 'email' not in st.session_state:
    st.session_state.email = ''

# --------------------------------------------------------------------------------
# 4. CUSTOM CSS STYLING
# --------------------------------------------------------------------------------
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #E3E7EC;
    }
    [data-testid=stSidebar] [data-testid=stImage]{
        text-align: center;
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 100%;
    }
    button[title="View fullscreen"]{
        visibility: hidden;
    }
    .css-15zrgzn {display: none}
    .css-eczf16 {display: none}
    .css-jn99sy {display: none}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------------------------------------
# 5. MAIN APPLICATION LOGIC
# --------------------------------------------------------------------------------
def main():
    
    # --- SCENARIO A: USER IS LOGGED IN ---
    if st.session_state.user:
        import app 

        with st.sidebar:
            st.write(f"Logged in as: **{st.session_state.email}**")
            if st.button("Log out"):
                st.session_state.user = None
                st.session_state.email = ''
                st.rerun() 
        
        # Change 3: Pass the 'db' tool to the app
        app.app_one(st.session_state.email, db)

    # --- SCENARIO B: USER IS NOT LOGGED IN ---
    else:
        with st.sidebar:
            st.image("https://i.imgur.com/aNTPhtD.png")
            
        choice = st.sidebar.selectbox('Login/Signup', ['Login', 'Sign up', 'Reset password'])
        
        # --- INPUT CLEANING (MOBILE FIX) ---
        raw_email = st.sidebar.text_input('Please enter your email address')
        email = raw_email.strip().lower()
        
        password = ""
        if choice != 'Reset password':
            password = st.sidebar.text_input('Please enter your password', type='password')

        # --- LOGIN FORM ---
        if choice == 'Login':
            with st.sidebar.form(key='login_form'):
                submit_login = st.form_submit_button('Login')
                
            if submit_login:
                if not email or not password:
                    st.sidebar.error("Please enter both email and password")
                else:
                    try:
                        user = auth.sign_in_with_email_and_password(email, password)
                        st.session_state.user = user
                        st.session_state.email = email
                        st.success("Logged in successfully!")
                        st.rerun()
                    except Exception as e:
                        st.sidebar.error("Invalid email or password. Try again.")

        # --- SIGN UP FORM ---
        elif choice == 'Sign up':
            with st.sidebar.form(key='signup_form'):
                submit_signup = st.form_submit_button('Create my account')
                
            if submit_signup:
                if not email or not password:
                    st.sidebar.error("Please enter both email and password")
                elif len(password) < 6:
                    st.sidebar.error("Password must be at least 6 characters")
                else:
                    try:
                        user = auth.create_user_with_email_and_password(email, password)
                        st.success('Account created! 🎉')
                        st.balloons()
                        
                        user = auth.sign_in_with_email_and_password(email, password)
                        st.session_state.user = user
                        st.session_state.email = email
                        st.rerun()
                    except Exception as e:
                        error_msg = str(e)
                        if "EMAIL_EXISTS" in error_msg:
                            st.sidebar.error("This email is already registered.")
                        elif "WEAK_PASSWORD" in error_msg:
                            st.sidebar.error("Password must be at least 6 characters.")
                        else:
                            st.sidebar.error("Signup failed. Check email format.")

        # --- RESET PASSWORD FORM ---
        elif choice == 'Reset password':
            with st.sidebar.form(key='reset_form'):
                submit_reset = st.form_submit_button('Send Reset Email')
            
            if submit_reset:
                try:
                    auth.send_password_reset_email(email)
                    st.success('Password reset email has been sent!')
                except Exception as e:
                    st.sidebar.error('Reset failed. Please check the email address.')

if __name__ == '__main__':
    main()
