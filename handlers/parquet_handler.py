class ParquetHandler:
    def __init__(self, path):
        self.path = path

    def read(self):
        return pd.read_parquet(self.path)

    def write(self, df):
        df.to_parquet(self.path, index=False)