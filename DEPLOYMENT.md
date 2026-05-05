# 🚀 Deployment Guide

## Step 1: Push to GitHub

```bash
git add .
git commit -m "Ready for deployment"
git push
```

---

## Step 2: Deploy Backend on Render

1. Go to https://render.com
2. Sign in with GitHub
3. Click **New → Web Service**
4. Connect your `aeo-analyzer` repository
5. Fill in settings:
   - **Name**: `aeo-analyzer-backend` (or your choice)
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`

6. Add Environment Variable:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key

7. Click **Deploy**

8. **Wait for deployment** (2-5 minutes)

9. **Copy your backend URL** - it will look like:
   ```
   https://aeo-analyzer-backend.onrender.com
   ```

---

## Step 3: Deploy Frontend on Streamlit Cloud

### 3a. Create `secrets.toml` (LOCAL ONLY - do NOT commit):

Create `.streamlit/secrets.toml`:
```toml
BACKEND_URL = "https://aeo-analyzer-backend.onrender.com"
```

### 3b. Push to GitHub

```bash
git add .
git commit -m "Add deployment configs"
git push
```

### 3c. Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click **New app**
3. Choose:
   - **Repository**: your `aeo-analyzer` repo
   - **Branch**: `main`
   - **Main file path**: `app.py`

4. Click **Deploy**

5. After deployment, go to **Settings** → **Secrets**:
   - Paste same content as your local `secrets.toml`:
   ```
   BACKEND_URL = "https://aeo-analyzer-backend.onrender.com"
   ```

---

## ✅ You're Done!

You now have:

**Backend API:**
```
https://aeo-analyzer-backend.onrender.com
```

**Frontend UI:**
```
https://your-username-aeo-analyzer.streamlit.app
```

Streamlit apps are public by default. Anyone with the URL can open the app. Example:
```
https://aeo-analyzer-rohx8fucn2jduvhsd4abrd.streamlit.app/
```

---

## 🎯 Demo to Recruiter

Show them:
1. Click on the Streamlit link
2. Enter a query + product
3. See live results

They'll be impressed! 🚀

---

## ⚠️ Important Notes

- **Render Free Tier**: Sleeps after 15 mins inactivity. First request takes 20-30 sec. This is normal.
- **Never commit `.env`**: It's already in `.gitignore`
- **API Keys**: Only add to Render/Streamlit dashboards, never in code
