from utils import *


# Load all archive data from Database
def load_all_archives(status: int = 0) -> list:
    ref = database.get_ref('archive')
    if ref is not None:
        archives = []
        for archive_id, archive in ref.get().items():
            if archive_id == 'arZero':
                continue
            archive['id'] = archive_id
            archives.append(archive)
        if status == 0:
            archives = archives
        return archives
    else:
        return []


# Get a single archive by ID
def get_archive(archive_id: str) -> dict:
    ref = database.get_ref('archive')
    if ref is not None:
        return ref.child(archive_id).get()
    return {}
