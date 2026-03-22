import pandas as pd
import boto3
from sqlalchemy import create_engine
import os

# 🔑 ENV VARIABLES
S3_BUCKET = os.getenv("S3_BUCKET")
S3_KEY = os.getenv("S3_KEY")

RDS_ENDPOINT = os.getenv("RDS_ENDPOINT")
RDS_USER = os.getenv("RDS_USER")
RDS_PASS = os.getenv("RDS_PASS")
RDS_DB = os.getenv("RDS_DB")
TABLE_NAME = os.getenv("TABLE_NAME")

GLUE_DB = os.getenv("GLUE_DB")
GLUE_TABLE = os.getenv("GLUE_TABLE")

# 📥 Read CSV from S3
def read_s3():
    print("📥 Reading file from S3...")
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
    df = pd.read_csv(obj['Body'])
    print(f"✅ File read successfully: {len(df)} rows, {len(df.columns)} columns")
    return df

# 📤 Upload Data to RDS
def upload_rds(df):
    try:
        print("📤 Uploading data to RDS...")
        engine = create_engine(
            f"mysql+pymysql://{RDS_USER}:{RDS_PASS}@{RDS_ENDPOINT}/{RDS_DB}"
        )
        df.to_sql(TABLE_NAME, con=engine, if_exists='replace', index=False)
        print("✅ Data uploaded to RDS successfully")
        return True
    except Exception as e:
        print("❌ RDS upload failed:", e)
        return False

# 🔧 Map pandas dtype to Glue type
def map_dtype(dtype):
    if "int" in str(dtype):
        return "int"
    elif "float" in str(dtype):
        return "double"
    else:
        return "string"

# ⚠️ Fallback to Glue with dynamic schema
def fallback_glue(df):
    print("⚠️ Falling back to Glue with dynamic schema...")
    glue = boto3.client('glue')

    columns = [{'Name': col, 'Type': map_dtype(dtype)} for col, dtype in zip(df.columns, df.dtypes)]

    try:
        glue.create_table(
            DatabaseName=GLUE_DB,
            TableInput={
                'Name': GLUE_TABLE,
                'StorageDescriptor': {
                    'Columns': columns,
                    'Location': f"s3://{S3_BUCKET}/{S3_KEY}",
                    'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
                    'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
                    'SerdeInfo': {
                        'SerializationLibrary': 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe',
                        'Parameters': {'field.delim': ','}
                    }
                },
                'TableType': 'EXTERNAL_TABLE'
            }
        )
        print("✅ Glue table created successfully with dynamic schema")
    except Exception as e:
        print("❌ Glue table creation failed:", e)

# 🚀 Main execution
def main():
    df = read_s3()
    success = upload_rds(df)
    if not success:
        fallback_glue(df)

if __name__ == "__main__":
    main()