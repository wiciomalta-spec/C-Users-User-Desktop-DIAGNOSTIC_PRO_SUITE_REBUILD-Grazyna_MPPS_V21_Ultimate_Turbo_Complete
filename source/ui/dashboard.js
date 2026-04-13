const logEl = document.getElementById('log');
const loader = document.getElementById('loader');
const crt = document.getElementById('crt');
const loaderText = document.getElementById('loader-text');

function log(msg){
  if (!logEl) return;
  const d=document.createElement('div');
  d.textContent = '['+new Date().toISOString()+'] '+msg;
  logEl.prepend(d);
}

let phase = 0;
const phases = [
  'BOOTING GRAŻYNA CORE...',
  'INITIALIZING MAX MODE...',
  'SPINNING UP DEEP SCANNER...',
  'ALIGNING QUANTUM HARMONIZER...',
  'LOADING ULTRA AI ENGINE...'
];

const loaderInterval = setInterval(()=>{
  loaderText.textContent = phases[phase % phases.length];
  phase++;
  if (phase > phases.length + 2) {
    clearInterval(loaderInterval);
    loader.classList.add('hidden');
    crt.classList.remove('hidden');
    log('GRAŻYNA — Cyberpunk dashboard online.');
  }
}, 900);

let tick = 0;
setInterval(()=>{
  if (!logEl || crt.classList.contains('hidden')) return;
  const load = (Math.sin(tick/5)*0.5+0.5)*100;
  const entropy = Math.random().toFixed(5);
  log('Quantum load: '+load.toFixed(2)+'% | entropy '+entropy);
  tick++;
}, 1000);
