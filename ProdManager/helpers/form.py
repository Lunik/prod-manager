
def strip_input(content):
  if content is None:
    return content

  if not isinstance(content, str):
    raise Exception(f"Type not handled : {content.__class__.__name__}")

  result = []
  for line in content.split('\n'):
    line = line.strip()
    if line != "":
      result.append(line)

  return '\n'.join(result)