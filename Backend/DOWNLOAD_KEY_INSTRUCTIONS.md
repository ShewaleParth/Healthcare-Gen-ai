# Download Your Service Account Key

## Quick Steps

Since you already have the service account set up in Google Cloud Console, you just need to download the key file.

### Option A: Download from Google Cloud Console (Recommended)

1. **Open Google Cloud Console**
   - Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=aarogya-genai-hackathon

2. **Find Your Service Account**
   - Look for the service account you created
   - It should be something like `aarogya-genai-hackathon@aarogya-genai-hackathon.iam.gserviceaccount.com`

3. **Create/Download Key**
   - Click on the service account
   - Go to the "Keys" tab
   - Click "Add Key" → "Create new key"
   - Choose **JSON** format
   - Click "Create"
   - The key file will download automatically

4. **Move the Key File**
   - Rename the downloaded file to: `aarogya-genai-hackathon-b5fdebb52a65.json`
   - Move it to: `d:\Gen Ai Hackathon\Backend\`
   - Final path should be: `d:\Gen Ai Hackathon\Backend\aarogya-genai-hackathon-b5fdebb52a65.json`

5. **Restart Backend**
   - Your backend server will auto-reload
   - Check for success messages:
     ```
     ✅ Using credentials from: aarogya-genai-hackathon-b5fdebb52a65.json
     ✅ Vertex AI initialized: aarogya-genai-hackathon
     ✅ BigQuery initialized: aarogya-genai-hackathon.aarogya_healthcare
     ```

### Option B: If You Already Downloaded It

If you already downloaded the key file somewhere else on your computer:

1. **Find the file** (usually in your Downloads folder)
2. **Copy it** to `d:\Gen Ai Hackathon\Backend\`
3. **Rename it** to `aarogya-genai-hackathon-b5fdebb52a65.json`

---

## Security Note

⚠️ **Important**: Never commit this JSON file to git!

Create a `.gitignore` file if you don't have one, and add:
```
*.json
.env
```

---

## What This File Contains

The service account key file contains:
- Project ID
- Private key for authentication
- Service account email
- Authentication endpoints

This allows your backend to authenticate as the service account and access Vertex AI and BigQuery.
