// Global State
let currentRoadmap = null;
let completedStepIds = [];
let allResources = [];

// DOM Elements
const modeBadge = document.getElementById("modeBadge");
const toggleSettingsBtn = document.getElementById("toggleSettingsBtn");
const closeSettingsBtn = document.getElementById("closeSettingsBtn");
const settingsDrawer = document.getElementById("settingsDrawer");
const geminiApiKeyInput = document.getElementById("geminiApiKey");
const toggleApiKeyVisibility = document.getElementById("toggleApiKeyVisibility");
const saveSettingsBtn = document.getElementById("saveSettingsBtn");
const clearSettingsBtn = document.getElementById("clearSettingsBtn");
const settingsStatus = document.getElementById("settingsStatus");

const goalForm = document.getElementById("goalForm");
const durationInput = document.getElementById("duration");
const durationVal = document.getElementById("durationVal");
const weeklyHoursInput = document.getElementById("weeklyHours");
const hoursVal = document.getElementById("hoursVal");

const emptyState = document.getElementById("emptyState");
const loadingState = document.getElementById("loadingState");
const loadingText = document.getElementById("loadingText");
const roadmapDashboard = document.getElementById("roadmapDashboard");
const progressCard = document.getElementById("progressCard");
const progressBar = document.getElementById("progressBar");
const progressPercent = document.getElementById("progressPercent");
const completedStepsFraction = document.getElementById("completedStepsFraction");

const roadmapTitle = document.getElementById("roadmapTitle");
const roadmapSummary = document.getElementById("roadmapSummary");
const metaDifficulty = document.getElementById("metaDifficulty");
const metaDuration = document.getElementById("metaDuration");
const metaHours = document.getElementById("metaHours");
const timelineContainer = document.getElementById("timelineContainer");

const adaptPathBtn = document.getElementById("adaptPathBtn");
const adaptModal = document.getElementById("adaptModal");
const closeAdaptModalBtn = document.getElementById("closeAdaptModalBtn");
const cancelAdaptBtn = document.getElementById("cancelAdaptBtn");
const submitAdaptBtn = document.getElementById("submitAdaptBtn");
const adaptationFeedback = document.getElementById("adaptationFeedback");

const toggleLibraryBtn = document.getElementById("toggleLibraryBtn");
const libraryModal = document.getElementById("libraryModal");
const closeLibraryModalBtn = document.getElementById("closeLibraryModalBtn");
const libraryGrid = document.getElementById("libraryGrid");
const librarySearchInput = document.getElementById("librarySearchInput");

// Initialize application
document.addEventListener("DOMContentLoaded", () => {
    // Load saved settings
    loadSettings();
    
    // Set up range slider listeners
    durationInput.addEventListener("input", (e) => {
        durationVal.textContent = `${e.target.value} Weeks`;
    });
    
    weeklyHoursInput.addEventListener("input", (e) => {
        hoursVal.textContent = `${e.target.value} Hours/week`;
    });
    
    // Toggle Settings drawer
    toggleSettingsBtn.addEventListener("click", () => {
        settingsDrawer.classList.add("open");
    });
    
    closeSettingsBtn.addEventListener("click", () => {
        settingsDrawer.classList.remove("open");
    });
    
    // Password toggle
    toggleApiKeyVisibility.addEventListener("click", () => {
        const type = geminiApiKeyInput.type === "password" ? "text" : "password";
        geminiApiKeyInput.type = type;
        toggleApiKeyVisibility.querySelector("i").className = 
            type === "password" ? "fa-solid fa-eye" : "fa-solid fa-eye-slash";
    });
    
    // Save Settings
    saveSettingsBtn.addEventListener("click", () => {
        const key = geminiApiKeyInput.value.trim();
        if (key) {
            localStorage.setItem("gemini_api_key", key);
            showStatus("API Key saved successfully!", "success");
            updateModeBadge(true);
            setTimeout(() => settingsDrawer.classList.remove("open"), 1000);
        } else {
            showStatus("Please enter a valid key.", "error");
        }
    });
    
    // Clear Settings
    clearSettingsBtn.addEventListener("click", () => {
        localStorage.removeItem("gemini_api_key");
        geminiApiKeyInput.value = "";
        showStatus("API Key cleared.", "info");
        updateModeBadge(false);
    });
    
    // Form Submit (Generate Roadmap)
    goalForm.addEventListener("submit", (e) => {
        e.preventDefault();
        generateRoadmap();
    });
    
    // Modal controls for Adapt Path
    adaptPathBtn.addEventListener("click", () => {
        adaptationFeedback.value = "";
        adaptModal.classList.add("open");
    });
    
    closeAdaptModalBtn.addEventListener("click", () => {
        adaptModal.classList.remove("open");
    });
    
    cancelAdaptBtn.addEventListener("click", () => {
        adaptModal.classList.remove("open");
    });
    
    submitAdaptBtn.addEventListener("click", () => {
        adaptRoadmap();
    });
    
    // Modal controls for RAG Library
    toggleLibraryBtn.addEventListener("click", () => {
        loadLibrary();
        libraryModal.classList.add("open");
    });
    
    closeLibraryModalBtn.addEventListener("click", () => {
        libraryModal.classList.remove("open");
    });
    
    // RAG Search filter keyup
    librarySearchInput.addEventListener("input", filterLibrary);
});

// Load Settings from LocalStorage
function loadSettings() {
    const key = localStorage.getItem("gemini_api_key");
    if (key) {
        geminiApiKeyInput.value = key;
        updateModeBadge(true);
    } else {
        updateModeBadge(false);
    }
}

// Update Mode indicator badge
function updateModeBadge(hasKey) {
    if (hasKey) {
        modeBadge.className = "status-badge live-active";
        modeBadge.querySelector("i").className = "fa-solid fa-toggle-on";
        modeBadge.querySelector("span").textContent = "AI Mode (Gemini API)";
    } else {
        modeBadge.className = "status-badge";
        modeBadge.querySelector("i").className = "fa-solid fa-toggle-off";
        modeBadge.querySelector("span").textContent = "Demo Mode (Mock LLM)";
    }
}

// Show settings drawer feedback message
function showStatus(msg, type) {
    settingsStatus.textContent = msg;
    settingsStatus.style.color = 
        type === "success" ? "var(--color-success)" : 
        type === "error" ? "var(--color-danger)" : "var(--text-secondary)";
    setTimeout(() => { settingsStatus.textContent = ""; }, 3000);
}

// Generate Roadmap via backend
async function generateRoadmap() {
    const goal = document.getElementById("learningGoal").value.trim();
    const difficulty = document.getElementById("difficulty").value;
    const learningStyle = document.getElementById("learningStyle").value;
    const durationWeeks = parseInt(durationInput.value);
    const weeklyHours = parseInt(weeklyHoursInput.value);
    const apiKey = localStorage.getItem("gemini_api_key");

    if (!goal) return;

    // Transition to loading UI
    emptyState.style.display = "none";
    roadmapDashboard.style.display = "none";
    progressCard.style.display = "none";
    loadingState.style.display = "flex";
    
    // Start simulation of Multiagent transitions
    const step1 = document.getElementById("loadStep1");
    const step2 = document.getElementById("loadStep2");
    const step3 = document.getElementById("loadStep3");
    
    // Set initial loading step
    loadingText.textContent = "Analyzing learning goals...";
    step1.className = "load-step active";
    step2.className = "load-step";
    step3.className = "load-step";

    const loadingPhrases = [
        { text: "Parsing request parameters...", delay: 1000 },
        { text: "Goal Analyzer Agent is planning sub-milestones...", delay: 2500 },
        { text: "Resource Retriever Agent (RAG) is scanning documents...", delay: 4500 },
        { text: "Finding best books, courses and tutorial videos...", delay: 6500 },
        { text: "Roadmap Generator Agent is designing milestone projects...", delay: 8500 },
        { text: "Synthesizing full study schedule...", delay: 11000 }
    ];

    const loadTimers = [];
    loadingPhrases.forEach(phrase => {
        const timer = setTimeout(() => {
            loadingText.textContent = phrase.text;
            if (phrase.text.includes("Retriever")) {
                step1.className = "load-step done";
                step1.querySelector("i").className = "fa-solid fa-circle-check";
                step2.className = "load-step active";
            } else if (phrase.text.includes("Roadmap")) {
                step2.className = "load-step done";
                step2.querySelector("i").className = "fa-solid fa-circle-check";
                step3.className = "load-step active";
            }
        }, phrase.delay);
        loadTimers.push(timer);
    });

    try {
        const response = await fetch("/api/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                goal: goal,
                difficulty: difficulty,
                duration_weeks: durationWeeks,
                weekly_hours: weeklyHours,
                learning_style: learningStyle,
                api_key: apiKey
            })
        });

        // Clear all loading timers
        loadTimers.forEach(clearTimeout);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const roadmap = await response.json();
        
        // Save to state
        currentRoadmap = roadmap;
        completedStepIds = [];
        
        // Finalize spinner checks
        step3.className = "load-step done";
        step3.querySelector("i").className = "fa-solid fa-circle-check";
        
        setTimeout(() => {
            loadingState.style.display = "none";
            renderRoadmap();
        }, 600);

    } catch (error) {
        console.error("Error generating roadmap:", error);
        loadTimers.forEach(clearTimeout);
        loadingState.style.display = "none";
        emptyState.style.display = "flex";
        alert("Failed to generate roadmap. Please check backend logs or try again.");
    }
}

// Adapt Roadmap based on feedback
async function adaptRoadmap() {
    const feedback = adaptationFeedback.value.trim();
    const apiKey = localStorage.getItem("gemini_api_key");

    if (!feedback || !currentRoadmap) return;

    // Close adapt modal
    adaptModal.classList.remove("open");

    // Show loading
    roadmapDashboard.style.display = "none";
    progressCard.style.display = "none";
    loadingState.style.display = "flex";
    
    // Set loading step states
    const step1 = document.getElementById("loadStep1");
    const step2 = document.getElementById("loadStep2");
    const step3 = document.getElementById("loadStep3");
    
    loadingText.textContent = "Adaptive Planner Agent is processing feedback...";
    step1.className = "load-step active";
    step1.querySelector("i").className = "fa-solid fa-circle-notch fa-spin";
    step2.className = "load-step";
    step2.querySelector("i").className = "fa-solid fa-circle-notch fa-spin";
    step3.className = "load-step";
    step3.querySelector("i").className = "fa-solid fa-circle-notch fa-spin";

    setTimeout(() => {
        loadingText.textContent = "Re-planning subsequent milestones...";
        step1.className = "load-step done";
        step1.querySelector("i").className = "fa-solid fa-circle-check";
        step2.className = "load-step active";
    }, 1500);

    setTimeout(() => {
        loadingText.textContent = "Fetching custom matching resources...";
        step2.className = "load-step done";
        step2.querySelector("i").className = "fa-solid fa-circle-check";
        step3.className = "load-step active";
    }, 3000);

    try {
        const response = await fetch("/api/adapt", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                roadmap: currentRoadmap,
                feedback: feedback,
                completed_step_ids: completedStepIds,
                api_key: apiKey
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const adaptedRoadmap = await response.json();
        
        // Save to state
        currentRoadmap = adaptedRoadmap;
        
        // Ensure steps marked as completed in completedStepIds stay marked
        currentRoadmap.steps.forEach(step => {
            if (completedStepIds.includes(step.id)) {
                step.status = "completed";
            }
        });
        
        step3.className = "load-step done";
        step3.querySelector("i").className = "fa-solid fa-circle-check";

        setTimeout(() => {
            loadingState.style.display = "none";
            renderRoadmap();
        }, 600);

    } catch (error) {
        console.error("Error adapting roadmap:", error);
        loadingState.style.display = "none";
        renderRoadmap();
        alert("Failed to adapt roadmap. Please try again.");
    }
}

// Render the roadmap state into the UI
function renderRoadmap() {
    if (!currentRoadmap) return;

    // Display wrappers
    roadmapDashboard.style.display = "block";
    progressCard.style.display = "block";

    // Set Header summaries
    roadmapTitle.textContent = currentRoadmap.title;
    roadmapSummary.textContent = currentRoadmap.summary;
    metaDifficulty.textContent = capitalizeFirstLetter(currentRoadmap.difficulty);
    metaDuration.textContent = `${currentRoadmap.duration_weeks} Weeks`;
    metaHours.textContent = `${currentRoadmap.weekly_hours} Hours/week`;

    // Clear timeline container
    timelineContainer.innerHTML = "";

    // Determine current active step (first pending step)
    let activeStepSet = false;

    currentRoadmap.steps.forEach((step, idx) => {
        const stepEl = document.createElement("div");
        stepEl.className = "timeline-step";
        
        // Assign status styles
        if (step.status === "completed" || completedStepIds.includes(step.id)) {
            stepEl.classList.add("completed");
        } else if (step.status === "struggling") {
            stepEl.classList.add("struggling");
            if (!activeStepSet) {
                stepEl.classList.add("active-step");
                activeStepSet = true;
            }
        } else {
            // Check if this is the first uncompleted step to make active
            if (!activeStepSet) {
                stepEl.classList.add("active-step");
                activeStepSet = true;
            }
        }

        // Draw Step Marker
        const marker = document.createElement("div");
        marker.className = "step-marker";
        marker.innerHTML = idx + 1;
        marker.addEventListener("click", () => toggleStepCompletion(step.id));
        stepEl.appendChild(marker);

        // Draw Step Content
        const content = document.createElement("div");
        content.className = "step-content";

        // Step Header
        const header = document.createElement("div");
        header.className = "step-header";
        
        const titleGroup = document.createElement("div");
        titleGroup.className = "step-title-group";
        const title = document.createElement("h3");
        title.textContent = step.title;
        titleGroup.appendChild(title);
        
        const duration = document.createElement("span");
        duration.className = "step-duration-badge";
        duration.textContent = step.duration_weeks;
        
        header.appendChild(titleGroup);
        header.appendChild(duration);
        content.appendChild(header);

        // Step Description
        const desc = document.createElement("p");
        desc.className = "step-desc";
        desc.textContent = step.description;
        content.appendChild(desc);

        // RAG Resources section
        if (step.resources && step.resources.length > 0) {
            const resTitle = document.createElement("div");
            resTitle.className = "step-resources-title";
            resTitle.textContent = "Curated Resources (RAG Matches)";
            content.appendChild(resTitle);

            const grid = document.createElement("div");
            grid.className = "resources-grid";

            step.resources.forEach(res => {
                const card = document.createElement("div");
                card.className = "resource-card";

                const resHeader = document.createElement("div");
                resHeader.className = "res-header";
                
                const rTitle = document.createElement("span");
                rTitle.className = "res-title";
                rTitle.textContent = res.title;
                
                const rTag = document.createElement("span");
                rTag.className = `res-tag tag-${res.type.toLowerCase()}`;
                rTag.textContent = res.type;

                resHeader.appendChild(rTitle);
                resHeader.appendChild(rTag);
                card.appendChild(resHeader);

                const rDesc = document.createElement("p");
                rDesc.className = "res-desc";
                rDesc.textContent = res.description;
                card.appendChild(rDesc);

                const rLink = document.createElement("a");
                rLink.className = "res-link";
                rLink.href = res.url;
                rLink.target = "_blank";
                rLink.innerHTML = `<i class="fa-solid fa-up-right-from-square"></i> Open Resource`;
                card.appendChild(rLink);

                grid.appendChild(card);
            });

            content.appendChild(grid);
        }

        // Milestone Project box
        const projectBox = document.createElement("div");
        projectBox.className = "project-box";
        
        const projHeader = document.createElement("div");
        projHeader.className = "project-box-header";
        
        const pTitle = document.createElement("span");
        pTitle.className = "project-title";
        pTitle.innerHTML = `<i class="fa-solid fa-laptop-code"></i> Milestone Verification`;
        
        // Complete project checkbox
        const isChecked = step.status === "completed" || completedStepIds.includes(step.id);
        const checkWrapper = document.createElement("label");
        checkWrapper.className = `checkbox-wrapper ${isChecked ? 'checked' : ''}`;
        checkWrapper.innerHTML = `
            <input type="checkbox" ${isChecked ? 'checked' : ''}>
            <span>${isChecked ? 'Completed' : 'Mark Done'}</span>
        `;
        checkWrapper.querySelector("input").addEventListener("change", () => toggleStepCompletion(step.id));

        projHeader.appendChild(pTitle);
        projHeader.appendChild(checkWrapper);
        projectBox.appendChild(projHeader);

        const pDesc = document.createElement("p");
        pDesc.className = "project-desc";
        pDesc.textContent = step.milestone_project;
        projectBox.appendChild(pDesc);

        content.appendChild(projectBox);
        stepEl.appendChild(content);
        timelineContainer.appendChild(stepEl);
    });

    updateProgress();
}

// Toggle Step Completion State
function toggleStepCompletion(stepId) {
    const stepIdx = currentRoadmap.steps.findIndex(s => s.id === stepId);
    if (stepIdx === -1) return;

    const step = currentRoadmap.steps[stepIdx];
    const isCompleted = completedStepIds.includes(stepId);

    if (isCompleted) {
        // Toggle off
        completedStepIds = completedStepIds.filter(id => id !== stepId);
        step.status = "pending";
    } else {
        // Toggle on
        completedStepIds.push(stepId);
        step.status = "completed";
    }

    renderRoadmap();
}

// Calculate and update progress metrics
function updateProgress() {
    if (!currentRoadmap || currentRoadmap.steps.length === 0) return;

    const total = currentRoadmap.steps.length;
    const completed = completedStepIds.length;
    const percent = Math.round((completed / total) * 100);

    progressBar.style.width = `${percent}%`;
    progressPercent.textContent = `${percent}% Completed`;
    completedStepsFraction.textContent = `${completed} of ${total} Steps`;
}

// Capitalize helper
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// Load RAG resource library database
async function loadLibrary() {
    if (allResources.length > 0) {
        renderLibrary(allResources);
        return;
    }

    try {
        const response = await fetch("/api/resources");
        if (!response.ok) throw new Error("Could not fetch resources");
        
        allResources = await response.json();
        renderLibrary(allResources);
    } catch (err) {
        console.error("Error loading RAG library:", err);
        libraryGrid.innerHTML = `<p style="grid-column: 1/-1; text-align: center; color: var(--color-danger);">Failed to load resources.</p>`;
    }
}

// Render library grid
function renderLibrary(resources) {
    libraryGrid.innerHTML = "";
    
    if (resources.length === 0) {
        libraryGrid.innerHTML = `<p style="grid-column: 1/-1; text-align: center; color: var(--text-muted);">No resources match filters.</p>`;
        return;
    }

    resources.forEach(res => {
        const item = document.createElement("div");
        item.className = "library-item panel-glass";
        
        item.innerHTML = `
            <div>
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
                    <h4 style="font-size:0.9rem; line-height:1.2; font-weight:600;">${res.title}</h4>
                    <span class="res-tag tag-${res.type.toLowerCase()}">${res.type}</span>
                </div>
                <p style="font-size:0.75rem; color:var(--text-secondary); margin-bottom:12px;">${res.description}</p>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid var(--border-color); padding-top:10px; margin-top:5px;">
                <span style="font-size:0.7rem; color:var(--text-muted); text-transform:uppercase; font-weight:700;">Level: ${res.difficulty}</span>
                <a href="${res.url}" target="_blank" class="res-link" style="font-size:0.75rem;"><i class="fa-solid fa-up-right-from-square"></i> Visit Site</a>
            </div>
        `;
        
        libraryGrid.appendChild(item);
    });
}

// Filter the RAG library search input
function filterLibrary() {
    const query = librarySearchInput.value.toLowerCase().trim();
    if (!query) {
        renderLibrary(allResources);
        return;
    }

    const filtered = allResources.filter(res => {
        return res.title.toLowerCase().includes(query) ||
               res.description.toLowerCase().includes(query) ||
               res.type.toLowerCase().includes(query) ||
               res.difficulty.toLowerCase().includes(query);
    });

    renderLibrary(filtered);
}
