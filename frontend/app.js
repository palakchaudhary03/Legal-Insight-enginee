const API = 'http://127.0.0.1:8000/api';
const file = document.getElementById('file'), go = document.getElementById('go'), name = document.getElementById('name'), err = document.getElementById('error');
let selected = null;
let allCases = [];

file.onchange = e => pick(e.target.files[0]);

function pick(f) {
  err.textContent = '';
  if (!f) return;
  if (!f.name.toLowerCase().endsWith('.pdf')) { err.textContent = 'Please choose a PDF.'; return; }
  if (f.size > 10 * 1024 * 1024) { err.textContent = 'PDF is larger than 10 MB.'; return; }
  selected = f; name.textContent = f.name; go.disabled = false;
}

async function stats() {
  try {
    let r = await fetch(API + '/stats'), d = await r.json();
    document.getElementById('status').textContent = d.index_ready ? 'Backend + index ready' : 'Backend ready · build index';
    document.getElementById('casesN').textContent = d.cases.toLocaleString();
    document.getElementById('yearsN').textContent = d.years || '—';
    document.getElementById('period').textContent = d.index_ready ? `${d.start_year}–${d.end_year}` : '1950–2024';
  } catch {
    document.getElementById('status').textContent = 'Backend offline';
  }
}

go.onclick = async () => {
  if (!selected) return;
  go.disabled = true; err.textContent = '';
  document.getElementById('loading').classList.remove('hidden');
  document.getElementById('results').classList.add('hidden');
  let fd = new FormData(); fd.append('file', selected);
  try {
    let r = await fetch(API + '/analyze', { method: 'POST', body: fd }), d = await r.json();
    if (!r.ok) throw Error(d.detail || 'Analysis failed');
    document.getElementById('summary').textContent = d.summary;
    document.getElementById('words').textContent = d.word_count.toLocaleString() + ' words';
    let t = document.getElementById('terms');
    t.innerHTML = d.key_terms.map(x => `<span class="chip">${safe(x)}</span>`).join('');

    allCases = d.similar_cases || [];
    populateYearFilter(allCases);
    renderCases(allCases);

    document.getElementById('results').classList.remove('hidden');
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
  } catch (e) {
    err.textContent = e.message;
  } finally {
    document.getElementById('loading').classList.add('hidden');
    go.disabled = false;
  }
};

function renderCases(list) {
  let c = document.getElementById('cases');
  c.innerHTML = list.length
    ? list.slice(0, 5).map((x, i) => `<div class="case"><strong>${i + 1}. ${safe(x.case_name)}</strong><span class="score">${Math.round(x.similarity * 100)}%</span><p>${x.year} · ${safe(x.preview)}</p></div>`).join('')
    : '<p class="muted">No matching cases found for this year.</p>';
}

function populateYearFilter(list) {
  let years = [...new Set(list.map(x => x.year))].sort((a, b) => b - a);
  let sel = document.getElementById('yearFilter');
  sel.innerHTML = '<option value="">All years</option>' + years.map(y => `<option value="${y}">${y}</option>`).join('');
}

document.getElementById('yearFilter').onchange = e => {
  let y = e.target.value;
  let filtered = y ? allCases.filter(x => String(x.year) === y) : allCases;
  renderCases(filtered);
};

document.getElementById('copyBtn').onclick = () => {
  let terms = [...document.querySelectorAll('#terms .chip')].map(x => x.textContent).join(', ');
  let text = `Summary:\n${document.getElementById('summary').textContent}\n\nKey Terms: ${terms}`;
  navigator.clipboard.writeText(text).then(() => {
    let b = document.getElementById('copyBtn');
    let old = b.textContent; b.textContent = 'Copied!';
    setTimeout(() => b.textContent = old, 1500);
  });
};

document.getElementById('printBtn').onclick = () => window.print();

function safe(x) {
  return String(x).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
}

stats();