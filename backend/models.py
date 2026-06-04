from pydantic import BaseModel, Field
from typing import List, Optional

class Resource(BaseModel):
    id: str
    title: str
    url: str
    type: str  # 'course', 'video', 'article', 'book', etc.
    description: str
    difficulty: str  # 'beginner', 'intermediate', 'advanced', 'all'

class RoadmapStep(BaseModel):
    id: str
    title: str
    description: str
    duration_weeks: str  # e.g., 'Week 1', 'Week 2-3'
    resources: List[Resource] = []
    milestone_project: str
    status: str = "pending"  # 'pending', 'completed', 'struggling'

class Roadmap(BaseModel):
    id: str
    title: str
    summary: str
    difficulty: str
    weekly_hours: int
    duration_weeks: int
    steps: List[RoadmapStep]

class RoadmapRequest(BaseModel):
    goal: str
    difficulty: str = "beginner"  # 'beginner', 'intermediate', 'advanced'
    duration_weeks: int = 4
    weekly_hours: int = 5
    learning_style: str = "mixed"  # 'practical', 'theoretical', 'mixed'
    api_key: Optional[str] = None

class AdaptationRequest(BaseModel):
    roadmap: Roadmap
    feedback: str
    completed_step_ids: List[str]
    api_key: Optional[str] = None
