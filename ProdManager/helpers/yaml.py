import yaml

def yaml_join(loader, node):
  seq = loader.construct_sequence(node)
  return ''.join([str(i) for i in seq])

myloader = yaml.SafeLoader
myloader.add_constructor('tag:yaml.org,2002:seq', yaml_join)
