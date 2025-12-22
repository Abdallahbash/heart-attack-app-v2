import streamlit as st
import pyrebase

# --------------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------------------------------------
# This MUST be the very first Streamlit command.
# It sets the browser tab title and favicon.
st.set_page_config(
    page_title="Heart Attack App", 
    page_icon=":hearts:", 
    layout="centered"
)

# --------------------------------------------------------------------------------
# 2. OPTIMIZED FIREBASE CONNECTION (The Speed Boost)
# --------------------------------------------------------------------------------
# @st.cache_resource tells Streamlit to run this function ONCE and cache the result.
# This prevents reconnecting to Firebase on every single user interaction.
# In login.py

@st.cache_resource
def get_firebase_auth():
    # Load config from Streamlit Secrets (Secure!)
    # This reads the keys you pasted into the Dashboard earlier.
    firebaseConfig = dict(st.secrets["firebase"])
    
    # Initialize the app only once
    firebase = pyrebase.initialize_app(firebaseConfig)
    return firebase.auth()

# Initialize auth using the cached function
auth = get_firebase_auth()

# --------------------------------------------------------------------------------
# 3. SESSION STATE MANAGEMENT
# --------------------------------------------------------------------------------
# This ensures the user stays logged in even if the page refreshes.
if 'user' not in st.session_state:
    st.session_state.user = None # Holds the user object if logged in
if 'email' not in st.session_state:
    st.session_state.email = ''  # Holds the user's email

# --------------------------------------------------------------------------------
# 4. CUSTOM CSS STYLING
# --------------------------------------------------------------------------------
# Consolidated all styling into one block for cleaner code and faster rendering.
st.markdown("""
<style>
    /* Change sidebar background color */
    [data-testid=stSidebar] {
        background-color: #E3E7EC;
    }
    /* Center the image in the sidebar */
    [data-testid=stSidebar] [data-testid=stImage]{
        text-align: center;
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 100%;
    }
    /* Hide the "View Fullscreen" button on images */
    button[title="View fullscreen"]{
        visibility: hidden;
    }
    /* Hide anchor links (the little chain icons next to headers) */
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
        # Import app here ("Lazy Import") so the login screen loads fast, 
        # even if app.py has heavy imports like TensorFlow or Pandas.
        import app 

        # Sidebar: Show user info and Logout button
        with st.sidebar:
            st.write(f"Logged in as: **{st.session_state.email}**")
            if st.button("Log out"):
                # Clear session state
                st.session_state.user = None
                st.session_state.email = ''
                # Rerun to show the login screen immediately
                st.rerun() 
        
        # Run the actual heart attack prediction app
        app.app_one(st.session_state.email)

    # --- SCENARIO B: USER IS NOT LOGGED IN ---
    else:
        # 1. Sidebar Image
        with st.sidebar:
            st.image("https://i.imgur.com/aNTPhtD.png")
            
        # 2. Navigation Menu (Login / Signup / Reset)
        choice = st.sidebar.selectbox('Login/Signup', ['Login', 'Sign up', 'Reset password'])
        
        # 3. Form Inputs (Email is needed for all 3 options)
        email = st.sidebar.text_input('Please enter your email address')
        
        # Password is needed for Login and Signup, but not Reset
        password = ""
        if choice != 'Reset password':
            password = st.sidebar.text_input('Please enter your password', type='password')

        # --- LOGIN FORM ---
        if choice == 'Login':
            # st.form creates a container that doesn't reload until "Submit" is pressed
            with st.sidebar.form(key='login_form'):
                submit_login = st.form_submit_button('Login')
                
            if submit_login:
                if not email or not password:
                    st.sidebar.error("Please enter both email and password")
                else:
                    try:
                        # Attempt to sign in with Firebase
                        user = auth.sign_in_with_email_and_password(email, password)
                        
                        # If successful, save to session state
                        st.session_state.user = user
                        st.session_state.email = email
                        
                        st.success("Logged in successfully!")
                        st.rerun() # Force reload to enter the app
                    except Exception as e:
                        # Generic error message for security
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
                        # Create the user in Firebase
                        user = auth.create_user_with_email_and_password(email, password)
                        st.success('Account created! 🎉')
                        st.balloons()
                        
                        # Auto-login the user immediately after signup
                        user = auth.sign_in_with_email_and_password(email, password)
                        st.session_state.user = user
                        st.session_state.email = email
                        st.rerun()
                    except Exception as e:
                        # Handle specific Firebase errors
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
