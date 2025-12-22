# Heart Disease Dataset Dictionary

This document provides a detailed explanation of the columns and data values in the `heart.csv` dataset. This dataset is commonly used for predicting the likelihood of a heart attack.

## Overview

- **Rows**: 1025 (in your dataset)
- **Columns**: 14
- **Target Variable**: `output`

## Column Descriptions

### 1. age
- **Description**: The age of the patient in years.
- **Type**: Numerical

### 2. sex
- **Description**: The gender of the patient.
- **Type**: Categorical
- **Values**:
  - `1`: Male
  - `0`: Female

### 3. cp (Chest Pain Type)
- **Description**: The type of chest pain experienced by the patient.
- **Type**: Categorical
- **Values**:
  - `0`: **Typical Angina**: Chest pain related to the heart.
  - `1`: **Atypical Angina**: Chest pain not related to the heart.
  - `2`: **Non-Anginal Pain**: Typically esophageal spasms (non heart related).
  - `3`: **Asymptomatic**: Chest pain not showing signs of disease.

### 4. trtbps (Resting Blood Pressure)
- **Description**: Resting blood pressure (in mm Hg) on admission to the hospital.
- **Type**: Numerical
- **Note**: A value of 130-140 is typically cause for concern.

### 5. chol (Cholesterol)
- **Description**: Serum cholesterol in mg/dl.
- **Type**: Numerical
- **Note**: Above 200 is cause for concern.

### 6. fbs (Fasting Blood Sugar)
- **Description**: Fasting blood sugar > 120 mg/dl.
- **Type**: Categorical (Binary)
- **Values**:
  - `1`: True (Fasting blood sugar > 120 mg/dl)
  - `0`: False (Fasting blood sugar <= 120 mg/dl)

### 7. restecg (Resting Electrocardiographic Results)
- **Description**: Resting electrocardiogram results.
- **Type**: Categorical
- **Values**:
  - `0`: **Normal**: Normal ECG.
  - `1`: **ST-T Wave Abnormality**: having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV).
  - `2`: **Left Ventricular Hypertrophy**: showing probable or definite left ventricular hypertrophy by Estes' criteria.

### 8. thalachh (Maximum Heart Rate)
- **Description**: Maximum heart rate achieved.
- **Type**: Numerical

### 9. exng (Exercise Induced Angina)
- **Description**: Exercise-induced angina.
- **Type**: Categorical
- **Values**:
  - `1`: Yes
  - `0`: No

### 10. oldpeak
- **Description**: ST depression induced by exercise relative to rest.
- **Type**: Numerical
- **Note**: Determines the stress level of the heart.

### 11. slp (Slope)
- **Description**: The slope of the peak exercise ST segment.
- **Type**: Categorical
- **Values**:
  - `0`: **Downsloping**: Signs of unhealthy heart.
  - `1`: **Flat**: Signs of unhealthy heart.
  - `2`: **Upsloping**: Signs of healthy heart (during exercise).

### 12. caa (Number of Major Vessels)
- **Description**: Number of major vessels (0-3) colored by fluoroscopy.
- **Type**: Numerical / Ordinal
- **Values**: `0`, `1`, `2`, `3`

### 13. thall (Thalassemia)
- **Description**: A blood disorder called thalassemia.
- **Type**: Categorical
- **Values**:
  - `0`: **Null** (Dropped from dataset usually, or missing).
  - `1`: **Fixed Defect**: No blood flow in some part of the heart.
  - `2`: **Normal**: Normal blood flow.
  - `3`: **Reversible Defect**: A blood flow is observed but it is not normal.

### 14. output (Target)
- **Description**: Diagnosis of heart disease.
- **Type**: Categorical (Binary)
- **Values**:
  - `1`: **High Chance of Heart Attack** (Disease present)
  - `0`: **Less Chance of Heart Attack** (No disease)