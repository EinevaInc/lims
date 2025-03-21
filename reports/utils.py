from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf_report(response, properties):
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, "Property Listing Report")
    y = 700
    for property in properties:
        p.drawString(100, y, f"Stand Number: {property.stand_number}, Land Use: {property.landuse_type}, Status: {property.sales_status}, Area: {property.size_area_sqm} SqM, Date Created: {property.date_created}")
        y -= 20
    p.showPage()
    p.save()
