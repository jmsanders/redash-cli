import os
import subprocess


class Editor:
    def __init__(self, client, path="/tmp/redash-cli.sql"):
        self.path = path
        self.client = client

    def save_query_to_file(self, query_id):
        with open(self.path, "w") as f:
            response = self.client.get(f"queries/{query_id}")
            f.write(response.get("query"))

    def read_query_from_file(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                return f.read()

    def open(self):
        subprocess.call([self.editor, self.path])

    @property
    def editor(self):
        return os.environ.get("EDITOR", "vim")