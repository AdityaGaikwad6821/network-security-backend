from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER


def generate_audit_pdf(
    audit_id,
    vendor,
    security_score,
    findings,
    suggestions,
    qr_file,
    output_file="security_audit_report.pdf"
):
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    story = []

    # Title
    story.append(Paragraph("Network Security Audit Report", title_style))
    story.append(Spacer(1, 20))

    # Basic Information
    story.append(Paragraph("<b>Basic Information</b>", styles["Heading2"]))
    story.append(Paragraph(f"Audit ID: {audit_id}", styles["Normal"]))
    story.append(Paragraph(f"Vendor: {vendor}", styles["Normal"]))
    story.append(Spacer(1, 15))

    # Security Score
    story.append(Paragraph("<b>Security Score</b>", styles["Heading2"]))
    story.append(
        Paragraph(
            f"Overall Security Score: <b>{security_score}/100</b>",
            styles["Normal"]
        )
    )
    story.append(Spacer(1, 15))

    # Findings
    story.append(Paragraph("<b>Security Findings</b>", styles["Heading2"]))

    if findings:
        table_data = [["Issue", "Severity"]]

        for finding in findings:
            table_data.append([
                finding["issue"],
                finding["severity"]
            ])

        table = Table(table_data, colWidths=[350, 100])

        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ])
        )

        story.append(table)

    else:
        story.append(
            Paragraph("No security issues found.", styles["Normal"])
        )

    story.append(Spacer(1, 15))

    # Suggestions
    story.append(Paragraph("<b>Suggestions / Remediation</b>", styles["Heading2"]))

    for suggestion in suggestions:
        story.append(
            Paragraph(f"• {suggestion}", styles["Normal"])
        )

    story.append(Spacer(1, 20))

    # QR Code
    story.append(Paragraph("<b>Audit Verification QR</b>", styles["Heading2"]))
    story.append(Spacer(1, 10))

    qr_image = Image(qr_file, width=150, height=150)
    story.append(qr_image)

    story.append(Spacer(1, 10))
    story.append(
        Paragraph(
            f"Scan this QR code to identify audit {audit_id}.",
            styles["Normal"]
        )
    )

    doc.build(story)

    return output_file


if __name__ == "__main__":

    findings = [
        {
            "issue": "Telnet service enabled",
            "severity": "High"
        },
        {
            "issue": "Logging is disabled",
            "severity": "Medium"
        },
        {
            "issue": "SNMP public community detected",
            "severity": "High"
        }
    ]

    suggestions = [
        "Disable Telnet and use SSH.",
        "Enable proper system logging.",
        "Replace the default SNMP community string."
    ]

    pdf_file = generate_audit_pdf(
        audit_id="AUDIT-2026-0001",
        vendor="Cisco",
        security_score=65,
        findings=findings,
        suggestions=suggestions,
        qr_file="AUDIT-2026-0001_qr.png"
    )

    print(f"PDF generated successfully: {pdf_file}")