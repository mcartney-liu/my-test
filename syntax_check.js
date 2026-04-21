const fs=require('fs');
const html=fs.readFileSync('C:/Users/haizhi/Projects/my-test/index.html','utf8');
const m=html.match(/<script>([\s\S]*?)<\/script>/);
if(!m){console.log('No script tag');process.exit(1);}
try{
  new Function(m[1]);
  console.log('Syntax OK, JS lines:',m[1].split('\n').length);
}catch(e){
  console.log('SYNTAX ERROR:',e.message.slice(0,300));
  // 尝试定位错误行
  const lines=m[1].split('\n');
  const match=e.message.match(/at position (\d+)/);
  if(match){
    const pos=parseInt(match[1]);
    const before=lines.slice(Math.max(0,pos-3),pos).join('\n');
    const after=lines.slice(pos,pos+3).join('\n');
    console.log('Around pos',pos,':',before,'|||',after);
  }
}
