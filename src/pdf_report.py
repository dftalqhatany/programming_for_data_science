from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import io


def generate_pdf(result):

    buffer = io.BytesIO()

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(buffer)

    elements = []

    elements.append(Paragraph("AI Data Quality Report", styles["Title"]))

    elements.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Executive Summary", styles["Heading2"]))
    elements.append(Paragraph(result["executive_summary"], styles["Normal"]))

    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Direct Answer", styles["Heading2"]))
    elements.append(Paragraph(result["direct_answer"], styles["Normal"]))

    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Findings", styles["Heading2"]))

    for f in result["findings"]:
        elements.append(Paragraph(f"- {f}", styles["Normal"]))

    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Recommendations", styles["Heading2"]))

    for r in result["recommendations"]:
        elements.append(Paragraph(f"- {r}", styles["Normal"]))

    doc.build(elements)

    buffer.seek(0)

    return buffer
