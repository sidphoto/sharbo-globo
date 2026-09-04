const app = document.querySelector('#app');
const EXPLAIN_KEY = 'sharbo:public-explain';
let explainMode = localStorage.getItem(EXPLAIN_KEY) === '1';
let scheduled = false;

const icons = {
  today:'<path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10.5V20h13v-9.5"/><path d="M9.5 20v-5h5v5"/>',
  radar:'<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c3 3 4 6 4 9s-1 6-4 9c-3-3-4-6-4-9s1-6 4-9z"/>',
  emerging:'<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
  business:'<path d="M3 21V10l6 3V9l6 4V8l6 4v9z"/><path d="M7 17h2M13 17h2M19 17h2"/>',
  'my-radar':'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M12 12l6-6"/>',
  archive:'<path d="M4 6h16v14H4z"/><path d="M3 4h18v3H3zM8 11h8M8 15h6"/>',
  calendar:'<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16"/>',
  language:'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.5 5.7 3.5 9s-1 6.3-3.5 9c-2.5-2.7-3.5-5.7-3.5-9S9.5 5.7 12 3z"/>',
  moon:'<path d="M20 15.5A8.5 8.5 0 1 1 8.5 4 6.5 6.5 0 0 0 20 15.5z"/>',
  sun:'<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
  user:'<circle cx="12" cy="8" r="3.5"/><path d="M4.5 20c.9-3.1 3.4-4.8 7.5-4.8s6.6 1.7 7.5 4.8"/>',
  info:'<circle cx="12" cy="12" r="9"/><path d="M12 10v7M12 7h.01"/>'
};

function svg(name){
  return `<svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">${icons[name] || icons.radar}</svg>`;
}

function currentView(){
  return (location.hash || '#/today').replace('#/','').split('/')[0] || 'today';
}

function scheduleEnhance(){
  if(scheduled) return;
  scheduled = true;
  requestAnimationFrame(()=>{
    scheduled = false;
    enhance();
  });
}

function replaceIcon(container, name){
  if(!container || container.querySelector(':scope > .ui-icon')) return;
  container.innerHTML = svg(name);
}

function enhanceNav(){
  document.querySelectorAll('.nav button[data-route]').forEach(button=>{
    const route = (button.dataset.route || '').replace('#/','').split('/')[0];
    const slot = button.querySelector(':scope > span:first-child');
    if(slot){ slot.classList.add('nav-icon'); replaceIcon(slot, route); }
  });
  document.querySelectorAll('.mobile-nav button[data-route]').forEach(button=>{
    const route = (button.dataset.route || '').replace('#/','').split('/')[0];
    const slot = button.querySelector(':scope > b:first-child');
    if(slot) replaceIcon(slot, route);
  });
}

function enhanceTopbar(){
  const date = document.querySelector('.topbar .date');
  if(date && !date.querySelector('.ui-icon')){
    const text = date.textContent.replace(/^📅\s*/u,'').trim();
    date.classList.add('public-date');
    date.innerHTML = `${svg('calendar')}<span>${escapeHtml(text)}</span>`;
  }

  const localeIcon = document.querySelector('.locale-control span[aria-hidden="true"]');
  if(localeIcon && !localeIcon.querySelector('.ui-icon')) localeIcon.innerHTML = svg('language');

  const theme = document.querySelector('#themeToggle');
  if(theme && !theme.querySelector('.ui-icon')){
    const isSun = /☀/.test(theme.textContent);
    theme.innerHTML = svg(isSun ? 'sun' : 'moon');
  }

  const myRadar = document.querySelector('.top-actions .pill-btn[data-route="#/my-radar"]');
  if(myRadar && !myRadar.querySelector('.ui-icon')){
    const label = myRadar.textContent.replace(/^👤\s*/u,'').trim();
    myRadar.innerHTML = `${svg('user')}<span>${escapeHtml(label)}</span>`;
  }

  const topMeta = document.querySelector('.topbar .top-meta');
  if(topMeta && !topMeta.querySelector('.public-demo-label')){
    const label = document.createElement('span');
    label.className = 'public-demo-label';
    label.textContent = 'Synthetic Public Demo';
    topMeta.append(label);
  }

  const actions = document.querySelector('.topbar .top-actions');
  if(actions && !actions.querySelector('.public-explain-toggle')){
    const button = document.createElement('button');
    button.className = 'pill-btn public-explain-toggle';
    button.type = 'button';
    button.setAttribute('aria-pressed', explainMode ? 'true' : 'false');
    button.title = 'Explain the public demo contract';
    button.innerHTML = `${svg('info')}<span>Explain / 說明</span>`;
    button.addEventListener('click',()=>{
      explainMode = !explainMode;
      localStorage.setItem(EXPLAIN_KEY, explainMode ? '1' : '0');
      button.setAttribute('aria-pressed', explainMode ? 'true' : 'false');
      applyExplainMode();
    });
    actions.prepend(button);
  }
}

function enhanceBoundary(){
  const sidebar = document.querySelector('.sidebar');
  if(!sidebar || sidebar.querySelector('.public-boundary-card')) return;
  const card = document.createElement('div');
  card.className = 'public-boundary-card';
  card.innerHTML = '<strong>Public / Production boundary</strong>Synthetic fixtures only. Real sources, queries, weights, production data and credentials are excluded.<br><a href="./">Project overview →</a>';
  const windowCard = sidebar.querySelector('.window-card');
  (windowCard || sidebar.lastElementChild)?.insertAdjacentElement('afterend', card);
}

function addKeyboardAccess(){
  document.querySelectorAll('[data-signal]').forEach(node=>{
    if(node.dataset.publicKeyboard === '1') return;
    node.dataset.publicKeyboard = '1';
    if(!node.hasAttribute('role')) node.setAttribute('role','button');
    if(!node.hasAttribute('tabindex')) node.tabIndex = 0;
    node.addEventListener('keydown',event=>{
      if(event.key === 'Enter' || event.key === ' '){
        event.preventDefault();
        node.click();
      }
    });
  });
}

function organizeToday(){
  if(currentView() !== 'today') return;
  const content = document.querySelector('.main .content');
  if(!content || content.dataset.publicOrganized === '1') return;

  const direct = Array.from(content.children).filter(el=>!el.classList.contains('footer'));
  const heroGrid = direct.find(el=>el.classList.contains('hero-grid'));
  if(!heroGrid) return;

  const hero = Array.from(heroGrid.children).find(el=>el.classList.contains('hero'));
  const oldInsightGrid = Array.from(heroGrid.children).find(el=>el !== hero && el.classList.contains('grid'));
  const insightCards = oldInsightGrid ? Array.from(oldInsightGrid.children).filter(el=>el.classList.contains('card')) : [];
  const directCards = direct.filter(el=>el.matches('section.card'));
  const top5 = directCards[0];
  const myRadar = directCards[1];
  const topicsHeading = direct.find(el=>el.classList.contains('section-title'));
  const topicsGrid = direct.find(el=>el.classList.contains('topic-grid'));
  const lowerGrid = direct.find(el=>el.classList.contains('lower-grid'));
  const lowerCards = lowerGrid ? Array.from(lowerGrid.children).filter(el=>el.classList.contains('card')) : [];
  const [focus, market, taiwan] = lowerCards;

  const home = document.createElement('div');
  home.className = 'public-home';
  heroGrid.classList.add('public-hero-grid');
  if(oldInsightGrid) oldInsightGrid.remove();
  home.append(heroGrid);

  if(top5){
    top5.classList.add('public-top5');
    top5.querySelectorAll('.signal-row').forEach(row=>{
      if(!row.querySelector('.public-open-hint')){
        const hint = document.createElement('span');
        hint.className = 'public-open-hint';
        hint.textContent = 'Open →';
        row.append(hint);
      }
    });
    home.append(top5);
  }

  if(insightCards.length){
    const wrap = document.createElement('section');
    wrap.className = 'public-insight-grid';
    if(insightCards[0]) insightCards[0].classList.add('public-emerging');
    if(insightCards[1]) insightCards[1].classList.add('public-impact');
    insightCards.forEach(card=>wrap.append(card));
    home.append(wrap);
  }

  if(market || taiwan){
    const wrap = document.createElement('section');
    wrap.className = 'public-context-grid';
    if(taiwan){ taiwan.classList.add('public-taiwan'); wrap.append(taiwan); }
    if(market){ market.classList.add('public-market'); wrap.append(market); }
    home.append(wrap);
  }

  if(focus){ focus.classList.add('public-focus'); home.append(focus); }
  if(myRadar){ myRadar.classList.add('public-my-radar'); home.append(myRadar); }

  if(topicsHeading || topicsGrid){
    const wrap = document.createElement('section');
    wrap.className = 'public-topics';
    if(topicsHeading) wrap.append(topicsHeading);
    if(topicsGrid) wrap.append(topicsGrid);
    home.append(wrap);
  }

  content.insertBefore(home, content.querySelector('.footer'));
  if(lowerGrid && lowerGrid.isConnected) lowerGrid.remove();
  content.dataset.publicOrganized = '1';
}

function enhanceRadar(){
  if(currentView() !== 'radar') return;
  const grid = document.querySelector('.radar-grid');
  if(grid) grid.classList.add('public-radar-list');
}

function explainNote(title, body){
  const note = document.createElement('div');
  note.className = 'public-explain-note';
  note.innerHTML = `<strong>${escapeHtml(title)}</strong>${body}`;
  return note;
}

function addContractInspector(){
  if(currentView() !== 'signal') return;
  const layout = document.querySelector('.detail-layout');
  if(!layout || layout.querySelector('.public-contract-inspector')) return;
  const id = decodeURIComponent((location.hash.split('/')[2] || 'synthetic-signal'));
  const inspector = document.createElement('aside');
  inspector.className = 'card card-pad public-contract-inspector';
  inspector.innerHTML = `
    <h3>Public Contract Inspector</h3>
    <p>This inspector explains the public data contract. It does not expose production validation thresholds or source intelligence.</p>
    <div class="contract-list">
      <div class="contract-row"><span>Canonical ID</span><b>${escapeHtml(id)}</b></div>
      <div class="contract-row"><span>Dataset</span><b class="contract-safe">Synthetic fixture</b></div>
      <div class="contract-row"><span>Narrative contract</span><b>7 required fields</b></div>
      <div class="contract-row"><span>Locales</span><b>stable IDs across locales</b></div>
      <div class="contract-row"><span>Public evidence URLs</span><b>example.invalid only</b></div>
      <div class="contract-row"><span>Production intelligence</span><b class="contract-safe">excluded</b></div>
    </div>`;
  layout.append(inspector);
}

function applyExplainMode(){
  document.querySelectorAll('.public-explain-note').forEach(node=>node.remove());
  if(!explainMode) return;

  if(currentView() === 'today'){
    const top5 = document.querySelector('.public-top5');
    if(top5) top5.append(explainNote('Why Top 5?', 'The public validator demonstrates cutoff-safe canonical records and authoritative source classes using synthetic fixtures. Production source weights and ranking policy are not distributed.'));

    const emerging = document.querySelector('.public-emerging');
    if(emerging) emerging.append(explainNote('Why Emerging?', 'The demo uses synthetic historical series to show persistence and maturity concepts. Production thresholds remain outside this repository.'));

    const impact = document.querySelector('.public-impact');
    if(impact) impact.append(explainNote('Why Impact Chain?', '<code>SUPPORTED</code> relationships require evidence signal IDs; <code>POTENTIAL</code> relationships must remain explicitly possible rather than asserted as fact.'));
  }

  if(currentView() === 'radar'){
    const title = document.querySelector('.page-title');
    if(title) title.insertAdjacentElement('afterend', explainNote('Radar contract', 'Search and filters operate only on the checked-in synthetic dataset. The public repository has no access path to private production data.'));
  }

  if(currentView() === 'signal'){
    const detail = document.querySelector('.detail-layout');
    if(detail) detail.insertAdjacentElement('beforebegin', explainNote('Signal contract', 'Canonical IDs, required narrative fields, evidence references and localization structure are inspectable here; deployment-specific intelligence policy is intentionally absent.'));
  }
}

function enhance(){
  const view = currentView();
  document.body.dataset.publicView = view;
  enhanceNav();
  enhanceTopbar();
  enhanceBoundary();
  organizeToday();
  enhanceRadar();
  addContractInspector();
  addKeyboardAccess();
  applyExplainMode();
}

function escapeHtml(value=''){
  return String(value).replace(/[&<>"']/g,char=>({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
  }[char]));
}

if(app){
  const observer = new MutationObserver(scheduleEnhance);
  observer.observe(app,{childList:true,subtree:true});
}
window.addEventListener('hashchange',scheduleEnhance);
window.addEventListener('load',scheduleEnhance);
scheduleEnhance();
