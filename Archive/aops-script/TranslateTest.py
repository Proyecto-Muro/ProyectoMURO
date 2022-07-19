import translators
from aops_script import get_items
from processproblem import process_item


text=process_item(get_items(2609131)[0])

print(translators.deepl(text, from_language="en", to_language="es"))

