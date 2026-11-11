# XML数据规范 v1

## 唯一主数据源

维护data/source/citywalk.xml；data/generated/catalog.json和miniprogram/data/catalog.js由脚本生成，不直接编辑。
XML采用UTF-8，无默认命名空间；根元素citywalk固定city=贵阳、schemaVersion=1。
datasetVersion使用日期加修订号，如2026-11-11.1；updatedAt为YYYY-MM-DD。

## 路线和点位字段

| 范围 | 字段 | 类型及含义 |
| --- | --- | --- |
| point | id | gyp_加3～6位数字；全局唯一、发布后不复用 |
| point | status | draft或verified |
| point | name/category/address/description/notice | 非空文本 |
| point | coordinates | 草案可省略；verified必填，system固定gcj02 |
| coordinates | latitude/longitude | 纬度-90～90；经度-180～180 |
| route | id | gyr_加3～6位数字；全局唯一 |
| route | name/district/metroStation/summary/notice | 非空文本；district指商圈，不是行政区字段 |
| route | distanceKm | 大于0且不超过50；unit=km、kind=estimate |
| route | tags/tag | 1～8个非空主题 |
| route | stops/stop | 每条2～20站 |
| stop | order | 从1开始连续递增，代表实际顺序 |
| stop | pointRef | 必须指向已存在的point.id |
| stop | stayMinutes | 0～1440整数，建议停留分钟数 |
| stop | walkMinutesFromPrevious | 从前一站走到本站的估算分钟数；首站固定0 |
| source | url/checkedAt/文本 | HTTP(S)来源地址、核验日期、来源标题 |

总耗时=所有stop的stayMinutes之和+walkMinutesFromPrevious之和，不在XML重复手填。
每条路线总耗时不超过1440分钟；数据总量限制为200条路线、500个点位。

## 约束如何分配

XSD检查元素顺序、必填项、类型、数量、状态、坐标范围、固定单位、全局ID唯一和点位引用。
构建器检查ID前缀、站序连续、首站步行时间为0、同路线点位不重复、来源URL和总耗时。
verified点位必须有来源和完整坐标；verified路线必须有来源，且所有引用点位已verified。
发布命令拒绝任何draft条目；开发构建允许draft，但页面必须显示草案提示。

## 调查与来源

成员2负责调查事实：点位入口、开放条件、步行连通性、商圈、地铁出口、距离和耗时。
每项verified记录至少包含一条可追溯来源；优先政府、景区或交通运营方公告，结合实测记录。
禁止将估计值写成实时数据；服务端或脚本无法证明记录真实性，verified必须经过人工审校。
当前两条草案仅用于联调，不是旅游推荐，不将名称后的“待核验”当成正式点位名。

## verified来源示例

```xml
<sources>
  <source url="https://example.com/replace-with-real-source" checkedAt="2026-11-11">替换为真实调查来源</source>
</sources>
```

示例URL不能用于完成真实核验。成员3需在数据审校时检查是否为真实有效页面。

## 输出契约

JSON根字段：schemaVersion、datasetVersion、city、updatedAt、points、routes。
points坐标缺失时coordinates=null；存在时为system、latitude、longitude对象。
routes新增walkingMinutes、stayingMinutes、totalMinutes三个派生字段。
stop.pointRef转换为pointId；客户端detail()再展开point，不在输出中复制整份点位。
