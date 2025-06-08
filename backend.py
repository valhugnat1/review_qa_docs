import json
import os
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

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

REVIEWS_FILE = "reviews.json"

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

# This part is just to run the server directly with `python main.py` if you want
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)