function badgeClass(level) {
    return `badge badge-${String(level).toLowerCase()}`;
}

function formatScore(value) {
    return Number(value).toFixed(3);
}

function renderTimeline(rows) {
    const tbody = document.querySelector("#timeline-table tbody");
    tbody.innerHTML = rows.slice(-8).map((row) => `
        <tr>
            <td>${row.month}</td>
            <td>${row.q1}</td>
            <td>${row.q2}</td>
            <td>${row.q3}</td>
            <td>${row.q4}</td>
            <td>${row.negative_sentiment}</td>
            <td>${row.proxy_activity}</td>
            <td>${row.military_mobility}</td>
        </tr>
    `).join("");
}

function renderFactors(factors) {
    const el = document.getElementById("factor-list");
    el.innerHTML = factors.map((factor) => `
        <article class="factor">
            <div>
                <h4>${factor.label}</h4>
                <p>${factor.description}</p>
            </div>
            <strong>${formatScore(factor.score)}</strong>
        </article>
    `).join("");
}

function renderTargets(targets) {
    const el = document.getElementById("target-grid");
    el.innerHTML = targets.map((target) => {
        const level = target.priority_tier === "Tier 1" ? "red" : target.priority_tier === "Tier 2" ? "orange" : "blue";
        return `
            <article class="target-card">
                <div class="target-head">
                    <h4>${target.name}</h4>
                    <span class="badge badge-${level}">${target.priority_tier}</span>
                </div>
                <p>${target.type}</p>
                <dl>
                    <div><dt>意图置信度</dt><dd>${formatScore(target.intent_confidence)}</dd></div>
                    <div><dt>威胁指数</dt><dd>${formatScore(target.threat)}</dd></div>
                    <div><dt>价值评分</dt><dd>${formatScore(target.value_score)}</dd></div>
                </dl>
            </article>
        `;
    }).join("");
}

function renderScenarios(scenarios) {
    const el = document.getElementById("scenario-list");
    el.innerHTML = scenarios.map((scenario) => `
        <article class="scenario">
            <div class="scenario-top">
                <h4>${scenario.name}</h4>
                <strong>${formatScore(scenario.probability)}</strong>
            </div>
            <p>${scenario.summary}</p>
        </article>
    `).join("");
}

function renderRecommendations(recommendations) {
    const el = document.getElementById("recommendation-list");
    el.innerHTML = recommendations.map((item) => `<li>${item}</li>`).join("");
}

function updateTopMetrics(dashboard) {
    document.getElementById("overall-score").textContent = formatScore(dashboard.integrated.overall_score);
    document.getElementById("strategic-prob").textContent = formatScore(dashboard.strategic.risk_probability);
    document.getElementById("operational-threat").textContent = formatScore(dashboard.operational.threat_index);
    document.getElementById("simulation-score").textContent = formatScore(dashboard.simulation.consistency_score);
    document.getElementById("overall-badge").className = badgeClass(dashboard.integrated.overall_level);
    document.getElementById("overall-badge").textContent = dashboard.integrated.overall_level;
    document.getElementById("strategic-badge").className = badgeClass(dashboard.strategic.risk_level);
    document.getElementById("strategic-badge").textContent = dashboard.strategic.risk_level;
    document.getElementById("operational-badge").className = badgeClass(dashboard.operational.risk_level);
    document.getElementById("operational-badge").textContent = dashboard.operational.risk_level;
    document.getElementById("hero-summary").textContent = dashboard.integrated.recommendations[0];
    document.getElementById("strategic-summary").textContent = dashboard.strategic.summary;
    document.getElementById("operational-summary").textContent = dashboard.operational.summary;
    document.getElementById("simulation-summary").textContent = dashboard.simulation.summary;
}

async function refreshDashboard() {
    const button = document.getElementById("refresh-button");
    button.disabled = true;
    button.textContent = "刷新中...";
    try {
        const response = await fetch("/api/dashboard");
        const dashboard = await response.json();
        updateTopMetrics(dashboard);
        renderTimeline(dashboard.timeline);
        renderFactors(dashboard.strategic.top_factors);
        renderTargets(dashboard.operational.targets);
        renderScenarios(dashboard.simulation.scenarios);
        renderRecommendations(dashboard.integrated.recommendations);
    } finally {
        button.disabled = false;
        button.textContent = "刷新数据";
    }
}

document.getElementById("refresh-button").addEventListener("click", refreshDashboard);
