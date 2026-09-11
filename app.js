import { CreateMLCEngine } from "https://esm.run/@mlc-ai/web-llm@0.2.79";
const MODEL="Llama-3.2-1B-Instruct-q4f16_1-MLC";
const CPU_MODEL="onnx-community/SmolLM2-135M-Instruct-ONNX";
let engine=null,cpuGenerator=null,stream=null,deferredInstall=null,mode=null;
const $=id=>document.getElementById(id);
function add(text,who="ai"){const d=document.createElement("div");d.className=`msg ${who}`;d.textContent=text;$("chat").appendChild(d);$("chat").scrollTop=$("chat").scrollHeight}
async function loadCpuModel(){
  const status=$("modelStatus");
  status.textContent="GPU unavailable. Starting CPU/WASM fallback brain…";
  $("progress").value=0;
  try{
    const {pipeline}=await import("https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.8.1");
    cpuGenerator=await pipeline("text-generation",CPU_MODEL,{
      device:"wasm",
      dtype:"q4",
      progress_callback:p=>{
        if(typeof p?.progress==="number")$("progress").value=Math.max(0,Math.min(1,p.progress));
        if(p?.status==="progress"&&p?.file)status.textContent=`Downloading ${p.file}: ${Math.round((p.progress||0)*100)}%`;
        else if(p?.status==="done")status.textContent="Preparing local CPU brain…";
      }
    });
    mode="cpu";
    $("progress").value=1;
    status.textContent="Local CPU brain ready. No hosted AI inference API is used.";
    add("AEGIS CPU fallback brain is ready. Inference runs locally in this browser via WebAssembly.");
  }catch(e){
    status.textContent=`CPU fallback failed: ${e?.message||e}`;
    add(`Local CPU brain could not start: ${e?.message||e}`);
  }
}
async function loadModel(){
  const status=$("modelStatus");
  $("load").disabled=true;
  try{
    if(navigator.gpu){
      status.textContent="Checking GPU and loading local GPU brain…";
      const adapter=await navigator.gpu.requestAdapter();
      if(adapter){
        engine=await CreateMLCEngine(MODEL,{initProgressCallback:p=>{status.textContent=p.text||`Loading ${(p.progress*100).toFixed(0)}%`;$("progress").value=Number.isFinite(p.progress)?p.progress:0}});
        mode="gpu";
        status.textContent="Local GPU brain ready. No hosted AI inference API is used.";
        $("progress").value=1;
        add("AEGIS GPU brain is ready. Chat inference runs locally on this phone.");
        return;
      }
    }
    await loadCpuModel();
  }catch(e){
    add(`GPU brain unavailable (${e?.message||e}). Switching to CPU/WASM fallback…`);
    await loadCpuModel();
  }finally{$("load").disabled=false}
}
async function media(kind){if(!navigator.mediaDevices?.getUserMedia){$("device").textContent="Camera/microphone APIs are unavailable in this browser/context.";return}try{if(stream)stream.getTracks().forEach(t=>t.stop());stream=await navigator.mediaDevices.getUserMedia(kind==="cam"?{video:{facingMode:{ideal:"environment"}},audio:true}:{audio:true});if(kind==="cam"){$("video").srcObject=stream;$('video').style.display="block";$("device").textContent="Camera + microphone granted for this session."}else $("device").textContent="Microphone granted for this session."}catch(e){$("device").textContent=`Permission/error: ${e?.name||e}`}}
function stopMedia(){if(stream)stream.getTracks().forEach(t=>t.stop());stream=null;$("video").srcObject=null;$("video").style.display="none";$("device").textContent="Device stream stopped."}
async function send(){
  const input=$("input"),text=input.value.trim();if(!text)return;
  input.value="";add(text,"user");
  if(!mode){add("Load the local brain first.");return}
  try{
    if(mode==="gpu"){
      const r=await engine.chat.completions.create({messages:[{role:"system",content:"You are AEGIS, a concise executive AI assistant running locally on the user's phone. Never claim access to tools, files, sensors, accounts, or data you do not actually have."},{role:"user",content:text}],temperature:.6,max_tokens:512});
      add(r.choices?.[0]?.message?.content||"No response.");
    }else{
      const messages=[{role:"system",content:"You are AEGIS, a concise executive AI assistant running locally on the user's phone. Never claim access to tools, files, sensors, accounts, or data you do not actually have."},{role:"user",content:text}];
      const r=await cpuGenerator(messages,{max_new_tokens:256,do_sample:false});
      const generated=r?.[0]?.generated_text;
      const answer=Array.isArray(generated)?generated.at(-1)?.content:generated;
      add(answer||"No response.");
    }
  }catch(e){add(`Local inference error: ${e?.message||e}`)}
}
$("load").onclick=loadModel;
$("cam").onclick=()=>media("cam");
$("mic").onclick=()=>media("mic");
$("stop").onclick=stopMedia;
$("send").onclick=send;
$("input").onkeydown=e=>{if(e.key==="Enter")send()};
if("serviceWorker"in navigator)navigator.serviceWorker.register("./sw.js").catch(()=>{});
window.addEventListener("beforeinstallprompt",e=>{e.preventDefault();deferredInstall=e;$("install").hidden=false});
$("install").onclick=async()=>{if(!deferredInstall)return;await deferredInstall.prompt();deferredInstall=null;$("install").hidden=true};
add("AEGIS Mobile shell loaded. Load the local brain when ready.");