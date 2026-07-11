import PyPDF2
import re

reader = PyPDF2.PdfReader(r'g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/01_Academic_Papers/[247] Igbaria and Siegel (1993) - The career decision of information systems people.pdf')
text = '\n'.join(page.extract_text() for page in reader.pages)

print('---BOUNDARY SPANNING---')
print(text[7000:9000])

print('---CORRELATION MATRIX---')
# find table with correlation
matches = list(re.finditer(r'Table.*?correlation|Means, Standard Deviations', text, re.IGNORECASE))
for match in matches:
    print('FOUND AT:', match.start())
    print(text[max(0, match.start()-200):match.start()+2000])
    print('-------------------------')
