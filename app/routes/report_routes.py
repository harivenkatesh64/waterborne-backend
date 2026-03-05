from fastapi import APIRouter, Depends, HTTPException
from app.database import reports_collection, alerts_collection
from datetime import datetime
from app.schemas.report_schema import HealthReport
from app.utils.dependencies import get_current_user
from app.utils.email_service import send_email
from app.database import users_collection
from app.models.report_model import ReportModel
from app.logger import logger

router = APIRouter()

# 🔥 Set Threshold (Change to 3 for testing)
THRESHOLD = 3

@router.post("/submit")
def submit_report(
    report: HealthReport,
    current_user=Depends(get_current_user)
):

    # 🔐 Only volunteers can submit reports
    if current_user.get("role") != "volunteer":
        raise HTTPException(
            status_code=403,
            detail="Only volunteers can submit reports"
        )

    # 📄 Create report document
    report_doc = ReportModel.create_report_document(report.dict())

    # Attach submitted_by from token
    report_doc["submitted_by"] = current_user["email"]

    # 💾 Save to MongoDB
    reports_collection.insert_one(report_doc)

    village = report_doc["village"]

    # 🧠 Identify which disease was submitted
    selected_disease = None

    if report_doc["diarrhea_cases"] == 1:
        selected_disease = "diarrhea"
    elif report_doc["fever_cases"] == 1:
        selected_disease = "fever"
    elif report_doc["vomiting_cases"] == 1:
        selected_disease = "vomiting"
    elif report_doc["jaundice_cases"] == 1:
        selected_disease = "jaundice"

    outbreak_detected = False
    case_count = 0

    if selected_disease:

        # 🔢 Count total cases for same village + same disease
        case_count = reports_collection.count_documents({
            "village": village,
            f"{selected_disease}_cases": 1
        })

        logger.info(
            f"Village: {village} | Disease: {selected_disease} | Total Cases: {case_count}"
        )

        if case_count >= THRESHOLD:
            print("OUTBREAK DETECTED")

            outbreak_detected = True

            # 🔥 Determine Severity
            if case_count >= 5:
                severity = "Critical"
            elif case_count >= 4:
                severity = "High"
            elif case_count >= 3:
                severity = "Medium"
            else:
                severity = "Warning"

            # 🔍 Check if active alert exists
            existing_alert = alerts_collection.find_one({
                "village": village,
                "disease": selected_disease,
                "status": "active"
            })

            if existing_alert:

                alerts_collection.update_one(
                    {"_id": existing_alert["_id"]},
                    {
                        "$set": {
                            "total_cases": case_count,
                            "severity": severity,
                            "updated_at": datetime.utcnow()
                        }
                    }
                )

                logger.info(
                    f"Alert UPDATED | Village: {village} | Severity: {severity}"
                )

            else:

                alert_doc = {
                    "village": village,
                    "disease": selected_disease,
                    "total_cases": case_count,
                    "severity": severity,
                    "risk_factors": report_doc["risk_factors"],
                    "water_source_condition": report_doc["water_source_condition"],
                    "created_at": datetime.utcnow(),
                    "status": "active",
                    "reported_by": current_user["email"]
                }

                alerts_collection.insert_one(alert_doc)

                logger.warning(
                    f"New Outbreak Alert | Village: {village} | Severity: {severity}"
                )

            # 🚨 SEND ALERT EMAILS USING BCC (ONE EMAIL)

            users = users_collection.find({
                "role": {"$in": ["admin", "volunteer"]}
            })

            email_list = [u["email"] for u in users]

            try:
                send_email(
                    email_list,
                    "⚠ Waterborne Disease Outbreak Alert",
                    f"""
Hello,

⚠ A potential outbreak has been detected.

Village: {village}
Disease: {selected_disease}
Total Cases: {case_count}
Severity Level: {severity}

Please take necessary precautions and coordinate with health authorities.

Smart Waterborne Disease Surveillance System
"""
                )

                logger.info("Alert email sent to all admins and volunteers")

            except Exception as e:
                logger.error(f"Alert email sending failed: {str(e)}")

    return {
        "message": "Case recorded successfully",
        "outbreak_alert": outbreak_detected
    }