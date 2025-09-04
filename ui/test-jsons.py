import json, pathlib

files = [
    "/home/simon-ruth/Documents/tasks/RAG_evaluator/rag-explorer/text-processing/data/nlp-processed/articles.jsonl",
    "/home/simon-ruth/Documents/tasks/RAG_evaluator/rag-explorer/text-processing/data/nlp-processed/references.jsonl",
    "/home/simon-ruth/Documents/tasks/RAG_evaluator/rag-explorer/text-processing/data/nlp-processed/rag_1.jsonl",   # add any other model files listed in config.json
]

def check_bom(path: pathlib.Path, fix: bool = False):
    """Check file for UTF-8 BOM and optionally strip it."""
    with open(path, "rb") as f:
        start = f.read(3)
    if start == b"\xef\xbb\xbf":
        print(f"[BOM FOUND] {path}")
        if fix:
            text = Path(path).read_text(encoding="utf-8-sig")
            Path(path).write_text(text, encoding="utf-8")
            print(f"  -> BOM removed from {path}")
    else:
        print(f"[OK] {path} (no BOM)")

for fp in files:
    p = pathlib.Path(fp)
    if not p.exists():
        print(f"[MISS] {fp} not found")
        continue
    if p.stat().st_size == 0:
        print(f"[EMPTY] {fp} is 0 bytes")
        continue
    with p.open("r", encoding="utf-8-sig") as f:  # -sig strips BOM if present
        for i, line in enumerate(f, 1):
            s = line.strip()
            if not s:
                print(f"[EMPTY LINE] {fp}:{i}")
                continue
            try:
                json.loads(s)
            except Exception as e:
                print(f"[BAD JSON] {fp}:{i} -> {e}")
                break
        else:
            print(f"[OK] {fp}")
            
    check_bom(p, fix=True)
            
            
