import json
import os
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import date, datetime

# --- Updated Pydantic Model for Data Validation ---
# We now match the detailed structure from the Vue app
class Review(BaseModel):
    user: str
    original_question: Optional[str] = None
    edited_question: str = Field(..., alias='question') # The 'alias' is not strictly needed if the frontend sends 'edited_question', but this shows how you can map fields. Let's stick to a simpler model matching the frontend exactly.

# Let's redefine the model to be simpler and match the final frontend code.
class ReviewPayload(BaseModel):
    user: str
    question: str # The final, potentially edited question
    answer: str # The final, potentially edited answer
    question_rating: int
    answer_rating: int
    comment: Optional[str] = None
    timestamp: str

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

REVIEWS_FILE = "data/reviews.json"

# --- API Endpoints ---

@app.post("/api/submit-review")
async def submit_review(review: ReviewPayload): # Use the new model
    """
    Receives a new review, reads existing reviews, appends, and saves.
    """
    reviews = []
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


@app.get("/api/reviews", response_model=List[ReviewPayload]) # Use the new model
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
        # Check if the review belongs to the user and was created today
        if review.get("user") == user:
            try:
                # Timestamps are in ISO format e.g., "2025-06-08T10:45:35.123Z"
                review_date = datetime.fromisoformat(review["timestamp"].replace("Z", "+00:00")).date()
                if review_date == today:
                    daily_count += 1
            except (ValueError, KeyError):
                # Ignore reviews with malformed timestamps or missing keys
                continue
                
    return {"daily_count": daily_count}


# This part is just to run the server directly with `python main.py` if you want
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
