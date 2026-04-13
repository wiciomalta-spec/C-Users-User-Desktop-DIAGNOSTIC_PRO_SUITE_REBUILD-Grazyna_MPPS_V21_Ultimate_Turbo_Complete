const logEl = document.getElementById('log');
function log(msg){ const d=document.createElement('div'); d.textContent=msg; logEl.prepend(d); }
log('Dashboard online.');
setInterval(()=>log('Tick '+Math.random()),1000);
