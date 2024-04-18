import json
import boto3
from fpdf import FPDF
import os
 
def generate_invoice_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Add invoice header
    pdf.set_fill_color(0, 119, 204)  # Set fill color to blue
    pdf.set_text_color(255, 255, 255)  # Set text color to white
    pdf.cell(200, 10, txt="Invoice", ln=True, align='C', fill=True)
    pdf.ln(10)  # Add a line break
    # Add customer information
    pdf.set_fill_color(255, 255, 255)  # Set fill color to white
    pdf.set_text_color(0, 0, 0)  # Set text color to black
    pdf.cell(0, 10, txt=f"Customer: {data['customer']}", ln=True)
    
    
    # Add invoice details
    pdf.cell(0, 10, txt="Invoice Details:", ln=True)
    pdf.cell(50, 10, txt="Product", border=1)  # Add a border to the cell
    pdf.cell(40, 10, txt="Quantity", border=1)  # Add a border to the cell
    pdf.cell(50, 10, txt="Price", border=1)  # Add a border to the cell
    pdf.cell(60, 10, txt="Total Price", border=1, ln=True)  # Add a border to the cell
    for product, details in data['products'].items():
        quantity = details['quantity']
        price = details['price']
        total_price = quantity * price
        pdf.cell(50, 10, txt=product, border=1)  # Product column
        pdf.cell(40, 10, txt=str(quantity), border=1)  # Quantity column
        pdf.cell(50, 10, txt=str(price), border=1)  # Price column
        pdf.cell(60, 10, txt=str(total_price), border=1, ln=True)  # Total price column
    pdf.ln(10)  # Add a line break
    pdf.cell(0, 10, txt=f"Amount: {data['amount']}", ln=True)
    
    # Check if discount is applicable
    if 'discount' in data:
        discount = data['discount']
        updated_total = data['amount'] - discount
        pdf.cell(0, 10, txt=f"Discount: {discount}", ln=True)  # Add discount
        pdf.cell(0, 10, txt=f"Total: {updated_total}", ln=True)  # Add updated total
    
    pdf.ln(10)  # Add a line break
    pdf_output = "/tmp/invoice.pdf"
    pdf.output(pdf_output)
    print("Invoice PDF generated.")
    return pdf_output
 
def upload_to_s3(pdf_file_path, s3_bucket, s3_key):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(pdf_file_path, s3_bucket, s3_key)
        print(f"PDF uploaded to S3 at {s3_bucket}/{s3_key}")
        return f"https://{s3_bucket}.s3.amazonaws.com/{s3_key}"
    except Exception as e:
        print(f"Error uploading PDF to S3: {e}")
        return None
 
def lambda_handler(event, context):
    print("Lambda function starting...")
    s3_bucket = '22185101-pdf-upload'
    print("Received event:", json.dumps(event))
    
    body = json.loads(event['body'])
    invoice_data = body['invoice_data']
    products = invoice_data['products']
    customer = invoice_data['customer']
    discount = invoice_data.get('discount', 0)  # Retrieve discount from the payload
    print("Discount received:", discount)
    
    # Include discount in the invoice data
    invoice_data_with_quantity = {
        "customer": customer,
        "amount": sum(details['price'] * details['quantity'] for details in products.values()),
        "discount": discount,  # Include discount in the invoice data
        "products": {product: {"quantity": details['quantity'], "price": details['price']} for product, details in products.items()}
    }
 
    pdf_file_path = generate_invoice_pdf(invoice_data_with_quantity)
    print("Invoice PDF generated:", pdf_file_path)
 
    s3_key = f"invoices/{customer}_invoice.pdf"
    s3_url = upload_to_s3(pdf_file_path, s3_bucket, s3_key)
 
    os.remove(pdf_file_path)
    print("Temporary PDF file removed.")
 
    print("Lambda function completed.")
 
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps({'s3_url': s3_url, 'discount': discount})  # Pass discount in the response
    }
