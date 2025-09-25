# 🔑 GitHub Token Setup Guide

## Why You Need a GitHub Token

Your application is configured to use GitHub for image storage (which is completely FREE!), but it needs a GitHub token to upload new images to your repository.

## Step 1: Create a GitHub Personal Access Token

1. **Go to GitHub**: Visit https://github.com/settings/tokens
2. **Click "Generate new token"** → **"Generate new token (classic)"**
3. **Set expiration**: Choose "No expiration" or "90 days"
4. **Select scopes**: Check these boxes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `public_repo` (Access public repositories)
5. **Click "Generate token"**
6. **Copy the token** (it starts with `ghp_` or `github_pat_`)

## Step 2: Add Token to Your Environment

### For Local Development:
Create a `.env` file in your project root:
```bash
GITHUB_TOKEN=your_token_here
```

### For Railway Deployment:
1. Go to your Railway project dashboard
2. Click on your service
3. Go to "Variables" tab
4. Add new variable:
   - **Name**: `GITHUB_TOKEN`
   - **Value**: `your_token_here`
5. Click "Add"

### For Render Deployment:
1. Go to your Render dashboard
2. Select your service
3. Go to "Environment" tab
4. Add new environment variable:
   - **Key**: `GITHUB_TOKEN`
   - **Value**: `your_token_here`
5. Click "Save Changes"

## Step 3: Test the Setup

After adding the token, restart your application and test uploading a new image. It should now be uploaded to GitHub and accessible via GitHub URLs.

## Benefits of GitHub Storage

- ✅ **Completely FREE** - No storage costs
- ✅ **Reliable** - GitHub's CDN serves images fast
- ✅ **Persistent** - Images survive deployments
- ✅ **Scalable** - No storage limits for reasonable usage
- ✅ **Version controlled** - All images are tracked in Git

## Troubleshooting

If images still don't display after setting up the token:

1. **Check token permissions**: Make sure the token has `repo` access
2. **Verify repository name**: Ensure `GITHUB_REPO_NAME` matches your actual repository
3. **Check branch name**: Ensure `GITHUB_BRANCH` matches your default branch
4. **Restart application**: After adding environment variables

## Security Note

- Never commit your GitHub token to code
- Use environment variables only
- The token gives access to your repository, so keep it secure
