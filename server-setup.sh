#!/bin/bash
# Server Setup Script for BookLib API Deployment
# Run this on 192.168.1.175 as root or with sudo

set -e

echo "=========================================="
echo "BookLib API Server Setup"
echo "=========================================="

# Create deployment directory
DEPLOY_PATH="/opt/booklib"
DEPLOY_USER="deploy"

echo "Creating deployment directory: $DEPLOY_PATH"
mkdir -p $DEPLOY_PATH

# Create deploy user if it doesn't exist
if ! id -u $DEPLOY_USER > /dev/null 2>&1; then
    echo "Creating deploy user: $DEPLOY_USER"
    useradd -m -s /bin/bash $DEPLOY_USER
    usermod -aG docker $DEPLOY_USER
else
    echo "Deploy user already exists: $DEPLOY_USER"
fi

# Set ownership
chown -R $DEPLOY_USER:$DEPLOY_USER $DEPLOY_PATH

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Add Jenkins server SSH public key to $DEPLOY_USER authorized_keys:"
echo "   sudo -u $DEPLOY_USER mkdir -p /home/$DEPLOY_USER/.ssh"
echo "   sudo -u $DEPLOY_USER vi /home/$DEPLOY_USER/.ssh/authorized_keys"
echo ""
echo "2. Ensure Docker and Docker Compose are installed"
echo "3. Create .env.production file in $DEPLOY_PATH with secure credentials"
echo "4. Configure your Jenkins pipeline with 'deploy-key' SSH credentials"
echo ""
echo "Deployment path: $DEPLOY_PATH"
echo "Deploy user: $DEPLOY_USER"
