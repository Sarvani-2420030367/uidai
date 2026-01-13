import hashlib

def generate_block_hash(row):
    """
    Simulates a blockchain block hash
    using district-level risk data
    """
    record_string = (
        str(row["state"]) +
        str(row["district"]) +
        str(row["enrollments"]) +
        str(row["demo_updates"]) +
        str(row["bio_updates"]) +
        str(row["risk_score"]) +
        str(row["risk_level"])
    )

    return hashlib.sha256(record_string.encode()).hexdigest()
