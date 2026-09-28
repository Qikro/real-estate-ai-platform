import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from app.core.config import settings

def generate_excel_report(report_data: dict, filename: str) -> str:
    os.makedirs(settings.REPORTS_DIR, exist_ok=True)
    file_path = os.path.join(settings.REPORTS_DIR, filename)

    wb = Workbook()
    ws = wb.active
    ws.title = "Underwriting & Financials"

    # Header styling
    header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    title_font = Font(name="Calibri", size=14, bold=True, color="0F172A")
    subtitle_font = Font(name="Calibri", size=10, italic=True, color="64748B")
    data_font = Font(name="Calibri", size=10)
    bold_font = Font(name="Calibri", size=10, bold=True)

    thin_border = Border(
        left=Side(style='thin', color='E2E8F0'),
        right=Side(style='thin', color='E2E8F0'),
        top=Side(style='thin', color='E2E8F0'),
        bottom=Side(style='thin', color='E2E8F0')
    )

    ws["A1"] = "REAL ESTATE AI OPERATIONS PLATFORM"
    ws["A1"].font = title_font
    ws["A2"] = f"Underwriting Model: {report_data.get('title', 'Investment Analysis')}"
    ws["A2"].font = subtitle_font
    ws["A3"] = f"Client: {report_data.get('client_name', 'Client')} | Target Market: {report_data.get('preferred_locations', 'Hyderabad')}"
    ws["A3"].font = subtitle_font

    headers = ["Parameter", "Value", "Unit / Metric", "Underwriting Notes"]
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=5, column=col_num, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    rows = [
        ("Asking Acquisition Price", report_data.get("asking_price", 0), "INR", "Base asking price from verified source"),
        ("Target Client Allocation", report_data.get("target_budget", 0), "INR", "Maximum authorized client capital"),
        ("Estimated Gross Annual Rent", report_data.get("asking_price", 0) * (report_data.get("gross_yield", 8.2) / 100), "INR / year", "Calculated from gross yield"),
        ("Gross Rental Yield", report_data.get("gross_yield", 8.2), "%", "Market rental benchmark"),
        ("Vacancy Allowance", report_data.get("vacancy_rate_pct", 5.0), "%", "Standard vacancy deduction"),
        ("Maintenance Reserve", report_data.get("maintenance_reserve_pct", 3.0), "%", "Annual reserve allowance"),
        ("Monthly Operating Expenses", report_data.get("monthly_expenses", 25000), "INR / month", "Estimated property tax, insurance, CAM"),
        ("Annual Operating Expenses", report_data.get("monthly_expenses", 25000) * 12, "INR / year", "Annualized operational costs"),
        ("Estimated Net Operating Income (NOI)", report_data.get("asking_price", 0) * (report_data.get("cap_rate", 6.8) / 100), "INR / year", "Net projected return before debt"),
        ("Net Capitalization Rate (Cap Rate)", report_data.get("cap_rate", 6.8), "%", "Underwritten cap rate")
    ]

    for row_idx, data in enumerate(rows, 6):
        for col_idx, val in enumerate(data, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.font = bold_font if col_idx == 1 else data_font
            cell.border = thin_border
            if isinstance(val, float):
                cell.number_format = '#,##0.00' if val > 100 else '0.00'

    ws.column_dimensions['A'].width = 34
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 16
    ws.column_dimensions['D'].width = 44

    wb.save(file_path)
    return file_path
