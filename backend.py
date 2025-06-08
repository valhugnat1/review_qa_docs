import json
import os
from typing import List, Optional, Dict

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date, datetime
from collections import Counter

# --- Pydantic Models for Data Validation ---

class ReviewPayload(BaseModel):
    user: str
    question: str
    answer: str
    question_rating: int
    answer_rating: int
    comment: Optional[str] = None
    timestamp: str
    # NEW: Added category to the review payload
    category: str

# NEW: Pydantic model for category statistics
class CategoryStat(BaseModel):
    category: str
    count: int


# --- FastAPI App Initialization ---
app = FastAPI()

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
DATA_DIR = "data"
REVIEWS_FILE = os.path.join(DATA_DIR, "reviews.json")
QA_PREFIX = "qa_"
QA_SUFFIX = ".json"


# --- Helper Function ---
def get_categories_from_files():
    """Scans the data directory for qa_{category}.json files."""
    categories = []
    if not os.path.exists(DATA_DIR):
        return []
    for filename in os.listdir(DATA_DIR):
        if filename.startswith(QA_PREFIX) and filename.endswith(QA_SUFFIX):
            # Extracts 'category' from 'qa_category.json'
            category = filename[len(QA_PREFIX):-len(QA_SUFFIX)]
            categories.append(category)
    return categories

# --- API Endpoints ---

@app.get("/api/categories")
async def get_available_categories():
    """
    Returns a list of available question categories based on filenames.
    """
    return get_categories_from_files()


@app.get("/api/questions")
async def get_questions_by_category(categories: Optional[List[str]] = Query(None)):
    """
    Fetches questions from the qa_{category}.json files corresponding to the
    provided list of categories.
    """
    all_qa_pairs = []
    if not categories:
        return {"qa_pairs": []}

    for category in categories:
        file_path = os.path.join(DATA_DIR, f"{QA_PREFIX}{category}{QA_SUFFIX}")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    data = json.load(f)
                    # Add the category to each question pair for frontend reference
                    for pair in data.get("qa_pairs", []):
                        pair["category"] = category
                        all_qa_pairs.append(pair)
                except json.JSONDecodeError:
                    # Ignore malformed JSON files
                    continue
    return {"qa_pairs": all_qa_pairs}


@app.post("/api/submit-review")
async def submit_review(review: ReviewPayload):
    """
    Receives a new review, including the category, and saves it.
    """
    reviews = []
    
    # Ensure the data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(REVIEWS_FILE):
        with open(REVIEWS_FILE, "r") as f:
            try:
                reviews = json.load(f)
            except json.JSONDecodeError:
                pass

    reviews.append(review.dict())

    try:
        with open(REVIEWS_FILE, "w") as f:
            json.dump(reviews, f, indent=2)
    except IOError as e:
        raise HTTPException(status_code=500, detail="Error saving the review.")

    return {"message": "Review saved successfully"}


@app.get("/api/reviews", response_model=List[ReviewPayload])
async def get_reviews():
    """
    Reads and returns all reviews for the leaderboard.
    """
    if not os.path.exists(REVIEWS_FILE):
        return []
    
    with open(REVIEWS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# --- NEW ENDPOINT ---
@app.get("/api/reviews/category-stats", response_model=List[CategoryStat])
async def get_category_stats():
    """
    Calculates and returns the number of reviews for each category.
    """
    reviews = await get_reviews()  # Reuse the existing function
    if not reviews:
        return []
    
    # Count occurrences of each category
    category_counts = Counter(review['category'] for review in reviews if 'category' in review)
    
    # Format the data for the response
    stats = [{"category": cat, "count": count} for cat, count in category_counts.items()]
    
    # Sort by count descending
    stats.sort(key=lambda x: x['count'], reverse=True)
    
    return stats


@app.get("/api/reviews/progress")
async def get_user_progress(user: str):
    """
    Calculates and returns the number of reviews submitted by a user for the current day.
    """
    if not os.path.exists(REVIEWS_FILE):
        return {"daily_count": 0}

    reviews = []
    with open(REVIEWS_FILE, "r") as f:
        try:
            reviews = json.load(f)
        except json.JSONDecodeError:
            return {"daily_count": 0}

    today = date.today()
    daily_count = 0
    for review in reviews:
        if review.get("user") == user:
            try:
                review_date = datetime.fromisoformat(review["timestamp"].replace("Z", "+00:00")).date()
                if review_date == today:
                    daily_count += 1
            except (ValueError, KeyError):
                continue
                
    return {"daily_count": daily_count}


if __name__ == "__main__":
    # Create a dummy data directory and a couple of qa files for testing
    print("Creating dummy data for testing...")
    os.makedirs(DATA_DIR, exist_ok=True)
    python_qa = {
        "qa_pairs": [
            {"question": "What is a decorator in Python?", "answer": "A decorator is a design pattern in Python that allows a user to add new functionality to an existing object without modifying its structure."},
            {"question": "Explain GIL in Python.", "answer": "The Global Interpreter Lock (GIL) is a mutex that protects access to Python objects, preventing multiple native threads from executing Python bytecodes at once."}
        ]
    }
    sql_qa = {
        "qa_pairs": [
            {"question": "What is the difference between `DELETE` and `TRUNCATE` in SQL?", "answer": "`DELETE` is a DML command that removes rows one by one and records an entry in the transaction log for each deleted row. `TRUNCATE` is a DDL command that deallocates the data pages and records only the page deallocations in the transaction log."},
            {"question": "What are SQL indexes?", "answer": "Indexes are special lookup tables that the database search engine can use to speed up data retrieval."}
        ]
    }
    with open(os.path.join(DATA_DIR, "qa_python.json"), "w") as f:
        json.dump(python_qa, f, indent=2)
    with open(os.path.join(DATA_DIR, "qa_sql.json"), "w") as f:
        json.dump(sql_qa, f, indent=2)
    print("Dummy files `qa_python.json` and `qa_sql.json` created.")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)