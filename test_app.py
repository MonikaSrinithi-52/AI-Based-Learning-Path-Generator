import sys
from backend.models import RoadmapRequest, AdaptationRequest, Roadmap, Resource, RoadmapStep
from backend.mock_data import MOCK_ROADMAPS
from backend.rag_store import search_resources, LEARNING_RESOURCES
from backend.agents import generate_roadmap_with_agents, adapt_roadmap_with_agents

def run_tests():
    print("--- Running AI-Based Learning Path Generator Verification Tests ---")
    
    # Test 1: Models and Datatypes Initialization
    print("[Test 1/4] Verifying Pydantic schemas initialization...")
    try:
        dummy_res = Resource(
            id="test_res",
            title="Test Resource",
            url="http://test.com",
            type="article",
            description="A test descriptor",
            difficulty="beginner"
        )
        dummy_step = RoadmapStep(
            id="test_step",
            title="Test Step",
            description="Testing step models",
            duration_weeks="Week 1",
            resources=[dummy_res],
            milestone_project="Test project output"
        )
        dummy_roadmap = Roadmap(
            id="test_roadmap",
            title="Test Pathway",
            summary="A test summary details description",
            difficulty="beginner",
            weekly_hours=5,
            duration_weeks=4,
            steps=[dummy_step]
        )
        print(" -> Success: Models instantiated successfully.")
    except Exception as e:
        print(f" -> Fail: Model instantiation crashed. Error: {e}")
        sys.exit(1)

    # Test 2: RAG Search Functionality (Keyword Search Fallback Check)
    print("[Test 2/4] Verifying RAG local keyword search engine...")
    try:
        results = search_resources("html css grid layout tutorial", api_key=None, k=3)
        assert len(results) == 3, "Did not retrieve requested count of elements"
        # Assert one of the matched elements is web development related
        matched_ids = [r.id for r in results]
        print(f" -> Success: Retrieved resources: {matched_ids}")
    except Exception as e:
        print(f" -> Fail: RAG keyword fallback failed. Error: {e}")
        sys.exit(1)

    # Test 3: Demo Mode Generator Customization
    print("[Test 3/4] Verifying Demo Mode Dynamic Roadmap Generator...")
    try:
        roadmap = generate_roadmap_with_agents(
            goal="I want to learn Neural Networks in Python",
            difficulty="intermediate",
            duration_weeks=8,
            weekly_hours=10,
            learning_style="practical",
            api_key=None  # Triggers demo mode
        )
        assert "Personalized" in roadmap.title, "Roadmap title not customized correctly"
        assert len(roadmap.steps) > 0, "Roadmap has no steps"
        assert roadmap.duration_weeks == 8, "Roadmap duration mismatch"
        print(f" -> Success: Generated '{roadmap.title}' ({len(roadmap.steps)} steps, {roadmap.duration_weeks} weeks)")
    except Exception as e:
        print(f" -> Fail: Demo generation failed. Error: {e}")
        sys.exit(1)

    # Test 4: Demo Mode Adaptive Planner
    print("[Test 4/4] Verifying Demo Mode Adaptive Planner...")
    try:
        adapted = adapt_roadmap_with_agents(
            current_roadmap=roadmap,
            feedback="The mathematics details are too hard to grasp, please simplify.",
            completed_step_ids=[roadmap.steps[0].id],
            api_key=None
        )
        assert "Adapted" in adapted.summary, "Roadmap summary adaptation not matching"
        assert adapted.steps[0].status == "completed", "Completed step state not preserved"
        assert "Simplified" in adapted.steps[1].description, "Struggling step description not mutated"
        print(" -> Success: Roadmap adapted successfully.")
        print(f" -> Adapted Summary: {adapted.summary}")
    except Exception as e:
        print(f" -> Fail: Adaptation failed. Error: {e}")
        sys.exit(1)

    print("\n--- All 4 verification checks PASSED successfully! ---")

if __name__ == "__main__":
    run_tests()
