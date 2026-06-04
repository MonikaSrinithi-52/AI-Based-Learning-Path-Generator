import re
from typing import List, Optional
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from backend.models import Resource

# Curated high-quality database of learning resources
LEARNING_RESOURCES = [
    # Frontend Web Development
    Resource(
        id="html_mdn",
        title="MDN Web Docs: HTML Basics",
        url="https://developer.mozilla.org/en-US/docs/Learn/HTML",
        type="article",
        description="The ultimate standard reference for learning how web pages are structured, formatted, and optimized for SEO and accessibility.",
        difficulty="beginner"
    ),
    Resource(
        id="fcc_responsive",
        title="freeCodeCamp Responsive Web Design Certification",
        url="https://www.freecodecamp.org/learn/2022/responsive-web-design/",
        type="course",
        description="Interactive coding tutorials covering HTML, CSS, Flexbox, Grid, semantic structures, and accessibility standards.",
        difficulty="beginner"
    ),
    Resource(
        id="flexbox_zombies",
        title="Flexbox Zombies Interactive Course",
        url="https://mastery.games/flexboxzombies/",
        type="course",
        description="A beautiful, story-driven interactive game that builds muscle memory for designing layouts using CSS Flexbox.",
        difficulty="beginner"
    ),
    Resource(
        id="css_tricks_grid",
        title="CSS-Tricks: Complete Guide to CSS Grid",
        url="https://css-tricks.com/snippets/css/complete-guide-grid/",
        type="article",
        description="A visual cheatsheet and detailed deep-dive outlining all properties and layout patterns of CSS Grid.",
        difficulty="intermediate"
    ),
    Resource(
        id="js_info",
        title="The Modern JavaScript Tutorial",
        url="https://javascript.info/",
        type="book",
        description="A detailed textbook tracing JavaScript from fundamentals to advanced concepts, asynchronous execution, and browser API bindings.",
        difficulty="beginner"
    ),
    Resource(
        id="fcc_js_dom",
        title="JavaScript DOM Manipulation Course (freeCodeCamp)",
        url="https://www.youtube.com/watch?v=5fb2aPlgoys",
        type="video",
        description="A comprehensive video tutorial detailing document tree selectors, class lists, and event listener attachments.",
        difficulty="intermediate"
    ),
    Resource(
        id="mdn_fetch_api",
        title="MDN: Using the Fetch API",
        url="https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch",
        type="article",
        description="Clear documentation covering REST API integrations, JSON parsing, error states, and handling promises using async/await.",
        difficulty="intermediate"
    ),
    Resource(
        id="react_docs_learn",
        title="React.dev: Learn React Tutorial",
        url="https://react.dev/learn",
        type="article",
        description="Official React documentation containing structured sandboxes to practice components, props flow, state hooks, and effect hooks.",
        difficulty="intermediate"
    ),
    Resource(
        id="react_net_ninja",
        title="React Crash Course for Beginners (Net Ninja)",
        url="https://www.youtube.com/playlist?list=PL4cUxeGkcC9gZD-Tvwfod2gaISMCGsG5d",
        type="video",
        description="A beginner-friendly video course covering Vite setup, functional components, state bindings, list rendering, and local APIs.",
        difficulty="beginner"
    ),
    Resource(
        id="react_useeffect_docs",
        title="React.dev: Synchronizing with Effects Hook",
        url="https://react.dev/learn/synchronizing-with-effects",
        type="article",
        description="Advanced documentation outlining how to write clean component lifecycles, hook into APIs, and clean up subscriptions.",
        difficulty="advanced"
    ),

    # Machine Learning & AI
    Resource(
        id="mml_book_site",
        title="Mathematics for Machine Learning Textbook",
        url="https://mml-book.github.io/",
        type="book",
        description="An open textbook outlining linear algebra, vector calculus, probability distributions, and optimizer math needed for ML.",
        difficulty="intermediate"
    ),
    Resource(
        id="numpy_quickstart",
        title="NumPy Quickstart Tutorial Guide",
        url="https://numpy.org/doc/stable/user/quickstart.html",
        type="article",
        description="Interactive documentation teaching n-dimensional arrays, vector computations, and broadcasting techniques in Python.",
        difficulty="beginner"
    ),
    Resource(
        id="andrew_ng_ml",
        title="Supervised Machine Learning: Regression and Classification",
        url="https://www.coursera.org/specializations/machine-learning-introduction",
        type="course",
        description="Andrew Ng's flagship intro course covering linear/logistic regression, cost functions, gradient descent, and regularization.",
        difficulty="beginner"
    ),
    Resource(
        id="scikit_learn_quick",
        title="Scikit-Learn Getting Started Guide",
        url="https://scikit-learn.org/stable/getting_started.html",
        type="article",
        description="Hands-on documentation on data preprocessing, model fitting, metric evaluation pipelines, and hyperparameter grids.",
        difficulty="intermediate"
    ),
    Resource(
        id="andrew_ng_unsupervised",
        title="Unsupervised Learning, Recommenders, Reinforcement (Andrew Ng)",
        url="https://www.coursera.org/learn/unsupervised-learning-recommenders-reinforcement-learning",
        type="course",
        description="A course that covers K-means clustering, anomaly detection, PCA dimensionality reduction, and recommendation engines.",
        difficulty="intermediate"
    ),
    Resource(
        id="deep_learning_spec",
        title="Deep Learning Specialization (DeepLearning.AI)",
        url="https://www.deeplearning.ai/courses/deep-learning-specialization/",
        type="course",
        description="A structured curriculum to build, optimize, and train deep artificial neural networks (ANNs), CNNs, and sequence models.",
        difficulty="intermediate"
    ),
    Resource(
        id="pytorch_blitz_tutorial",
        title="PyTorch Deep Learning in 60 Minutes",
        url="https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html",
        type="article",
        description="A fast-paced guide to tensor computing, automatic differentiation, training neural networks, and writing custom dataset loaders.",
        difficulty="intermediate"
    ),
    Resource(
        id="cs231n_stanford",
        title="Stanford CS231n: Deep Learning for Computer Vision",
        url="http://cs231n.stanford.edu/",
        type="course",
        description="Industry standard Stanford lectures detailing Convolutional Neural Networks (CNNs), object detectors, and image segmentation.",
        difficulty="advanced"
    ),

    # Python Programming
    Resource(
        id="py_tutorial",
        title="The Official Python Language Tutorial",
        url="https://docs.python.org/3/tutorial/index.html",
        type="book",
        description="The primary Python standard library guide detailing variables, lists, dicts, custom modules, and error debugging.",
        difficulty="beginner"
    ),
    Resource(
        id="py_w3",
        title="W3Schools Python Syntax Reference",
        url="https://www.w3schools.com/python/",
        type="article",
        description="Interactive online sandbox featuring bite-sized code blocks to review variable assignments and loop mechanics.",
        difficulty="beginner"
    ),
    Resource(
        id="real_py_collections",
        title="Real Python: Guide to Python Lists and Tuples",
        url="https://realpython.com/python-lists-tuples/",
        type="article",
        description="A detailed article outlining how data is structured and mutated in Python sequences, referencing memory and sorting rules.",
        difficulty="beginner"
    ),
    Resource(
        id="automate_boring_stuff",
        title="Automate the Boring Stuff with Python Book",
        url="https://automatetheboringstuff.com/",
        type="book",
        description="Learn practical tasks: scraping web pages, manipulating directories, searching file trees, and scheduling scripts.",
        difficulty="beginner"
    ),
    Resource(
        id="real_py_oop",
        title="Real Python: Object-Oriented Programming (OOP) in Python 3",
        url="https://realpython.com/python3-object-oriented-programming/",
        type="article",
        description="Learn how to write custom Classes, initialize state variables, hook up methods, and understand class inheritance overrides.",
        difficulty="intermediate"
    ),

    # UI/UX Design
    Resource(
        id="nn_heuristics",
        title="Nielsen Norman Group: 10 Usability Heuristics",
        url="https://www.nngroup.com/articles/ten-usability-heuristics/",
        type="article",
        description="The benchmark checklist for system design, including visibility of system status, error prevention, and user control.",
        difficulty="beginner"
    ),
    Resource(
        id="google_ux_cert",
        title="Google UX Design Professional Certificate",
        url="https://www.coursera.org/professional-certificates/google-ux-design",
        type="course",
        description="A detailed, comprehensive certificate course covering user personas, wireframes, user testing, and Figma components.",
        difficulty="beginner"
    ),
    Resource(
        id="refactoring_ui_book",
        title="Refactoring UI Book",
        url="https://www.refactoringui.com/",
        type="book",
        description="Highly visual guidelines on creating aesthetic layouts, using color schemes, shadows, borders, and choosing fonts.",
        difficulty="beginner"
    ),
    Resource(
        id="figma_learn_portal",
        title="Figma Learning Portal tutorials",
        url="https://learn.figma.com/",
        type="course",
        description="A portal with structured video tutorials to master Figma structures, absolute layouts, variables, and components libraries.",
        difficulty="beginner"
    ),
    Resource(
        id="figma_prototyping",
        title="Figma Guide: Prototyping Transitions & Actions",
        url="https://help.figma.com/hc/en-us/articles/360040314193-Guide-to-prototyping-in-Figma",
        type="article",
        description="Guides on setting up interactive prototyping flows, overlay transitions, smart animations, and trigger systems.",
        difficulty="intermediate"
    ),
]

def keyword_fallback_search(query: str, k: int = 3, target_difficulty: str = "all") -> List[Resource]:
    """
    Performs a high-performance token-matching keyword search over local resources.
    Highly resilient fallback when no internet/API key is present.
    """
    words = set(re.findall(r'\w+', query.lower()))
    scored_resources = []
    
    for r in LEARNING_RESOURCES:
        # Calculate matching score
        title_text = r.title.lower()
        desc_text = r.description.lower()
        
        score = 0
        for w in words:
            if w in title_text:
                score += 3  # Higher weight for title matches
            elif w in desc_text:
                score += 1
                
        if score > 0:
            # Adjust score based on difficulty match if specified
            if target_difficulty != "all":
                if r.difficulty == target_difficulty:
                    score += 2
                elif r.difficulty == "all":
                    score += 1
            scored_resources.append((score, r))
            
    # Sort by score descending
    scored_resources.sort(key=lambda x: x[0], reverse=True)
    results = [r for _, r in scored_resources]
    
    # Fill in k items from LEARNING_RESOURCES if match count < k
    if len(results) < k:
        existing_ids = {r.id for r in results}
        # Add general resources first
        for r in LEARNING_RESOURCES:
            if len(results) >= k:
                break
            if r.id not in existing_ids:
                # If target difficulty matches or resource is beginner
                if target_difficulty == "all" or r.difficulty == target_difficulty or r.difficulty == "beginner":
                    results.append(r)
                    existing_ids.add(r.id)
                    
        # Still not k items? Add any remaining resource
        for r in LEARNING_RESOURCES:
            if len(results) >= k:
                break
            if r.id not in existing_ids:
                results.append(r)
                existing_ids.add(r.id)
                
    return results[:k]

def search_resources(query: str, api_key: Optional[str] = None, k: int = 3, difficulty: str = "all") -> List[Resource]:
    """
    RAG Search. Uses Semantic Vector Search via LangChain + GoogleGenAI if api_key is provided,
    otherwise falls back to keyword matching search.
    """
    if not api_key:
        return keyword_fallback_search(query, k=k, target_difficulty=difficulty)
        
    try:
        # Set up LangChain InMemoryVectorStore with GoogleGenerativeAIEmbeddings
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )
        
        # Load resources as Documents
        docs = []
        for r in LEARNING_RESOURCES:
            doc_content = f"Title: {r.title}\nDescription: {r.description}\nType: {r.type}\nDifficulty: {r.difficulty}"
            doc = Document(
                page_content=doc_content,
                metadata={"id": r.id}
            )
            docs.append(doc)
            
        # Build Vector Store
        vector_store = InMemoryVectorStore.from_documents(docs, embeddings)
        
        # Perform similarity search
        search_results = vector_store.similarity_search(query, k=k)
        
        # Resolve Document metadata IDs back to Resource objects
        matched_resources = []
        matched_ids = [doc.metadata["id"] for doc in search_results]
        
        for mid in matched_ids:
            for r in LEARNING_RESOURCES:
                if r.id == mid:
                    matched_resources.append(r)
                    break
                    
        return matched_resources
        
    except Exception as e:
        print(f"RAG Semantic Vector Search failed: {e}. Falling back to Keyword Search.")
        return keyword_fallback_search(query, k=k, target_difficulty=difficulty)
