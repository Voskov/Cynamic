import shelve
from pathlib import Path
from handlers.json_handler import JSONHandler
from parsers.defaultparser import BaseParser


def main():
    json_sample_path = Path(__file__).parent / "sample_data" / "sample_data.json"
    sample_raw_data = JSONHandler.read(json_sample_path)
    parsed_samples = BaseParser.parse_batch(sample_raw_data)
    with shelve.open("parsed_samples.shlv", "c") as samples:
        for i, sample in enumerate(parsed_samples):
            samples[str(i)] = sample


if __name__ == '__main__':
    main()
