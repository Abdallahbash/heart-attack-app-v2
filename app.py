import streamlit as st
import numpy as np
import requests
import pickle
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit_option_menu import option_menu 
from streamlit_lottie import st_lottie   

# --------------------------------------------------------------------------------
# 1. CACHED FUNCTIONS
# --------------------------------------------------------------------------------

@st.cache_resource
def load_model():
    # Make sure this path is exactly where your file is located
    return pickle.load(open("Model_datasets/final_model.pickle", "rb"))

@st.cache_data
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# --------------------------------------------------------------------------------
# 2. HELPER FUNCTIONS
# --------------------------------------------------------------------------------

def send_email_report(user_email, result_text):
    try:
        # Load credentials from st.secrets
        gmail_user = st.secrets["email"]["gmail_user"] 
        gmail_password = st.secrets["email"]["gmail_password"]

        msg = MIMEMultipart()
        msg['From'] = f"Heart Attack App <{gmail_user}>"
        msg['To'] = user_email
        msg['Subject'] = "❤️ Your Heart Attack Risk Prediction Result"

        body = f"""
        Hello,

        Thank you for using the Heart Attack Prediction App!

        Your prediction result:
        {result_text}

        DISCLAIMER: This is an AI-powered tool for informational purposes only. 
        It is not a substitute for professional medical advice.

        Stay healthy!
        
        —
        Heart Attack Prediction App
        """
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email Error: {e}")
        return False

# --------------------------------------------------------------------------------
# 3. MAIN APP FUNCTION
# --------------------------------------------------------------------------------

# CHANGE 1: Accept the 'db' variable here
def app_one(email=None, db=None):
    
    loaded_model = load_model()
    anim_heart = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_zw7jo1.json")
    anim_coding = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_ggxx4yii.json")

    # --- MENU CONFIGURATION ---
    menu_styles = {
        "container": {"padding": "5!important", "background-color": "#E3E7EC"},
        "icon": {"color": "black", "font-size": "16px"}, 
        "nav-link": {"font-size": "17px", "text-align": "left", "margin":"0px", "font-family": "Calibri"},
        "nav-link-selected": {"background-color": "#FF4B4B"},
    }
    
    selected = option_menu(None, ["App", "Insight", "Contact"], 
        icons=['activity', "bi bi-info-circle", 'envelope'], 
        menu_icon="cast", default_index=0, orientation="horizontal", styles=menu_styles)

    # ==========================
    # SECTION: PREDICTION APP
    # ==========================
    if selected == 'App':
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("<h1 style='font-family: Cooper Black; color: #FF4B4B;'>Heart Attack Risk</h1>", unsafe_allow_html=True)
            st.caption("Please fill out the medical form below. Hover over the question marks (?) for simple explanations.")
        with col2:
            if anim_heart:
                st_lottie(anim_heart, height=130, key="heart_anim")

        st.write("---")

        # --- FORM INPUTS ---
        
        # Section 1: Basic Vitals
        st.subheader("1. Patient Vitals")
        c1, c2 = st.columns(2)
        
        with c1:
            age = st.slider("Age", 18, 120, 50)
            sex = st.radio("Gender", ('Male', 'Female'))
            
            trestbps = st.slider(
                'Resting Blood Pressure (mm Hg)', 
                80, 200, 120,
                help="Normal BP is around 120/80. High BP is a risk factor."
            )
            
            chol = st.slider(
                'Cholesterol (mg/dl)', 
                100, 600, 200,
                help="Total cholesterol level. Higher levels can indicate blocked arteries."
            )
            
            fbs_choice = st.radio(
                "Fasting Blood Sugar > 120 mg/dl?", 
                ['No (Normal)', 'Yes (High)'],
                help="Is your blood sugar high after fasting? This is a sign of diabetes risk."
            )

        with c2:
            thalach = st.slider(
                'Max Heart Rate Achieved', 
                60, 220, 150,
                help="The highest heart rate you reached during the stress test."
            )
            
            exang_choice = st.radio(
                'Exercise Induced Angina?', 
                ["No", "Yes"],
                help="Do you feel chest pain when you exercise?"
            )

        # Section 2: Clinical Metrics
        st.write("---")
        st.subheader("2. Clinical Test Results")
        st.caption("These values usually come from a doctor's report or ECG test.")
        
        c3, c4 = st.columns(2)
        
        with c3:
            cp_choice = st.selectbox(
                'Chest Pain Type', 
                (
                    "Typical Angina (Pressure/Squeeze)", 
                    "Atypical Angina (Sharp/Stabbing)", 
                    "Non-anginal Pain (Not Heart Related)", 
                    "Asymptomatic (No Pain)"
                ),
                help="Typical: Squeezing sensation during stress. Atypical: Sharp pain. Non-anginal: Muscular/Digestive."
            )
            
            restecg_choice = st.selectbox(
                'Resting ECG Results', 
                (
                    "Normal", 
                    "ST-T Wave Abnormality (Irregular)", 
                    "Left Ventricular Hypertrophy (Thickened Heart)"
                ),
                help="Results from the electrocardiogram while at rest."
            )

            oldpeak = st.number_input(
                'Oldpeak (ST Depression)', 
                0.0, 10.0, 0.0,
                help="A technical reading from the ECG indicating how much the heart is stressed during exercise."
            )

        with c4:
            slope_choice = st.selectbox(
                'Heart Rate Slope (During Exercise)', 
                (
                    "Upsloping (Healthy/Normal)", 
                    "Flatsloping (Minimal Change)", 
                    "Downsloping (Unhealthy Sign)"
                ),
                help="How your heart rate recovers or changes during peak exercise."
            )
            
            ca_choice = st.selectbox(
                'Number of Major Vessels (0-3)', 
                ("0", "1", "2", "3"),
                help="Number of major blood vessels seen clearly on the Fluoroscopy scan. Fewer visible vessels can mean blockages."
            )
            
            thal_choice = st.selectbox(
                'Thallium Stress Result', 
                (
                    "Normal", 
                    "Fixed Defect (Past Heart Issue)", 
                    "Reversible Defect (Current Issue)"
                ),
                help="Result of the Thallium stress test. 'Fixed' means permanent damage (scar), 'Reversible' means reduced blood flow."
            )

        # --- MAPPING INPUTS ---
        
        sex_map = {"Male": 1, "Female": 0}
        fbs_map = {'No (Normal)': 0, 'Yes (High)': 1}
        exang_map = {"No": 0, "Yes": 1}
        
        cp_map = {
            "Typical Angina (Pressure/Squeeze)": 0, 
            "Atypical Angina (Sharp/Stabbing)": 1, 
            "Non-anginal Pain (Not Heart Related)": 2, 
            "Asymptomatic (No Pain)": 3
        }
        
        restecg_map = {
            "Normal": 0, 
            "ST-T Wave Abnormality (Irregular)": 1, 
            "Left Ventricular Hypertrophy (Thickened Heart)": 2
        }
        
        slope_map = {
            "Upsloping (Healthy/Normal)": 0, 
            "Flatsloping (Minimal Change)": 1, 
            "Downsloping (Unhealthy Sign)": 2
        }
        
        thal_map = {
            "Normal": 2, 
            "Fixed Defect (Past Heart Issue)": 1, 
            "Reversible Defect (Current Issue)": 3
        }

        # --- PREDICTION BUTTON ---
        st.write("---")
        center_c1, center_c2, center_c3 = st.columns([1,2,1])
        with center_c2:
            predict_btn = st.button("Analyze Risk", type="primary", use_container_width=True)

        if predict_btn:
            try:
                user_input = [
                    age, sex_map[sex], cp_map[cp_choice], trestbps, chol,
                    fbs_map[fbs_choice], restecg_map[restecg_choice], thalach,
                    exang_map[exang_choice], oldpeak, slope_map[slope_choice],
                    int(ca_choice), thal_map[thal_choice]
                ]

                input_reshaped = np.asarray(user_input).reshape(1, -1)
                prediction = loaded_model.predict(input_reshaped)

                if prediction[0] == 0:
                    st.success("✅ **Result:** Low probability of heart attack.")
                    st.balloons()
                    result_msg = "Congratulation! The probability of having a heart attack is low."
                    
                    with st.expander("See Prevention Tips", expanded=True):
                         # I replaced the GIF with text in case the GIF link breaks in future
                        st.markdown("""
                        * **Stop smoking:** Even 1-2 cigarettes a day increases risk.
                        * **Eat Healthy:** More fruits and vegetables.
                        * **Move More:** Physical activity is key.
                        """)
                else:
                    st.error("⚠️ **Warning:** High probability of heart attack detected.")
                    result_msg = "Warning! High chance of heart attack detected. Please consult a doctor immediately."
                    st.markdown("### 🚨 Please consult a doctor immediately.")

                # --- CHANGE 2: SAVE TO FIREBASE DATABASE ---
                if db:
                    # Construct the record
                    patient_record = {
                        "Age": age,
                        "Sex": sex,
                        "BloodPressure": trestbps,
                        "Cholesterol": chol,
                        "HeartRate": thalach,
                        "Prediction": "Low Risk" if prediction[0] == 0 else "High Risk",
                        "Doctor_Email": email,
                        "Timestamp": str(np.datetime64('now'))
                    }
                    # Save it to the 'Patients_Analysis' folder in Database
                    db.child("Patients_Analysis").push(patient_record)
                    st.toast("Patient Data Saved to Database! 💾")
                # ---------------------------------------------

                if email:
                    with st.spinner("Sending report to your email..."):
                        sent = send_email_report(email, result_msg)
                        if sent:
                            st.toast("Email sent successfully!", icon="📧")
                        else:
                            st.error("Could not send email.")
            
            except Exception as e:
                st.error(f"An error occurred: {e}")

        # --- MEDICAL GLOSSARY (FIXED) ---
        with st.expander("📚 Medical Glossary"):
            st.write("Reference definitions for the medical terms used above:")
            st.markdown("""
            * **Angina:** Chest pain caused by reduced blood flow to the heart.
            * **Oldpeak (ST Depression):** A technical finding on an ECG trace indicating heart stress during exercise.
            * **Thallium Test:** A scan that shows how well blood flows into your heart muscle.
            * **Major Vessels:** The main blood vessels supplying the heart. Seeing fewer on a scan may indicate blockages.
            """)

    # ==========================
    # SECTION: INSIGHTS
    # ==========================
    if selected == 'Insight':
        st.title("Heart Health Insights")
        try:
            st.image("Media/info1.jpg")
            st.write("---")
            st.video("https://www.youtube.com/watch?v=p6RJvWMgy5w")
        except:
            st.info("Visual content not found. Please ensure Media folder is correct.")

    # ==========================
    # SECTION: CONTACT
    # ==========================
    if selected == 'Contact':
        col1, col2 = st.columns(2)
        with col1:
            st.header("Contact Us")
            
            contact_form = f"""
            <form action="https://formsubmit.co/{st.secrets.get('email', {}).get('contact_email', 'abdallahbashabsha45@gmail.com')}" method="POST">
                <input type="hidden" name="_captcha" value="false">
                <input type="text" name="name" placeholder="Your name" required style="width: 100%; margin-bottom: 10px; padding: 8px;">
                <input type="email" name="email" placeholder="Your email" required style="width: 100%; margin-bottom: 10px; padding: 8px;">
                <textarea name="message" placeholder="Your message" style="width: 100%; margin-bottom: 10px; padding: 8px;"></textarea>
                <button type="submit" style="background-color: #FF4B4B; color: white; border: none; padding: 10px 20px; cursor: pointer;">Send Message</button>
            </form>
            """
            st.markdown(contact_form, unsafe_allow_html=True)
