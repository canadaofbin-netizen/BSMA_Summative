import sys
sys.stdout.reconfigure(encoding='utf-8')
import glob

marrone_files = glob.glob(r'C:\Users\yunky\.gemini\antigravity\brain\24b0e3bc-d58a-4110-960c-eef25f2d0ce8\scratch\pdf_texts\*Marrone*.txt')
with open(marrone_files[0], 'r', encoding='utf-8') as f:
    text = f.read()

# Search for reliability-related text
for kw in ['alpha', 'Alpha', 'reliability', 'Cronbach']:
    idx = text.find(kw)
    if idx > -1:
        print(f'=== Found "{kw}" ===')
        print(text[max(0,idx-100):idx+200])
        print()

# Search for Ancona and Caldwell
idx2 = text.find('Ancona and Caldwell')
if idx2 > -1:
    print('=== ANCONA AND CALDWELL ===')
    print(text[max(0,idx2-100):idx2+300])

# Search for six items  
idx3 = text.find('six items')
if idx3 > -1:
    print('\n=== SIX ITEMS ===')
    print(text[max(0,idx3-200):idx3+300])

# Find role overload items count
idx4 = text.find('role overload')
contexts = []
start = 0
while True:
    idx4 = text.lower().find('role overload', start)
    if idx4 == -1: break
    context = text[max(0,idx4-50):idx4+200]
    if 'item' in context.lower() or 'scale' in context.lower():
        print(f'\n=== ROLE OVERLOAD WITH ITEM/SCALE ===')
        print(context)
    start = idx4 + 1
