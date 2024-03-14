import json
import boto3
from fpdf import FPDF

def generate_invoice_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add invoice header
    pdf.cell(200, 10, txt="Invoice", ln=True, align='C')
    pdf.ln(10)  # Add a line break

    # Add customer information
    pdf.cell(0, 10, txt=f"Customer: {data['customer']}", ln=True)
    pdf.cell(0, 10, txt=f"Amount: {data['amount']}", ln=True)
    pdf.ln(10)  # Add a line break

    # Add invoice details
    pdf.cell(0, 10, txt="Invoice Details:", ln=True)
    for product, cost in data['products'].items():
        pdf.cell(0, 10, txt=f"Product: {product}, Cost: {cost}", ln=True)
    total_cost = sum(data['products'].values())
    pdf.cell(0, 10, txt=f"Total: {total_cost}", ln=True)

    pdf_output = "/tmp/invoice.pdf"
    pdf.output(pdf_output)

    return pdf_output


def lambda_handler(event, context):
    print("Lambda function starting...")
    s3_bucket = '22185101-pdf-upload'
    print("event:", event)
    
    # Parse the body of the event as JSON
    body = json.loads(event['body'])

    # Access the 'invoice_data' key from the parsed body
    invoice_data = body['invoice_data']
    products = invoice_data['products']
    customer = invoice_data['customer']
    
    invoice_data = {"customer": customer, "amount": sum(products.values()), "products": products}
    
    pdf_file_path = generate_invoice_pdf(invoice_data)

    s3_key = f"invoices/{customer}_invoice.pdf"
    s3_client = boto3.client('s3')

    try:
        s3_client.upload_file(pdf_file_path, s3_bucket, s3_key)
        print(f"PDF uploaded to S3 at {s3_bucket}/{s3_key}")
    except Exception as e:
        print(f"Error uploading PDF to S3: {e}")

    os.remove(pdf_file_path)
    print("Temporary PDF file removed.")

    print("Lambda function completed.")

    return {
        'statusCode': 200,
        'body': json.dumps('Invoice PDF generated and stored in S3!')
    }