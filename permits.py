# Fake permit records for our two demo locations.
# In production, this would come from a real municipal permit registry
# (e.g., Dubai Municipality's open Building Permits dataset).

PERMITS = {
    "test_2_0000_0000": {
        "parcel_id": "PARCEL-4471",
        "permit_type": None,          # no permit on file at all
        "permit_status": "none",
        "issue_date": None,
        "approved_use": None,
    },
    "test_55_0256_0000": {
        "parcel_id": "PARCEL-9902",
        "permit_type": "new_construction",
        "permit_status": "approved",
        "issue_date": "2021-03-15",
        "approved_use": "residential",
    },
    "test_102_0512_0000": {
        "parcel_id": "PARCEL-3318",
        "permit_type": "new_construction",
        "permit_status": "pending",       # application submitted, not yet approved
        "issue_date": None,
        "approved_use": "commercial",     # matches what's being built
    },
    "test_77_0512_0256": {
        "parcel_id": "PARCEL-7743",
        "permit_type": "new_construction",
        "permit_status": "approved",
        "issue_date": "2022-08-01",
        "approved_use": "commercial",   # matches what's being built
    },
    "test_2_0000_0512": {
        "parcel_id": "PARCEL-5561",
        "permit_type": None,
        "permit_status": "none",      # no permit on file
        "issue_date": None,
        "approved_use": None,
    },
    "test_121_0768_0256": {
        "parcel_id": "PARCEL-8820",
        "permit_type": "building_extension",
        "permit_status": "pending",
        "issue_date": None,
        "approved_use": "mixed_use",  # matches what's being built
    },
}
