// 自动生成，请修改data/source/citywalk.xml
module.exports = {
  "schemaVersion": 1,
  "datasetVersion": "2026-11-11.1",
  "city": "贵阳",
  "updatedAt": "2026-11-11",
  "points": [
    {
      "id": "gyp_001",
      "status": "draft",
      "name": "甲秀楼（待核验）",
      "category": "文化地标",
      "address": "待成员2调查补全",
      "description": "示例点位；开放情况、位置、步行入口和介绍来源需要核验。",
      "notice": "未核验，暂不支持地图导航。",
      "coordinates": null,
      "sources": []
    },
    {
      "id": "gyp_002",
      "status": "draft",
      "name": "青云路（待核验）",
      "category": "街区",
      "address": "待成员2调查补全",
      "description": "示例点位；街区范围、通行条件和适宜停留点需要核验。",
      "notice": "未核验，不提供营业时间承诺。",
      "coordinates": null,
      "sources": []
    },
    {
      "id": "gyp_003",
      "status": "draft",
      "name": "文昌阁（待核验）",
      "category": "文化地标",
      "address": "待成员2调查补全",
      "description": "用于演示路线引用同一份点位数据，实际内容由团队调查补充。",
      "notice": "未核验，暂不支持地图导航。",
      "coordinates": null,
      "sources": []
    }
  ],
  "routes": [
    {
      "id": "gyr_001",
      "status": "draft",
      "name": "贵阳老城漫步 · 联调草案",
      "district": "待核验商圈A",
      "metroStation": "待核验地铁站",
      "summary": "演示两点路线与耗时汇总，非已核验攻略。",
      "distanceKm": 2.4,
      "distanceKind": "estimate",
      "tags": [
        "老城",
        "文化"
      ],
      "stops": [
        {
          "order": 1,
          "pointId": "gyp_001",
          "stayMinutes": 20,
          "walkMinutesFromPrevious": 0
        },
        {
          "order": 2,
          "pointId": "gyp_002",
          "stayMinutes": 30,
          "walkMinutesFromPrevious": 35
        }
      ],
      "walkingMinutes": 35,
      "stayingMinutes": 50,
      "totalMinutes": 85,
      "notice": "距离和耗时为联调占位值，发布前必须调查和替换。",
      "sources": []
    },
    {
      "id": "gyr_002",
      "status": "draft",
      "name": "贵阳文化街区 · 联调草案",
      "district": "待核验商圈B",
      "metroStation": "待核验地铁站",
      "summary": "演示按主题、商圈和耗时筛选。",
      "distanceKm": 1.8,
      "distanceKind": "estimate",
      "tags": [
        "街巷",
        "文化"
      ],
      "stops": [
        {
          "order": 1,
          "pointId": "gyp_003",
          "stayMinutes": 25,
          "walkMinutesFromPrevious": 0
        },
        {
          "order": 2,
          "pointId": "gyp_001",
          "stayMinutes": 20,
          "walkMinutesFromPrevious": 25
        }
      ],
      "walkingMinutes": 25,
      "stayingMinutes": 45,
      "totalMinutes": 70,
      "notice": "路线连通性未验证，仅供开发测试。",
      "sources": []
    }
  ]
};
