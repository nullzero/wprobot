# -*- coding: utf-8 -*-
"""
This is a user configuration file.
"""

pageConf = u"ผู้ใช้:Nullzerobot/ปรับปรุงชื่อฉลาก"

checklist = [ # make sure that each one will not overlap each other
    {
        "name": "disambiguous",
        "claims": [{"name": "P31", "ref": "P143", "nameItem": "Q4167410", "refItem": "Q565074"}],
        "description": u"หน้าแก้ความกำกวมวิกิพีเดีย",
        "detectFromTitle": u"(แก้ความกำกวม)",
        "detectFromNamespace": None,
    },
    {
        "name": "template",
        "claims": [{"name": "P31", "ref": None, "nameItem": "Q11266439", "refItem": None}],
        "description": u"หน้าแม่แบบวิกิพีเดีย",
        "detectFromNamespace": 10,
        "detectFromTitle": None,
    },
    {
        "name": "category",
        "claims": [{"name": "P31", "ref": None, "nameItem": "Q4167836", "refItem": None}],
        "description": u"หน้าหมวดหมู่วิกิพีเดีย",
        "detectFromNamespace": 14,
        "detectFromTitle": None,
    },
]

namespaces = [0, 10, 14]