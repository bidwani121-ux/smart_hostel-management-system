import qrcode

student_id = "STU001"

qr = qrcode.make(student_id)

qr.save("student_STU001.png")

print("Student QR Code generated successfully!")