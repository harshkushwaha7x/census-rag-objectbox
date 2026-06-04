# Deployment Guide

This guide covers various deployment options for the Census RAG application.

---

## Table of Contents

1. [Local Deployment](#local-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Considerations](#production-considerations)

---

## Local Deployment

### Prerequisites
- Python 3.8+
- Groq API key
- 4GB+ RAM recommended

### Steps

1. **Clone and Setup**
```bash
git clone https://github.com/harshkushwaha7x/census-rag-objectbox.git
cd census-rag-objectbox
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

3. **Run Application**
```bash
cd app
streamlit run app.py
```

4. **Access**
Open browser to `http://localhost:8501`

---

## Docker Deployment

### Using Docker Compose (Recommended)

1. **Setup Environment**
```bash
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

2. **Build and Run**
```bash
docker-compose up -d
```

3. **View Logs**
```bash
docker-compose logs -f
```

4. **Stop Application**
```bash
docker-compose down
```

### Using Docker Only

1. **Build Image**
```bash
docker build -t census-rag:latest .
```

2. **Run Container**
```bash
docker run -d \
  --name census-rag \
  -p 8501:8501 \
  -v $(pwd)/objectbox:/app/objectbox \
  -e GROQ_API_KEY=your_api_key_here \
  census-rag:latest
```

3. **Check Status**
```bash
docker ps
docker logs census-rag
```

---

## Cloud Deployment

### Streamlit Cloud

1. **Prerequisites**
   - GitHub repository
   - Streamlit Cloud account

2. **Steps**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `app/app.py` as the main file
   - Add `GROQ_API_KEY` to Secrets
   - Deploy

3. **Secrets Configuration**
```toml
# In Streamlit Cloud Secrets
GROQ_API_KEY = "your_groq_api_key_here"
```

### AWS Deployment

#### EC2 Instance

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t3.medium or larger
   - Open port 8501

2. **Connect and Setup**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install -y python3-pip git

# Clone and setup
git clone https://github.com/harshkushwaha7x/census-rag-objectbox.git
cd census-rag-objectbox
pip3 install -r requirements.txt

# Configure
cp .env.example .env
nano .env  # Add GROQ_API_KEY

# Run with systemd (recommended)
sudo nano /etc/systemd/system/census-rag.service
```

3. **Systemd Service File**
```ini
[Unit]
Description=Census RAG Streamlit App
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/census-rag-objectbox
Environment="PATH=/home/ubuntu/.local/bin:/usr/bin"
ExecStart=/home/ubuntu/.local/bin/streamlit run app/app.py --server.port 8501
Restart=always

[Install]
WantedBy=multi-user.target
```

4. **Start Service**
```bash
sudo systemctl daemon-reload
sudo systemctl enable census-rag
sudo systemctl start census-rag
sudo systemctl status census-rag
```

#### ECS (Elastic Container Service)

1. **Push Docker Image to ECR**
```bash
# Authenticate
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account-id.dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag census-rag:latest your-account-id.dkr.ecr.us-east-1.amazonaws.com/census-rag:latest
docker push your-account-id.dkr.ecr.us-east-1.amazonaws.com/census-rag:latest
```

2. **Create ECS Task Definition**
```json
{
  "family": "census-rag",
  "networkMode": "awsvpc",
  "containerDefinitions": [
    {
      "name": "census-rag",
      "image": "your-account-id.dkr.ecr.us-east-1.amazonaws.com/census-rag:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "GROQ_API_KEY",
          "value": "your_api_key"
        }
      ],
      "memory": 2048,
      "cpu": 1024
    }
  ]
}
```

3. **Create Service with Load Balancer**

### Google Cloud Platform

#### Cloud Run

1. **Build and Push**
```bash
gcloud builds submit --tag gcr.io/your-project-id/census-rag
```

2. **Deploy**
```bash
gcloud run deploy census-rag \
  --image gcr.io/your-project-id/census-rag \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GROQ_API_KEY=your_api_key \
  --memory 2Gi \
  --port 8501
```

### Azure

#### Container Instances

1. **Create Container**
```bash
az container create \
  --resource-group census-rag-rg \
  --name census-rag-app \
  --image your-dockerhub-username/census-rag:latest \
  --dns-name-label census-rag \
  --ports 8501 \
  --environment-variables GROQ_API_KEY=your_api_key \
  --memory 2 \
  --cpu 1
```

### Heroku

1. **Prerequisites**
```bash
heroku login
heroku create census-rag-app
```

2. **Add Buildpack**
```bash
heroku buildpacks:set heroku/python
```

3. **Configure**
```bash
heroku config:set GROQ_API_KEY=your_api_key
```

4. **Create Procfile**
```
web: streamlit run app/app.py --server.port=$PORT --server.address=0.0.0.0
```

5. **Deploy**
```bash
git push heroku main
```

---

## Production Considerations

### Security

1. **API Key Management**
   - Use secret managers (AWS Secrets Manager, Azure Key Vault)
   - Never commit `.env` files
   - Rotate keys regularly

2. **Network Security**
   - Use HTTPS/SSL certificates
   - Configure firewall rules
   - Implement rate limiting

3. **Access Control**
   - Add authentication (OAuth, API keys)
   - Implement user sessions
   - Log access attempts

### Performance

1. **Caching**
   - Enable Streamlit caching
   - Cache embeddings and model outputs
   - Use Redis for distributed caching

2. **Scaling**
   - Horizontal scaling with load balancer
   - Use CDN for static assets
   - Optimize chunk size and retrieval

3. **Monitoring**
   - Set up application monitoring (DataDog, New Relic)
   - Configure alerts for errors
   - Track response times

### Database

1. **ObjectBox Persistence**
   - Use persistent volumes
   - Regular backups
   - Consider managed vector databases for scale

2. **Backup Strategy**
```bash
# Backup ObjectBox database
tar -czf objectbox-backup-$(date +%Y%m%d).tar.gz objectbox/

# Restore
tar -xzf objectbox-backup-20240604.tar.gz
```

### Maintenance

1. **Updates**
   - Keep dependencies updated
   - Monitor security advisories
   - Test updates in staging first

2. **Logging**
```python
# Configure production logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

3. **Health Checks**
```python
# Add health check endpoint
@app.route('/health')
def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}
```

---

## Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `GROQ_API_KEY` | Yes | Groq API key | None |
| `MODEL_NAME` | No | LLM model name | Llama3-8b-8192 |
| `CHUNK_SIZE` | No | Document chunk size | 1000 |
| `CHUNK_OVERLAP` | No | Chunk overlap size | 200 |

---

## Troubleshooting Deployment

### Common Issues

1. **Port Already in Use**
```bash
# Check what's using port 8501
lsof -i :8501  # Linux/Mac
netstat -ano | findstr :8501  # Windows

# Kill the process or use different port
streamlit run app.py --server.port 8502
```

2. **Memory Issues**
   - Increase container/instance memory
   - Reduce `MAX_DOCUMENTS_TO_PROCESS`
   - Enable swap space

3. **API Connection Errors**
   - Verify API key
   - Check network connectivity
   - Review firewall rules

---

## Support

For deployment issues:
- 📧 Email: nebeyoumusie@gmail.com
- 💬 GitHub Issues: [Create Issue](https://github.com/harshkushwaha7x/census-rag-objectbox/issues)
