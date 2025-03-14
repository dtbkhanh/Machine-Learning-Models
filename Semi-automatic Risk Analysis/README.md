# Credit decision-making with Machine Learning models

Traditional techniques for credit decision-making require lots of time and implicit knowledge from experts.  To enhance the predictive power of risk analysis, I have introduced Machine Learning models using the concept of Preference Learning alongside traditional methods. I developed a web application to address the current challenges in Credit Risk Analytics, particularly for Small and Medium-Sized Enterprises.
- This application collects and studies the preferences of credit analysts based on given financial features, allowing it to generate ranking results for thousands of companies quickly. A web application is built to facilitate user interaction.
- Each time, a pair of companies are shown along with their information (company names, revenues, etc.), and users are asked to choose which one is better. The user interactions on the UI are then captured and stored inside the database.
- After collecting data from users, I proceed with analyzing the data and building Machine Learning models.
- The application is written in Python 3, using Python frameworks of Dash and Flask.

With the integration of Machine Learning, risk experts can use this application as a convenient tool for rapid cross-reference checking. It can produce ranking results in just a matter of seconds, significantly reducing the workload involved in data processing and speeding up decision-making processes.

## Result summary:
- In general, I have successfully built SVM and kNN models with an average accuracy of 78%.
- The models are highly adaptable. The machine can learn and train on any information we input. The data features can be changed, added, or removed. The training and learning part of the model is fixed.
- Although both models can achieve the same average accuracy, SVM is a better and more reliable choice than kNN. This is because kNN's results depend on the training set, and each different set requires a different chosen k-value to reach the best accuracy score. Additionally, as the dataset grows, kNN requires more memory and results in slower predictions since it is a lazy learner and needs to load the entire training dataset each time.
- I'm unable to increase the accuracy further due to the following reasons:
  - Lack of training data: With only 4 users taking the test, we have limited viewpoints and many data points are duplicated.
  - Invisible factors: User voting may be influenced by prior knowledge of the companies, as many cases and companies are already known to them. This bias affects the voting results.

For future perspectives, we could develop comprehensive Machine Learning algorithms based on this work, to increase the performance and optimize the model. Also, the non-linearity properties of training data need to be deeply analyzed.

---
## 📁 Folder Structure

1. **App UI**:  This is our main application. The application is built using Python frameworks of Dash and Flask.

2. **App Screenshots**: The screenshots of our main application. 
 
3. **Data Preparation**:
  - Creating_company_pairs.sql: for cleansing and modifying Financial Dataset, then creating all possible company pairs for voting, each pairs will have a unique ID.
  - pairs_grouping.py: after creating company pairs, group them into different group of n number of pairs, each group will have a unique ID. For each voting session a group of n pairs will be given to users to vote. After one voting session is finished, the next group will be given to users in the next session. 

4. **Empirical Study with Real-World Data**: After collecting data from users, we start analyzing and building Machine Learning models.
The two files "Data Analytics_02.ipynb" and "Risk Models - Machine Learning.ipynb" can be opened using Jupyter Notebook.
