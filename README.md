

# Data Pipeline: Postgres & API → BigQuery

## 📌 Overview
This project implements an **incremental data pipeline** using Google Cloud services:
- Extracts data from a Postgres database (Cloud SQL).
- Extracts data from a public REST API.
- Loads both into **BigQuery raw datasets**.
- Transforms them into a **staging table** for analytics.
- Automated with **Cloud Run Jobs** + **Cloud Scheduler**.

---

## ⚙️ Tech Stack
- **Python 3.10**
- **SQLAlchemy + Pandas**
- **Google Cloud BigQuery Client**
- **Docker + Cloud Run**
- **Cloud SQL (Postgres)**
- **Cloud Scheduler**

---

## 🏗️ Architecture
![architecture](docs/architecture.png)

1. Extract users from Postgres → `raw_data.users`.
2. Extract posts from API → `raw_data.posts`.
3. Transform and join data → `staging_data.user_posts`.
4. Cloud Scheduler triggers the Cloud Run Job on a schedule.

---

## 🚀 Running Locally

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/data-pipeline.git
cd data-pipeline
pip install -r requirements.txt
````

Set the required environment variables:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=<path-to-service-account-key>
export GCP_PROJECT_ID=<your-gcp-project-id>

export PG_HOST=<postgres-host>
export PG_PORT=<postgres-port>
export PG_DB=<postgres-database>
export PG_USER=<postgres-username>
export PG_PASSWORD=<postgres-password>
```

Run the pipeline:

```bash
python main.py
```

---

## ☁️ Deployment on GCP

### 1. Build and push Docker image

```bash
docker build -t us-central1-docker.pkg.dev/<PROJECT_ID>/<REPO_NAME>/data-pipeline:latest .
docker push us-central1-docker.pkg.dev/<PROJECT_ID>/<REPO_NAME>/data-pipeline:latest
```

### 2. Deploy as Cloud Run Job

```bash
gcloud run jobs create data-pipeline-job \
  --image=us-central1-docker.pkg.dev/<PROJECT_ID>/<REPO_NAME>/data-pipeline:latest \
  --region=us-central1 \
  --set-cloudsql-instances <PROJECT_ID>:us-central1:<INSTANCE_NAME> \
  --set-env-vars GCP_PROJECT_ID=<PROJECT_ID>,PG_HOST=/cloudsql/<PROJECT_ID>:us-central1:<INSTANCE_NAME>,PG_PORT=5432,PG_DB=<DB_NAME>,PG_USER=<DB_USER>,PG_PASSWORD=<DB_PASSWORD>
```

### 3. Schedule Job with Cloud Scheduler

In the GCP Console:

* Navigate to **Cloud Run → Jobs → Triggers**.
* Add a **Scheduler trigger** (e.g., daily at midnight).

---

## 📊 BigQuery Outputs

* **raw\_data.users** → Extracted from Postgres
* **raw\_data.posts** → Extracted from API
* **staging\_data.user\_posts** → Joined dataset

(Screenshots are available in the `docs/` folder)

---

## ✅ Notes

* The pipeline supports **incremental ingestion** (only fetches new records based on timestamp/ID).
* Designed for **scalability and automation** using Cloud Run + Scheduler.
* Configurable via environment variables for portability across environments.
  EOF



تحب أكتبلك كمان سكريبت bash صغير يولّد **docs/architecture.png** (رسم معماري بسيط) باستخدام mermaid؟
```
