from fastapi import APIRouter
from models.nosql.activitylog import ActivityLog
from schemas.activitylog import CreateActivity

activity_router = APIRouter(prefix="/activity",tags=["Activity"])

@activity_router.post("/add")
async def add_activity(activity: CreateActivity ):
    log = ActivityLog(action=activity.action, performed_by=activity.performed_by)
    await log.insert()
    return log

@activity_router.get("/all-activity")
async def get_all_activity():
    return await ActivityLog.find_all().sort("-created_at").to_list()