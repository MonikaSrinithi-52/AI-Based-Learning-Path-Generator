import json
import re
from typing import List, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from backend.models import Roadmap, RoadmapStep, Resource
from backend.rag_store import search_resources
from backend.mock_data import MOCK_ROADMAPS

def clean_json_string(text: str) -> str:
    """
    Cleans up LLM markdown blocks and returns just the raw JSON substring.
    """
    text = text.strip()
    # Match ```json ... ``` or ``` ... ```
    match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Try finding the first '{' and last '}'
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        return text[start:end+1].strip()
        
    return text

def run_goal_analyzer(
    goal: str,
    difficulty: str,
    duration_weeks: int,
    weekly_hours: int,
    learning_style: str,
    api_key: str
) -> dict:
    """
    Goal Analyzer Agent: Analyzes user learning goal and breaks it down into structured milestones.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.2
    )
    
    max_steps = max(3, min(10, duration_weeks)) # Cap steps between 3 and 10
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a professional educational counselor and curriculum designer (Goal Analyzer Agent).\n"
            "Your job is to analyze a learner's goal and structure it into a series of logical milestones.\n"
            "You MUST output raw JSON matching the requested structure. Do not output conversational filler."
        )),
        ("user", (
            "Analyze the following learning request and break it down into milestones:\n"
            "- Learning Goal: {goal}\n"
            "- Skill Level: {difficulty}\n"
            "- Course Duration: {duration_weeks} weeks\n"
            "- Available Time: {weekly_hours} hours per week\n"
            "- Learning Style: {learning_style}\n\n"
            "Create a maximum of {max_steps} milestones. For each milestone, specify its sequence, "
            "a short title, a detailed sub-topic description of what to learn, and its duration in weeks (e.g., 'Week 1', 'Weeks 2-3').\n\n"
            "You must return ONLY a JSON object with this exact format:\n"
            "{{\n"
            "  \"title\": \"Name of the overall learning path (e.g., Machine Learning Fundamentals)\",\n"
            "  \"summary\": \"A brief summary of what the learner will achieve and the pedagogy.\",\n"
            "  \"milestones\": [\n"
            "    {{\n"
            "      \"step_id\": \"step_1\",\n"
            "      \"title\": \"Milestone Title\",\n"
            "      \"description\": \"Description of what concepts are covered.\",\n"
            "      \"duration_weeks\": \"Week 1\"\n"
            "    }}\n"
            "  ]\n"
            "}}\n"
            "Ensure the JSON is valid and complete."
        ))
    ])
    
    chain = prompt | llm
    response = chain.invoke({
        "goal": goal,
        "difficulty": difficulty,
        "duration_weeks": duration_weeks,
        "weekly_hours": weekly_hours,
        "learning_style": learning_style,
        "max_steps": max_steps
    })
    
    cleaned = clean_json_string(response.content)
    return json.loads(cleaned)

def run_roadmap_generator(
    goal: str,
    difficulty: str,
    duration_weeks: int,
    weekly_hours: int,
    learning_style: str,
    milestones_with_resources: list,
    api_key: str
) -> dict:
    """
    Roadmap Generator Agent: Synthesizes milestones and retrieved resources,
    appending custom milestone verification projects for each step.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.3
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are the Roadmap Generator Agent. Your job is to take a set of milestones "
            "and their retrieved learning resources, and compile them into a beautiful, personalized, step-by-step roadmap.\n"
            "For each milestone, you must invent a practical 'milestone_project' (a mini-project, challenge, or practical assignment "
            "aligned with their learning style and difficulty) that the user can build to prove they mastered that step.\n"
            "You MUST output raw JSON matching the schema. No markdown formatting outside of JSON code blocks."
        )),
        ("user", (
            "Compile the following structured milestones and resources into a unified roadmap:\n"
            "- Target Goal: {goal}\n"
            "- Difficulty: {difficulty}\n"
            "- Duration: {duration_weeks} weeks\n"
            "- Commited time: {weekly_hours} hours/week\n"
            "- Style preference: {learning_style}\n"
            "- Milestones with retrieved RAG resources: {milestones_data}\n\n"
            "Create a cohesive learning path. You must output a JSON matching this schema:\n"
            "{{\n"
            "  \"id\": \"roadmap_unique_id\",\n"
            "  \"title\": \"Refined Roadmap Title\",\n"
            "  \"summary\": \"Polished summary of the learning journey.\",\n"
            "  \"difficulty\": \"{difficulty}\",\n"
            "  \"weekly_hours\": {weekly_hours},\n"
            "  \"duration_weeks\": {duration_weeks},\n"
            "  \"steps\": [\n"
            "    {{\n"
            "      \"id\": \"step_id_from_input\",\n"
            "      \"title\": \"Step Title\",\n"
            "      \"description\": \"Enriched step description explaining how to use resources.\",\n"
            "      \"duration_weeks\": \"Duration string from input\",\n"
            "      \"resources\": [\n"
            "        {{\n"
            "          \"id\": \"resource_id\",\n"
            "          \"title\": \"Resource Title\",\n"
            "          \"url\": \"Resource URL\",\n"
            "          \"type\": \"Resource Type (course/video/article/book)\",\n"
            "          \"description\": \"A short note on why this resource is useful for this step.\",\n"
            "          \"difficulty\": \"Resource difficulty\"\n"
            "        }}\n"
            "      ],\n"
            "      \"milestone_project\": \"Explain a hands-on project the user should code/build to test this step.\",\n"
            "      \"status\": \"pending\"\n"
            "    }}\n"
            "  ]\n"
            "}}\n"
        ))
    ])
    
    # Serialize milestone data for prompt
    milestones_data_str = json.dumps(milestones_with_resources, indent=2)
    
    chain = prompt | llm
    response = chain.invoke({
        "goal": goal,
        "difficulty": difficulty,
        "duration_weeks": duration_weeks,
        "weekly_hours": weekly_hours,
        "learning_style": learning_style,
        "milestones_data": milestones_data_str
    })
    
    cleaned = clean_json_string(response.content)
    return json.loads(cleaned)

def run_adaptive_planner(
    current_roadmap_dict: dict,
    feedback: str,
    completed_step_ids: List[str],
    api_key: str
) -> dict:
    """
    Adaptive Planner Agent: Evaluates user's learning status and feedback to adapt
    remaining (non-completed) steps in the roadmap.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.3
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are the Adaptive Planner Agent. Your job is to modify an existing learning roadmap "
            "based on the learner's feedback and progress.\n"
            "Keep completed steps exactly as they are (you can mark their status as 'completed').\n"
            "Modify the remaining steps (pending or struggling steps) to address their feedback.\n"
            "If they find things too hard, simplify future descriptions and project scopes, and suggest easier resources.\n"
            "If they find it too easy or fast, speed up pacing and add advanced coding challenges.\n"
            "You MUST return raw JSON matching the Roadmap schema. No filler text."
        )),
        ("user", (
            "Adapt the learning path based on the user state:\n"
            "- Current Roadmap:\n{current_roadmap}\n"
            "- Completed Step IDs: {completed_step_ids}\n"
            "- Learner's Feedback: \"{feedback}\"\n\n"
            "Modify the pending/remaining steps to adapt to this feedback. Output the updated roadmap JSON matching the standard format:\n"
            "{{\n"
            "  \"id\": \"roadmap_id\",\n"
            "  \"title\": \"Roadmap Title\",\n"
            "  \"summary\": \"Updated summary reflecting the adapted path.\",\n"
            "  \"difficulty\": \"difficulty_level\",\n"
            "  \"weekly_hours\": weekly_hours_integer,\n"
            "  \"duration_weeks\": duration_weeks_integer,\n"
            "  \"steps\": [\n"
            "     ...\n"
            "  ]\n"
            "}}\n"
        ))
    ])
    
    chain = prompt | llm
    response = chain.invoke({
        "current_roadmap": json.dumps(current_roadmap_dict, indent=2),
        "completed_step_ids": str(completed_step_ids),
        "feedback": feedback
    })
    
    cleaned = clean_json_string(response.content)
    return json.loads(cleaned)

# --- DEMO MODE MOCK IMPLEMENTATION ---

def generate_demo_roadmap(
    goal: str,
    difficulty: str,
    duration_weeks: int,
    weekly_hours: int,
    learning_style: str
) -> Roadmap:
    """
    Dynamically builds and adapts a mock roadmap for Demo Mode.
    """
    goal_lower = goal.lower()
    if any(x in goal_lower for x in ["ml", "machine", "deep", "ai", "neural", "vision", "data science"]):
        key = "machine_learning"
    elif any(x in goal_lower for x in ["web", "front", "html", "css", "js", "javascript", "react", "website", "node"]):
        key = "web_dev"
    elif any(x in goal_lower for x in ["ui", "ux", "design", "figma", "wireframe", "prototype", "user experience"]):
        key = "ui_ux_design"
    else:
        key = "python_scratch"
        
    base_roadmap = MOCK_ROADMAPS[key]
    
    # Adjust step durations to fit the requested duration_weeks
    steps = [step.copy() for step in base_roadmap["steps"]]
    num_steps = len(steps)
    
    weeks_per_step = max(1, duration_weeks // num_steps)
    current_week = 1
    
    adjusted_steps = []
    for i, s in enumerate(steps):
        s_copy = s.copy()
        
        # Adjust week duration formatting
        if i == num_steps - 1:
            end_week = duration_weeks
        else:
            end_week = current_week + weeks_per_step - 1
            if end_week < current_week:
                end_week = current_week
                
        if current_week == end_week:
            s_copy["duration_weeks"] = f"Week {current_week}"
        else:
            s_copy["duration_weeks"] = f"Weeks {current_week}-{end_week}"
            
        current_week = end_week + 1
        
        # Turn resource dicts into Resource models
        res_list = []
        for r in s_copy["resources"]:
            res_list.append(Resource(**r))
        s_copy["resources"] = res_list
        
        adjusted_steps.append(RoadmapStep(**s_copy))
        
    # Return Roadmap model
    return Roadmap(
        id=f"demo_{key}_{duration_weeks}w",
        title=f"Personalized: {base_roadmap['title']}",
        summary=f"Adapted for your specific goal: '{goal}'. " + base_roadmap["summary"],
        difficulty=difficulty,
        weekly_hours=weekly_hours,
        duration_weeks=duration_weeks,
        steps=adjusted_steps
    )

def adapt_demo_roadmap(
    current_roadmap: Roadmap,
    feedback: str,
    completed_step_ids: List[str]
) -> Roadmap:
    """
    Adapts a Demo Mode roadmap using heuristic rules based on feedback.
    """
    feedback_lower = feedback.lower()
    adapted_steps = []
    
    for step in current_roadmap.steps:
        step_copy = step.model_copy(deep=True)
        
        if step_copy.id in completed_step_ids:
            step_copy.status = "completed"
        else:
            # Modify step based on feedback keywords
            if any(w in feedback_lower for w in ["hard", "difficult", "struggle", "math", "confused", "slow"]):
                step_copy.description = f"Simplified (Beginner-focused): {step_copy.description}"
                step_copy.milestone_project = f"Simplified Task: {step_copy.milestone_project} (with extra mentorship guidance)"
                step_copy.status = "struggling"
                
                # Prepend a helper note to resources
                for r in step_copy.resources:
                    r.description = "[EASY-PACED HELP] " + r.description
            elif any(w in feedback_lower for w in ["easy", "fast", "bore", "advance", "quick"]):
                step_copy.description = f"Accelerated (Deep-dive focus): {step_copy.description}"
                step_copy.milestone_project = f"Advanced Challenge: {step_copy.milestone_project} (Build with production-grade security and optimization)"
                
                # Prepend an advanced note to resources
                for r in step_copy.resources:
                    r.description = "[ADVANCED FOCUS] " + r.description
            
        adapted_steps.append(step_copy)
        
    return Roadmap(
        id=current_roadmap.id,
        title=current_roadmap.title,
        summary=f"Adapted path based on feedback: '{feedback}'. " + current_roadmap.summary,
        difficulty=current_roadmap.difficulty,
        weekly_hours=current_roadmap.weekly_hours,
        duration_weeks=current_roadmap.duration_weeks,
        steps=adapted_steps
    )

# --- PUBLIC INTERFACE ---

def generate_roadmap_with_agents(
    goal: str,
    difficulty: str,
    duration_weeks: int,
    weekly_hours: int,
    learning_style: str,
    api_key: Optional[str] = None
) -> Roadmap:
    """
    Generates a personalized Roadmap using a multiagent chain if api_key is available,
    otherwise uses the rule-based Demo generator.
    """
    if not api_key:
        return generate_demo_roadmap(
            goal=goal,
            difficulty=difficulty,
            duration_weeks=duration_weeks,
            weekly_hours=weekly_hours,
            learning_style=learning_style
        )
        
    try:
        # Step 1: Run Goal Analyzer Agent to get milestones
        milestones_json = run_goal_analyzer(
            goal=goal,
            difficulty=difficulty,
            duration_weeks=duration_weeks,
            weekly_hours=weekly_hours,
            learning_style=learning_style,
            api_key=api_key
        )
        
        # Step 2: Run Resource Retriever Agent (RAG) for each milestone
        milestones_with_resources = []
        for ms in milestones_json.get("milestones", []):
            ms_copy = ms.copy()
            # Retrieve k=2 resources from vector/keyword database matching milestone title and description
            query = f"{ms['title']} {ms['description']}"
            retrieved = search_resources(query, api_key=api_key, k=2, difficulty=difficulty)
            
            # Serialize retrieved resources to plain dictionaries
            ms_copy["resources"] = [r.model_dump() for r in retrieved]
            milestones_with_resources.append(ms_copy)
            
        # Step 3: Run Roadmap Generator Agent to synthesize steps and add milestone projects
        roadmap_json = run_roadmap_generator(
            goal=goal,
            difficulty=difficulty,
            duration_weeks=duration_weeks,
            weekly_hours=weekly_hours,
            learning_style=learning_style,
            milestones_with_resources=milestones_with_resources,
            api_key=api_key
        )
        
        # Deserialize dict back into full Pydantic Roadmap model
        steps = []
        for s in roadmap_json.get("steps", []):
            resources = [Resource(**r) for r in s.get("resources", [])]
            steps.append(RoadmapStep(
                id=s["id"],
                title=s["title"],
                description=s["description"],
                duration_weeks=s["duration_weeks"],
                resources=resources,
                milestone_project=s["milestone_project"],
                status=s.get("status", "pending")
            ))
            
        return Roadmap(
            id=roadmap_json.get("id", "rag_roadmap"),
            title=roadmap_json.get("title", milestones_json.get("title", "AI Learning Path")),
            summary=roadmap_json.get("summary", milestones_json.get("summary", "")),
            difficulty=difficulty,
            weekly_hours=weekly_hours,
            duration_weeks=duration_weeks,
            steps=steps
        )
        
    except Exception as e:
        print(f"Multiagent Agent path generation failed: {e}. Falling back to Demo Path generator.")
        return generate_demo_roadmap(
            goal=goal,
            difficulty=difficulty,
            duration_weeks=duration_weeks,
            weekly_hours=weekly_hours,
            learning_style=learning_style
        )

def adapt_roadmap_with_agents(
    current_roadmap: Roadmap,
    feedback: str,
    completed_step_ids: List[str],
    api_key: Optional[str] = None
) -> Roadmap:
    """
    Adapts an existing Roadmap using the Adaptive Planner Agent if api_key is available,
    otherwise uses the rule-based Demo adapter.
    """
    if not api_key:
        return adapt_demo_roadmap(
            current_roadmap=current_roadmap,
            feedback=feedback,
            completed_step_ids=completed_step_ids
        )
        
    try:
        current_roadmap_dict = current_roadmap.model_dump()
        
        # Run Adaptive Planner Agent
        adapted_json = run_adaptive_planner(
            current_roadmap_dict=current_roadmap_dict,
            feedback=feedback,
            completed_step_ids=completed_step_ids,
            api_key=api_key
        )
        
        steps = []
        for s in adapted_json.get("steps", []):
            resources = [Resource(**r) for r in s.get("resources", [])]
            steps.append(RoadmapStep(
                id=s["id"],
                title=s["title"],
                description=s["description"],
                duration_weeks=s["duration_weeks"],
                resources=resources,
                milestone_project=s["milestone_project"],
                status=s.get("status", "pending")
            ))
            
        return Roadmap(
            id=adapted_json.get("id", current_roadmap.id),
            title=adapted_json.get("title", current_roadmap.title),
            summary=adapted_json.get("summary", current_roadmap.summary),
            difficulty=adapted_json.get("difficulty", current_roadmap.difficulty),
            weekly_hours=adapted_json.get("weekly_hours", current_roadmap.weekly_hours),
            duration_weeks=adapted_json.get("duration_weeks", current_roadmap.duration_weeks),
            steps=steps
        )
        
    except Exception as e:
        print(f"Adaptive Planner agent failed: {e}. Falling back to Demo Adaptation.")
        return adapt_demo_roadmap(
            current_roadmap=current_roadmap,
            feedback=feedback,
            completed_step_ids=completed_step_ids
        )
