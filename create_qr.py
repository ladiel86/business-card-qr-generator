import qrcode
from PIL import Image

# --- CONFIGURATION ---
use_logo = True  # Set this to False to generate QR code *without* logo
fill_color_hex = "#0050B5" # Define the QR code color
back_color_hex = "#000000" # Define the background color

# --- Contact Information ---
# Refer to https://www.rfc-editor.org/rfc/rfc6350.html#section-6, for more information on vCard format.
vcard_data = f"""BEGIN:VCARD
VERSION:3.0
N:Smith;John
FN:John Smith
ORG:The Best Company
TITLE:Entrepreneur
TEL;type=WORK,voice;value=uri:tel:+1234567890
EMAIL:john.smith@gmail.com
URL;type=LinkedIn:https://www.linkedin.com/in/johnsmith
END:VCARD"""

# --- Generate the QR Code's internal data structure ---
qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=0,  # No border to maximize space for the logo
)
qr.add_data(vcard_data)
qr.make(fit=True)

# --- Using logo, prepare and modify QR grid ---
if use_logo:
    try:
        logo_img = Image.open("logo.png").convert("RGBA")
    except FileNotFoundError:
        print("Warning: 'logo.png' not found. Proceeding without logo.")
        use_logo = False
    else:
        qr_image_size = qr.modules_count * qr.box_size
        logo_max_size = qr_image_size // 4  # Logo ≈ 1/4 of QR width
        logo_img.thumbnail((logo_max_size, logo_max_size))

        # Calculate hole for logo
        logo_module_width = round(logo_img.width / qr.box_size) + 2
        logo_module_height = round(logo_img.height / qr.box_size) + 2
        module_count = qr.modules_count
        modules = qr.modules

        center_module = module_count // 2
        start_c = center_module - logo_module_width // 2
        end_c = start_c + logo_module_width
        start_r = center_module - logo_module_height // 2
        end_r = start_r + logo_module_height

        # Create transparent space for the logo
        for r in range(start_r, end_r):
            for c in range(start_c, end_c):
                if 0 <= r < module_count and 0 <= c < module_count:
                    modules[r][c] = False

# --- Render the QR Code ---
qr_img = qr.make_image(fill_color=fill_color_hex, back_color=back_color_hex).convert('RGBA')

# --- Paste logo if enabled ---
if use_logo:
    logo_pos = ((qr_img.width - logo_img.width) // 2, (qr_img.height - logo_img.height) // 2)
    mask = logo_img.split()[3] if 'A' in logo_img.getbands() else None
    qr_img.paste(logo_img, logo_pos, mask=mask)

# --- Save the final image ---
final_filename = "contact_qr_final.png"
qr_img.save(final_filename)

print(f"Success! Your final QR code has been saved as '{final_filename}'")
if use_logo:
    print("Logo was included in the QR code.")
else:
    print("Generated QR code without logo.")
