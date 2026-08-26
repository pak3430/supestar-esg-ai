if ('scrollRestoration' in window.history) {
  window.history.scrollRestoration = 'manual';
}

const restorePageStart = () => window.scrollTo({ top: 0, left: 0, behavior: 'auto' });
window.addEventListener('pageshow', () => {
  restorePageStart();
  requestAnimationFrame(restorePageStart);
});

const messages = document.querySelector('#messages');
const form = document.querySelector('#chatForm');
const input = document.querySelector('#questionInput');
const sendButton = document.querySelector('#sendButton');
const resetButton = document.querySelector('#resetButton');
const quickPrompts = document.querySelector('#quickPrompts');
const runtimeState = document.querySelector('#runtimeState');
const initialMarkup = messages.innerHTML;
const conversation = [];
const CHAT_RETRY_DELAYS_MS = [700, 1600];
const RETRYABLE_HTTP_STATUS = new Set([404, 408, 425, 429, 500, 502, 503, 504]);

const escapeHtml = (value = '') => String(value)
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&#039;');

const scrollToBottom = () => {
  requestAnimationFrame(() => messages.scrollTo({ top: messages.scrollHeight, behavior: 'smooth' }));
};

function addUserMessage(question) {
  const node = document.querySelector('#userMessageTemplate').content.cloneNode(true);
  node.querySelector('p').textContent = question;
  messages.append(node);
  scrollToBottom();
}

function addLoading() {
  const node = document.querySelector('#loadingTemplate').content.cloneNode(true);
  messages.append(node);
  scrollToBottom();
  return messages.lastElementChild;
}

function statusClass(status) {
  return ({ PROCEED: 'proceed', REVIEW: 'review', STOP: 'stop' })[status] || 'stop';
}

function renderEvidence(evidence = []) {
  if (!evidence.length) return '<p class="muted">표시할 근거가 없습니다.</p>';
  return `<ul class="evidence-list">${evidence.map((item) => `
    <li><strong>${escapeHtml(item.claim || '근거')}</strong><br>${escapeHtml(item.sourceDocument || '')} · ${escapeHtml(item.section || '')}</li>
  `).join('')}</ul>`;
}

function renderActions(result) {
  const missing = (result.missingEvidence || []).map((item) => `누락: ${item}`);
  const actions = [...missing, ...(result.nextActions || [])];
  if (!actions.length) return '<p class="muted">현재 실행에서 추가 요청사항이 없습니다.</p>';
  return `<ul class="action-list">${actions.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul>`;
}

function renderDomainData(result) {
  const data = result.data || {};
  if (Array.isArray(data.orderedNodes)) {
    return `<div class="node-flow">${data.orderedNodes.map((node) => `<span>${escapeHtml(node)}</span>`).join('')}</div>`;
  }
  if (data.candidateScope !== undefined) {
    return `<table><tr><th>분류 후보</th><th>규칙 추적</th><th>미해결 입력</th></tr><tr><td>${escapeHtml(data.candidateScope || '미확정')}</td><td>${escapeHtml((data.ruleTrace || []).join(', ') || '없음')}</td><td>${escapeHtml((data.unresolvedFields || []).join(', ') || '없음')}</td></tr></table>`;
  }
  if (Array.isArray(data.conceptRows)) {
    return `<table><thead><tr><th>개념</th><th>구분축</th><th>의미</th><th>확인조건</th></tr></thead><tbody>${data.conceptRows.map((row) => `<tr><td>${escapeHtml(row.concept)}</td><td>${escapeHtml(row.axis)}</td><td>${escapeHtml(row.meaning)}</td><td>${escapeHtml((row.checks || []).join(', '))}</td></tr>`).join('')}</tbody></table>`;
  }
  if (data.axes) {
    return `<div class="axis-grid">${Object.entries(data.axes).map(([axis, row]) => `<div class="axis-card"><strong>${escapeHtml(axis)}</strong><p>${escapeHtml((row.requiredTopics || []).join(' · '))}</p><span class="status-pill ${row.evidenceProvided ? 'proceed' : 'review'}">${row.evidenceProvided ? 'EVIDENCE PRESENT' : 'EVIDENCE MISSING'}</span></div>`).join('')}</div>`;
  }
  if (Array.isArray(data.completedStages)) {
    const all = ['PLANNING', 'ELIGIBILITY', 'REGISTERED', 'IMPLEMENTING', 'MONITORING', 'VERIFIED', 'CERTIFIED', 'UTILIZATION', 'REGISTRY_MANAGED'];
    return `<div class="node-flow">${all.map((stage) => `<span>${data.completedStages.includes(stage) ? '✓ ' : ''}${escapeHtml(stage)}</span>`).join('')}</div>`;
  }
  if (Array.isArray(data.gateResults)) {
    return `<table><thead><tr><th>Gate</th><th>항목</th><th>제출상태</th><th>판정</th></tr></thead><tbody>${data.gateResults.map((row) => `<tr><td>${escapeHtml(row.gate)}</td><td>${escapeHtml(row.subject)}</td><td>${escapeHtml(row.submittedState)}</td><td><span class="status-pill ${statusClass(row.verdict)}">${escapeHtml(row.verdict)}</span></td></tr>`).join('')}</tbody></table>`;
  }
  return `<pre>${escapeHtml(JSON.stringify(data, null, 2))}</pre>`;
}

function renderArtifacts(artifacts = []) {
  if (!artifacts.length) return '<p class="muted">이 경로는 별도 사용자 산출물을 만들지 않았습니다.</p>';
  return `<div class="artifact-list">${artifacts.map((artifact) => `
    <details class="artifact">
      <summary><span>${escapeHtml(artifact.name)}</span><small>${escapeHtml(artifact.sha256.slice(0, 12))}… · ${artifact.bytes} bytes</small></summary>
      <pre>${escapeHtml(artifact.content || '')}</pre>
    </details>
  `).join('')}</div>`;
}

function renderTrace(trace = []) {
  return `<div class="execution-list">${trace.map((step) => `
    <div class="execution-step">
      <span class="order">${step.order}</span>
      <div><strong>${escapeHtml(step.role)}</strong><small>${escapeHtml(step.runSkill)} · ${escapeHtml(step.runId)}</small></div>
      <b>${escapeHtml(step.status)}</b>
    </div>
  `).join('')}</div>`;
}

function renderKacExecution(kac = {}) {
  const chains = Array.isArray(kac.chains) ? kac.chains : [];
  if (!chains.length) {
    return '<p class="muted">이번 질문에서 확정된 Concept Skill이 없습니다. 질문 대상을 더 구체적으로 입력해 주세요.</p>';
  }
  return `<div class="kac-runtime">
    ${chains.map((chain) => `
      <section class="kac-chain">
        <div class="kac-chain-head">
          <div><small>SELECTED CONCEPT</small><strong>${escapeHtml(chain.identity)}</strong></div>
          <span>${chain.conceptSkillRead ? 'CONCEPT SKILL READ' : 'MISSING'}</span>
        </div>
        <p>${escapeHtml(chain.definition || '')}</p>
        <div class="trace">${(chain.nodes || []).map((node) => `<span title="${escapeHtml(node.path || '')}">${escapeHtml(node.stage)}<small>${escapeHtml(node.label || '')}</small></span>`).join('')}</div>
        <details class="kac-files">
          <summary>실제로 읽은 Stage 파일과 해시</summary>
          <ul>${(chain.nodes || []).map((node) => `<li><strong>${escapeHtml(node.stage)}</strong><code>${escapeHtml(node.path || '')}</code><small>${escapeHtml((node.sha256 || '').slice(0, 16))}${node.sha256 ? '…' : ''}</small></li>`).join('')}</ul>
        </details>
      </section>
    `).join('')}
    <p class="kac-seal">봉인 Stage vault 변경: ${kac.sealedVaultMutation ? '발생' : '없음'} · 전체 체인 파일: ${kac.allChainFilesPresent ? '확인' : '일부 누락'}</p>
  </div>`;
}

function renderContextExtraction(context = {}) {
  const fields = Array.isArray(context.fields) ? context.fields : [];
  const conflicts = Array.isArray(context.conflicts) ? context.conflicts : [];
  if (!fields.length && !conflicts.length) {
    return '<p class="muted">이 질문에서 운영 판단 필드로 승격된 사용자 사실이 없습니다.</p>';
  }
  const rows = fields.map((item) => `
    <tr>
      <td><strong>${escapeHtml(item.field)}</strong></td>
      <td>${escapeHtml(typeof item.value === 'string' ? item.value : JSON.stringify(item.value))}</td>
      <td>${escapeHtml(item.source)} · ${escapeHtml(item.confidence)}</td>
      <td>${escapeHtml(item.rule)}</td>
    </tr>`).join('');
  const conflictBlock = conflicts.length
    ? `<div class="safety-note"><strong>충돌 감지</strong><ul>${conflicts.map((item) => `<li>${escapeHtml(item.reason)} · ${escapeHtml(item.evidenceSnippet)}</li>`).join('')}</ul></div>`
    : '<p class="kac-seal">구조화 입력 충돌: 없음</p>';
  return `
    ${fields.length ? `<table><thead><tr><th>필드</th><th>값</th><th>출처</th><th>추출 규칙</th></tr></thead><tbody>${rows}</tbody></table>` : ''}
    ${conflictBlock}`;
}

function renderOutputRiskGate(gate = {}) {
  const reasons = Array.isArray(gate.reasonCodes) ? gate.reasonCodes : [];
  return `<div class="safety-note">
    <strong>${escapeHtml(gate.decision || 'OUTPUT GATE UNKNOWN')}</strong>
    <p>검증 판정: ${escapeHtml(gate.verifiedStatus || '')} · 잔여 위험: ${escapeHtml(gate.residualRisk || '검증된 fallback 사용')}</p>
    ${reasons.length ? `<ul>${reasons.map((reason) => `<li>${escapeHtml(reason)}</li>`).join('')}</ul>` : '<p>모델 문장이 검증된 판정·근거·권한 경계를 통과했습니다.</p>'}
  </div>`;
}

function renderAiGeneration(ai = {}) {
  const generated = ai.generationUsed === true;
  const changed = ai.modelOutputChangedFromFallback === true;
  const promptTokens = ai.promptTokensTotal ?? ai.promptTokens;
  const responseTokens = ai.responseTokensTotal ?? ai.responseTokens;
  const modelHash = ai.modelOutputSha256 ? `${String(ai.modelOutputSha256).slice(0, 16)}…` : '없음';
  const fallbackHash = ai.fallbackOutputSha256 ? `${String(ai.fallbackOutputSha256).slice(0, 16)}…` : '없음';
  return `<div class="safety-note">
    <strong>${generated ? '실제 모델 생성 사용' : '검증된 구조화 답변 사용'}</strong>
    <p>Provider: ${escapeHtml(ai.provider || 'none')} · Model: ${escapeHtml(ai.model || 'none')} · 시도: ${escapeHtml(ai.generationAttempts ?? 0)}회 · Temperature: ${escapeHtml(ai.temperature ?? 'N/A')}</p>
    <p>입력 토큰: ${escapeHtml(promptTokens ?? 'N/A')} · 출력 토큰: ${escapeHtml(responseTokens ?? 'N/A')} · 기준 답안과 다른 생성문: ${changed ? '예' : '아니오'}</p>
    <p>모델 출력 해시: ${escapeHtml(modelHash)} · 안전 폴백 해시: ${escapeHtml(fallbackHash)}</p>
    ${ai.styleVariant ? `<p>표현 방식: ${escapeHtml(ai.styleVariant)}</p>` : ''}
  </div>`;
}

function renderGuidanceSteps(steps = []) {
  if (!steps.length) return '';
  return `<section class="guidance-section">
    <h4>지금 할 일</h4>
    <ol class="guidance-steps">${steps.map((step, index) => `
      <li>
        <span>${index + 1}</span>
        <div><strong>${escapeHtml(step.title)}</strong><p>${escapeHtml(step.description)}</p></div>
      </li>`).join('')}
    </ol>
  </section>`;
}

function renderMarketHandoff(handoff) {
  if (!handoff?.url) return '';
  return `<section class="market-handoff">
    <div class="market-kicker">이해에서 실제 행동으로</div>
    <h4>${escapeHtml(handoff.title)}</h4>
    <p>${escapeHtml(handoff.description)}</p>
    <p class="market-context">${escapeHtml(handoff.context)}</p>
    <a href="${escapeHtml(handoff.url)}" target="_blank" rel="noopener noreferrer">
      <span>${escapeHtml(handoff.label)}</span><span aria-hidden="true">↗</span>
    </a>
    <small>${escapeHtml(handoff.note)}</small>
  </section>`;
}

function renderTechnicalDetails(result, preserved) {
  const composite = result.compositeExecution || {};
  return `<details class="technical-details">
    <summary>
      <span>답변 근거와 실행기록 보기</span>
      <small>지식행동사슬·근거·산출물·검증기록</small>
    </summary>
    <div class="technical-body">
      <section class="result-section technical-status">
        <h4>검증 상태</h4>
        <div class="result-meta">
          <span class="status-pill ${statusClass(result.status)}">${escapeHtml(result.status)}</span>
          <span class="route-pill">${escapeHtml(result.routeLabel)}</span>
          <span class="ai-mode-pill">${escapeHtml(result.answerMode || 'STRUCTURED_GROUNDED')}</span>
          ${composite.directEntryPoint ? '<span class="ai-mode-pill">COMPOSITE DIRECT</span>' : ''}
          <span class="ai-mode-pill">${escapeHtml(result.outputRiskGate?.decision || 'OUTPUT GATE')}</span>
          <span class="preserved-pill">INPUT BYTES ${preserved ? 'PRESERVED' : 'MISMATCH'}</span>
        </div>
      </section>
      <section class="result-section">
        <h4>자연어에서 구조화한 사용자 입력</h4>
        <p class="chain-explanation">사용자 발화에 명시된 사실만 계약 필드로 승격하며, 추정하거나 충돌하는 값은 UNKNOWN으로 남깁니다.</p>
        ${renderContextExtraction(result.contextExtraction)}
      </section>
      <section class="result-section">
        <h4>이번 질문에서 실제 실행된 지식행동사슬</h4>
        <p class="chain-explanation">정적 예시가 아니라 선택된 Concept Skill과 연결 파일의 경로·해시입니다.</p>
        ${renderKacExecution(result.kacExecution)}
      </section>
      <section class="result-section">
        <h4>뒷단에서 실행된 구조</h4>
        <p class="chain-explanation">${composite.directEntryPoint
          ? `웹은 ${escapeHtml(composite.runComposite)} 하나만 호출했고, 내부 실행은 Composite Run Record로 검증했습니다.`
          : '실행 진입점 정보를 확인할 수 없습니다.'}</p>
        ${renderTrace(result.trace)}
      </section>
      <section class="result-section">
        <h4>상세 결과</h4>
        <div class="domain-view">${renderDomainData(result)}</div>
      </section>
      <section class="result-section">
        <h4>근거</h4>
        ${renderEvidence(result.evidence)}
      </section>
      <section class="result-section">
        <h4>추가 확인사항</h4>
        ${renderActions(result)}
      </section>
      <section class="result-section">
        <h4>생성된 산출물</h4>
        ${renderArtifacts(result.artifacts)}
      </section>
      <section class="result-section">
        <h4>실행기록</h4>
        <p class="record-line"><strong>입력 SHA-256</strong> ${escapeHtml(result.inputEvidence?.sha256 || '')}</p>
        <p class="record-line"><strong>기록 위치</strong> ${escapeHtml(result.runRecord?.orchestratorResponse || '')}</p>
        <div class="safety-note">${escapeHtml(result.safetyBoundary)}</div>
        <h4>AI 생성 증거</h4>
        ${renderAiGeneration(result.aiRuntime)}
        ${renderOutputRiskGate(result.outputRiskGate)}
      </section>
    </div>
  </details>`;
}

function addResult(result) {
  const article = document.createElement('article');
  article.className = 'message assistant-message';
  const preserved = result.inputEvidence?.bytesPreservedAcrossRouterAndSelectedSkill;
  const guidance = result.userGuidance || {};
  const paragraphs = (guidance.paragraphs || [result.summary]).map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`).join('');
  article.innerHTML = `
    <div class="avatar"><img src="/assets/supe_star_ai.png" alt=""></div>
    <div class="bubble result-bubble">
      <div class="human-answer">
        <span class="speaker">수페스타</span>
        <span class="friendly-status ${statusClass(result.status)}">${escapeHtml(guidance.statusLabel || '안내를 준비했어요')}</span>
        <h3>${escapeHtml(guidance.title || result.summary)}</h3>
        <div class="answer-copy">${paragraphs}</div>
        ${guidance.rationale ? `<div class="why-card"><strong>왜 이렇게 확인해야 하나요?</strong><p>${escapeHtml(guidance.rationale)}</p></div>` : ''}
        ${renderGuidanceSteps(guidance.steps)}
        ${guidance.followUp ? `<div class="follow-up"><strong>다음 질문</strong><p>${escapeHtml(guidance.followUp)}</p></div>` : ''}
        ${renderMarketHandoff(guidance.marketHandoff)}
      </div>
      ${renderTechnicalDetails(result, preserved)}
    </div>`;
  messages.append(article);
  conversation.push({
    role: 'assistant',
    content: [guidance.title, ...(guidance.paragraphs || [])].filter(Boolean).join(' '),
  });
  scrollToBottom();
}

function addError(message) {
  const article = document.createElement('article');
  article.className = 'message assistant-message';
  article.innerHTML = `<div class="avatar"><img src="/assets/supe_star_ai.png" alt=""></div><div class="bubble"><span class="speaker">수페스타</span><p>실행을 완료하지 못했습니다: ${escapeHtml(message)}</p></div>`;
  messages.append(article);
  scrollToBottom();
}

const wait = (milliseconds) => new Promise((resolve) => window.setTimeout(resolve, milliseconds));

async function parseChatResponse(response) {
  const text = await response.text();
  let payload = null;
  if (text) {
    try {
      payload = JSON.parse(text);
    } catch {
      payload = null;
    }
  }
  if (response.ok && payload && typeof payload === 'object') return payload;
  const message = payload?.error
    || (RETRYABLE_HTTP_STATUS.has(response.status)
      ? '공개 서버가 준비되는 중입니다.'
      : `요청을 처리하지 못했습니다. (HTTP ${response.status})`);
  const error = new Error(message);
  error.retryable = RETRYABLE_HTTP_STATUS.has(response.status);
  error.status = response.status;
  throw error;
}

async function requestChat(body) {
  let lastError = null;
  for (let attempt = 0; attempt <= CHAT_RETRY_DELAYS_MS.length; attempt += 1) {
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      return await parseChatResponse(response);
    } catch (error) {
      lastError = error;
      const networkFailure = error instanceof TypeError;
      const canRetry = attempt < CHAT_RETRY_DELAYS_MS.length && (networkFailure || error.retryable);
      if (!canRetry) break;
      await wait(CHAT_RETRY_DELAYS_MS[attempt]);
    }
  }
  throw new Error(lastError?.message || '공개 서버 응답을 확인하지 못했습니다. 잠시 후 다시 시도해 주세요.');
}

async function runQuestion(question) {
  // The server decides whether a question is an explicit follow-up.  Send only
  // recent user-authored text; never feed assistant prose back as context.
  const history = conversation.filter((item) => item.role === 'user').slice(-3);
  addUserMessage(question);
  conversation.push({ role: 'user', content: question });
  const loading = addLoading();
  sendButton.disabled = true;
  input.disabled = true;
  try {
    const payload = await requestChat({ question, history });
    loading.remove();
    addResult(payload);
  } catch (error) {
    loading.remove();
    addError(error.message || String(error));
  } finally {
    sendButton.disabled = false;
    input.disabled = false;
    input.focus({ preventScroll: true });
  }
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const question = input.value.trim();
  if (!question) return;
  input.value = '';
  runQuestion(question);
});

input.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});

quickPrompts.addEventListener('click', (event) => {
  const button = event.target.closest('[data-question]');
  if (!button || sendButton.disabled) return;
  runQuestion(button.dataset.question);
});

resetButton.addEventListener('click', () => {
  messages.innerHTML = initialMarkup;
  conversation.length = 0;
  input.value = '';
  input.focus({ preventScroll: true });
});

fetch('/api/health')
  .then((response) => response.json())
  .then((health) => {
    const ok = health.status === 'ok';
    runtimeState.classList.add(ok ? 'ready' : 'error');
    const ai = health.aiRuntime || {};
    let modeLabel = '구조화 지식 모드';
    if (ai.connected && ai.mode === 'CLOUD_AI_GROUNDED') {
      modeLabel = `서버 AI · ${ai.model}`;
    } else if (ai.connected && ai.mode === 'LOCAL_AI_GROUNDED') {
      modeLabel = `로컬 AI · ${ai.model}`;
    }
    runtimeState.querySelector('span:last-child').textContent = ok ? modeLabel : '서비스 점검 필요';
  })
  .catch(() => {
    runtimeState.classList.add('error');
    runtimeState.querySelector('span:last-child').textContent = '실행 엔진 연결 실패';
  });
