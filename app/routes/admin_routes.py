from fastapi import APIRouter, Depends, HTTPException
from app.database import reports_collection
from app.database import alerts_collection
from app.utils.dependencies import get_current_user
from datetime import datetime
from app.middleware.role_middleware import require_role
from app.models.report_model import ReportModel

router = APIRouter()


@router.get("/all-reports")
def get_all_reports(user=Depends(get_current_user)):

    require_role(user, "admin")

    reports = list(reports_collection.find({}))

    clean_reports = [ReportModel.sanitize_report_output(r) for r in reports]

    return clean_reports

@router.get("/outbreak-alerts")
def get_outbreak_alerts(current_user=Depends(get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    alerts = list(alerts_collection.find({"status": "active"}, {"_id": 0}))
    return alerts

@router.put("/resolve-alert/{village}")
def resolve_alert(village: str, current_user=Depends(get_current_user)):

    # 🔐 Only admin can resolve alerts
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    result = alerts_collection.update_one(
        {
            "village": village,
            "status": "active"
        },
        {
            "$set": {
                "status": "resolved",
                "resolved_at": datetime.utcnow()
            }
        }
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="No active alert found")

    return {"message": f"Alert for {village} marked as resolved"}

# ✅ 4️⃣ Admin Statistics
@router.get("/stats")
def get_admin_stats(current_user=Depends(get_current_user)):

    # 🔐 Only Admin
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    total_reports = reports_collection.count_documents({})

    active_alerts = alerts_collection.count_documents({
        "status": "active"
    })

    resolved_alerts = alerts_collection.count_documents({
        "status": "resolved"
    })

    total_alerts = alerts_collection.count_documents({})

    return {
        "total_reports": total_reports,
        "active_alerts": active_alerts,
        "resolved_alerts": resolved_alerts,
        "total_alerts": total_alerts
    }