import os
import json
import boto3
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter
 
def lambda_handler(event, context):
    # Extract invoice information from the event
    invoice_data = event['invoice_data']
    recipient_email = event['recipient_email']
 
    # Generate PDF invoice
    pdf_content = generate_invoice_pdf(invoice_data)
 
    # Upload PDF content to S3
    s3_bucket = '22185101-pdf-upload'
    pdf_key = f'invoices/{recipient_email}/invoice.pdf'
    upload_to_s3(pdf_content, s3_bucket, pdf_key)
 
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Invoice PDF stored in S3 successfully.'})
    }
 
def generate_invoice_pdf(invoice_data):
    buffer = BytesIO()
 
    # Create PDF using reportlab
    with canvas.Canvas(buffer) as pdf:
        pdf.drawString(100, 800, 'Invoice')
        pdf.drawString(100, 780, '-------------------------')
 
        # Populate the PDF with invoice data
        for i, (item, amount) in enumerate(invoice_data.items(), start=1):
            pdf.drawString(100, 780 - i * 20, f'{item}: ${amount:.2f}')
 
        pdf.drawString(100, 780 - (i + 1) * 20, '-------------------------')
        total_amount = sum(invoice_data.values())
        pdf.drawString(100, 780 - (i + 2) * 20, f'Total: ${total_amount:.2f}')
 
    buffer.seek(0)
    return buffer.getvalue()
 
def upload_to_s3(pdf_content, s3_bucket, pdf_key):
    # Create an S3 client
    s3_client = boto3.client('s3')
 
    # Upload the PDF content to S3
    try:
        response = s3_client.put_object(
            Bucket=s3_bucket,
            Key=pdf_key,
            Body=pdf_content,
            ContentType='application/pdf'
        )
        print(f"Invoice PDF uploaded to S3 bucket {s3_bucket} with key {pdf_key}.")
    except Exception as e:
        print(f"Error uploading Invoice PDF to S3: {str(e)}")