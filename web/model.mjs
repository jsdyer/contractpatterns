import {counts,sum} from './shared.mjs';
export const present=rows=>rows;
export function normalizeVendor(name){return String(name||'').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase().replace(/[^a-z0-9]+/g,' ').trim();}
export function clusters(rows,days){
 const groups=new Map();
 for(const r of rows){if(r.kind!=='Award'||!r.vendor_key||!r.date)continue;const key=JSON.stringify([r.department,r.vendor_key]);if(!groups.has(key))groups.set(key,[]);groups.get(key).push(r);}
 const result=[];
 for(const records of groups.values()){
  records.sort((a,b)=>a.date.localeCompare(b.date));const dates=records.map(r=>Date.parse(r.date));let right=0,furthest=-1;
  for(let left=0;left<records.length;left++){
   right=Math.max(right,left+1);while(right<records.length&&(dates[right]-dates[left])/86400000<=days)right++;
   // A later interval is a subset exactly when its right endpoint has not advanced.
   if(right-left<2||right<=furthest)continue;furthest=right;
   const set=records.slice(left,right);result.push({label:records[left].vendor+' · '+records[left].department,value:set.length,total:sum(set,'amount'),start:records[left].date,end:set.at(-1).date,ids:set.map(r=>r.id)});
  }
 }
 return result.sort((a,b)=>b.value-a.value||b.total-a.total);
}
export function analyse(rows,state,data){const groups=clusters(rows,Number(state.days)||30),awards=rows.filter(r=>r.kind==='Award'),amendments=rows.filter(r=>r.kind==='Amendment');return{metrics:[{label:'Disclosures selected',value:rows.length,note:'Not unique contracts'},{label:'Reported original award value',value:'$'+sum(awards,'amount').toLocaleString('en-CA',{maximumFractionDigits:0}),note:'Award rows only; not cumulative totals'},{label:'Amendment records',value:amendments.length,note:'Dates can retain original award date'},{label:'Repeated-award windows',value:groups.length,note:`Within ${state.days} days; investigation leads`}],panels:[{title:'Repeated awards in selected window',items:groups.map(g=>({...g,label:g.label+' · '+g.start+' to '+g.end})),note:'Amount bands apply to the selected award rows. Overlapping subset windows are suppressed; these are not findings of contract splitting.'},{title:'Disclosure rows by department',items:counts(rows,'department'),note:'Open a row to inspect the possible department/procurement chain and ambiguity flags.'}]};}
