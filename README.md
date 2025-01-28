# 🚑 Temporal Trends and Survival Determinants in Capnography: A Machine Learning Study  

## 📌 Overview  
This project explores the **predictive potential of End-Tidal Carbon Dioxide (EtCO₂) capnography** in cardiac resuscitation using **machine learning models**. By analyzing **temporal trends in EtCO₂** and patient responses to **epinephrine administration**, the study identifies critical **survival determinants** for **Return of Spontaneous Circulation (ROSC)**.

## 📊 Key Features  
- **🩺 Data-Driven Insights:** Analyzes the relationship between **EtCO₂ trends** and **cardiac resuscitation outcomes**.  
- **📈 Machine Learning Models:** Implements **Random Forest and Logistic Regression** to predict **ROSC**.  
- **⚡ Flask Application:** Provides a streamlined **data processing tool** for healthcare professionals.  
- **🔬 Feature Engineering:** Computes **EtCO₂ slope, peak time, duration, and proportional changes**.  
- **📡 Real-Time Decision Support:** Enables **AI-powered clinical insights** for improved resuscitation strategies.  

---

## 🔬 Methodology  

### 1️⃣ Data Processing  
- Uses **Pragmatic Airway Resuscitation Trial (PART) dataset** with patient demographics and EtCO₂ readings.  
- Cleans and structures data for **ML modeling**.  

### 2️⃣ Feature Engineering  
- Computes **EtCO₂ slope** to evaluate capnography trends.  
- Extracts **epinephrine response metrics** such as **T_lag, T_peak, and T_duration**.  

### 3️⃣ Machine Learning Modeling  
- **Random Forest Classifier:** Achieves **90% accuracy, AUC 0.96**.  
- **Logistic Regression:** Serves as a baseline with **85% accuracy**.  
- **Odds Ratio & Feature Importance Analysis:** Identifies key predictors of **ROSC**.  

### 4️⃣ Flask Application  
- **Live Data Processing Tool:** Converts **medical waveform data** into ML-ready datasets.  
- **Real-time Predictions:** Enables clinicians to assess survival probabilities based on **EtCO₂ trends**.  

---

## 🚀 Live Demo  
You can access the **live Flask application** for data preprocessing here:  
🔗 **[Live Application](https://banupr15.pythonanywhere.com)**  

---

## 📖 Research Publications  
- **[JAMA Network Open](https://your-publication-link.com)** – *Temporal Trends in End-Tidal Capnography and Outcomes in Out-of-Hospital Cardiac Arrest*.  
- **AI for Capnography:** *Artificial Intelligence for End Tidal Capnography Guided Resuscitation: A Conceptual Framework*.  

---

## ⚙️ Installation & Setup  
### 🔹 Prerequisites  
- Python 3.8+  
- Flask  
- Scikit-learn  
- Pandas, NumPy, Matplotlib  
- TensorFlow/PyTorch (for advanced modeling)  
