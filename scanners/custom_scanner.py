class Scanner:
    def __init__(self, profile=None, logger=None):
        self.profile = profile
        self.logger = logger

    def run(self):
        # Пример для пользовательского сканера — вернёт пустой результат
        if self.logger:
            self.logger.info("Custom scanner executed")
        return []