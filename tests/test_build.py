from pathlib import Path
import tempfile
import unittest

from sitegen.build import build


class BuildSmokeTest(unittest.TestCase):
    def test_build_preserves_routes_and_static_assets(self):
        root = Path(__file__).parents[1]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            build(root, output)
            self.assertTrue((output / "index.html").exists())
            self.assertTrue((output / "about" / "index.html").exists())
            self.assertTrue((output / "posts" / "semantic-versioning-p1" / "index.html").exists())
            self.assertTrue((output / "projects" / "microservices-based-web-app" / "index.html").exists())
            self.assertFalse((output / "posts" / "semantic-versioning" / "index.html").exists())
            self.assertTrue((output / "static" / "css" / "style.css").exists())
            self.assertTrue((output / ".nojekyll").exists())


if __name__ == "__main__":
    unittest.main()
