import logging
from pathlib import Path
from typing import List

from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)


class Loader:
    def __init__(self, path: str):
        self.documents = []
        self.path = path

    def load(self):
        logger.info(f"load({self.path})")
        p = Path(self.path)
        if p.is_dir():
            self.load_directory()
        elif p.is_file():
            self.load_file()

    def load_documents(self):
        self.load()
        return self.documents

    def load_file(self):
        raise NotImplementedError()

    def load_directory(self):
        raise NotImplementedError()


class PDFFileLoader(Loader):
    """Load files as PDF, extract text."""

    def _load_pdf(self, filename):
        logger.info(f"Loading PDF '{filename}'")
        reader = PdfReader(filename)
        return "".join([page.extract_text() for page in reader.pages])

    def load_file(self):
        logger.info(f"load_file('{self.path}')")
        self.documents.append(self._load_pdf(self.path))

    def load_directory(self):
        p = Path(self.path)
        logger.info(f"load_directory('{str(p)}')")
        for filename in p.rglob("*.pdf"):
            self.documents.append(self._load_pdf(filename))


class TextFileLoader(Loader):
    def __init__(self, path: str, encoding: str = "utf-8"):
        self.documents = []
        self.path = path
        self.encoding = encoding

    def load_file(self):
        filename = Path(self.path)
        self.documents.append(
            filename.read_text(encoding=self.encoding)
        )

    def load_directory(self):
        p = Path(self.path)
        for filename in p.rglob("*.txt"):
            self.documents.append(
                filename.read_text(encoding=self.encoding)
            )


class CharacterTextSplitter:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        assert (
            chunk_size > chunk_overlap
        ), "Chunk size must be greater than chunk overlap"

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunks.append(text[i : i + self.chunk_size])
        return chunks

    def split_texts(self, texts: List[str]) -> List[str]:
        chunks = []
        for text in texts:
            chunks.extend(self.split(text))
        return chunks



if __name__ == "__main__":
    loader = TextFileLoader("data/KingLear.txt")
    loader.load()
    splitter = CharacterTextSplitter()
    chunks = splitter.split_texts(loader.documents)
    print(len(chunks))
    print(chunks[0])
    print("--------")
    print(chunks[1])
    print("--------")
    print(chunks[-2])
    print("--------")
    print(chunks[-1])
