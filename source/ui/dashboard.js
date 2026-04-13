const logEl = document.getElementById('log');

function log(msg){
  const d=document.createElement('div');
  d.textContent = '['+new Date().toISOString()+'] '+msg;
  logEl.prepend(d);
}

log('GRAŻYNA — Cyberpunk dashboard online.');
let tick = 0;

setInterval(()=>{
  const load = (Math.sin(tick/5)*0.5+0.5)*100;
  log('Quantum load: '+load.toFixed(2)+'% | entropy '+Math.random().toFixed(5));
  tick++;
}, 900);
