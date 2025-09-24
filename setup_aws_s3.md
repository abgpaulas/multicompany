# AWS S3 Setup Guide for Render Deployment

## Problem
Your Render deployment uses Railway PostgreSQL database (persistent) but local filesystem (ephemeral). This means:
- ✅ Database data persists across deployments
- ❌ Uploaded files (images) are lost on each deployment

## Solution: AWS S3 Cloud Storage

### Step 1: Create AWS S3 Bucket

1. **Sign up for AWS** (if you don't have an account):
   - Go to https://aws.amazon.com/
   - Create a free account (includes 5GB free storage for 12 months)

2. **Create S3 Bucket**:
   - Go to AWS S3 Console
   - Click "Create bucket"
   - Bucket name: `your-app-name-media-files` (must be globally unique)
   - Region: Choose closest to your users (e.g., `us-east-1`)
   - Uncheck "Block all public access" (we need public read for images)
   - Acknowledge the warning about public access
   - Click "Create bucket"

### Step 2: Create IAM User for S3 Access

1. **Go to IAM Console**:
   - Navigate to IAM in AWS Console
   - Click "Users" → "Create user"

2. **Create User**:
   - Username: `render-s3-user`
   - Select "Programmatic access"

3. **Attach Policy**:
   - Click "Attach existing policies directly"
   - Search and select: `AmazonS3FullAccess`
   - Click "Next" → "Create user"

4. **Save Credentials**:
   - **IMPORTANT**: Copy and save these values securely:
     - Access Key ID
     - Secret Access Key

### Step 3: Configure Render Environment Variables

In your Render dashboard:

1. Go to your service
2. Click "Environment" tab
3. Add these environment variables:

```
USE_S3=True
AWS_ACCESS_KEY_ID=your_access_key_id_here
AWS_SECRET_ACCESS_KEY=your_secret_access_key_here
AWS_STORAGE_BUCKET_NAME=your-bucket-name-here
AWS_S3_REGION_NAME=us-east-1
```

### Step 4: Deploy and Test

1. **Deploy your changes**:
   - Commit and push your code
   - Render will automatically redeploy

2. **Test image uploads**:
   - Try uploading images in your app
   - Check if they persist after redeployment

## Alternative Solutions

### Option 1: Cloudinary (Easier Setup)
If AWS seems complex, consider Cloudinary:

1. **Sign up at https://cloudinary.com/**
2. **Add to requirements.txt**:
   ```
   cloudinary==1.36.0
   ```
3. **Update settings.py**:
   ```python
   import cloudinary
   import cloudinary.uploader
   import cloudinary.api
   
   cloudinary.config(
     cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
     api_key=os.getenv('CLOUDINARY_API_KEY'),
     api_secret=os.getenv('CLOUDINARY_API_SECRET')
   )
   ```

### Option 2: Render Disk Storage (Limited)
Render offers persistent disk storage, but it's:
- More expensive
- Less reliable than cloud storage
- Not recommended for production

## Cost Estimation

### AWS S3 (Recommended)
- **Free tier**: 5GB storage + 20,000 GET requests + 2,000 PUT requests per month
- **After free tier**: ~$0.023 per GB per month + $0.0004 per 1,000 requests
- **Typical cost**: $1-5/month for small to medium apps

### Cloudinary
- **Free tier**: 25GB storage + 25GB bandwidth per month
- **After free tier**: $89/month for next tier
- **Good for**: Apps with heavy image processing needs

## Troubleshooting

### Images still not showing?
1. Check environment variables are set correctly
2. Verify S3 bucket permissions are public-read
3. Check Render deployment logs for errors
4. Test S3 connection with AWS CLI

### Permission denied errors?
1. Ensure IAM user has S3FullAccess policy
2. Check bucket CORS configuration if needed
3. Verify bucket is in the same region as AWS_S3_REGION_NAME

## Next Steps

1. Choose your preferred solution (AWS S3 recommended)
2. Follow the setup steps above
3. Deploy and test
4. Your images will now persist across deployments! 🎉
