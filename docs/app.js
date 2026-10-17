'use strict';
// All CSV handling runs inside the browser; no network endpoints or telemetry.
(function () {
  const input=document.getElementById('csv');
  const container=document.getElementById('result');
  const p10state=document.getElementById('p10state');
  const p10badge=document.getElementById('p10badge');
  const required=[
    ['B4096','fill','4096',2],['B4096','clone','4096',2],
    ['B16384','fill','16384',1],['B16384','clone','16384',1],
    ['UPDATE','full','1728',1],['UPDATE','delta','384',1],['UPDATE','clone','1536',1],
    ['IO','roundtrip','1024',1],['IO','roundtrip','65536',1],['IO','roundtrip','262144',1],
    ['ENDURANCE','QUICK','150',1],['RUN','final','0',1]
  ];
  function esc(v){return String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
  function parseCSV(csv){
    csv=csv.replace(/^\uFEFF/,'');
    const rows=[];let row=[],field='',quoted=false;
    for(let i=0;i<csv.length;i++){
      const ch=csv[i];
      if(quoted){if(ch==='"'){if(csv[i+1]==='"'){field+='"';i++;}else quoted=false;}else field+=ch;}
      else if(ch==='"')quoted=true;
      else if(ch===','){row.push(field);field='';}
      else if(ch==='\n'){row.push(field.replace(/\r$/,''));if(row.some(s=>s.length))rows.push(row);row=[];field='';}
      else field+=ch;
    }
    if(quoted)throw new Error('引用符が閉じられていません');
    row.push(field.replace(/\r$/,''));if(row.some(s=>s.length))rows.push(row);
    if(!rows.length)throw new Error('CSVが空です');
    const header=rows[0];if(new Set(header).size!==header.length)throw new Error('重複列名があります');
    return rows.slice(1).map((parts)=>Object.fromEntries(header.map((k,i)=>[k,(parts[i]||'')])));
  }
  function analyze(rows){
    if(!rows.length)return {version:'不明',state:'EMPTY',message:'CSVにデータ行がありません',items:[]};
    const keys=Object.keys(rows[0]);const has=(...cols)=>cols.every(k=>keys.includes(k));
    if(has('Stage','Method','Blocks','Trial','Status','Detail')){
      const items=required.map(([stage,method,n,want])=>{
        const count=rows.filter(r=>r.Stage===stage&&r.Method===method&&r.Blocks===n&&r.Status==='PASS').length;
        return {label:`${stage} / ${method}`,blocks:n,value:`${count}/${want}`,ok:count>=want};
      });
      const stopped=rows.find(r=>['STOP','FAIL','REFUSED'].includes(r.Status));
      const state=stopped?'STOP':items.every(r=>r.ok)?'PASS':'INCOMPLETE';
      return {version:'P1.0',state,message:stopped?`${stopped.Detail||'停止'} — 施工を再実行せず結果を共有してください。`:(state==='PASS'?'全必須工程のPASSを確認':'未完了の必須工程があります。'),items};
    }
    if(has('Method','Trial','Blocks','Status','DestinationZ')){
      const items=['fill','clone'].map(method=>{
        const count=rows.filter(r=>r.Method===method&&r.Blocks==='512'&&r.Status==='PASS').length;
        return {label:method,blocks:'512',value:`${count}/5`,ok:count>=5};
      });
      const bad=rows.some(r=>r.Status!=='PASS');
      return {version:'P0.8',state:bad?'STOP':items.every(x=>x.ok)?'PASS':'INCOMPLETE',message:'512ブロックの反復試験',items};
    }
    if(has('Method','Blocks','Status','ApproximateFileTimestampMs')||has('Method','Status','ApproximateFileTimestampMs')){
      const isP07=has('Blocks');const version=isP07?'P0.7':'P0.6';
      const methods=isP07?['place','fill','clone']:['place','fill','clone','update','io','endurance'];
      const items=methods.map(method=>{
        const r=rows.find(x=>x.Method===method&&x.Status==='PASS');
        return {label:method,blocks:r?.Blocks||'—',value:r?'PASS':'MISSING',ok:!!r};
      });
      const bad=rows.some(r=>r.Status!=='PASS');
      return {version,state:bad?'STOP':items.every(x=>x.ok)?'PASS':'INCOMPLETE',message:'時刻差は参考値。精密な速度倍率の証拠には使用できません。',items};
    }
    return {version:'不明',state:'UNSUPPORTED',message:'未対応のCSV形式です。列名を確認してください。',items:[]};
  }
  function render(file,report){
    const statuses={PASS:'PASS',STOP:'STOP',INCOMPLETE:'未完了',UNSUPPORTED:'未対応',EMPTY:'空'};
    const ok=report.state==='PASS';
    container.className='';
    container.innerHTML=`<div class="resultsummary"><h3>${esc(file)} · ${esc(report.version)}</h3><span class="tag ${ok?'pass':report.state==='STOP'?'fail':'pending-tag'}">${esc(statuses[report.state]||report.state)}</span></div><p class="details">${esc(report.message)}</p>` +
      (report.items.length?`<div style="overflow:auto"><table class="resulttable"><thead><tr><th>対象</th><th>ブロック数</th><th>結果</th></tr></thead><tbody>`+
      report.items.map(r=>`<tr><td>${esc(r.label)}</td><td>${esc(r.blocks)}</td><td>${r.ok?'✓':'—'} ${esc(r.value)}</td></tr>`).join('')+
      '</tbody></table></div>':'');
    if(report.version==='P1.0'){
      p10state.textContent=statuses[report.state]||report.state;
      p10state.style.fontSize='25px';
      p10badge.textContent=statuses[report.state]||report.state;
      p10badge.className='tag '+(ok?'pass':report.state==='STOP'?'fail':'pending-tag');
    }
  }
  input.addEventListener('change',async()=>{
    const f=input.files&&input.files[0];if(!f)return;
    if(f.size>5*1024*1024){container.className='empty';container.textContent='ファイルが5MBを超えています。より小さな状態CSVを選んでください。';return;}
    try{const csv=await f.text();render(f.name,analyze(parseCSV(csv)));}
    catch(e){container.className='empty';container.textContent='CSV読込エラー: '+e.message;}
  });
  // Export parser for Node.js regression tests without invoking the DOM renderer.
  if(typeof module!=='undefined'&&module.exports)module.exports={parseCSV,analyze};
})();
