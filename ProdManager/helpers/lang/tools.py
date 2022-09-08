from ProdManager.plugins import lang

def text(message_id, count=1):
  return f"{lang.get(message_id)}{'s' if count > 1 else ''}"
