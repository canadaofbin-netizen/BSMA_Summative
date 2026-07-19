import fitz, sys; doc = fitz.open(sys.argv[1]); text = chr(10).join([page.get_text() for page in doc]); print('Length:', len(text)); print('Boundary at:', text.lower().find('boundary'))
