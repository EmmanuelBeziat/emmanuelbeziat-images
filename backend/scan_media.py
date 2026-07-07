import os
import sys
import mimetypes
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine, Base
from app.models.image import Image
from app.crud.image import generate_public_id

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif', '.svg', '.bmp', '.heic', '.mp4', '.webm', '.mov'}
UPLOAD_DIR = Path(__file__).resolve().parent.parent / 'media'


def scan():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    added = 0
    skipped = 0

    for root, _dirs, files in os.walk(UPLOAD_DIR):
        for filename in files:
            filepath = Path(root) / filename
            if filepath.suffix.lower() not in ALLOWED_EXTENSIONS:
                continue

            relative_url = str(filepath.relative_to(UPLOAD_DIR)).replace(os.sep, '/')

            existing = db.query(Image).filter(Image.url == relative_url).first()
            if existing:
                skipped += 1
                continue

            public_id = generate_public_id()
            while db.query(Image).filter(Image.public_id == public_id).first():
                public_id = generate_public_id()

            mime_type, _ = mimetypes.guess_type(str(filepath))
            if not mime_type:
                mime_type = 'application/octet-stream'

            image = Image(
                public_id=public_id,
                filename=filename,
                original_filename=filename,
                folder=None,
                url=relative_url,
                mime_type=mime_type,
                size=filepath.stat().st_size
            )
            db.add(image)
            added += 1
            print(f'  + {relative_url}')

    db.commit()
    db.close()
    print(f'\nTerminé : {added} ajouté(s), {skipped} déjà en base.')


if __name__ == '__main__':
    print(f'Scan de {UPLOAD_DIR}...\n')
    scan()
