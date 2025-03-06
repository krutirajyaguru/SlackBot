# SlackBot

The Slack Bot project aims to develop a Python-based bot that integrates with the popular messaging platform Slack and utilizes Reddit's API to enhance collaboration and information sharing within a Slack workspace. The bot will provide various functionalities such as fetching Reddit posts, sharing them in Slack channels, and enabling users to interact with Reddit content directly from Slack.
# Dockerized Data Pipeline for Reddit Sentiment Analysis

## Overview
This project implements a **Dockerized Data Pipeline** that collects Reddit posts, analyzes their sentiment, and publishes the most positive or negative posts to Slack every 10 minutes. The pipeline leverages **MongoDB**, **PostgreSQL**, and **Docker Compose** to efficiently process and store data.

![Pipeline Structure](../../_images/structure_reddit.svg)

## Features
- **Data Collection**: Scrapes Reddit posts and stores them in **MongoDB**.
- **ETL Pipeline**: Extracts, transforms, and loads (ETL) data from **MongoDB** to **PostgreSQL**.
- **Sentiment Analysis**: Uses NLP techniques to analyze sentiment.
- **Slack Bot Integration**: Publishes top positive/negative posts to Slack.
- **Dockerized Deployment**: Runs all services in isolated containers using **Docker Compose**.

---

## Tech Stack
- **Docker & Docker Compose** - Containerized deployment
- **Python** - ETL scripting and sentiment analysis
- **MongoDB** - Initial data storage (NoSQL)
- **PostgreSQL** - Processed data storage (SQL)
- **Slack API** - Bot integration for message publishing

---

## Project Structure
```
📂 dockerized-reddit-pipeline
│── 📁 src                  # Source code for ETL, sentiment analysis, and bot
│   │── etl.py              # Extract-Transform-Load (ETL) process
│   │── sentiment_analysis.py  # NLP-based sentiment analysis
│   │── slack_bot.py        # Slack bot integration
│── 📁 config               # Configuration files (API keys, database connections)
│── 📁 docker               # Docker-related files
│   │── Dockerfile          # Docker configuration for services
│   │── docker-compose.yml  # Orchestrate multiple containers
│── 📁 db                   # Database initialization scripts
│── README.md               # Project documentation
│── requirements.txt        # Python dependencies
```

---

## Installation & Setup
### Prerequisites
Ensure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Python (for local testing)

### Steps to Run the Project
1. **Clone the Repository**
   ```sh
   git clone https://github.com/your-username/dockerized-reddit-pipeline.git
   cd dockerized-reddit-pipeline
   ```

2. **Set Up Environment Variables**
   Create a `.env` file in the `config/` folder with the following:
   ```env
   REDDIT_API_KEY=your_reddit_api_key
   REDDIT_SECRET=your_reddit_api_secret
   SLACK_WEBHOOK_URL=your_slack_webhook
   ```

3. **Build and Start Containers**
   ```sh
   docker-compose up --build
   ```

4. **Check Running Containers**
   ```sh
   docker ps
   ```

5. **Monitor Logs**
   ```sh
   docker-compose logs -f
   ```

---

## Pipeline Breakdown
### 1. **Data Collection**
- Fetches posts from Reddit using the Reddit API.
- Stores raw data in **MongoDB**.

### 2. **ETL (Extract-Transform-Load)**
- Extracts data from **MongoDB**.
- Cleans, processes, and applies **sentiment analysis**.
- Loads transformed data into **PostgreSQL**.

### 3. **Slack Bot**
- Fetches the most positive/negative post.
- Publishes it to a **Slack channel** every 10 minutes.

---

## Challenges & Learning Outcomes
- **Installing and configuring Docker & Docker Compose**.
- **Building a scalable data pipeline with ETL processes**.
- **Working with NoSQL (MongoDB) and SQL (PostgreSQL) databases**.
- **Implementing sentiment analysis with NLP techniques**.
- **Integrating Slack API for automated messaging**.

---

## Contributing
Want to improve this project? Contributions are welcome!
1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Open a pull request.

---

## License
This project is licensed under the MIT License.

---
