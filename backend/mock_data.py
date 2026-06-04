# Fallback mock roadmaps for Demo Mode when Gemini API key is not provided or for instant preview.

MOCK_ROADMAPS = {
    "web_dev": {
        "id": "web_dev_path",
        "title": "Modern Frontend Web Development",
        "summary": "Master HTML, CSS, JavaScript, and React to build responsive, dynamic, and high-performance web applications. This path goes from core programming basics to advanced layout techniques and modern component-driven libraries.",
        "difficulty": "beginner",
        "weekly_hours": 8,
        "duration_weeks": 8,
        "steps": [
            {
                "id": "wd_step1",
                "title": "Core HTML5 & Responsive Semantic Structure",
                "description": "Understand the architecture of the web. Learn HTML5 semantic elements, forms, accessibility (a11y) basics, and SEO tags to build solid document foundations.",
                "duration_weeks": "Week 1",
                "resources": [
                    {
                        "id": "res_html_mdn",
                        "title": "MDN Web Docs: HTML Basics",
                        "url": "https://developer.mozilla.org/en-US/docs/Learn/HTML",
                        "type": "article",
                        "description": "The absolute standard reference for learning how web pages are structured and formatted.",
                        "difficulty": "beginner"
                    },
                    {
                        "id": "res_fcc_html",
                        "title": "freeCodeCamp Responsive Web Design Certification",
                        "url": "https://www.freecodecamp.org/learn/2022/responsive-web-design/",
                        "type": "course",
                        "description": "Interactive HTML tutorials building semantic pages directly in the browser.",
                        "difficulty": "beginner"
                    }
                ],
                "milestone_project": "Build a semantic personal portfolio page with contact forms and metadata.",
                "status": "pending"
            },
            {
                "id": "wd_step2",
                "title": "CSS3 Styling, Flexbox, & Modern Grid Layouts",
                "description": "Master styling web pages. Deep dive into the box model, selectors, CSS variables, transitions, and layout tools like Flexbox and CSS Grid.",
                "duration_weeks": "Week 2",
                "resources": [
                    {
                        "id": "res_css_flexbox_zombie",
                        "title": "Flexbox Zombies Game",
                        "url": "https://mastery.games/flexboxzombies/",
                        "type": "course",
                        "description": "An interactive, beautifully designed game to build muscle memory for CSS Flexbox layouts.",
                        "difficulty": "beginner"
                    },
                    {
                        "id": "res_css_tricks_grid",
                        "title": "CSS-Tricks: Complete Guide to CSS Grid",
                        "url": "https://css-tricks.com/snippets/css/complete-guide-grid/",
                        "type": "article",
                        "description": "The ultimate visual guide and reference sheet for CSS Grid layout properties.",
                        "difficulty": "intermediate"
                    }
                ],
                "milestone_project": "Design a highly responsive multi-column landing page with hover micro-animations.",
                "status": "pending"
            },
            {
                "id": "wd_step3",
                "title": "JavaScript Fundamentals & DOM Manipulation",
                "description": "Add life to your web pages. Learn variables, data types, control flow, functions, arrays, objects, and how to programmatically change HTML elements.",
                "duration_weeks": "Week 3-4",
                "resources": [
                    {
                        "id": "res_js_info",
                        "title": "The Modern JavaScript Tutorial",
                        "url": "https://javascript.info/",
                        "type": "book",
                        "description": "From scratch to advanced topics with detailed explanations, tasks, and browser interactions.",
                        "difficulty": "beginner"
                    },
                    {
                        "id": "res_js_dom_youtube",
                        "title": "JavaScript DOM Manipulation Course (freeCodeCamp)",
                        "url": "https://www.youtube.com/watch?v=5fb2aPlgoys",
                        "type": "video",
                        "description": "Video tutorial covering event listeners, class list management, and dynamic element creation.",
                        "difficulty": "intermediate"
                    }
                ],
                "milestone_project": "Develop an interactive task manager (To-Do App) that persists data using local storage.",
                "status": "pending"
            },
            {
                "id": "wd_step4",
                "title": "Asynchronous JavaScript & API Integration",
                "description": "Connect to external data. Master JavaScript Promises, async/await, API fetching, JSON parsing, and handling error states in front-end applications.",
                "duration_weeks": "Week 5",
                "resources": [
                    {
                        "id": "res_fetch_api_mdn",
                        "title": "MDN: Using the Fetch API",
                        "url": "https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch",
                        "type": "article",
                        "description": "Guides and references for initiating networking requests and handling responses.",
                        "difficulty": "intermediate"
                    },
                    {
                        "id": "res_mock_api",
                        "title": "JSONPlaceholder - Free Mock REST API",
                        "url": "https://jsonplaceholder.typicode.com/",
                        "type": "course",
                        "description": "A playground environment to safely test GET, POST, PUT, and DELETE fetch operations.",
                        "difficulty": "beginner"
                    }
                ],
                "milestone_project": "Build a real-time Weather Dashboard fetching data from a public weather API.",
                "status": "pending"
            },
            {
                "id": "wd_step5",
                "title": "React Core: Components, Props, and State",
                "description": "Transition to modern component libraries. Understand JSX, React component tree structures, standard props flow, and state hooks (`useState`).",
                "duration_weeks": "Week 6-7",
                "resources": [
                    {
                        "id": "res_react_docs",
                        "title": "React.dev: Quick Start Guide",
                        "url": "https://react.dev/learn",
                        "type": "article",
                        "description": "Official documentation containing visual sandbox tutorials and interactive code snippets.",
                        "difficulty": "intermediate"
                    },
                    {
                        "id": "res_react_net_ninja",
                        "title": "React crash course by Net Ninja",
                        "url": "https://www.youtube.com/playlist?list=PL4cUxeGkcC9gZD-Tvwfod2gaISMCGsG5d",
                        "type": "video",
                        "description": "Step-by-step video crash course on setting up React, components, and state management.",
                        "difficulty": "beginner"
                    }
                ],
                "milestone_project": "Build a dynamic product catalog with search filtering, categorizing, and a persistent shopping cart.",
                "status": "pending"
            },
            {
                "id": "wd_step6",
                "title": "Advanced React: Side Effects & Global State",
                "description": "Understand component lifecycle and API fetching hooks (`useEffect`). Learn the basics of Context API or simple global state management.",
                "duration_weeks": "Week 8",
                "resources": [
                    {
                        "id": "res_react_useeffect",
                        "title": "React.dev: Synchronizing with Effects",
                        "url": "https://react.dev/learn/synchronizing-with-effects",
                        "type": "article",
                        "description": "Deep-dive documentation detailing how to correctly handle side effects in functional components.",
                        "difficulty": "advanced"
                    }
                ],
                "milestone_project": "Develop a collaborative dashboard displaying user-specific feed items fetched on component load.",
                "status": "pending"
            }
        ]
    },
    "machine_learning": {
        "id": "ml_path",
        "title": "Machine Learning & Deep Learning Roadmap",
        "summary": "Step into the world of Artificial Intelligence. Transition from simple statistical analysis to advanced deep neural networks using Python and industry-standard frameworks.",
        "difficulty": "intermediate",
        "weekly_hours": 10,
        "duration_weeks": 8,
        "steps": [
            {
                "id": "ml_step1",
                "title": "Mathematics Foundations & Python Setup",
                "description": "Review essential linear algebra, multivariate calculus, probability theory, and set up your Python environment with NumPy and Pandas.",
                "duration_weeks": "Week 1",
                "resources": [
                    {
                        "id": "res_ml_math_book",
                        "title": "Mathematics for Machine Learning Book",
                        "url": "https://mml-book.github.io/",
                        "type": "book",
                        "description": "A comprehensive open source textbook connecting mathematical concepts directly to ML algorithms.",
                        "difficulty": "intermediate"
                    },
                    {
                        "id": "res_numpy_quick",
                        "title": "NumPy Quickstart Tutorial",
                        "url": "https://numpy.org/doc/stable/user/quickstart.html",
                        "type": "article",
                        "description": "Official guides to multi-dimensional arrays, vectorization, and matrix manipulation.",
                        "difficulty": "beginner"
                    }
                ],
                "milestone_project": "Perform matrix operations and exploratory data analysis (EDA) on a housing dataset using Pandas.",
                "status": "pending"
            },
            {
                "id": "ml_step2",
                "title": "Classical Machine Learning: Supervised Models",
                "description": "Learn basic machine learning models: Linear Regression, Logistic Regression, Decision Trees, and Support Vector Machines (SVM).",
                "duration_weeks": "Week 2-3",
                "resources": [
                    {
                        "id": "res_ml_andrew_ng",
                        "title": "Supervised Machine Learning Course (Coursera/DeepLearning.AI)",
                        "url": "https://www.coursera.org/specializations/machine-learning-introduction",
                        "type": "course",
                        "description": "Andrew Ng's world-famous introduction to regression, classification, and mathematical foundations.",
                        "difficulty": "beginner"
                    },
                    {
                        "id": "res_scikit_learn_docs",
                        "title": "Scikit-Learn Getting Started Guide",
                        "url": "https://scikit-learn.org/stable/getting_started.html",
                        "type": "article",
                        "description": "Quick tutorials to fit models, transform data, and evaluate accuracy metrics.",
                        "difficulty": "intermediate"
                    }
                ],
                "milestone_project": "Build an ML classification pipeline to predict customer churn using Scikit-Learn.",
                "status": "pending"
            },
            {
                "id": "ml_step3",
                "title": "Unsupervised Learning & Feature Engineering",
                "description": "Explore clustering techniques (K-Means, DBSCAN), Dimensionality Reduction (PCA), and data preprocessing/feature extraction.",
                "duration_weeks": "Week 4",
                "resources": [
                    {
                        "id": "res_ml_unsupervised_course",
                        "title": "Unsupervised Learning, Recommenders, Reinforcement (Andrew Ng)",
                        "url": "https://www.coursera.org/learn/unsupervised-learning-recommenders-reinforcement-learning",
                        "type": "course",
                        "description": "Covers recommendation systems, clustering algorithms, and principal component analysis.",
                        "difficulty": "intermediate"
                    }
                ],
                "milestone_project": "Segment customers into distinct marketing personas based on spending behavior using K-Means.",
                "status": "pending"
            },
            {
                "id": "ml_step4",
                "title": "Introduction to Neural Networks & Deep Learning",
                "description": "Learn the mechanics of Artificial Neural Networks (ANNs), backpropagation, activation functions, and optimization techniques.",
                "duration_weeks": "Week 5-6",
                "resources": [
                    {
                        "id": "res_dl_specialization",
                        "title": "Deep Learning Specialization by DeepLearning.AI",
                        "url": "https://www.deeplearning.ai/courses/deep-learning-specialization/",
                        "type": "course",
                        "description": "Deep dive into building neural networks, structuring projects, and mastering hyperparameter tuning.",
                        "difficulty": "intermediate"
                    },
                    {
                        "id": "res_pytorch_blitz",
                        "title": "PyTorch Deep Learning in 60 Minutes",
                        "url": "https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html",
                        "type": "article",
                        "description": "Official interactive walkthrough of PyTorch tensor logic and building simple classifiers.",
                        "difficulty": "intermediate"
                    }
                ],
                "milestone_project": "Design and train a PyTorch neural network to classify handwritten digits (MNIST dataset) with >95% accuracy.",
                "status": "pending"
            },
            {
                "id": "ml_step5",
                "title": "Deep Learning for Computer Vision: CNNs",
                "description": "Dive into Convolutional Neural Networks (CNNs). Learn image convolutions, pooling layers, data augmentation, and transfer learning.",
                "duration_weeks": "Week 7-8",
                "resources": [
                    {
                        "id": "res_cs231n",
                        "title": "Stanford CS231n: Deep Learning for Computer Vision",
                        "url": "http://cs231n.stanford.edu/",
                        "type": "course",
                        "description": "Top-tier Stanford lectures on image classification, object detection, and visual models.",
                        "difficulty": "advanced"
                    }
                ],
                "milestone_project": "Build an image classifier using transfer learning (ResNet50) in PyTorch to identify custom object categories.",
                "status": "pending"
            }
        ]
    },
    "python_scratch": {
        "id": "python_scratch_path",
        "title": "Python Programming from Scratch",
        "summary": "Learn to write clean, efficient, and pythonic code. Perfect for absolute beginners starting their coding journey, transitioning from scripting to object-oriented structures.",
        "difficulty": "beginner",
        "weekly_hours": 6,
        "duration_weeks": 4,
        "steps": [
            {
                "id": "py_step1",
                "title": "Syntax, Variables & Data Types",
                "description": "Learn Python basic keywords, data types (integers, strings, floats, booleans), variables, operators, and basic user console input/output.",
                "duration_weeks": "Week 1",
                "resources": [
                    {
                        "id": "res_py_official_tutorial",
                        "title": "Official Python Tutorial",
                        "url": "https://docs.python.org/3/tutorial/index.html",
                        "type": "book",
                        "description": "The official language reference document for Python's syntax and built-in components.",
                        "difficulty": "beginner"
                    },
                    {
                        "id": "res_py_w3schools",
                        "title": "W3Schools Python Reference Guide",
                        "url": "https://www.w3schools.com/python/",
                        "type": "article",
                        "description": "Highly accessible, interactive, and quick reference list for syntax testing.",
                        "difficulty": "beginner"
                    }
                ],
                "milestone_project": "Create a fully interactive 'Guess the Number' text-based console game.",
                "status": "pending"
            },
            {
                "id": "py_step2",
                "title": "Control Flow, Loops & Data Collections",
                "description": "Control your code's path. Master if-statements, while loops, for loops, and basic collection structures (Lists, Tuples, Dictionaries, Sets).",
                "duration_weeks": "Week 2",
                "resources": [
                    {
                        "id": "res_py_realpython",
                        "title": "Real Python: Python Collections and Lists",
                        "url": "https://realpython.com/python-lists-tuples/",
                        "type": "article",
                        "description": "In-depth visual articles and exercises on mutating, slicing, and querying Python sequences.",
                        "difficulty": "beginner"
                    }
                ],
                "milestone_project": "Build a command-line Inventory Tracker for a store (using dicts and lists) supporting add/remove/search.",
                "status": "pending"
            },
            {
                "id": "py_step3",
                "title": "Functions, Error Handling & File I/O",
                "description": "Write reusable blocks. Learn custom function definition, parameters, return values, exception handling (try-except), and writing/reading local text files.",
                "duration_weeks": "Week 3",
                "resources": [
                    {
                        "id": "res_py_boring_stuff",
                        "title": "Automate the Boring Stuff with Python Book",
                        "url": "https://automatetheboringstuff.com/",
                        "type": "book",
                        "description": "Learn practical coding tasks: manipulating files, parsing directories, and scripting tasks.",
                        "difficulty": "beginner"
                    }
                ],
                "milestone_project": "Write a log parser script that reads an server log file and generates a summary report of errors to a new file.",
                "status": "pending"
            },
            {
                "id": "py_step4",
                "title": "Object-Oriented Programming (OOP) & Modules",
                "description": "Understand structured programming. Learn how to write Classes, define class properties and methods, implement inheritance, and structure code using external import packages.",
                "duration_weeks": "Week 4",
                "resources": [
                    {
                        "id": "res_py_oop_guide",
                        "title": "Real Python: Object-Oriented Programming (OOP) in Python 3",
                        "url": "https://realpython.com/python3-object-oriented-programming/",
                        "type": "article",
                        "description": "Clear step-by-step introduction to defining classes, constructors, methods, and base overrides.",
                        "difficulty": "intermediate"
                    }
                ],
                "milestone_project": "Build a CLI Library Catalog system modeling books, users, and borrowing transactions via OOP concepts.",
                "status": "pending"
            }
        ]
    },
    "ui_ux_design": {
        "id": "ui_ux_path",
        "title": "UI/UX Design Fundamentals",
        "summary": "Learn user-centric design frameworks. Transition from user empathy research, wireframing, color theory, and typographic systems to high-fidelity clickable mockups using modern design software.",
        "difficulty": "beginner",
        "weekly_hours": 5,
        "duration_weeks": 4,
        "steps": [
            {
                "id": "uiux_step1",
                "title": "UX Research, Empathy & Wireframing",
                "description": "Learn user-centered research. Conduct interviews, create user personas, construct user journeys, and sketch initial low-fidelity layouts/wireframes.",
                "duration_weeks": "Week 1",
                "resources": [
                    {
                        "id": "res_nngroup",
                        "title": "Nielsen Norman Group UX Basics Articles",
                        "url": "https://www.nngroup.com/articles/ten-usability-heuristics/",
                        "type": "article",
                        "description": "The golden rules of web usability heuristics and research methodologies.",
                        "difficulty": "beginner"
                    },
                    {
                        "id": "res_google_ux",
                        "title": "Google UX Design Professional Certificate",
                        "url": "https://www.coursera.org/professional-certificates/google-ux-design",
                        "type": "course",
                        "description": "Structured curriculum covering full-scope UX design foundations and tool configurations.",
                        "difficulty": "beginner"
                    }
                ],
                "milestone_project": "Create user research profiles, personas, and paper wireframe sketches for a local organic food delivery app.",
                "status": "pending"
            },
            {
                "id": "uiux_step2",
                "title": "Visual Design: Grid Systems, Hierarchy & Typography",
                "description": "Understand visual aesthetics. Learn typography selection, establishing visual hierarchy, designing consistent grid baselines, and custom color theory applications.",
                "duration_weeks": "Week 2",
                "resources": [
                    {
                        "id": "res_refactoring_ui",
                        "title": "Refactoring UI Book (by Tailwind creators)",
                        "url": "https://www.refactoringui.com/",
                        "type": "book",
                        "description": "Highly practical, visual design tricks to elevate UI layout structures from developer-grade to professional-grade.",
                        "difficulty": "beginner"
                    }
                ],
                "milestone_project": "Design a clean, visually balanced hero landing page on paper (or digital tool) emphasizing typography and clear CTA buttons.",
                "status": "pending"
            },
            {
                "id": "uiux_step3",
                "title": "High-Fidelity Component UI & Figma Mastery",
                "description": "Bring designs to digital form. Master Figma layout frames, auto-layout configurations, components libraries, and text/color styles.",
                "duration_weeks": "Week 3",
                "resources": [
                    {
                        "id": "res_figma_learn",
                        "title": "Figma Learn Portal",
                        "url": "https://learn.figma.com/",
                        "type": "course",
                        "description": "Official interactive video guides covering standard tools, components, and auto-layouts.",
                        "difficulty": "beginner"
                    }
                ],
                "milestone_project": "Build a responsive digital UI design library in Figma (buttons, cards, forms) utilizing Auto-Layout.",
                "status": "pending"
            },
            {
                "id": "uiux_step4",
                "title": "Interactive Prototyping & User Testing",
                "description": "Create clickable flows. Implement transitions, interactive component animations, overlay triggers in Figma, and conduct simulated user usability testing sessions.",
                "duration_weeks": "Week 4",
                "resources": [
                    {
                        "id": "res_figma_proto",
                        "title": "Figma: Guide to Prototyping and Transitions",
                        "url": "https://help.figma.com/hc/en-us/articles/360040314193-Guide-to-prototyping-in-Figma",
                        "type": "article",
                        "description": "Official guides detailing smart animations, hover behaviors, and page linkages.",
                        "difficulty": "intermediate"
                    }
                ],
                "milestone_project": "Build a high-fidelity, clickable mobile prototype of the food delivery app and complete a user testing report.",
                "status": "pending"
            }
        ]
    }
}
