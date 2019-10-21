import os
import subprocess

class Editor:
    def __init__(self, path="/tmp/redash-cli.sql"):
        self.path = path

    def edit(self, client, query_id):
        self.save_query_to_file(client, query_id)
        self.open()
        return self.read_query_from_file()

    def save_query_to_file(self, client, query_id):
        with open(self.path, "w") as f:
            response = client.get(f"queries/{query_id}")
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