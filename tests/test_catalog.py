import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("builder",ROOT/"scripts/build_catalog.py")
builder=importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

class CatalogContractTests(unittest.TestCase):
    def setUp(self):
        self.root=ET.parse(ROOT/"data/source/citywalk.xml").getroot()

    def build(self, root=None, release=False):
        with tempfile.TemporaryDirectory() as folder:
            file=Path(folder)/"input.xml"
            ET.ElementTree(self.root if root is None else root).write(file,encoding="utf-8",xml_declaration=True)
            return builder.build(file,release)

    def test_valid_draft_and_durations(self):
        data=self.build()
        self.assertEqual([r["totalMinutes"] for r in data["routes"]],[85,70])
        self.assertEqual(data["routes"][0]["walkingMinutes"],35)
        self.assertEqual(data["routes"][0]["stayingMinutes"],50)

    def test_draft_release_denied(self):
        with self.assertRaisesRegex(ValueError,"draft"):self.build(release=True)

    def test_duplicate_id(self):
        items=self.root.find("points")
        items.append(copy.deepcopy(items[0]))
        with self.assertRaises(ValueError):self.build()

    def test_unknown_reference(self):
        self.root.find("routes/route/stops/stop").set("pointRef","gyp_999")
        with self.assertRaises(ValueError):self.build()

    def test_wrong_order(self):
        self.root.find("routes/route/stops/stop").set("order","2")
        with self.assertRaisesRegex(ValueError,"顺序"):self.build()

    def test_negative_minutes(self):
        self.root.find("routes/route/stops/stop").set("stayMinutes","-1")
        with self.assertRaises(ValueError):self.build()

    def test_first_leg_is_zero(self):
        self.root.find("routes/route/stops/stop").set("walkMinutesFromPrevious","5")
        with self.assertRaisesRegex(ValueError,"首站"):self.build()

    def test_duplicate_stop(self):
        stops=self.root.find("routes/route/stops")
        stops[1].set("pointRef",stops[0].get("pointRef"))
        with self.assertRaisesRegex(ValueError,"重复引用"):self.build()

    def test_verified_without_source(self):
        self.root.find("points/point").set("status","verified")
        with self.assertRaisesRegex(ValueError,"来源"):self.build()

    def test_invalid_coordinates(self):
        p=self.root.find("points/point")
        c=ET.Element("coordinates",{"system":"gcj02"})
        ET.SubElement(c,"latitude").text="100"
        ET.SubElement(c,"longitude").text="106.7"
        p.insert(4,c)
        with self.assertRaises(ValueError):self.build()

    def test_negative_distance(self):
        self.root.find("routes/route/distanceKm").text="-2"
        with self.assertRaises(ValueError):self.build()

    def test_bad_source_url(self):
        s=ET.SubElement(self.root.find("points/point"),"sources")
        ET.SubElement(s,"source",{"url":"javascript:alert(1)","checkedAt":"2026-11-11"}).text="测试来源"
        with self.assertRaisesRegex(ValueError,"HTTP"):self.build()

    def test_wrong_id_prefix(self):
        self.root.find("routes/route").set("id","gyp_999")
        with self.assertRaisesRegex(ValueError,"前缀"):self.build()

    def test_entity_declarations_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            file=Path(folder)/"bad.xml"
            file.write_text('<!DOCTYPE x [<!ENTITY a "x">]><x>&a;</x>',encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"实体"):builder.build(file)

if __name__=="__main__":unittest.main()
