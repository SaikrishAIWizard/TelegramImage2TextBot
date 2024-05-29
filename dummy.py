import easyocr

reader = easyocr.Reader(['en'])

result = reader.readtext('')

total_text = ""
for i in result:
    total_text += i[1] + ' '
print(total_text)
