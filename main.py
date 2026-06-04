import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.models import RoadmapRequest, AdaptationRequest, Roadmap
from backend.agents import generate_roadmap_with_agents, adapt_roadmap_with_agents
from backend.rag_store import LEARNING_RESOURCES

app = FastAPI(
    title="AI-Based Learning Path Generator API",
    description="A multiagent RAG application to generate and adapt personalized learning roadmaps.",
    version="1.0.0"
)

# Enable CORS for cross-origin local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static frontend directory
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
if not os.path.exists(frontend_dir):
    os.makedirs(frontend_dir)
    
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
def read_root():
    """Serves the main application user interface."""
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "AI-Based Learning Path Generator Backend is Running. Frontend index.html not found."}

@app.post("/api/generate", response_model=Roadmap)
def generate_roadmap(request: RoadmapRequest):
    """
    Analyzes user goals, queries RAG store for resources, and compiles a personalized roadmap.
    Uses Multiagent chains if api_key is supplied; otherwise runs custom Demo Mode generator.
    """
    try:
        roadmap = generate_roadmap_with_agents(
            goal=request.goal,
            difficulty=request.difficulty,
            duration_weeks=request.duration_weeks,
            weekly_hours=request.weekly_hours,
            learning_style=request.learning_style,
            api_key=request.api_key
        )
        return roadmap
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/adapt", response_model=Roadmap)
def adapt_roadmap(request: AdaptationRequest):
    """
    Evaluates learning feedback and adapts future steps of the learning roadmap.
    """
    try:
        adapted_roadmap = adapt_roadmap_with_agents(
            current_roadmap=request.roadmap,
            feedback=request.feedback,
            completed_step_ids=request.completed_step_ids,
            api_key=request.api_key
        )
        return adapted_roadmap
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/resources")
def get_all_resources():
    """Retrieves all preloaded learning resources stored in the RAG database."""
    return LEARNING_RESOURCES

if __name__ == "__main__":
    import uvicorn
    # Run the server locally on port 8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
