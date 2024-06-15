import base64
from io import BytesIO
import os
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from passlib.context import CryptContext
from PIL import Image
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # hash da senha do usuário

class Funcoes(object):
	@staticmethod
	def verify_password(plain_password, password):
		return pwd_context.verify(plain_password, password)

	# sempre gera um hash diferente, mas o método verify criado na API consegue comparar
	@staticmethod
	def get_password_hash(password):
		return pwd_context.hash(password)

	
	def generate_pdf_file(data, title):
		try:
			buffer = BytesIO()
			p = canvas.Canvas(buffer, pagesize=letter)
			width, height = letter

			# Create a PDF document
			p.drawString(100, 750, title)

			y = height - 100  # Starting position for the first line of text
			for entry in data:
				for key, value in entry.items():
					if key == "foto" and isinstance(value, str) and value.startswith("data:image"):
						try:
							# Extract base64 image data
							header, encoded = value.split(",", 1)
							image_data = base64.b64decode(encoded)
							
							# Save the image to a temporary file
							with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_image_file:
								temp_image_file.write(image_data)
								temp_image_path = temp_image_file.name

							# Draw the image onto the PDF
							p.drawImage(temp_image_path, 100, y - 200, width=200, height=200)
							y -= 220  # Move down after adding the image

							# Remove the temporary image file
							os.remove(temp_image_path)
						except Exception as e:
							return {"erro": True, "msgErro": f"Error processing image: {e}"}
					else:
						try:
							p.drawString(100, y, f"{key}: {value}")
							y -= 20  # Move down for the next line
						except Exception as e:
							return {"erro": True, "msgErro": f"Error writing text: {e}"}

				y -= 20  # Add extra space between entries

				# Check if the page needs to be broken
				if y < 50:
					p.showPage()  # Add a new page
					y = height - 50  # Reset y position for new page

			p.save()
			buffer.seek(0)
			return buffer
		except Exception as e:
			return {"erro": True, "msgErro": f"Error generating PDF: {e}"}