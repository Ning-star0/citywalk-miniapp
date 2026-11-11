#!/usr/bin/env python3
"""XML/XSD -> 稳定JSON与小程序模块。仅使用Python标准库和xmllint。"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

def text(node, key):
    return node.findtext(key, "").strip()

def read_sources(node):
    return [{"title": (s.text or "").strip(), "url": s.get("url"), "checkedAt": s.get("checkedAt")}
            for s in node.findall("sources/source")]

def validate_business(root, release=False):
    points = {p.get("id"): p for p in root.findall("points/point")}
    for kind in ("points/point", "routes/route"):
        prefix = "gyp_" if kind.startswith("points") else "gyr_"
        for item in root.findall(kind):
            if not re.fullmatch(prefix + r"[0-9]{3,6}", item.get("id", "")):
                raise ValueError("ID前缀不匹配: " + item.get("id", ""))
            sources = read_sources(item)
            if any(urlparse(s["url"]).scheme not in ("https", "http") or not urlparse(s["url"]).netloc for s in sources):
                raise ValueError("来源必须为HTTP(S)完整URL")
            if item.get("status") == "verified":
                if not sources:
                    raise ValueError("verified条目必须有来源: " + item.get("id"))
                if prefix == "gyp_" and item.find("coordinates") is None:
                    raise ValueError("verified点位必须有GCJ-02坐标")
            if release and item.get("status") != "verified":
                raise ValueError("发布被阻止: 尚有draft数据 " + item.get("id"))
    for route in root.findall("routes/route"):
        stops = route.findall("stops/stop")
        if [int(s.get("order")) for s in stops] != list(range(1, len(stops) + 1)):
            raise ValueError("点位顺序必须从1开始连续递增")
        if int(stops[0].get("walkMinutesFromPrevious")) != 0:
            raise ValueError("首站没有前站，步行耗时必须为0")
        refs = [s.get("pointRef") for s in stops]
        if len(refs) != len(set(refs)):
            raise ValueError("同一路线不能重复引用点位")
        if any(ref not in points for ref in refs):
            raise ValueError("引用了不存在的点位")
        if route.get("status") == "verified" and any(points[ref].get("status") != "verified" for ref in refs):
            raise ValueError("verified路线不可引用draft点位")
        if sum(int(s.get("stayMinutes")) + int(s.get("walkMinutesFromPrevious")) for s in stops) > 1440:
            raise ValueError("路线总耗时不可超过1440分钟")

def build(xml_path, release=False):
    raw = xml_path.read_bytes()
    if len(raw) > 2 * 1024 * 1024 or re.search(br"<!DOCTYPE|<!ENTITY", raw, re.I):
        raise ValueError("XML过大或包含不允许的DTD/实体声明")
    executable = shutil.which("xmllint")
    if not executable:
        raise RuntimeError("请安装xmllint：macOS通常自带；Ubuntu安装libxml2-utils；Windows可用WSL运行npm脚本")
    result = subprocess.run([executable, "--nonet", "--noout", "--schema", str(ROOT / "data/schema/citywalk.xsd"), str(xml_path)], capture_output=True, text=True)
    if result.returncode:
        raise ValueError(result.stderr.strip())
    root = ET.fromstring(raw)
    validate_business(root, release)
    points = []
    for p in root.findall("points/point"):
        c = p.find("coordinates")
        points.append({"id": p.get("id"), "status": p.get("status"), "name": text(p,"name"),
                       "category":text(p,"category"),"address":text(p,"address"),
                       "description":text(p,"description"),"notice":text(p,"notice"),
                       "coordinates": None if c is None else {"system":"gcj02","latitude":float(text(c,"latitude")),"longitude":float(text(c,"longitude"))},
                       "sources": read_sources(p)})
    routes = []
    for r in root.findall("routes/route"):
        stops = [{"order":int(s.get("order")),"pointId":s.get("pointRef"),
                  "stayMinutes":int(s.get("stayMinutes")),"walkMinutesFromPrevious":int(s.get("walkMinutesFromPrevious"))}
                 for s in r.findall("stops/stop")]
        walking = sum(s["walkMinutesFromPrevious"] for s in stops)
        staying = sum(s["stayMinutes"] for s in stops)
        routes.append({"id":r.get("id"),"status":r.get("status"),"name":text(r,"name"),
                       "district":text(r,"district"),"metroStation":text(r,"metroStation"),
                       "summary":text(r,"summary"),"distanceKm":float(text(r,"distanceKm")),
                       "distanceKind":"estimate","tags":[(t.text or "").strip() for t in r.findall("tags/tag")],
                       "stops":stops,"walkingMinutes":walking,"stayingMinutes":staying,
                       "totalMinutes":walking+staying,"notice":text(r,"notice"),"sources":read_sources(r)})
    return {"schemaVersion":1,"datasetVersion":root.get("datasetVersion"),"city":root.get("city"),
            "updatedAt":root.get("updatedAt"),"points":points,"routes":routes}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--xml",type=Path,default=ROOT/"data/source/citywalk.xml")
    parser.add_argument("--check",action="store_true")
    parser.add_argument("--release",action="store_true")
    parser.add_argument("--outdir",type=Path)
    args=parser.parse_args()
    if args.release and args.check: parser.error("--release和--check不能组合")
    catalog=build(args.xml,args.release)
    payload=json.dumps(catalog,ensure_ascii=False,indent=2)+"\n"
    if args.outdir:
        outputs={args.outdir/"catalog.json":payload}
    else:
        outputs={ROOT/"data/generated/catalog.json":payload,
                 ROOT/"miniprogram/data/catalog.js":"// 自动生成，请修改data/source/citywalk.xml\nmodule.exports = "+payload.rstrip()+";\n"}
    for filename,body in outputs.items():
        if args.check:
            if not filename.exists() or filename.read_text(encoding="utf-8") != body:
                raise ValueError("生成物未更新，请运行npm run data:build: "+str(filename))
        else:
            filename.parent.mkdir(parents=True,exist_ok=True)
            filename.write_text(body,encoding="utf-8")
    print("校验通过: %d条路线 / %d个点位%s" % (len(catalog["routes"]),len(catalog["points"]),"（发布模式）" if args.release else "（开发草案）"))

if __name__ == "__main__":
    try: main()
    except Exception as e:
        print(str(e),file=sys.stderr)
        sys.exit(1)
