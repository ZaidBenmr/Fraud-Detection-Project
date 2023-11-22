<div align="center">
  <div id="user-content-toc">
    <ul>
      <summary><h1 style="display: inline-block;"> Electricity Fraud Detection - Intership at Veolia Gmbh (Amendis)</h1></summary>
      <summary><h2 style="display: inline-block;"> Data Science and Analysis Project</h2></summary> 
    </ul>
  </div>
  
  <p>Gain insights from electricity consumption data to detect fraudulent activities by users and design a Business Intelligence user interface to visualize the results.</p>
    🛸
    🌪️
    🛸
</div>
<br>
<div align="center">
      <img src="https://img.shields.io/github/stars/hamagistral/DataEngineers-Glassdoor?color=blue&style=social"/>
</div>

## 📝 Table of Contents

1. [ Project Overview ](#introduction)
2. [ Project Architecture ](#arch)
3. [ Contact ](#contact)
<hr>

### 🔬 Analysis Page
![1](https://github.com/BENAMAR-Zaid/Fraud-Detection-Project/assets/105943885/9f050d5c-81aa-4c91-bcee-97830fd30804)
![2](https://github.com/BENAMAR-Zaid/Fraud-Detection-Project/assets/105943885/76cf820f-669e-4171-ad13-a5c4a4f08431)
![3](https://github.com/BENAMAR-Zaid/Fraud-Detection-Project/assets/105943885/663aeb3e-f051-42cb-9665-bf8caeeaaaff)
![4](https://github.com/BENAMAR-Zaid/Fraud-Detection-Project/assets/105943885/cfae5b81-5f23-463c-89cb-23fb276920aa)

### 🔬 Fraud detection results pages
![5](https://github.com/BENAMAR-Zaid/Fraud-Detection-Project/assets/105943885/b83d1bbd-a697-45c6-bad8-0dbd3603c984)
![6](https://github.com/BENAMAR-Zaid/Fraud-Detection-Project/assets/105943885/701d1c1a-2f0e-4940-9634-e6d807365a14)
![7](https://github.com/BENAMAR-Zaid/Fraud-Detection-Project/assets/105943885/42c12094-3fc9-4334-8ccb-c7432d1b2137)
![8](https://github.com/BENAMAR-Zaid/Fraud-Detection-Project/assets/105943885/a9888f71-2411-4b29-a968-142dc90f5b2d)



<a name="introduction"></a>
## 🔬 Project Overview :

### 🎯 Goal :

The main objective of project is to develop a machine learning model for detecting fraudulent activities in the electricity sector and creating a results visualization platform. This platform includes both a business intelligence component and a page for downloading analysis results.

### 🧭 Steps :

In this project, I started with the data preprocessing phase and then proceeded to develop the algorithm using various techniques such as random forests, logistic regression, support vector machines, KNN, Naïve Bayes, and DNN. I conducted tests and comparisons among these models to select the one that offered the best results in terms of accuracy, precision, and other performance criteria before deploying it on an API using FastAPI.

In our way to develope and build this project, i've passed with the following steps : 
#### 1- Data cleaning and preprocessing to remove irrelevant information and ensure consistency, including dropping duplicates, handling missing values, eliminating outliers, and performing one-hot encoding.
#### 2- Exploratory data analysis (EDA) is performed on the cleaned data to gain insights into trends and patterns. This includes identifying the most common fraudulent sectors, understanding the behavior of consumption data from fraudulent users, and recognizing the most common patterns among them. EDA also involves creating visualizations to aid in understanding the data.
#### 3- After EDA, feature engineering is performed to represent customer load profiles. Instead of directly feeding the load profile with numerous lines to the model, it is necessary to extract the most relevant features and represent them in a single vector. This simplifies the data and makes it more comprehensible to the model.
#### 4- After training various models such as random forests, logistic regression, support vector machines, KNN, Naïve Bayes, and DNN. I conducted tests and comparisons among these models to select the one that offered the best results in terms of accuracy, precision, and other performance criteria before deploying it on a web application using FastAPI.
#### 5- In the FastAPI web application, I created an ML pipeline that will be utilized by an API function. When this function is called, it automatically triggers analysis to detect fraudulent activity.
#### 6- Development of an Angular 17 UI to visualize the results of fraud detection analyses, either in the form of BI graphs, or as a table. On the other, analysis results can be downloaded as Excel files.

<a name="arch"></a>
## 📝 Project Architecture

![Project_Arch](https://github.com/BENAMAR-Zaid/Fraud-Detection-Project/assets/105943885/889f2643-6849-419c-bce9-9239ae22f8e9)

### 🛠️ Technologies Used

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Jupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=for-the-badge&logo=Jupyter)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-FDEE21?style=flat-square&logo=apachespark&logoColor=black)
![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Angular](https://img.shields.io/badge/angular-%23DD0031.svg?style=for-the-badge&logo=angular&logoColor=white)

<a name="installation"></a>
## 🖥️ Installation : 
Clone the repository:

```
git clone https://github.com/BENAMAR-Zaid/Fraud-Detection-Project.git
```

### - Run FastAPI

1. Change directory to FastAPI:

```
cd Back-end
```

2. Launch project : 

```
python -m uvicorn main:app --reload
```

### - Run Angular 17 Dashboard : 

1. Change directory to Angular:

```
cd Angular-Dashboard
```

2. Run the app:

```
ng serve
```


<a name="contact"></a>
## 📨 Contact Me

[LinkedIn](https://www.linkedin.com/in/zaid-benamar/) •
[Gmail](zaid.benmr@gmail.com)
