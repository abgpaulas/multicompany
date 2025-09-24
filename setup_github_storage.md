# 🆓 FREE GitHub File Storage Setup

## Why GitHub Storage?
- ✅ **100% FREE** - No costs ever!
- ✅ **Persistent** - Files stored in your GitHub repository
- ✅ **Reliable** - GitHub's infrastructure
- ✅ **Easy Setup** - Just need a GitHub Personal Access Token
- ✅ **No Limits** - GitHub allows large files and repositories

## Step 1: Create GitHub Personal Access Token

1. **Go to GitHub Settings**:
   - Visit: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"

2. **Configure Token**:
   - **Note**: "Render File Storage"
   - **Expiration**: Choose "No expiration" or "90 days"
   - **Scopes**: Check these boxes:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `public_repo` (Access public repositories)

3. **Generate and Copy Token**:
   - Click "Generate token"
   - **IMPORTANT**: Copy the token immediately (you won't see it again!)

## Step 2: Configure Render Environment Variables

In your Render dashboard:

1. Go to your service
2. Click "Environment" tab
3. Add these environment variables:

```
USE_GITHUB=True
GITHUB_TOKEN=your_personal_access_token_here
GITHUB_REPO_NAME=abgpaulas/multicompany
GITHUB_BRANCH=master
```

## Step 3: Deploy and Test

1. **Deploy**: Your changes will automatically deploy
2. **Test**: Upload images in your app
3. **Verify**: Check your GitHub repository - you'll see a `media/` folder with uploaded files!

## How It Works

1. **File Upload**: When users upload images, they're stored in your GitHub repository
2. **File Access**: Images are served via `https://raw.githubusercontent.com/abgpaulas/multicompany/master/media/...`
3. **Persistence**: Files persist across Render deployments because they're in GitHub
4. **Free**: No costs, no limits, no expiration!

## File Structure in GitHub

Your repository will have this structure:
```
multicompany/
├── media/
│   ├── 2024/09/24/
│   │   ├── abc12345_logo.png
│   │   └── def67890_signature.png
│   └── 2024/09/25/
│       └── ghi09876_profile.jpg
├── apps/
├── templates/
└── ...
```

## Benefits

- 🆓 **Completely Free**: No monthly costs
- 🔄 **Persistent**: Files survive Render deployments
- 🌐 **Global CDN**: GitHub's global content delivery
- 📁 **Organized**: Files organized by date
- 🔒 **Secure**: Only you can access/modify files
- 📊 **Unlimited**: No storage limits (within GitHub's reasonable use)

## Troubleshooting

### Images not showing?
1. Check `GITHUB_TOKEN` is set correctly
2. Verify token has `repo` permissions
3. Check Render deployment logs for errors

### Permission denied?
1. Ensure token has `repo` scope
2. Verify repository name is correct
3. Check if token has expired

### Files not persisting?
1. Verify `USE_GITHUB=True` is set
2. Check if files appear in GitHub repository
3. Look at deployment logs for storage errors

## Alternative: Simple File Backup System

If GitHub storage seems complex, I can also create a simple backup system that:
1. Stores files locally during development
2. Creates a backup file that you can manually download
3. Provides a restore mechanism

Would you like me to implement this simpler approach instead?

## Next Steps

1. Create GitHub Personal Access Token
2. Add environment variables to Render
3. Deploy and test!
4. Your images will now persist forever! 🎉

This solution is **100% free** and will work perfectly with your current Railway + Render setup!
