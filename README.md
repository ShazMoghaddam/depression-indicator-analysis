# 🧠 Adult Depression Indicator Analysis

## 📘 Project Overview
This project analyses an adult depression dataset sourced from **DATA.GOV** to explore mental health indicators and build simple predictive models.  
As part of my data science learning journey, I applied end-to-end techniques including data cleaning, exploratory data analysis (EDA), preprocessing, modelling, evaluation, and visualisation.  
The goal was to understand the dataset, extract meaningful insights, and build baseline predictive models suitable for a GitHub portfolio project.

---

## 📊 Data Source
The dataset used in this analysis comes from:
**DATA.GOV – Adult Depression: LGHC Indicator 24**

This dataset contains:
- Weighted frequencies  
- Percent estimates  
- 95% confidence limits  
- Demographic strata  
- Time categories  
- Other indicator metadata  

I used this dataset to construct a binary depression indicator for predictive modelling.

---

## 🛠️ Methodology

### **1. Data Cleaning & Preprocessing**
- Checked for missing values  
- Imputed missing numeric values with *median*  
- Imputed categorical values with *most frequently occurring value*  
- Scaled numeric features for modelling  
- One-hot encoded categorical variables  
- Split the dataset using **stratified train/test split**

### **2. Exploratory Data Analysis (EDA)**
I explored:
- Distributions of all numeric features  
- Frequency plots of categorical variables  
- Correlation heatmap  
- Trend patterns across time and demographic strata  

Created **publication-ready plots** for GitHub using Seaborn & Matplotlib:
- Histograms  
- Bar charts  
- Correlation heatmap  
- ROC curves  
- Confusion matrices  

### **3. Target Creation**
A binary target variable **HighDepression** was created:
- Value = **1** if `Percent > median(Percent)`
- Value = **0** otherwise

This allowed classification modelling.

### **4. Modelling**
Two baseline classification models were built:

#### **Logistic Regression**
- Robust linear classifier  
- Good for interpretability  
- Performed well with this structured dataset  

#### **Decision Tree (max_depth=4)**
- Easy to interpret visually  
- Helps identify feature splits  
- Visualised using Matplotlib’s `plot_tree()`  

### **5. Evaluation Metrics**
For each model:
- Accuracy  
- Precision  
- Recall  
- F1-score  
- ROC-AUC  
- Confusion Matrix  
- ROC Curve  

Models were wrapped in **Scikit-Learn Pipelines**, ensuring:
- No data leakage  
- Clean and reproducible workflow  

---

## 🔍 Key Findings

### **📌 Insights from EDA**
- Depression estimates vary across demographic strata and time categories.  
- Some numeric variables show moderate correlation with each other, but categorical features carry important signal when encoded.

### **📌 Model Insights**
- Logistic Regression produced stable, consistent predictive performance.  
- Decision Tree helped reveal meaningful thresholds and splits in the data.  
- Logistic Regression achieved slightly higher ROC-AUC, while Decision Tree offered interpretability.

### **📌 What This Means**
Even simple baseline models can capture patterns in the dataset and highlight influential features.  
This project demonstrates the full workflow of a data science analysis—from cleaning to modelling to insights.

---

## 📂 Project Structure

👤 Author

Shaz
📍 Based in London
🎓 Imperial College London Data Science Bootcamp Graduate
💼 Aspiring Data Scientist & Python Developer
🌱 Passionate about learning, analysing data, and building useful tools
