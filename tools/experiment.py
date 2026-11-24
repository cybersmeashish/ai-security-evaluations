import csv,hashlib,json,os,time
from pathlib import Path
import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer
from cache_scope import declared_reuse_eligible
ort.disable_telemetry_events()

def run(root,output):
    folder=Path(os.environ.get("AI_CACHE_MODEL_DIRECTORY",str(root.parent/"work/models/embedding")))
    manifest=json.loads((root/"fixtures/model-manifest.json").read_text())
    for f in manifest["files"]:assert hashlib.sha256((folder/f["local_file"]).read_bytes()).hexdigest()==f["sha256"],f["local_file"]
    data=json.loads((root/"fixtures/pairs.json").read_text());pairs=data["pairs"]
    tok=Tokenizer.from_file(str(folder/"tokenizer.json"));tok.enable_truncation(max_length=256);tok.enable_padding(pad_id=0,pad_token="[PAD]")
    texts=[p[k]["text"] for p in pairs for k in ("a","b")];enc=tok.encode_batch(texts)
    arrays={"input_ids":np.array([e.ids for e in enc],dtype=np.int64),"attention_mask":np.array([e.attention_mask for e in enc],dtype=np.int64),"token_type_ids":np.array([e.type_ids for e in enc],dtype=np.int64)}
    opts=ort.SessionOptions();opts.intra_op_num_threads=2;opts.inter_op_num_threads=1
    session=ort.InferenceSession(str(folder/"model.onnx"),sess_options=opts,providers=["CPUExecutionProvider"])
    started=time.perf_counter();outputs=session.run(None,{i.name:arrays[i.name] for i in session.get_inputs()});x=outputs[0];mask=arrays["attention_mask"]
    if x.ndim==3:x=(x*mask[:,:,None]).sum(axis=1)/mask.sum(axis=1)[:,None]
    x=x/np.maximum(np.linalg.norm(x,axis=1,keepdims=True),1e-12);elapsed=(time.perf_counter()-started)*1000
    rows=[]
    for i,p in enumerate(pairs):rows.append({"pair_id":p["id"],"cosine":float(np.clip(x[i*2]@x[i*2+1],-1,1)),"expected_reuse":p["expected_reuse"],"declared_metadata_gate":declared_reuse_eligible(p["a"],p["b"])})
    summaries={}
    for threshold in (0.85,0.90,0.95,0.97):
        summaries[str(threshold)]={"naive_accepts":sum(y["cosine"]>=threshold for y in rows),"naive_false_reuse":sum(y["cosine"]>=threshold and not y["expected_reuse"] for y in rows),"metadata_gated_false_reuse":sum(y["cosine"]>=threshold and y["declared_metadata_gate"] and not y["expected_reuse"] for y in rows),"metadata_gated_correct_hits":sum(y["cosine"]>=threshold and y["declared_metadata_gate"] and y["expected_reuse"] for y in rows)}
    with (output/"pair-results.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    return {"scope":"actual learned-encoder similarities on 16 synthetic English pairs; declared scope/entity annotations are fixture inputs, not a production authorization or extraction system","pairs":len(rows),"thresholds":summaries,"model_repository":manifest["repository"],"model_revision":manifest["revision"],"onnxruntime":ort.__version__,"encoding_batch_ms":elapsed,"answering_LLM_executed":False,"rows":rows}
