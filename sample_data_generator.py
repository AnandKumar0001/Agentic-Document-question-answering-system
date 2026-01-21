"""Sample data generator for testing the document QA system."""
import json
from pathlib import Path
from datetime import datetime

# Sample documents
SAMPLE_DOCUMENTS = [
    {
        "name": "machine_learning_guide.txt",
        "content": """Machine Learning: A Comprehensive Guide

1. Introduction
Machine Learning (ML) is a subset of artificial intelligence that focuses on developing algorithms and statistical models that enable computer systems to learn and improve from experience without being explicitly programmed. The field has evolved significantly over the past decades, providing solutions to complex problems across various domains.

2. Types of Machine Learning

2.1 Supervised Learning
Supervised learning involves training models using labeled data, where each input has a corresponding correct output. Common algorithms include:
- Linear Regression: Used for predicting continuous values
- Logistic Regression: Used for binary classification
- Decision Trees: Tree-based classification method
- Support Vector Machines (SVM): Effective for high-dimensional data
- Neural Networks: Deep learning approach

2.2 Unsupervised Learning
Unsupervised learning works with unlabeled data to discover patterns:
- Clustering: K-means, Hierarchical Clustering
- Dimensionality Reduction: PCA, t-SNE
- Association Rules: Market basket analysis

2.3 Reinforcement Learning
Agents learn by interacting with environments and receiving rewards/penalties.

3. Key Metrics for Evaluation
- Accuracy: Correct predictions / Total predictions
- Precision: True positives / (True positives + False positives)
- Recall: True positives / (True positives + False negatives)
- F1-Score: Harmonic mean of precision and recall
- AUC-ROC: Area under the receiver operating characteristic curve

4. Best Practices
- Always split data into training, validation, and test sets
- Perform feature scaling and normalization
- Handle missing values appropriately
- Avoid overfitting through regularization
- Use cross-validation for robust evaluation
"""
    },
    {
        "name": "data_science_fundamentals.txt",
        "content": """Data Science Fundamentals

1. What is Data Science?
Data Science is an interdisciplinary field that combines statistics, computer science, and domain expertise to extract meaningful insights from data. It involves collecting, processing, analyzing, and visualizing data to support decision-making.

2. The Data Science Process

2.1 Problem Definition
Clearly define the business problem and establish measurable objectives. Understand stakeholder requirements and project constraints.

2.2 Data Collection
Gather relevant data from various sources including databases, APIs, sensors, and user interactions. Ensure data quality and completeness.

2.3 Data Exploration (EDA)
Exploratory Data Analysis involves:
- Understanding data structure and types
- Identifying missing values and outliers
- Calculating summary statistics
- Creating visualizations for pattern discovery

2.4 Data Preprocessing
- Handle missing values (imputation or removal)
- Remove duplicates
- Encode categorical variables
- Handle outliers
- Feature scaling and normalization

2.5 Feature Engineering
Create new features from existing data to improve model performance. Techniques include:
- Polynomial features
- Interaction terms
- Binning
- Encoding techniques

2.6 Model Selection and Training
Choose appropriate algorithms and train models using the preprocessed data.

2.7 Model Evaluation
Assess model performance using appropriate metrics and validation techniques.

2.8 Deployment and Monitoring
Deploy the model to production and continuously monitor its performance.

3. Tools and Technologies
Popular data science tools include Python, R, SQL, Pandas, NumPy, Scikit-learn, TensorFlow, and Spark.

4. Career Path
Data Science professionals typically have backgrounds in statistics, mathematics, computer science, or related fields. Continuous learning is essential due to the rapid evolution of the field.
"""
    },
    {
        "name": "deep_learning_overview.txt",
        "content": """Deep Learning: An Overview

1. Introduction
Deep Learning is a subset of machine learning that uses artificial neural networks with multiple layers to progressively extract higher-level features from raw input. It has revolutionized fields like computer vision, natural language processing, and speech recognition.

2. Neural Network Basics

2.1 Neurons and Layers
- Input Layer: Receives raw data
- Hidden Layers: Process information through learned transformations
- Output Layer: Produces predictions
- Weights: Parameters that are learned during training
- Activation Functions: ReLU, Sigmoid, Tanh

2.2 Backpropagation
The algorithm used to train neural networks by computing gradients of the loss function with respect to weights and updating them accordingly.

3. Popular Deep Learning Architectures

3.1 Convolutional Neural Networks (CNN)
Specialized for image processing:
- Convolutional layers: Extract spatial features
- Pooling layers: Reduce dimensionality
- Fully connected layers: Classification

3.2 Recurrent Neural Networks (RNN)
Suitable for sequential data:
- Vanilla RNN: Basic sequential processing
- LSTM (Long Short-Term Memory): Handles long-term dependencies
- GRU (Gated Recurrent Unit): Simplified version of LSTM

3.3 Transformer Architecture
State-of-the-art for NLP:
- Self-attention mechanisms
- Parallel processing capabilities
- Applications: BERT, GPT, T5

3.4 Generative Models
- Autoencoders: Dimensionality reduction and reconstruction
- Generative Adversarial Networks (GANs): Create new data
- Variational Autoencoders (VAE): Probabilistic models

4. Training Deep Learning Models
- Large amounts of data required
- GPU acceleration is essential
- Hyperparameter tuning: Learning rate, batch size, epochs
- Regularization techniques: Dropout, L1/L2, Batch Normalization
- Optimization algorithms: SGD, Adam, RMSprop

5. Applications
- Computer Vision: Object detection, image segmentation, face recognition
- Natural Language Processing: Machine translation, text generation, sentiment analysis
- Speech Recognition: Voice assistants, transcription
- Recommendation Systems: Personalized suggestions
- Autonomous Vehicles: Perception and control

6. Challenges and Considerations
- Computational cost and resource requirements
- Need for large labeled datasets
- Model interpretability (black box problem)
- Overfitting on small datasets
- Ethical considerations and bias
"""
    }
]

# Sample test cases for evaluation
SAMPLE_TEST_CASES = [
    {
        "id": 1,
        "query": "What are the main types of machine learning?",
        "ground_truth_answer": "The main types of machine learning are supervised learning (using labeled data), unsupervised learning (finding patterns in unlabeled data), and reinforcement learning (learning through interaction with an environment).",
        "ground_truth_contexts": ["supervised learning", "unsupervised learning", "reinforcement learning"]
    },
    {
        "id": 2,
        "query": "What is the difference between precision and recall in machine learning?",
        "ground_truth_answer": "Precision is the ratio of true positives to all predicted positives (TP/(TP+FP)), while recall is the ratio of true positives to all actual positives (TP/(TP+FN)). Precision measures accuracy of positive predictions, while recall measures coverage of actual positives.",
        "ground_truth_contexts": ["precision", "recall", "true positives", "false positives", "false negatives"]
    },
    {
        "id": 3,
        "query": "What are the steps in the data science process?",
        "ground_truth_answer": "The data science process includes: 1) Problem Definition, 2) Data Collection, 3) Exploratory Data Analysis, 4) Data Preprocessing, 5) Feature Engineering, 6) Model Selection and Training, 7) Model Evaluation, and 8) Deployment and Monitoring.",
        "ground_truth_contexts": ["problem definition", "data collection", "EDA", "preprocessing", "feature engineering", "model training", "evaluation", "deployment"]
    },
    {
        "id": 4,
        "query": "What are LSTM and GRU networks used for?",
        "ground_truth_answer": "LSTM (Long Short-Term Memory) and GRU (Gated Recurrent Unit) are types of recurrent neural networks designed to handle sequential data and overcome the vanishing gradient problem. They are particularly effective at capturing long-term dependencies in sequences.",
        "ground_truth_contexts": ["LSTM", "GRU", "RNN", "sequential data", "long-term dependencies"]
    },
    {
        "id": 5,
        "query": "What is the purpose of dropout in deep learning?",
        "ground_truth_answer": "Dropout is a regularization technique used during training where random neurons are 'dropped out' (set to zero) with a certain probability. This prevents co-adaptation of neurons and helps reduce overfitting by forcing the network to learn more robust features.",
        "ground_truth_contexts": ["dropout", "regularization", "overfitting", "neurons"]
    }
]


def create_sample_files():
    """Create sample document files for testing."""
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)

    for doc in SAMPLE_DOCUMENTS:
        file_path = data_dir / doc["name"]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(doc["content"])
        print(f"Created: {file_path}")

    # Also create a JSON file with test cases
    test_cases_file = data_dir / "test_cases.json"
    with open(test_cases_file, 'w', encoding='utf-8') as f:
        json.dump(SAMPLE_TEST_CASES, f, indent=2)
    print(f"Created: {test_cases_file}")


if __name__ == "__main__":
    create_sample_files()
    print(f"\nSample files created at {Path(__file__).parent / 'data'}")
    print(f"Total documents: {len(SAMPLE_DOCUMENTS)}")
    print(f"Total test cases: {len(SAMPLE_TEST_CASES)}")
