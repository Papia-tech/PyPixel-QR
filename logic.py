import qrcode
import base64
from io import BytesIO
from js import document
from pyodide.ffi import create_proxy

# Select HTML elements
ui_input = document.getElementById("url-input")
ui_gen_btn = document.getElementById("gen-btn")
ui_refresh_btn = document.getElementById("refresh-icon")
ui_image = document.getElementById("qr-image")
ui_placeholder = document.getElementById("placeholder")
ui_status = document.getElementById("status")

def generate_qr(event):
    data = ui_input.value
    if not data:
        ui_status.innerText = "Input cannot be empty!"
        return

    try:
        ui_status.innerText = "Generating..."
        
        # QR Generation
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Encode to Base64
        buf = BytesIO()
        img.save(buf, format="PNG")
        img_str = base64.b64encode(buf.getvalue()).decode()

        # Display Result
        ui_image.src = "data:image/png;base64," + img_str
        ui_image.style.display = "block"
        ui_placeholder.style.display = "none"
        ui_status.innerText = "Done!"
    except Exception as e:
        ui_status.innerText = f"Error: {str(e)}"

def refresh_screen(event):
    # Just clear everything back to start
    ui_input.value = ""
    ui_image.style.display = "none"
    ui_placeholder.style.display = "block"
    ui_status.innerText = "Ready!"

# Create Proxies
gen_proxy = create_proxy(generate_qr)
refresh_proxy = create_proxy(refresh_screen)

# Listeners
ui_gen_btn.addEventListener("click", gen_proxy)
ui_refresh_btn.addEventListener("click", refresh_proxy)

# Finalize Setup
ui_gen_btn.disabled = False
ui_gen_btn.innerText = "Generate QR"
ui_status.innerText = "Ready!"
