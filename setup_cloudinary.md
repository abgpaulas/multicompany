# Cloudinary Setup Guide (Easier Alternative)

## Why Cloudinary?
- ✅ Easier setup than AWS S3
- ✅ Built-in image optimization and transformations
- ✅ Generous free tier (25GB storage + 25GB bandwidth)
- ✅ No complex IAM configuration needed

## Step 1: Sign Up for Cloudinary

1. Go to https://cloudinary.com/
2. Click "Sign Up For Free"
3. Complete the registration
4. You'll get a dashboard with your credentials

## Step 2: Get Your Credentials

From your Cloudinary dashboard, note down:
- **Cloud name** (e.g., `myapp123`)
- **API Key** (e.g., `123456789012345`)
- **API Secret** (e.g., `abcdefghijklmnop`)

## Step 3: Update Your Code

I'll create a Cloudinary configuration for you. This is simpler than AWS S3 setup.

## Step 4: Configure Render Environment Variables

In your Render dashboard, add:
```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
USE_CLOUDINARY=True
```

## Cost Comparison

| Service | Free Tier | Paid Plans |
|---------|-----------|------------|
| **Cloudinary** | 25GB storage + 25GB bandwidth | $89/month |
| **AWS S3** | 5GB storage + limited requests | $1-5/month |

**Recommendation**: Start with Cloudinary for simplicity, migrate to AWS S3 later if costs become an issue.
