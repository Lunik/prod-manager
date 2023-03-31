import os
import ProdManager

tag_version = os.environ.get('CI_COMMIT_TAG')

assert tag_version == ProdManager.__version__, \
  f"❌ The version in ProdManager/__init__.py ({ProdManager.__version__}) doesn't match the Git tag ({tag_version})."

print(f"✅ The version of ProdManager ({ProdManager.__version__}) match the Git tag.")
