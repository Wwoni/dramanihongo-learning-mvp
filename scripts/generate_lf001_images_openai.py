#!/usr/bin/env python3
"""
Generate images with OpenAI Images API and update tracking docs.

Required:
  - OPENAI_API_KEY in environment

Example:
  python3 scripts/generate_lf001_images_openai.py \
    --model gpt-image-1 \
    --quality medium \
    --size 1024x1024
"""

import argparse
import base64
import datetime as dt
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "docs" / "pastel_image_generation_manifest_lf001_v1.json"
DEFAULT_SHOTLIST_MD = ROOT / "docs" / "pastel_image_shotlist_v1.md"
DEFAULT_RESULTS_MD = ROOT / "docs" / "image_generation_results_lf001_v1.md"
DEFAULT_OUTPUT_DIR = ROOT / "outputs" / "images" / "lf001"
DOTENV_PATH = ROOT / ".env"


def load_dotenv(path):
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip("'").strip('"')
        if key and key not in os.environ:
            os.environ[key] = val


def call_openai_image(api_key, model, quality, size, prompt):
    url = "https://api.openai.com/v1/images/generations"
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "quality": quality,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {err_body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e}") from e

    obj = json.loads(body)
    data_items = obj.get("data") or []
    if not data_items:
        raise RuntimeError(f"Unexpected response: {body[:500]}")
    b64_data = data_items[0].get("b64_json")
    if not b64_data:
        raise RuntimeError("Missing b64_json in image response")
    return base64.b64decode(b64_data)


def load_manifest(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def update_results_md(results_md, results):
    text = results_md.read_text(encoding="utf-8")
    target_ids = set(results.keys())
    out_lines = []
    for line in text.splitlines():
        if not line.startswith("| "):
            out_lines.append(line)
            continue
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) != 7:
            out_lines.append(line)
            continue
        asset_id = parts[0]
        if asset_id not in target_ids:
            out_lines.append(line)
            continue
        r = results.get(asset_id)
        if not r:
            out_lines.append(line)
            continue
        if r["status"] == "generated":
            parts[1] = "generated"
            parts[2] = r["output_path"]
            parts[3] = "pending"
            parts[4] = "pending"
            parts[5] = "pending"
            parts[6] = ""
        else:
            parts[1] = "failed"
            err = r.get("error", "generation failed")
            err = " ".join(str(err).split())
            if len(err) > 220:
                err = err[:217] + "..."
            parts[6] = err
        out_lines.append("| " + " | ".join(parts) + " |")
    results_md.write_text("\n".join(out_lines) + "\n", encoding="utf-8")


def update_shotlist_md(shotlist_md, results):
    text = shotlist_md.read_text(encoding="utf-8")
    target_ids = set(results.keys())
    out_lines = []
    for line in text.splitlines():
        if not line.startswith("| "):
            out_lines.append(line)
            continue
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) != 6:
            out_lines.append(line)
            continue
        asset_id = parts[0]
        if asset_id not in target_ids:
            out_lines.append(line)
            continue
        r = results.get(asset_id)
        if not r:
            out_lines.append(line)
            continue
        parts[5] = "generated_pending_review" if r["status"] == "generated" else "generation_failed"
        out_lines.append("| " + " | ".join(parts) + " |")
    new_text = "\n".join(out_lines)
    if "generated_pending_review" not in new_text:
        new_text += "\n"
    if "- `generated_pending_review`" not in new_text:
        new_text = new_text.replace(
            "- `generation_requested`: 생성 요청 제출, 결과 대기",
            "- `generation_requested`: 생성 요청 제출, 결과 대기\n- `generated_pending_review`: 이미지 생성 완료, 시각 검수 대기\n- `generation_failed`: 생성 실패",
        )
    shotlist_md.write_text(new_text + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-image-1")
    parser.add_argument("--quality", default="medium", choices=["low", "medium", "high", "auto"])
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--results-md", default=str(DEFAULT_RESULTS_MD))
    parser.add_argument("--shotlist-md", default=str(DEFAULT_SHOTLIST_MD))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    manifest = pathlib.Path(args.manifest)
    if not manifest.is_absolute():
        manifest = ROOT / manifest
    results_md = pathlib.Path(args.results_md)
    if not results_md.is_absolute():
        results_md = ROOT / results_md
    shotlist_md = pathlib.Path(args.shotlist_md)
    if not shotlist_md.is_absolute():
        shotlist_md = ROOT / shotlist_md
    output_dir = pathlib.Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir
    latest_json = output_dir / "latest_generation_results.json"

    load_dotenv(DOTENV_PATH)
    items = load_manifest(manifest)
    output_dir.mkdir(parents=True, exist_ok=True)
    run_id = dt.datetime.now().strftime("%Y%m%d_%H%M%S")

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not args.dry_run and not api_key:
        print("ERROR: OPENAI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)

    result_rows = []
    result_map = {}
    for item in items:
        asset_id = item["asset_id"]
        out_name = f"{asset_id}.png"
        rel_path = str((output_dir / out_name).relative_to(ROOT))
        try:
            if args.dry_run:
                status = "generated"
                result_map[asset_id] = {"status": status, "output_path": rel_path}
                result_rows.append({**item, "status": status, "output_path": rel_path, "dry_run": True})
                continue
            image_bytes = call_openai_image(
                api_key=api_key,
                model=args.model,
                quality=args.quality,
                size=args.size,
                prompt=item["prompt"],
            )
            out_path = output_dir / out_name
            with out_path.open("wb") as f:
                f.write(image_bytes)
            status = "generated"
            result_map[asset_id] = {"status": status, "output_path": rel_path}
            result_rows.append({**item, "status": status, "output_path": rel_path})
            print(f"[OK] {asset_id} -> {rel_path}")
        except Exception as e:  # pylint: disable=broad-except
            err = str(e)
            result_map[asset_id] = {"status": "failed", "error": err}
            result_rows.append({**item, "status": "failed", "error": err})
            print(f"[FAIL] {asset_id}: {err}", file=sys.stderr)

    run_log = {
        "run_id": run_id,
        "model": args.model,
        "quality": args.quality,
        "size": args.size,
        "items": result_rows,
    }
    write_json(output_dir / f"generation_results_{run_id}.json", run_log)
    write_json(latest_json, run_log)

    if args.dry_run:
        print("Dry run complete. No markdown files were updated.")
    else:
        update_results_md(results_md, result_map)
        update_shotlist_md(shotlist_md, result_map)
        print(f"Updated: {results_md}")
        print(f"Updated: {shotlist_md}")
    print(f"Log: {latest_json}")


if __name__ == "__main__":
    main()
