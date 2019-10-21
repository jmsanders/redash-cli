from configparser import ConfigParser


class Config:
    def __init__(self, path=None):
        self.config = ConfigParser()
        self.path = path
        self.config.read(self.path)

    def persist(self):
        with open(self.path, "w") as f:
            self.config.write(f)

    def set(self, configuration, value):
        self.config["DEFAULT"][configuration] = value
        self.persist()

    def get(self, configuration):
        return self.config["DEFAULT"][configuration]

    @property
    def api_key(self):
        return self.get("api_key")

    @property
    def organization(self):
        return self.get("organization")

    @property
    def data_source_id(self):
        return self.get("data_source_id")
