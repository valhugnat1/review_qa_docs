import json
import os
from typing import List, Optional
from datetime import date, datetime
from collections import Counter

import uvicorn
import boto3
from botocore.client import Config
from botocore.exceptions import NoCredentialsError, ClientError
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv # <-- 1. IMPORT THE LIBRARY

# --- Load Environment Variables from .env file ---
load_dotenv() # <-- 2. LOAD THE VARIABLES

# --- Pydantic Models for Data Validation ---

class ReviewPayload(BaseModel):
    user: str
    question: str
    answer: str
    question_rating: int
    answer_rating: int
    comment: Optional[str] = None
    timestamp: str
    category: str

class CategoryStat(BaseModel):
    category: str
    count: int

# --- Scaleway S3 Client Setup ---
class S3Storage:
    def __init__(self):
        try:
            self.bucket_name = os.environ['SCW_BUCKET_NAME']
            self.client = boto3.client(
                's3',
                endpoint_url=f"https://{os.environ['SCW_ENDPOINT_URL']}",
                aws_access_key_id=os.environ['SCW_ACCESS_KEY'],
                aws_secret_access_key=os.environ['SCW_SECRET_KEY'],
                region_name=os.environ['SCW_REGION'],
                config=Config(signature_version='s3v4')
            )
        except KeyError as e:
            raise RuntimeError(f"Environment variable {e} not set. Please create a .env file and fill it out.") from e

    def get_json_object(self, key: str) -> Optional[dict]:
        """Fetches and parses a JSON object from the S3 bucket."""
        try:
            response = self.client.get_object(Bucket=self.bucket_name, Key=key)
            content = response['Body'].read().decode('utf-8')
            return json.loads(content)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                return None
            raise HTTPException(status_code=500, detail=f"S3 ClientError getting object: {e}")
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Failed to decode JSON from {key}")

    def put_json_object(self, key: str, data: dict):
        """Uploads a dictionary as a JSON object to the S3 bucket."""
        try:
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=json.dumps(data, indent=2),
                ContentType='application/json'
            )
        except NoCredentialsError:
            raise HTTPException(status_code=401, detail="S3 credentials not available.")
        except ClientError as e:
            raise HTTPException(status_code=500, detail=f"S3 ClientError putting object: {e}")

    def list_objects(self, prefix: str) -> List[str]:
        """
        Lists object keys in the bucket with a given prefix.
        Handles 'NoSuchKey' error by returning an empty list.
        """
        try:
            response = self.client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            return [item['Key'] for item in response.get('Contents', [])]
        except ClientError as e:
            # If the error is NoSuchKey, it means no objects matched the prefix.
            # Treat this as a valid case and return an empty list.
            if e.response['Error']['Code'] == 'NoSuchKey':
                return []
            # For any other client error, raise it as it might be a real issue.
            raise HTTPException(status_code=500, detail=f"S3 ClientError listing objects: {e}")

# --- FastAPI App Initialization ---

app = FastAPI()
storage = S3Storage()

# --- CORS Middleware ---
origins = ["http://localhost:8080"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Constants ---
REVIEWS_FILE_KEY = "reviews.json"
QA_PREFIX = "qa_"
QA_SUFFIX = ".json"


# --- API Endpoints (No changes needed below this line) ---

@app.get("/api/categories")
async def get_available_categories():
    """
    Returns a list of available question categories based on object keys.
    """
    object_keys = storage.list_objects(prefix=QA_PREFIX)
    categories = [
        key[len(QA_PREFIX):-len(QA_SUFFIX)]
        for key in object_keys
        if key.endswith(QA_SUFFIX)
    ]
    return categories

@app.get("/api/questions")
async def get_questions_by_category(categories: Optional[List[str]] = Query(None)):
    """
    Fetches questions from the qa_{category}.json objects corresponding to the
    provided list of categories.
    """
    if not categories:
        return {"qa_pairs": []}

    all_qa_pairs = []
    for category in categories:
        file_key = f"{QA_PREFIX}{category}{QA_SUFFIX}"
        data = storage.get_json_object(file_key)
        if data:
            for pair in data.get("qa_pairs", []):
                pair["category"] = category
                all_qa_pairs.append(pair)

    return {"qa_pairs": all_qa_pairs}


@app.post("/api/submit-review")
async def submit_review(review: ReviewPayload):
    """
    Receives a new review, including the category, and saves it to object storage.
    """
    reviews_data = storage.get_json_object(REVIEWS_FILE_KEY)
    reviews = reviews_data if isinstance(reviews_data, list) else []

    reviews.append(review.dict())
    storage.put_json_object(REVIEWS_FILE_KEY, reviews)

    return {"message": "Review saved successfully"}


@app.get("/api/reviews", response_model=List[ReviewPayload])
async def get_reviews():
    """
    Reads and returns all reviews for the leaderboard from object storage.
    """
    reviews = storage.get_json_object(REVIEWS_FILE_KEY)
    return reviews if isinstance(reviews, list) else []


@app.get("/api/reviews/category-stats", response_model=List[CategoryStat])
async def get_category_stats():
    """
    Calculates and returns the number of reviews for each category.
    """
    reviews = await get_reviews()
    if not reviews:
        return []

    category_counts = Counter(r['category'] for r in reviews if 'category' in r)
    stats = [{"category": cat, "count": count} for cat, count in category_counts.items()]
    stats.sort(key=lambda x: x['count'], reverse=True)
    return stats


@app.get("/api/reviews/progress")
async def get_user_progress(user: str):
    """

    Calculates and returns the number of reviews submitted by a user for the current day.
    """
    reviews = await get_reviews()
    if not reviews:
        return {"daily_count": 0}

    today = date.today()
    daily_count = 0
    for review_data in reviews:
        if review_data.get("user") == user:
            try:
                review_date = datetime.fromisoformat(review_data["timestamp"].replace("Z", "+00:00")).date()
                if review_date == today:
                    daily_count += 1
            except (ValueError, KeyError):
                continue
    
    return {"daily_count": daily_count}