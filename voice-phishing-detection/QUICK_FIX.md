# Quick Fix Guide

## The Pydantic Error

You're seeing this error because you're running:
```
uvicorn backend.app:app --reload
```

This uses your **global Python** which has an old Supabase library.

### ✅ Solution: Use the Virtual Environment

**Stop the current server** (Ctrl+C) and run:

```bash
backend\venv\Scripts\python -m uvicorn backend.app:app --reload
```

This uses the venv's Python which has the correct versions.

---

## Alternative: Fix Your Global Python

If you want to use `uvicorn` directly, upgrade your global Supabase:

```bash
pip install --upgrade supabase realtime pydantic
```

But I recommend using the venv instead for consistency.

---

## The Stop Button Issue

The stop button needs to close the WebSocket connection for the manually started call.

I'll fix this now in the code.
