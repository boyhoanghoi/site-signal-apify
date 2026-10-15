import os

if os.environ.get("APIFY_IS_AT_HOME") == "1":
    import asyncio
    from .actor import run_actor
    asyncio.run(run_actor())
else:
    from .cli import main
    raise SystemExit(main())
