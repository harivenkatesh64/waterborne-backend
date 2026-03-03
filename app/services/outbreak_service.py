from app.database import reports_collection
from datetime import datetime, timedelta

def check_outbreak(report):

    total_today = (
        report["diarrhea_cases"] +
        report["fever_cases"] +
        report["vomiting_cases"] +
        report["jaundice_cases"]
    )

    # Threshold Rule
    if total_today > 20:
        return True

    # Trend Rule (7 day average)
    last_week = datetime.utcnow() - timedelta(days=7)

    old_reports = list(reports_collection.find({
        "village": report["village"],
        "timestamp": {"$gte": last_week}
    }))

    if len(old_reports) == 0:
        return False

    avg = sum(
        r["diarrhea_cases"] +
        r["fever_cases"] +
        r["vomiting_cases"] +
        r["jaundice_cases"]
        for r in old_reports
    ) / len(old_reports)

    if total_today > avg * 2:
        return True

    return False