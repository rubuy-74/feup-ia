# Multi-Class Prediction of Obesity Risk - IART

This project implements a machine learning pipeline to analyze and predict obesity levels based on a dataset. It explores various machine learning models, feature engineering techniques, and evaluation metrics to provide insights into obesity classification.

## Table of Contents
- [Overview](#overview)
- [Dataset](#dataset)
- [Pipeline](#pipeline)
- [Models](#models)
- [Evaluation](#evaluation)
- [Results](#results)
- [How to Run](#how-to-run)
- [Dependencies](#dependencies)


## Overview
The goal of this project is to classify individuals into one of seven obesity categories using a dataset of health and lifestyle features. The project includes:
- Data preprocessing and feature engineering.
- Implementation of multiple machine learning models.
- Evaluation of models using metrics, visualizations, and comparisons.
- Insights into feature importance and model performance.


## Summary of the Notebook

The notebook provides a comprehensive guide to building a machine learning pipeline for classifying obesity levels. Below are the main points covered:

1. **Objective**:
   - To classify individuals into one of seven obesity categories using health and lifestyle data.

2. **Data Preprocessing**:
   - Loading and cleaning the dataset.
   - Encoding categorical variables and scaling numerical features.

3. **Feature Engineering**:
   - Calculating BMI and identifying key numerical and categorical features.

4. **Model Training**:
   - Implementing and training various machine learning models, including Decision Trees, KNN, SVM, Neural Networks, and Ensemble Methods.

5. **Evaluation**:
   - Comparing models using metrics like accuracy, precision, recall, and F1-score.
   - Visualizing results with confusion matrices, ROC curves, and learning curves.

6. **Key Insights**:
   - Neural Networks achieved the best accuracy (~87.93%) and generalization.
   - Feature selection significantly improved KNN performance but had minimal impact on Decision Trees.
   - Models faced challenges with overlapping classes like "Normal_Weight" and "Overweight_Level_I."

This summary highlights the structured approach and key findings of the notebook, making it easier for users to understand its purpose and outcomes.


## Dataset
The dataset contains both numerical and categorical features related to health and lifestyle, such as:
- **Numerical Features**: Age, Height, Weight, BMI, etc.
- **Categorical Features**: Gender, family history of overweight, eating habits, etc.
- **Target Variable**: `NObeyesdad` (7 obesity categories).


## Pipeline
The project follows a structured pipeline:
1. **Data Preprocessing**:
   - Loading datasets.
   - Handling missing values and duplicates.
   - Encoding categorical variables.
2. **Feature Engineering**:
   - Calculating BMI.
   - Identifying numerical and categorical columns.
3. **Data Splitting and Scaling**:
   - Splitting data into training and testing sets.
   - Scaling features for better model performance.
4. **Model Training**:
   - Training multiple machine learning models with and without feature selection.
5. **Evaluation**:
   - Comparing models using metrics like accuracy, precision, recall, and F1-score.
   - Visualizing results with confusion matrices, ROC curves, and learning curves.
   - Validation curves and feature usage are analyzed to assess overfitting and feature importance.


## Models
The following models are implemented:
1. **Decision Trees**:
   - With and without feature selection.
2. **K-Nearest Neighbors (KNN)**:
   - Hyperparameter tuning to find the optimal number of neighbors.
3. **Support Vector Machines (SVM)**:
   - Linear kernel with and without feature selection.
4. **Neural Networks**:
   - Multi-layer perceptron for classification.
5. **Ensemble Methods**:
   - Voting classifier combining multiple models.


## Evaluation
The models are evaluated using:
- **Metrics**:
  - Accuracy, Precision, Recall, F1-Score, and Execution Time.
- **Visualizations**:
  - Confusion Matrices, ROC Curves, Learning Curves, and Validation Curves.
- **Feature Importance**:
  - Analysis of features used by each model.


## Results
- **Best Model**: Neural Network achieved the highest accuracy (~87.93%) and generalization.
- **Feature Selection**: Improved KNN performance significantly but had minimal impact on Decision Trees.
- **Class-Specific Challenges**: Models struggled with overlapping classes like "Normal_Weight" and "Overweight_Level_I."
- **Execution Time**: Decision Tree (No FS) was the fastest, while Neural Networks balanced accuracy and time.


## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/feup-ia-2.git
   cd feup-ia-2
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the notebook:
   ```bash
   jupyter notebook main.ipynb
   ```

## Dependencies
- Python 3.8+
- Libraries:
  - `pandas`, `numpy`, `matplotlib`, `seaborn`
  - `scikit-learn`
  - `jupyter`


## Acknowledgments
This project was developed as part of the **Intelligent Artificial Systems** course at FEUP. Special thanks to the course instructors for their guidance.