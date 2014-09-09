detecting_malicious_app
=======================
•	Collected 38k apps’ detailed data and posts with Facebook Graph API, and extracted 5 features after literature review.
•	Designed the Weighted Multi-Dimensional Relationship Model according to extracted features to calculate the relational score between each pair of apps, and conducted the analysis on three dimensions - apps’ description, company information and post content by computing cosine-similarity and tf-idf score.
•	Generated a relational score matrix as input for Hierarchical Agglomerative Clustering to cluster apps with similarity.
•	Codes are in corresponding folders except output folder. 
•	Output folder contains the data sets we collected, and the results of feature analysis.
