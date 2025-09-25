# 🆓 GitHub Storage Setup Guide

## Quick Fix for Image Upload Issues

Your Django app is already configured with GitHub storage! You just need to set up the environment variables.

## Step 1: Create GitHub Personal Access Token

1. **Go to GitHub Settings**:
   - Visit: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"

2. **Configure Token**:
   - **Note**: "Django App File Storage"
   - **Expiration**: Choose "No expiration" or "90 days"
   - **Scopes**: Check these boxes:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `public_repo` (Access public repositories)

3. **Generate and Copy Token**:
   - Click "Generate token"
   - **IMPORTANT**: Copy the token immediately (you won't see it again!)

## Step 2: Configure Environment Variables

### For Local Development:
Create a `.env` file in your project root:

```env
# GitHub Storage Settings (FREE!)
USE_GITHUB=True
GITHUB_TOKEN=your_github_personal_access_token_here
GITHUB_REPO_NAME=abgpaulas/multicompany
GITHUB_BRANCH=master
```

### For Railway/Render Deployment:
Add these environment variables in your deployment platform:

```env
USE_GITHUB=True
GITHUB_TOKEN=your_github_personal_access_token_here
GITHUB_REPO_NAME=abgpaulas/multicompany
GITHUB_BRANCH=master
```

## Step 3: Test the Setup

Run this command to test GitHub storage:

```bash
python manage.py test_github_storage
```

## Step 4: Deploy and Test

1. **Deploy** your changes
2. **Upload an image** in your app
3. **Check your GitHub repository** - you'll see a `media/` folder with uploaded files!

## How It Works

1. **File Upload**: When users upload images, they're stored in your GitHub repository
2. **File Access**: Images are served via `https://raw.githubusercontent.com/abgpaulas/multicompany/master/media/...`
3. **Persistence**: Files persist across deployments because they're in GitHub
4. **Free**: No costs, no limits, no expiration!

## File Structure in GitHub

Your repository will have this structure:
```
multicompany/
├── media/
│   ├── 2024/12/19/
│   │   ├── abc12345_logo.png
│   │   └── def67890_signature.png
│   └── 2024/12/20/
│       └── ghi09876_profile.jpg
├── apps/
├── templates/
└── ...
```

## Benefits

- 🆓 **Completely Free**: No monthly costs
- 🔄 **Persistent**: Files survive deployments
- 🌐 **Global CDN**: GitHub's global content delivery
- 📁 **Organized**: Files organized by date
- 🔒 **Secure**: Only you can access/modify files
- 📊 **Unlimited**: No storage limits (within GitHub's reasonable use)

## Troubleshooting

### Images not showing?
1. Check `GITHUB_TOKEN` is set correctly
2. Verify token has `repo` permissions
3. Check deployment logs for errors
4. Run `python manage.py test_github_storage`

### Permission denied?
1. Ensure token has `repo` scope
2. Verify repository name is correct
3. Check if token has expired

### Files not persisting?
1. Verify `USE_GITHUB=True` is set
2. Check if files appear in GitHub repository
3. Look at deployment logs for storage errors

## Your Current Configuration

✅ **GitHub Storage Backend**: Already implemented
✅ **Settings Configuration**: Already configured
✅ **Requirements**: PyGithub already included
✅ **Environment Template**: Updated with GitHub settings

## Next Steps

1. **Create GitHub Personal Access Token** (2 minutes)
2. **Add environment variables** to your deployment platform (1 minute)
3. **Deploy and test** (automatic)
4. **Your images will now persist forever!** 🎉

This solution is **100% free** and will work perfectly with your current setup!
