#!/bin/bash

echo "=== AI Phone System GitHub Upload Script ==="
echo ""

# Check if already authenticated
if ! gh auth status > /dev/null 2>&1; then
    echo "Step 1: Authenticate with GitHub"
    echo "Please run: gh auth login"
    echo "Follow the prompts to authenticate with your GitHub account"
    echo ""
    exit 1
fi

echo "✓ GitHub authentication verified"

# Create repository
echo "Step 2: Creating GitHub repository..."
REPO_NAME="ai-phone-system"

if gh repo create "$REPO_NAME" --public --description "AI Phone System for Green Slice Lawn Care - Twilio + Abacus.ai Integration" --clone=false; then
    echo "✓ Repository created successfully"
else
    echo "Repository might already exist, continuing..."
fi

# Add remote and push
echo "Step 3: Adding remote and pushing code..."
git remote add origin "https://github.com/$(gh api user --jq .login)/$REPO_NAME.git" 2>/dev/null || echo "Remote already exists"

echo "Step 4: Pushing code to GitHub..."
if git push -u origin main; then
    echo ""
    echo "🎉 SUCCESS! Your AI Phone System code has been uploaded to GitHub!"
    echo ""
    echo "Repository URL: https://github.com/$(gh api user --jq .login)/$REPO_NAME"
    echo ""
    echo "Next steps for Railway deployment:"
    echo "1. Go to railway.app"
    echo "2. Create a new project"
    echo "3. Connect your GitHub repository: $REPO_NAME"
    echo "4. Set your environment variables in Railway dashboard"
    echo "5. Deploy!"
    echo ""
else
    echo "❌ Failed to push to GitHub. Please check your authentication and try again."
fi
