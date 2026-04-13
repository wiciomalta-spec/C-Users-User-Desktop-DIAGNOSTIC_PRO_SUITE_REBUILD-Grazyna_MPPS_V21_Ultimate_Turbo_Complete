const loader = document.getElementById('loader');
const crt = document.getElementById('crt');
const loaderText = document.getElementById('loader-text');
const logEl = document.getElementById('log');

const phases = [
  'BOOTING GRAŻYNA ULTIMATE...',
  'INITIALIZING MAX MODE PRO...',
  'SPINNING UP DEEP SCANNER PRO...',
  'STABILIZING QUANTUM HARMONIZER PRO...',
  'LOADING AI ENGINE PRO...',
  'LINKING PLUGIN RING...'
];

let phase = 0;
const loaderInterval = setInterval(()=>{
  loaderText.textContent = phases[phase % phases.length];
  phase++;
  if (phase > phases.length + 2) {
    clearInterval(loaderInterval);
    loader.classList.add('hidden');
    crt.classList.remove('hidden');
    log('GRAŻYNA ULTIMATE cockpit online.');
  }
}, 800);

function log(msg){
  if (!logEl) return;
  const d=document.createElement('div');
  d.textContent = '['+new Date().toISOString()+'] '+msg;
  logEl.prepend(d);
}

let t = 0;
setInterval(()=>{
  if (crt.classList.contains('hidden')) return;
  const cpu = 40 + Math.random()*50;
  const risk = Math.random();
  const coh = (Math.sin(t/7)*0.5+0.5);
  log(MAX=% | RISK= | Q-COH=);
  t++;
}, 900);
