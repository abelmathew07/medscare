from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
import io
from flask_restful import Resource
from flask import request, make_response
import datetime
import pytz

id=1009273
ist = pytz.timezone('Asia/Kolkata')
now = datetime.datetime.now(ist)
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

class GenerateOPTicket:
    def generate_pdf(self, data):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        styles = getSampleStyleSheet()
        normal_style = styles['Normal']
        bold_style = styles['Normal']
        bold_style.fontName = 'Helvetica-Bold'
        italic_style = styles['Normal']
        italic_style.fontName = 'Helvetica-Oblique'
        
        try:

            logo_path = 'pic/logo.png'  
            try:
                p.drawImage(logo_path, 440, 680, width=100, height=100)
            except Exception as e:
                print("Error loading hospital logo:", e)

            # Hospital name

            p.setFont("Helvetica-Bold", 20)
            p.drawString(100, 750, f"Dr.Susan's Multi-Speciality Hospital")
            p.setFont("Helvetica", 14)
            p.drawString(120, 730, f"Anchuthengu, chirayankeezhu P O, kollam")
            p.setFont("Helvetica", 12)
            p.drawString(160, 710, f"2001/7986/7328972/1005")
            p.setFont("Helvetica", 10)
            p.drawString(140, 690, f"Mob no:+91 1242328237,Ph no:0471 838374")
            p.setFont("Helvetica-Bold", 18)
            p.drawString(210, 640, f"Out Patient Ticket")
            p.setFont("Helvetica", 12)
            p.drawString(230, 620, f"Ticket ID:{data['id']}")

            # Patient details
            if 'patient_name' in data:
                p.setFont("Helvetica-Bold", 12)
                p.drawString(50, 590, f"Patient Name: {data['patient_name']}")
            if 'address' in data:
                p.setFont("Helvetica", 12)
                p.drawString(50, 570, f"Address: {data['address']}")
                p.drawString(400, 590, f" Date/Time: {formatted_time}")
                p.drawString(400, 570, f" Age: {data['Age']}")
                p.drawString(475, 570, f" Gender: {data['Gender']}")
                p.drawString(100, 540, f"Heart Rate: {data['hr']}bpm")
                p.drawString(230, 540, f"Temp: {data['temperature']}C")
                p.drawString(310, 540, f"SpO2: {data['spo2']} %")
            # Symptoms and predicted disease
            if 'symptoms' in data:
                p.drawString(100, 520, f"Symptoms: {data['symptoms']}")
            if 'predicted_disease' in data:
                # p.drawString(50, 670, f"Predicted Disease: {data['predicted_disease']}")
                p.drawString(100, 500, f"Predicted Disease: {data['predicted_disease']}")

            # Add more details as needed

            p.showPage()
            p.save()

            pdf_data = buffer.getvalue()
            buffer.close()
            return pdf_data
        except Exception as e:
            print("Error generating PDF:", e)
            return None
