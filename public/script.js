"use strict";

const ASSISTANT_API = "http://127.0.0.1:8080";

let allArticles = [];
let currentCategory = "All";


function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function getArticleScore(article) {
    const value = article.ai_score ?? article.score ?? 0;
    const score = Number(value);

    return Number.isFinite(score) ? score : 0;
}


async function loadIntelligence() {
    const content = document.getElementById("content");

    try {
        const response = await fetch("website_data.json", {
            cache: "no-store"
        });

        if (!response.ok) {
            throw new Error(
                `website_data.json returned HTTP ${response.status}`
            );
        }

        const data = await response.json();
        const categories = data.categories ?? {};

        allArticles = [];

        let highestScore = 0;

        for (const [category, articles] of Object.entries(categories)) {
            if (!Array.isArray(articles)) {
                continue;
            }

            for (const article of articles) {
                const normalizedArticle = {
                    ...article,
                    category: article.category || category
                };

                const score = getArticleScore(normalizedArticle);

                highestScore = Math.max(highestScore, score);
                allArticles.push(normalizedArticle);
            }
        }

        document.getElementById("totalArticles").textContent =
            allArticles.length;

        document.getElementById("totalCategories").textContent =
            Object.keys(categories).length;

        document.getElementById("highestScore").textContent =
            highestScore;

        buildCategoryButtons(Object.keys(categories));
        renderArticles();

    } catch (error) {
        console.error(error);

        content.innerHTML = `
            <div class="error">
                Could not load website_data.json.<br>
                ${escapeHtml(error.message)}
            </div>
        `;
    }
}


function buildCategoryButtons(categories) {
    const buttonArea = document.getElementById("buttons");

    buttonArea.innerHTML = "";

    const allButton = document.createElement("button");

    allButton.type = "button";
    allButton.textContent = "All";
    allButton.classList.add("active");

    allButton.addEventListener("click", () => {
        setCategory("All", allButton);
    });

    buttonArea.appendChild(allButton);

    for (const category of categories) {
        const button = document.createElement("button");

        button.type = "button";
        button.textContent = category;

        button.addEventListener("click", () => {
            setCategory(category, button);
        });

        buttonArea.appendChild(button);
    }
}


function setCategory(category, selectedButton) {
    currentCategory = category;

    document
        .querySelectorAll("#buttons button")
        .forEach(button => {
            button.classList.remove("active");
        });

    selectedButton.classList.add("active");

    renderArticles();
}


function renderArticles() {
    const searchInput = document.getElementById("search");
    const content = document.getElementById("content");

    const searchValue = searchInput.value
        .trim()
        .toLowerCase();

    const filtered = allArticles.filter(article => {
        const categoryMatch =
            currentCategory === "All"
            || article.category === currentCategory;

        const searchableText = [
            article.title,
            article.description,
            article.summary,
            article.source,
            article.category,
            article.region,
            article.country,
            article.language,
            article.published,
            article.priority_level,
            article.link
        ]
            .filter(Boolean)
            .join(" ")
            .toLowerCase();

        return (
            categoryMatch
            && searchableText.includes(searchValue)
        );
    });

    filtered.sort((first, second) => {
        return (
            getArticleScore(second)
            - getArticleScore(first)
        );
    });

    if (filtered.length === 0) {
        content.innerHTML = `
            <div class="empty">
                No intelligence found.
            </div>
        `;

        return;
    }

    content.innerHTML = filtered
        .map(createArticleCard)
        .join("");
}


function createArticleCard(article) {
    const score = getArticleScore(article);

    const title = escapeHtml(
        article.title || "Untitled article"
    );

    const link = escapeHtml(
        article.link || "#"
    );

    const category = escapeHtml(
        article.category || "Uncategorized"
    );

    const priority = escapeHtml(
        article.priority_level || "Standard"
    );

    const source = escapeHtml(
        article.source || "Unknown source"
    );

    const region = escapeHtml(
        article.region || "N/A"
    );

    const country = escapeHtml(
        article.country || "N/A"
    );

    const language = escapeHtml(
        article.language || "N/A"
    );

    const published = escapeHtml(
        article.published || "Date unavailable"
    );

    return `
        <article class="card">

            <div class="score-row">
                <span>Score ${score}</span>
                <span>${category}</span>
                <span>${priority}</span>
            </div>

            <h3>
                <a
                    href="${link}"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    ${title}
                </a>
            </h3>

            <div class="meta">
                Source: ${source}<br>
                Region: ${region}
                &nbsp;|&nbsp;
                Country: ${country}
                &nbsp;|&nbsp;
                Language: ${language}<br>
                Published: ${published}
            </div>

        </article>
    `;
}


function setAssistantStatus(status, text) {
    const statusElement =
        document.getElementById("assistantStatus");

    statusElement.className =
        `assistant-status ${status}`;

    statusElement.textContent = text;
}


async function checkAssistantApi() {
    setAssistantStatus(
        "checking",
        "Checking API"
    );

    try {
        const response = await fetch(
            `${ASSISTANT_API}/health`,
            {
                method: "GET",
                cache: "no-store"
            }
        );

        if (!response.ok) {
            throw new Error(
                `HTTP ${response.status}`
            );
        }

        const data = await response.json();

        if (data.status !== "ok") {
            throw new Error(
                "Unexpected API response"
            );
        }

        setAssistantStatus(
            "online",
            "AI Online"
        );

        return true;

    } catch (error) {
        console.error(
            "Assistant API unavailable:",
            error
        );

        setAssistantStatus(
            "offline",
            "AI Offline"
        );

        return false;
    }
}


function addChatMessage(role, text, extraClass = "") {
    const messages =
        document.getElementById("chatMessages");

    const message = document.createElement("div");

    message.className = [
        "chat-message",
        role === "user"
            ? "user-message"
            : "assistant-message",
        extraClass
    ]
        .filter(Boolean)
        .join(" ");

    const roleLabel = document.createElement("div");

    roleLabel.className = "message-role";
    roleLabel.textContent =
        role === "user"
            ? "YOU"
            : "LKS AI";

    const content = document.createElement("div");

    content.className = "message-content";
    content.textContent = text;

    message.appendChild(roleLabel);
    message.appendChild(content);

    messages.appendChild(message);

    messages.scrollTop =
        messages.scrollHeight;

    return message;
}


function setAssistantBusy(isBusy) {
    const sendButton =
        document.getElementById("assistantSend");

    const questionInput =
        document.getElementById("assistantQuestion");

    sendButton.disabled = isBusy;
    questionInput.disabled = isBusy;

    sendButton.textContent =
        isBusy
            ? "Thinking..."
            : "Ask LKS AI";
}


async function askAssistant(question) {
    const cleanQuestion = question.trim();

    if (!cleanQuestion) {
        return;
    }

    addChatMessage(
        "user",
        cleanQuestion
    );

    setAssistantBusy(true);

    const thinkingMessage = addChatMessage(
        "assistant",
        "Searching the verified LKS-HUB knowledge base...",
        "thinking-message"
    );

    try {
        const response = await fetch(
            `${ASSISTANT_API}/ask`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: cleanQuestion
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error
                || `Assistant returned HTTP ${response.status}`
            );
        }

        thinkingMessage.remove();

        addChatMessage(
            "assistant",
            data.answer
            || "The assistant returned an empty answer."
        );

        setAssistantStatus(
            "online",
            "AI Online"
        );

    } catch (error) {
        console.error(error);

        thinkingMessage.remove();

        addChatMessage(
            "assistant",
            (
                "The LKS AI Assistant is currently unavailable. "
                + "Make sure assistant_api.py is running on port 8080.\n\n"
                + `Technical detail: ${error.message}`
            ),
            "error-message"
        );

        setAssistantStatus(
            "offline",
            "AI Offline"
        );

    } finally {
        setAssistantBusy(false);

        document
            .getElementById("assistantQuestion")
            .focus();
    }
}


function initializeAssistant() {
    const form =
        document.getElementById("assistantForm");

    const questionInput =
        document.getElementById("assistantQuestion");

    form.addEventListener("submit", event => {
        event.preventDefault();

        const question = questionInput.value;

        questionInput.value = "";

        askAssistant(question);
    });

    questionInput.addEventListener(
        "keydown",
        event => {
            if (
                event.key === "Enter"
                && !event.shiftKey
            ) {
                event.preventDefault();
                form.requestSubmit();
            }
        }
    );

    document
        .querySelectorAll(".suggestion-button")
        .forEach(button => {
            button.addEventListener("click", () => {
                const question =
                    button.dataset.question || "";

                questionInput.value = question;
                form.requestSubmit();
            });
        });

    checkAssistantApi();
}


document
    .getElementById("search")
    .addEventListener(
        "input",
        renderArticles
    );


document.addEventListener(
    "DOMContentLoaded",
    () => {
        loadIntelligence();
        initializeAssistant();
    }
);