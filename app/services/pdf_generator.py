import os
from datetime import datetime, timezone
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from app.core.config import settings

def generate_pdf_report(report_data: dict, filename: str) -> str:
    os.makedirs(settings.REPORTS_DIR, exist_ok=True)
    file_path = os.path.join(settings.REPORTS_DIR, filename)

    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=15
    )
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155')
    )
    badge_style = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#2563EB')
    )

    story = []

    # Header
    story.append(Paragraph("REAL ESTATE AI OPERATIONS COMPANY", badge_style))
    story.append(Paragraph(report_data.get("title", "Commercial Property Investment Report"), title_style))
    meta_text = f"Prepared for: <b>{report_data.get('client_name', 'Client')}</b> &nbsp;|&nbsp; Target Market: <b>{report_data.get('preferred_locations', 'Hyderabad')}</b> &nbsp;|&nbsp; Date: {datetime.now(timezone.utc).strftime('%d %b %Y')}"
    story.append(Paragraph(meta_text, subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=15))

    # Executive Summary
    story.append(Paragraph("1. Executive Summary", h2_style))
    exec_summary = report_data.get("executive_summary", "Comprehensive investment assessment based on verified Hyderabad market parameters.")
    story.append(Paragraph(exec_summary, body_style))
    story.append(Spacer(1, 10))

    # Key Metrics Table
    story.append(Paragraph("2. Financial Underwriting & Projections", h2_style))
    metrics_data = [
        ["Metric", "Value", "Notes / Verification"],
        ["Asking Price", f"INR {report_data.get('asking_price', 0):,.2f}", "Verified listing asking price"],
        ["Target Budget", f"INR {report_data.get('target_budget', 0):,.2f}", "Client portfolio allocation"],
        ["Gross Rental Yield", f"{report_data.get('gross_yield', 0):.2f}%", "Market baseline estimate"],
        ["Est. Net Cap Rate", f"{report_data.get('cap_rate', 0):.2f}%", "After vacancy and maintenance reserve"],
        ["Vacancy Assumption", f"{report_data.get('vacancy_rate_pct', 5.0):.1f}%", "Standard institutional assumption"],
        ["Maintenance Reserve", f"{report_data.get('maintenance_reserve_pct', 3.0):.1f}%", "Annual capital expenditure reserve"],
        ["Est. Monthly Expenses", f"INR {report_data.get('monthly_expenses', 0):,.2f}", "Maintenance & property management"]
    ]
    t = Table(metrics_data, colWidths=[150, 150, 220])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    # Risks & Caveats
    story.append(Paragraph("3. Investment Risks & Market Considerations", h2_style))
    risks = report_data.get("risks_and_caveats", "Subject to tenant lease agreement, market vacancy, and regulatory compliance.")
    story.append(Paragraph(risks, body_style))
    story.append(Spacer(1, 10))

    # Legal Due Diligence Checklist
    story.append(Paragraph("4. Legal Due Diligence Checklist", h2_style))
    checklist = report_data.get("legal_due_diligence_checklist", "- Verify Title Deed and 30-year Encumbrance Certificate (EC)\n- GHMC/HMDA layout and occupancy approvals\n- RERA registration verification")
    formatted_checklist = "<br/>".join([f"&#8226; {line.strip('- ')}" for line in checklist.split("\n") if line.strip()])
    story.append(Paragraph(formatted_checklist, body_style))
    story.append(Spacer(1, 15))

    # Disclaimer
    disclaimer_text = (
        "<b>Notice & Disclaimer:</b> This report is generated by the Real Estate AI Operations Platform for informational "
        "and preliminary evaluation purposes only. It does not constitute legal, tax, or regulated financial advice. "
        "All property listings, rental yield projections, and legal status must be independently verified by legal counsel prior to transaction execution."
    )
    story.append(Paragraph(disclaimer_text, ParagraphStyle('Disclaimer', parent=styles['Normal'], fontSize=7.5, leading=10, textColor=colors.HexColor('#94A3B8'))))

    doc.build(story)
    return file_path
