# Raw Material


# 🚀 Project 3: Data Ingestion from S3 to RDS with Glue Fallback

## 📌 Objective

Develop a Dockerized Python application that automates the process of:

- Reading data from an Amazon S3 bucket  
- Pushing it to an RDS (MySQL-compatible) database  
- Automatically falling back to AWS Glue if the RDS database is unavailable or the push operation fails  

This project helps integrate multiple AWS services (S3, RDS, Glue), work with data pipelines, and use Docker for packaging and deployment.

---

## 🏗️ Architecture

```
Normal Flow:
S3 → Python → RDS ✅

Failure Flow:
S3 → Python → ❌ RDS → ✅ Glue
```

👉 This is a real-world fault-tolerant pipeline 🔥

---

## 📁 Step 1: Prepare Project Files

Create a folder and inside it create:

```
project-folder/
│── data.csv    # Sample dataset
│── app.py      # Python script (S3 → RDS → Glue fallback)
│── Dockerfile
│── requirements.txt
│── .env
```

[click to see file's](https://github.com/nikiimisal/Internship__Project__3__-Raw-material/tree/main) 

You can:
- Create files directly in terminal  
- OR clone a repo and edit  
- OR create locally and upload to EC2  

>I have created this files in directly in terminal


<p align="center">
  <img src="https://github.com/nikiimisal/Internship--Project-s/blob/main/img/proj-3/Screenshot%202026-03-22%20221106.png?raw=true" width="700" alt="Initialize Repository Screenshot">
</p>


---

## 🔐 Step 2: IAM User (Permission System)

Go to → ***AWS** → **IAM** → **Users** → **Create User**

Configuration Fill:
- Name: `project-user`
- Enable: ✅ Programmatic access  

Attach Permissions:
- `AmazonS3FullAccess`  
- `AmazonRDSFullAccess`  
- `AWSGlueConsoleFullAccess`

Go to Security Credentials → Access Keys → Create  

Save:

```
AWS_ACCESS_KEY_ID=XXXX
AWS_SECRET_ACCESS_KEY=XXXX
```

👉 These will be used inside Docker


| **IAM-Role**    | **Access keys**          |
|--------------------------------|------------------------------------|
| ![VS](https://github.com/nikiimisal/Internship--Project-s/blob/main/img/proj-3/Screenshot%202026-03-22%20222054.png?raw=true) | ![AWS](https://github.com/nikiimisal/Internship--Project-s/blob/main/img/proj-3/Screenshot%202026-03-22%20221928.png?raw=true) |



---

## ☁️ Step 3: Set up Amazon S3

1. Open AWS Console → S3  
2. Create bucket (e.g., `my-data-bucket-277`)  
3. Upload `data.csv`  
4. Note the bucket name and object key (`data.csv`) for environment variables.



| **Bucket**    | **Object**          |
|--------------------------------|------------------------------------|
| ![VS](https://github.com/nikiimisal/Internship--Project-s/blob/main/img/proj-3/Screenshot%202026-03-21%20175357.png?raw=true) | ![AWS](https://github.com/nikiimisal/Internship--Project-s/blob/main/img/proj-3/Screenshot%202026-03-21%20175405.png?raw=true) |


  
---

## 🗄️ Step 4: Set up Amazon RDS (MySQL)

Go to AWS Console → RDS → Create database

Select:
- Engine: MySQL  
- Version: 8.0  
- Free tier  

Configure:
- DB Identifier: `my-rds`  
- Database Name: `mydb`  
- Username: `admin`  
- Password: `password123`  
- Public access: Enabled  

Note the endpoint:
```
my-rds.xxxxx.region.rds.amazonaws.com
```

<p align="center">
  <img src="https://github.com/nikiimisal/Internship--Project-s/blob/main/img/proj-3/Screenshot%202026-03-22%20222309.png?raw=true" width="700" alt="Initialize Repository Screenshot">
</p>



---

## 🧾 Step 4a: Create Table in RDS

```SQL
CREATE DATABASE mydb;

USE mydb;

CREATE TABLE mytable (
id INT PRIMARY KEY,
name VARCHAR(100),
age INT,
city VARCHAR(100)
);
```
>For this, we’ll need to launch a server instance — we can do that later.

---

## 🧠 Step 5: Set up AWS Glue (Fallback)

Go to AWS Glue → Data Catalog

- Create database: `fallback_db`  
- Do NOT create tables manually  

👉 Python script will create tables automatically if RDS fails.



<p align="center">
  <img src="https://github.com/nikiimisal/Internship--Project-s/blob/main/img/proj-3/Screenshot%202026-03-22%20115306.png?raw=true" width="700" alt="Initialize Repository Screenshot">
</p>


---

## 💻 Step 6: Launch EC2 Instance

Go to EC2 → Launch Instance

- Amazon Linux 2 / 2023  
- Instance type: `t2.micro `

Enable:
- SSH (port 22)  

Download `.pem` key

Connect:
```Bash
ssh -i "your-key.pem" ec2-user@your-ec2-ip
```


<p align="center">
  <img src="https://github.com/nikiimisal/Internship--Project-s/blob/main/img/proj-3/Screenshot%202026-03-22%20221543.png?raw=true" width="500" alt="Initialize Repository Screenshot">
</p>


---

## 🐳 Step 7: Install Docker

```Bash
sudo yum update -y
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user
```

Reconnect SSH so the user is added to the Docker group.

---

## 🏗️ Step 8: Build Docker Image

```Bash
docker build -t s3-rds-glue-app .
```
This creates a Docker image with your Python script and dependencies.

---

## ▶️ Step 9: Run Docker Container

```Bash
docker run --env-file .env s3-rds-glue-app
```

---

## ⚙️ Expected Behavior

- Reads CSV from S3  
- Uploads to RDS  

### If RDS works:
- Data inserted successfully
- To see inserted data for that see step 10


<p align="center">
  <img src="https://github.com/nikiimisal/Internship--Project-s/blob/main/img/proj-3/Screenshot%202026-03-22%20132428.png?raw=true" width="700" alt="Initialize Repository Screenshot">
</p>

---

### If RDS fails:
- Error occurs  
- Glue fallback triggered  
- Table created in Glue
- For that see  step 11

---

## 🔍 Step 10: Verification

### Check RDS:

```Bash
SELECT * FROM mytable;
```


---


<p align="center">
  <img src="https://github.com/nikiimisal/Internship--Project-s/blob/main/img/proj-3/Screenshot%202026-03-22%20132504.png?raw=true" width="700" alt="Initialize Repository Screenshot">
</p>

---

### Check Glue:

- Go to Glue → Tables → `my_glue_table`  
- Columns match CSV  

### Optional (Athena):

```SQL
SELECT * FROM my_glue_table;
```


---

## 🧪 Step 11: Test Glue Fallback (Optional)

Edit `.env`:

```
RDS_PASS=wrongpassword
```

Run again:

```Bash
docker run --env-file .env s3-rds-glue-app
```

Output:

```
📤 Uploading data to RDS...
❌ RDS upload failed
⚠️ Falling back to Glue...
✅ Glue table created successfully
```



---


<p align="center">
  <img src="https://github.com/nikiimisal/Internship--Project-s/blob/main/img/proj-3/Screenshot%202026-03-22%20132531.png?raw=true" width="700" alt="Initialize Repository Screenshot">
</p>


---
Verify Glue table:

Go to Glue → Tables → my_glue_table

Columns reflect CSV headers: id, name, age, city

✅ This step confirms the fallback mechanism works.


---

<p align="center">
  <img src="https://github.com/nikiimisal/Internship--Project-s/blob/main/img/proj-3/Screenshot%202026-03-22%20121556.png?raw=true" width="700" alt="Initialize Repository Screenshot">
</p>

---

## 📜 Step 12: Docker Logs

```Bash
docker ps                      # find running container
docker logs <container_id>
```
Logs will show:

- RDS success OR
- Glue fallback triggered

---



## 🧹 Step 13: Cleanup

```
docker stop <container_id>
```

---




# 📄 Summary Report: Data Ingestion Pipeline (S3 → RDS → Glue Fallback)

## 1. Repository
Python script and Dockerfile are stored in GitHub:  
[Click here](https://github.com/nikiimisal/Internship__Project__3__-Raw-material)

## 2. Data Flow
Fault-tolerant pipeline: reads CSV from **S3**, inserts into **RDS MySQL**, falls back to **AWS Glue** if RDS fails.

- **Normal Flow:** S3 → Python → RDS ✅  
- **Failure Flow:** S3 → Python → ❌ RDS → AWS Glue ✅  

**Implementation:** pandas parses CSV, SQLAlchemy + PyMySQL inserts into RDS, boto3 triggers Glue fallback.

---

## 3. AWS Services Used
- **S3:** Stores raw CSV files  
- **RDS (MySQL):** Main database  
- **Glue:** Fallback table creation  
- **IAM:** Permissions & credentials  
- **EC2:** Hosts Docker container

---

## 4. Docker Setup
- **Base Image:** Python 3.9  
- **Dependencies:** boto3, pandas, sqlalchemy, pymysql  
- **Execution:** Script runs automatically on container start  
- **Env Variables:** `.env` file contains AWS credentials, S3 & RDS info  

**Commands:**
```
docker build -t s3-rds-glue-app .
docker run --env-file .env s3-rds-glue-app
```

---

## 5. Challenges & Solutions
| Challenge                     | Solution |
|--------------------------------|---------|
| RDS connection failure         | Fallback to Glue using try-except |
| Dependency management          | Docker + requirements.txt ensures consistency |
| AWS permissions                | IAM user with proper access (S3, RDS, Glue) |
| Testing fallback               | Intentionally wrong RDS password to trigger Glue |

---

## ✅ Conclusion
This project implements a **scalable, fault-tolerant data pipeline** using **AWS services and Docker**, ensuring reliable data ingestion and automatic fallback handling.

---
---

