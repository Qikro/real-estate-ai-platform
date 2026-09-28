from datetime import datetime, timezone
from typing import Dict, Any
import json
from sqlalchemy.orm import Session
from app.agents.base import BaseAgent
from app.models.entities import InvestorReport, PropertyListing
from app.services.pdf_generator import generate_pdf_report
from app.services.excel_generator import generate_excel_report

class InvestorReportingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Investor Research & Reporting Agent",
            role="Real Estate Investment Underwriting and Report Generator",
            description="Performs financial underwriting, yields, net operating income models, and produces PDF & Excel investment memorandums."
        )

    def execute(self, tenant_id: str, command: str, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        self.status = "RUNNING"
        self.last_run = datetime.now(timezone.utc)
        self.total_runs += 1
        self.total_cost_usd += 0.015

        property_id = payload.get("property_id")
        prop = None
        if property_id:
            prop = db.query(PropertyListing).filter(PropertyListing.id == property_id, PropertyListing.tenant_id == tenant_id).first()

        if not prop:
            prop = db.query(PropertyListing).filter(
                PropertyListing.tenant_id == tenant_id,
                PropertyListing.availability_status == "AVAILABLE"
            ).first()

        if not prop:
            self.status = "IDLE"
            return {"status": "FAILED", "message": "No available properties found to generate report."}

        client_name = payload.get("client_name", "Vertex Capital India")
        target_budget = payload.get("target_budget", prop.asking_price * 1.1)

        # Financial Underwriting calculations
        asking_price = prop.asking_price
        # Baseline commercial yield for Hyderabad Grade A is ~7.5 - 8.5%
        gross_yield = 8.2
        gross_annual_rent = asking_price * (gross_yield / 100.0)
        vacancy_rate = 5.0
        maintenance_rate = 3.0
        monthly_expenses = round((asking_price * 0.007) / 12, 2)  # ~0.7% annual OPEX
        annual_opex = monthly_expenses * 12

        effective_gross_income = gross_annual_rent * (1 - (vacancy_rate / 100.0))
        net_operating_income = effective_gross_income - annual_opex - (gross_annual_rent * (maintenance_rate / 100.0))
        cap_rate = round((net_operating_income / asking_price) * 100.0, 2)

        title = f"Investment Memorandum: {prop.title} ({prop.neighborhood})"
        exec_summary = (
            f"Underwriting analysis for {prop.title}, an institutional-grade {prop.category} asset situated in {prop.neighborhood}, "
            f"Hyderabad. Asking acquisition price is INR {asking_price:,.2f} with an underwritten gross rental yield of {gross_yield:.1f}% "
            f"and an estimated net capitalization rate of {cap_rate:.2f}%. Hyderabad's western corridor continues to exhibit strong tech absorption "
            f"and sustained commercial capital value appreciation."
        )

        risks = (
            "1. Tenant Renewal & Lease Expiration: Assumes tenancy lease roll-over at market rates.\n"
            "2. Macro Interest Rate Environment: Cost of debt may fluctuate based on RBI repo adjustments.\n"
            "3. Micro-market Vacancy: Sub-market office supply additions in Kokapet and Financial District over 24 months."
        )

        checklist = (
            "- Title Search & Encumbrance Certificate (EC) for past 30 years.\n"
            "- Verification of HMDA / GHMC Building Sanction Plan and Occupancy Certificate (OC).\n"
            "- Telangana RERA registration status audit.\n"
            "- Pre-lease agreements, lock-in terms, and tenant security deposit escrows.\n"
            "- Municipal property tax and electricity dues clearance verification."
        )

        report_data = {
            "title": title,
            "client_name": client_name,
            "preferred_locations": f"{prop.neighborhood}, Hyderabad",
            "target_budget": target_budget,
            "asking_price": asking_price,
            "gross_yield": gross_yield,
            "cap_rate": cap_rate,
            "monthly_expenses": monthly_expenses,
            "vacancy_rate_pct": vacancy_rate,
            "maintenance_reserve_pct": maintenance_rate,
            "executive_summary": exec_summary,
            "risks_and_caveats": risks,
            "legal_due_diligence_checklist": checklist
        }

        # Generate PDF and Excel
        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"report_{tenant_id[:8]}_{timestamp_str}.pdf"
        xlsx_filename = f"model_{tenant_id[:8]}_{timestamp_str}.xlsx"

        pdf_path = generate_pdf_report(report_data, pdf_filename)
        xlsx_path = generate_excel_report(report_data, xlsx_filename)

        report = InvestorReport(
            tenant_id=tenant_id,
            title=title,
            property_id=prop.id,
            client_name=client_name,
            target_budget=target_budget,
            property_type=prop.category,
            preferred_locations=f"{prop.neighborhood}, Hyderabad",
            executive_summary=exec_summary,
            asking_price=asking_price,
            estimated_rental_yield=gross_yield,
            gross_yield=gross_yield,
            cap_rate=cap_rate,
            monthly_expenses=monthly_expenses,
            vacancy_rate_pct=vacancy_rate,
            maintenance_reserve_pct=maintenance_rate,
            risks_and_caveats=risks,
            legal_due_diligence_checklist=checklist,
            sources_json=json.dumps([{"source": prop.listing_source, "url": prop.original_url}]),
            pdf_path=pdf_path,
            xlsx_path=xlsx_path,
            status="READY"
        )
        db.add(report)
        db.commit()

        self.log_audit(
            db=db,
            tenant_id=tenant_id,
            action="INVESTOR_REPORT_GENERATED",
            entity_type="InvestorReport",
            entity_id=report.id,
            details={
                "title": report.title,
                "pdf": pdf_filename,
                "xlsx": xlsx_filename,
                "cap_rate": cap_rate
            }
        )

        self.status = "IDLE"
        return {
            "status": "SUCCESS",
            "message": f"Successfully generated investor memorandum and financial model for {client_name}.",
            "report_id": report.id,
            "title": report.title,
            "cap_rate": f"{cap_rate}%",
            "gross_yield": f"{gross_yield}%",
            "pdf_download": f"/api/reports/{report.id}/download/pdf",
            "xlsx_download": f"/api/reports/{report.id}/download/xlsx"
        }
