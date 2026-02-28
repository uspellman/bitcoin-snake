import pyperclip

pyperclip.copy("Hello, world!")
result = pyperclip.paste()
print(f"Pasted from clipboard: {result}")