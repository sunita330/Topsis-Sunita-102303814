from flask import Flask, render_template, request
import os
from topsis_logic import topsis
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        file = request.files["file"]
        weights = request.form["weights"]
        impacts = request.form["impacts"]
        email = request.form["email"]

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(OUTPUT_FOLDER, "output.xlsx")

        file.save(input_path)

        topsis(input_path, weights, impacts, output_path)

        send_email(email, output_path)

        return "Result sent to email successfully ✅"

    return render_template("index.html")

def send_email(receiver_email, attachment_path):
    sender_email = "sunitajogpal614@gmail.com"
    sender_password = "abcd efgh ijkl mnop"

    msg = EmailMessage()
    msg["Subject"] = "TOPSIS Result"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content("Please find the TOPSIS result attached.")

    with open(attachment_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename="TOPSIS_Result.xlsx"
        )
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()

if __name__ == "__main__":
    app.run(debug=True)
