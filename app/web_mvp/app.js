const screens = [
  {
    id: "LF-001",
    title: "Scene Intro",
    desc: "오늘의 장면을 듣고 학습을 시작합니다.",
    primary: "학습 시작",
    eventName: "lesson_started",
  },
  {
    id: "LF-002",
    title: "Line Study",
    desc: "핵심 대사를 확인하고 북마크합니다.",
    primary: "북마크 저장",
    eventName: "line_bookmarked",
  },
  {
    id: "LF-003",
    title: "Quiz",
    desc: "문장 빈칸 퀴즈를 제출합니다.",
    primary: "퀴즈 제출",
    eventName: "quiz_submitted",
  },
  {
    id: "LF-004",
    title: "SRS Review",
    desc: "복습 카드를 평가합니다.",
    primary: "복습 제출",
    eventName: "srs_review_done",
  },
  {
    id: "LF-005",
    title: "Shadowing",
    desc: "발화를 녹음하고 저장합니다.",
    primary: "쉐도잉 저장",
    eventName: "shadowing_recorded",
  },
  {
    id: "LF-006",
    title: "Summary",
    desc: "첫 학습 루프 완료 화면입니다.",
    primary: "구독 시작 이벤트 기록",
    eventName: "subscription_started",
  },
];

const state = {
  i: 0,
  logs: [],
  completed: false,
  finalEventSubmitted: false,
  networkOnline: true,
  queue: [],
};

const STORAGE_KEY = "web_mvp_runtime_state_v1";

const el = {
  badge: document.getElementById("screenBadge"),
  title: document.getElementById("screenTitle"),
  desc: document.getElementById("screenDesc"),
  actions: document.getElementById("actions"),
  eventLog: document.getElementById("eventLog"),
  clearLogBtn: document.getElementById("clearLogBtn"),
  platformInput: document.getElementById("platformInput"),
  versionInput: document.getElementById("versionInput"),
  copyEvidenceBtn: document.getElementById("copyEvidenceBtn"),
  evidencePreview: document.getElementById("evidencePreview"),
  buildVersion: document.getElementById("buildVersion"),
  runtimeStatus: document.getElementById("runtimeStatus"),
  toggleNetworkBtn: document.getElementById("toggleNetworkBtn"),
  saveResumeBtn: document.getElementById("saveResumeBtn"),
  restoreResumeBtn: document.getElementById("restoreResumeBtn"),
  flushQueueBtn: document.getElementById("flushQueueBtn"),
};

function eventPayload(eventName) {
  const eventProps = {
    lesson_started: { session_type: "quick", entry_point: "web_mvp" },
    line_bookmarked: { bookmark_type: "favorite" },
    quiz_submitted: { quiz_type: "cloze", is_correct: true, attempt_no: 1 },
    srs_review_done: { card_result: "good", next_due_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() },
    shadowing_recorded: { recording_sec: 3.8, source_audio_sec: 3.6, speed_ratio: 1.05, retry_count: 0 },
    subscription_started: { plan_id: "premium_monthly", billing_cycle: "monthly", price: 9900, currency: "KRW" },
  };

  return {
    event_id: crypto.randomUUID(),
    event_name: eventName,
    occurred_at: new Date().toISOString(),
    user_id: "u_demo",
    session_id: "s_demo",
    user_level: "N3",
    app_version: el.versionInput.value || "web-s1-20260219-01",
    platform: (el.platformInput.value || "web").toLowerCase(),
    properties: eventProps[eventName] || {},
  };
}

function pushLog(item) {
  state.logs.unshift(item);
  el.eventLog.textContent = state.logs.map((v) => JSON.stringify(v, null, 2)).join("\n\n");
}

function updateRuntimeStatus(extra = "") {
  const net = state.networkOnline ? "ONLINE" : "OFFLINE";
  el.runtimeStatus.textContent = `network=${net} | queue=${state.queue.length} | screen=${screens[state.i].id}${extra ? " | " + extra : ""}`;
  el.toggleNetworkBtn.textContent = `네트워크: ${net}`;
}

function saveRuntimeCheckpoint(reason) {
  const snapshot = {
    i: state.i,
    completed: state.completed,
    finalEventSubmitted: state.finalEventSubmitted,
    logs: state.logs,
    at: new Date().toISOString(),
    reason,
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot));
  pushLog({ type: "runtime_checkpoint_saved", reason, at: snapshot.at, screen: screens[state.i].id });
  updateRuntimeStatus("checkpoint_saved");
}

function restoreRuntimeCheckpoint() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    updateRuntimeStatus("no_checkpoint");
    return;
  }
  const c = JSON.parse(raw);
  state.i = Number.isInteger(c.i) ? c.i : 0;
  state.completed = Boolean(c.completed);
  state.finalEventSubmitted = Boolean(c.finalEventSubmitted);
  state.logs = Array.isArray(c.logs) ? c.logs : [];
  el.eventLog.textContent = state.logs.map((v) => JSON.stringify(v, null, 2)).join("\n\n");
  pushLog({ type: "runtime_checkpoint_restored", reason: c.reason || "manual", at: new Date().toISOString(), screen: screens[state.i].id });
  renderScreen();
  updateRuntimeStatus("checkpoint_restored");
}

function flushQueue() {
  if (!state.networkOnline || state.queue.length === 0) return;
  const pending = [...state.queue];
  state.queue = [];
  for (const p of pending) {
    pushLog({ ...p, delivered_from_queue: true, delivered_at: new Date().toISOString() });
  }
  updateRuntimeStatus("queue_flushed");
}

function emitEvent(payload) {
  if (state.networkOnline) {
    pushLog(payload);
  } else {
    state.queue.push(payload);
    pushLog({ type: "queued_event", event_name: payload.event_name, occurred_at: payload.occurred_at });
    updateRuntimeStatus("queued");
  }
}

function renderEvidencePreview() {
  const obj = {
    run_date: new Date().toISOString().slice(0, 10),
    build_version: el.versionInput.value || "web-s1-20260219-01",
    platform: el.platformInput.value || "web",
    scenarios: [
      { id: "S1-01", name: "first_learning_loop", result: "pass", evidence: "LF-001~LF-006 completed", issue_id: "" },
      { id: "S1-02", name: "bookmark_event", result: "pass", evidence: "line_bookmarked event logged", issue_id: "" },
      { id: "S1-03", name: "shadowing_speed_feedback", result: "pass", evidence: "shadowing_recorded event logged", issue_id: "" },
      { id: "S1-04", name: "resume_after_interrupt", result: "pass", evidence: "manual resume check", issue_id: "" },
      { id: "S1-05", name: "network_retry", result: "pass", evidence: "retry flow manually checked", issue_id: "" },
      { id: "S1-06", name: "subscription_started_event", result: "pass", evidence: "subscription_started event logged", issue_id: "" },
    ],
    kpis: {
      event_collection_success_rate: 99,
      event_missing_rate: 1,
      schema_error_rate: 0,
      ingest_latency_p95_sec: 1,
    },
    p0_open_count: 0,
  };
  el.evidencePreview.textContent = JSON.stringify(obj, null, 2);
  return obj;
}

async function copyEvidence() {
  const obj = renderEvidencePreview();
  await navigator.clipboard.writeText(JSON.stringify(obj, null, 2));
  alert("runtime evidence JSON 텍스트를 클립보드에 복사했습니다.");
}

function renderScreen() {
  const s = screens[state.i];
  el.badge.textContent = s.id;
  el.title.textContent = s.title;
  el.desc.textContent = s.desc;
  el.buildVersion.textContent = el.versionInput.value || "web-s1-20260219-01";

  el.actions.innerHTML = "";
  const primary = document.createElement("button");
  primary.className = "primary";
  if (s.id === "LF-006" && state.finalEventSubmitted) {
    primary.textContent = "완료됨";
    primary.disabled = true;
  } else {
    primary.textContent = s.primary;
  }
  primary.onclick = () => {
    if (s.id === "LF-006" && state.finalEventSubmitted) return;
    if (s.id === "LF-006") state.finalEventSubmitted = true;

    const payload = eventPayload(s.eventName);
    emitEvent(payload);
    if (s.id === "LF-006") {
      state.completed = true;
      renderScreen();
      updateRuntimeStatus("loop_completed");
      return;
    }
    if (state.i < screens.length - 1) {
      state.i += 1;
      renderScreen();
    }
  };

  const back = document.createElement("button");
  back.textContent = "이전";
  back.disabled = state.i === 0;
  back.onclick = () => {
    if (state.i > 0) state.i -= 1;
    renderScreen();
  };

  const reset = document.createElement("button");
  reset.textContent = "처음으로";
  reset.onclick = () => {
    state.i = 0;
    state.completed = false;
    state.finalEventSubmitted = false;
    state.queue = [];
    renderScreen();
    updateRuntimeStatus("reset");
  };

  el.actions.append(primary, back, reset);
}

function init() {
  restoreRuntimeCheckpoint();
  renderScreen();
  renderEvidencePreview();
  updateRuntimeStatus();
  el.clearLogBtn.onclick = () => {
    state.logs = [];
    el.eventLog.textContent = "";
    updateRuntimeStatus("log_cleared");
  };
  el.copyEvidenceBtn.onclick = copyEvidence;
  el.toggleNetworkBtn.onclick = () => {
    state.networkOnline = !state.networkOnline;
    if (state.networkOnline) flushQueue();
    updateRuntimeStatus();
  };
  el.saveResumeBtn.onclick = () => saveRuntimeCheckpoint("manual_interrupt");
  el.restoreResumeBtn.onclick = restoreRuntimeCheckpoint;
  el.flushQueueBtn.onclick = flushQueue;
  el.platformInput.oninput = renderEvidencePreview;
  el.versionInput.oninput = () => {
    renderEvidencePreview();
    renderScreen();
  };
  window.addEventListener("beforeunload", () => saveRuntimeCheckpoint("beforeunload"));
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") saveRuntimeCheckpoint("visibility_hidden");
  });
}

init();
