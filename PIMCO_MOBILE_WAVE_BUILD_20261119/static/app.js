function showPage(id){
document.querySelectorAll('.page').forEach(p=>p.classList.toggle('active',p.id===id));
document.querySelectorAll('nav button').forEach(n=>n.classList.toggle('selected',n.dataset.page===id));
window.scrollTo({top:0,behavior:'smooth'});
}
let toastTimer;
function toast(m){
let e=document.getElementById('toast');
e.textContent=m;e.classList.add('show');
clearTimeout(toastTimer);
toastTimer=setTimeout(()=>e.classList.remove('show'),2300);
}
function openDeposit(){
document.getElementById('depositModal').hidden=false;
document.getElementById('depositMessage').textContent='';
}
function closeDeposit(){
document.getElementById('depositModal').hidden=true;
}
async function copyPaymentNumber(){
try{
await navigator.clipboard.writeText('0758878297');
toast('Payment number copied');
}catch(e){toast('Payment number: 0758878297');}
}
async function submitDeposit(){
const amount=Number(document.getElementById('depositAmount').value);
const reference=document.getElementById('depositReference').value.trim();
const button=document.getElementById('depositSubmit');
const message=document.getElementById('depositMessage');
if(!Number.isSafeInteger(amount)||amount<=0){
message.textContent='Enter a valid amount in UGX.';return;
}
if(!reference){
message.textContent='Enter your transaction reference.';return;
}
button.disabled=true;
button.textContent='Submitting...';
try{
const response=await fetch('/api/deposits',{
method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({amount,reference})
});
const result=await response.json();
if(!response.ok)throw new Error(result.error||'Could not submit request.');
message.textContent='Request submitted. Status: PENDING. Payment verification is required before wallet credit.';
document.getElementById('depositAmount').value='';
document.getElementById('depositReference').value='';
}catch(error){
message.textContent=error.message||'Connection error. Please try again.';
}finally{
button.disabled=false;
button.textContent='I Have Sent Money';
}
}

document.addEventListener('DOMContentLoaded',()=>{
let h=document.getElementById('particles');
for(let i=0;i<22;i++){
let p=document.createElement('i');
p.className='particle';
p.style.left=Math.random()*100+'%';
p.style.animationDuration=13+Math.random()*17+'s';
p.style.animationDelay=-Math.random()*25+'s';
h.appendChild(p);
}
let notes=[
'256***9870 — deposit preview UGX 30,000',
'256***4512 — withdrawal preview UGX 15,000',
'256***7821 — deposit preview UGX 50,000',
'256***1190 — withdrawal preview UGX 20,000'
];
let n=0,el=document.getElementById('activity');
function rotate(){el.textContent=notes[n++%notes.length]}
rotate();
setInterval(rotate,5500);
});
