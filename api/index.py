import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from backend.models import RoadmapRequest, AdaptationRequest, Roadmap
from backend.agents import generate_roadmap_with_agents, adapt_roadmap_with_agents
from backend.rag_store import LEARNING_RESOURCES

app = FastAPI(
    title="AI-Based Learning Path Generator API",
    description="A multiagent RAG application to generate and adapt personalized learning roadmaps.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints
@app.post("/api/generate", response_model=Roadmap)
def generate_roadmap(request: RoadmapRequest):
    """
    Analyzes user goals, queries RAG store for resources, and compiles a personalized roadmap.
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

# Serve static files locally (fallback when not running on Vercel CDN)
if not os.environ.get("VERCEL"):
    root_dir = os.path.dirname(os.path.dirname(__file__))
    
    @app.get("/")
    def read_root():
        return FileResponse(os.path.join(root_dir, "index.html"))
        
    @app.get("/styles.css")
    def read_css():
        return FileResponse(os.path.join(root_dir, "styles.css"))
        
    @app.get("/app.js")
    def read_js():
        return FileResponse(os.path.join(root_dir, "app.js"))
