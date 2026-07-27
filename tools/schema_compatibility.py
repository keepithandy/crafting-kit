"""Read-only content schema compatibility classification."""
def classify_schema_version(content, current=1):
    version=content.get("version") if isinstance(content,dict) else None
    if version is None: status="missing"
    elif not isinstance(version,int) or isinstance(version,bool): status="malformed"
    elif version==current: status="current"
    elif version<current: status="legacy"
    else: status="future"
    return {"status":status,"version":version,"currentVersion":current,"compatible":status in ("current","legacy"),"migrationRequired":status=="legacy"}
