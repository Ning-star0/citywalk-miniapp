#!/usr/bin/env python3
"""后续可选：用已登录的gh批量发布任务，不保存token。先用--dry-run查看内容。"""
import argparse
import json
import shutil
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument("--repo",required=True,help="owner/repo")
parser.add_argument("--dry-run",action="store_true")
args=parser.parse_args()
tasks=json.loads((ROOT/".github/tasks.json").read_text(encoding="utf-8"))
if args.dry_run:
    for task in tasks: print(task["title"]+"\n"+task["body"]+"\n")
else:
    if not shutil.which("gh"):
        raise SystemExit("未安装gh。可用GitHub网页或连接器创建Issue；无需在此填写密码或token。")
    existing=subprocess.check_output(["gh","issue","list","--repo",args.repo,"--state","all","--limit","1000","--json","title"],text=True)
    titles={x["title"] for x in json.loads(existing)}
    for task in tasks:
        if task["title"] in titles:
            print("已存在，跳过："+task["title"])
            continue
        result=subprocess.run(["gh","issue","create","--repo",args.repo,"--title",task["title"],"--body-file","-"],input=task["body"],text=True)
        if result.returncode: raise SystemExit(result.returncode)
