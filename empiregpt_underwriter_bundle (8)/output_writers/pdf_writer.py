from fpdf import FPDF

def export_pdf(deal):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Investor Deal Summary", ln=1, align="C")
    for k, v in deal.items():
        pdf.cell(200, 10, txt=f"{k}: {v}", ln=1)
    pdf.output("deal_summary.pdf")