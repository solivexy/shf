import logging
from fastapi import APIRouter, HTTPException, Response
from services.analysis_service import analysis_service
from services.report_service import report_service

logger = logging.getLogger("api_reports")
router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("")
async def list_reports(limit: int = 25):
    """
    Returns persistent quantitative evaluation logs and dossiers across multi-agent workflows.
    """
    runs = await analysis_service.get_all_reports(limit=limit)
    reports = []
    for run in runs:
        task_id = run.get("task_id", "UNKNOWN")
        ticker = run.get("ticker", "UNKNOWN")
        pm = run.get("portfolio_manager") or {}
        news = run.get("news_intelligence") or {}
        summary = pm.get("mandate_summary") or news.get("summary") or "Complete multi-agent quantitative evaluation."
        decision = pm.get("decision", "HOLD")
        confidence = pm.get("confidence", 85.0)
        created_at = run.get("created_at")
        
        reports.append({
            "report_id": task_id,
            "ticker": ticker,
            "summary": summary,
            "decision": decision,
            "confidence": confidence,
            "created_at": created_at,
            "pdf_url": f"/api/v1/reports/pdf/{task_id}",
            "csv_url": f"/api/v1/reports/csv/{task_id}"
        })
    return {"reports": reports, "total": len(reports)}


@router.get("/pdf/{task_id}")
async def get_pdf_report(task_id: str):
    """
    Downloads a professional PDF investment research report for a completed analysis task.
    """
    run_result = await analysis_service.get_task_status(task_id)
    if not run_result:
        raise HTTPException(status_code=404, detail=f"Analysis task {task_id} not found.")

    pdf_bytes = report_service.generate_pdf_report(run_result)
    headers = {
        "Content-Disposition": f"attachment; filename=SHF_Research_Report_{run_result.ticker}_{task_id}.pdf"
    }
    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)


@router.get("/csv/{task_id}")
async def get_csv_report(task_id: str):
    """
    Downloads structured CSV export of agent outputs and timeline metrics.
    """
    run_result = await analysis_service.get_task_status(task_id)
    if not run_result:
        raise HTTPException(status_code=404, detail=f"Analysis task {task_id} not found.")

    csv_text = report_service.generate_csv_export(run_result)
    headers = {
        "Content-Disposition": f"attachment; filename=SHF_Export_{run_result.ticker}_{task_id}.csv"
    }
    return Response(content=csv_text, media_type="text/csv", headers=headers)
