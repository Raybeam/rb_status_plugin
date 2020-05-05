from plugins.lumen_plugin.report_repo import VariablesReportRepo
from plugins.lumen_plugin.report_instance import ReportInstance
import datetime
import logging
log = logging.getLogger(__name__)

dummy_reports = [
    {
        "id": 1,
        "passed": False,
        "updated": datetime.datetime.now(),
        "title": "Diary of a Madman",
        "description": (
            "Donec posuere tincidunt metus sed dictum. Proin commodo nibh ",
            "magna, vitae tristique ex rhoncus vitae.",
        ),
        "owner_name": "Odele Barnewelle",
        "owner_email": "obarnewelle0@devhub.com",
        "errors": [
            {
                "id": 1,
                "title": "CD DiorSkin Forever Flawless Fusion Wear Makeup SPF 25 - 010",
                "description": "Unspecified open wound of left breast, initial encounter",
            },
            {
                "id": 2,
                "title": "Adoxa",
                "description": (
                    "Primary blast injury of unspecified ear, subsequent ",
                    "encounter",
                ),
            },
        ],
    },
    {
        "id": 2,
        "passed": True,
        "updated": datetime.datetime.now(),
        "title": "Atragon (Kaitei Gunkan)",
        "description": (
            "Morbi eget diam porta, auctor est a, hendrerit lorem. Nulla sit ",
            "amet tincidunt lacus, id varius tellus.",
        ),
        "owner_name": "Godard McOnie",
        "owner_email": "gmconie1@gizmodo.com",
    },
    {
        "id": 3,
        "passed": True,
        "updated": datetime.datetime.now(),
        "title": "Sweet Mud (Adama Meshuga'at)",
        "description": (
            "Nunc augue nulla, imperdiet eu ornare a, dignissim convallis ",
            "ipsum. Praesent tellus ipsum, malesuada at neque id, scelerisque consequat ",
            "magna.",
        ),
        "owner_name": "Camila Dickinson",
        "owner_email": "cdickinson2@1688.com",
    },
    {
        "id": 4,
        "passed": False,
        "updated": datetime.datetime.now(),
        "title": "Say It Isn't So",
        "description": "Nam hendrerit mauris est, laoreet pulvinar elit laoreet vel.",
        "owner_name": "Ian Iskower",
        "owner_email": "iiskower3@yahoo.com",
        "errors": [
            {
                "id": 4,
                "title": "Bacitracin Zinc and Polymyxin B Sulfate",
                "description": "Displaced transverse fracture of left patella",
            }
        ],
    },
    {
        "id": 5,
        "passed": True,
        "updated": datetime.datetime.now(),
        "title": "Soldier of Orange (a.k.a. Survival Run) (Soldaat van Oranje)",
        "description": (
            "Ut semper dolor sit amet diam ultrices, nec porttitor erat ",
            "viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        ),
        "owner_name": "Brad Edgeson",
        "owner_email": "bedgeson4@wikipedia.org",
    },
]

def get_all_reports(session=None):
    reports = []
    passed = True
    updated = None

    for report in VariablesReportRepo.list():
        try:
            ri = ReportInstance.get_latest(report)

            if not updated:
                updated = ri.updated

            if updated < ri.updated:
                updated = ri.updated

            r = {
                "id": ri.dag_id,
                "passed": ri.passed,
                "updated": ri.updated,
                "title": report.name,
                "owner_email": report.emails,
                "subscribers": report.emails,
            }

            r["errors"] = ri.errors()
            if len(r["errors"]) > 0:
                passed = False

            log.info(r)
            reports.append(r)
        except Exception as e:
            log.exception(e)
            log.error("Failed to generate report: " + str(e))
            flash("Failed to generate report: " + str(e), "error")

    return reports