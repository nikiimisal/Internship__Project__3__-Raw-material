🚀 Project 3: Data Ingestion from S3 to RDS with Glue Fallback
📌 Objective

Build a Dockerized Python application to:

Read data from Amazon S3
Insert data into Amazon RDS (MySQL)
Fall back to AWS Glue if RDS is unavailable

# Archecture

```
Normal Flow:
S3 → Python → RDS ✅

Failure Flow:
S3 → Python → ❌ RDS → ✅ Glue
```
>👉 This = real-world fault-tolerant pipeline 🔥


Step 1: Prepare the files  aaplya project laganarya

create a folder for project in that folder create files
such as 
data.csv   # Your app.py is the Python script that handles S3 → RDS → Glue fallback.
app.py 
Dockerfile 
requriment.txt..

link deto mi ithe folders chyaa

> i have created this files in directly in terminal



or 
you can clone my repo in your terminal and edit je edit karyachay 
or 
create a file in locally and  Upload Project Files to EC2
On your local machine, copy project folder to EC2: 



🧱 STEP 1: IAM USER (Permission System)
Create:

Go to → Amazon Web Services → IAM → Users → Create User

Fill:
Name: project-user

Select:
✅ Programmatic access

Attach Permissions:

Select:

AmazonS3FullAccess
AmazonRDSFullAccess
AWSGlueConsoleFullAccess

then go to security crediential tyat --> Access keys then create and 
Save Keys:
AWS_ACCESS_KEY_ID=XXXX
AWS_SECRET_ACCESS_KEY=XXXX

👉 This will be used in Docker


Step 2: Set up Amazon S3
1 Open AWS Console → S3 Service.
2 Create a new bucket (e.g., `my-data-bucket-277`).
3 Upload the `data.csv` file to this bucket.
4 Note the bucket name and object key (`data.csv`) for environment variables.



Step 4: Set up AWS Glue (Fallback)
Open AWS Console → AWS Glue → Data Catalog.
Create a database: fallback_db.
Do not create tables manually; the Python script will create them automatically if RDS fails.


Step 3: Set up Amazon RDS (MySQL)
Open AWS Console → RDS Service → Create database.
Select:
Engine: MySQL
Version: Latest compatible (e.g., MySQL 8.0)
Free tier (for testing)
Configure:
DB Identifier: `my-rds`
Database Name: `mydb`
Master Username: `admin`
Master Password: `password123`
Public access: Enabled (for EC2 connectivity)
Note the RDS endpoint (e.g.,`my-rds.cl8mw8agi9uc.eu-north-1.rds.amazonaws.com`).


Step 3a: Create table in RDS

Connect via Query Editor or MySQL client:

CREATE DATABASE mydb;

USE mydb;

CREATE TABLE mytable (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    city VARCHAR(100)
);

>for that and docker sathi pn launch a instance so we can run some commands on there

Step 5: Launch EC2 Instance
Open AWS Console → EC2 → Launch Instance.
Choose Amazon Linux 2023 (or 2) AMI.
Instance type: t2.micro (free tier).
Configure:
Enable SSH (port 22)
Launch and download the .pem key file.
Connect to EC2:
ssh -i "your-key.pem" ec2-user@your-ec2-ip



Step 6: Install Docker on EC2
sudo yum update -y
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

Reconnect SSH so the user is added to the Docker group.



Step 10: Build Docker Image
docker build -t s3-rds-glue-app .
This creates a Docker image with your Python script and dependencies.


Step 11: Run Docker Container
docker run --env-file .env s3-rds-glue-app
Expected Behavior:
Reads CSV from S3
Uploads to RDS:
If RDS is available → data inserted
If RDS fails → fallback to Glue (creates table dynamically)


Step 12: Verification
Check RDS
Go to RDS Query Editor → run:
SELECT * FROM mytable;
Check Glue
Go to Glue → Tables → my_glue_table
Columns will reflect your CSV headers (dynamic schema)
Check via Athena (optional)
Database: fallback_db
Query: SELECT * FROM my_glue_table;




Step 13: Docker Logs (Optional)
docker ps           # find running container
docker logs <container_id>
Logs show whether RDS upload succeeded or Glue fallback was triggered.


Step 14: Optional Testing Glue Fallback
To force Glue fallback, temporarily provide wrong RDS password in .env:
RDS_PASS=wrongpassword
Re-run container → Glue table will be created.
Step 15: Clean-up (Optional)
Delete old tables in Glue if you want to re-run.
Stop container: docker stop <container_id>


🔹 Step 10: Test Glue Fallback

To simulate a failure in RDS:

Edit .env to provide a wrong RDS password:
RDS_PASS=wrongpassword
Run container again:
docker run --env-file .env s3-rds-glue-app
Output:
📤 Uploading data to RDS...
❌ RDS upload failed
⚠️ Falling back to Glue...
✅ Glue table created successfully
Verify Glue table:
Go to Glue → Tables → my_glue_table
Columns reflect CSV headers: id, name, age, city

✅ This step confirms the fallback mechanism works.



































