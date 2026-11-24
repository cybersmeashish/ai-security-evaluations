"""Obtain exact public artifacts; no model-supplied Python is executed."""
from pathlib import Path
import argparse,hashlib,json,re,urllib.request
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--target",type=Path,required=True);a=p.parse_args();m=json.loads((Path(__file__).resolve().parents[1]/"fixtures/model-manifest.json").read_text())
 if m["repository"]!="sentence-transformers/all-MiniLM-L6-v2" or not re.fullmatch(r"[0-9a-f]{40}",m["revision"]):raise RuntimeError("unapproved source")
 a.target.mkdir(parents=True,exist_ok=True)
 for item in m["files"]:
  if item["local_file"] not in ("model.onnx","tokenizer.json","README.md","config.json") or type(item["bytes"]) is not int or not 0<item["bytes"]<200_000_000:raise RuntimeError("unapproved artifact")
  dest=a.target/item["local_file"]
  if dest.exists() and hashlib.sha256(dest.read_bytes()).hexdigest()==item["sha256"]:continue
  u="https://huggingface.co/"+m["repository"]+"/resolve/"+m["revision"]+"/"+item["source_file"]
  with urllib.request.urlopen(u,timeout=120) as response:raw=response.read(item["bytes"]+1)
  if len(raw)!=item["bytes"] or hashlib.sha256(raw).hexdigest()!=item["sha256"]:raise RuntimeError("artifact mismatch")
  dest.write_bytes(raw)
 print("Exact encoder artifacts verified outside public source.")
