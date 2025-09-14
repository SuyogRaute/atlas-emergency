# Atlas-Alert Ocean Hazard Monitoring System

*Ocean safety through crowdsourced reporting and AI-powered threat assessment*

[![Deployed on Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?style=for-the-badge&logo=vercel)](https://vercel.com/rahulmediaworkv-3058s-projects/v0-v0vercelocean12)
[![Built with v0](https://img.shields.io/badge/Built%20with-v0.app-black?style=for-the-badge)](https://v0.app/chat/projects/gJ4X7Xdk9PK)

## Overview

Atlas-Alert is a comprehensive ocean hazard monitoring and emergency response system that combines:

- **Crowdsourced Reporting**: Citizens can report ocean hazards through web, mobile, and SMS
- **Social Media Monitoring**: AI-powered analysis of Twitter/X posts using hashtags like #OceanRanger and #BlueWatch
- **Real-time Threat Assessment**: ML models score and classify hazard reports for credibility and urgency
- **Automated Response**: Chatbot outreach to social media users for verification and additional details
- **Emergency Alerts**: SMS broadcasting to authorities and affected populations
- **Live Mapping**: Real-time visualization of hazard zones and rescue team locations

## Architecture

### Frontend (Next.js)
- Citizen reporting interface
- Admin dashboard for emergency management
- Live map with hazard zones and team tracking
- Real-time updates via WebSocket

### Backend (FastAPI + Python)
- RESTful API for all system operations
- PostGIS database for geospatial data
- Celery + Redis for background processing
- ONNX Runtime for ML model inference
- WebSocket support for real-time updates

### Key Features
- **Multi-source Data Ingestion**: App reports, SMS, social media
- **AI-Powered Analysis**: Text classification, image analysis, credibility scoring
- **Spatial Clustering**: DBSCAN algorithm for hotspot detection
- **Emergency Escalation**: Automated alerts to Coast Guard, NDMA, and local authorities
- **Team Management**: Live tracking of rescue teams and resource allocation

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- PostgreSQL with PostGIS extension
- Redis server

### Backend Setup
\`\`\`bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
\`\`\`

### Frontend Setup
\`\`\`bash
npm install
npm run dev
\`\`\`

### Environment Variables
\`\`\`env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/atlas_alert

# Redis
REDIS_URL=redis://localhost:6379/0

# Twilio SMS
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM_NUMBER=+1234567890

# Twitter API
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_BEARER_TOKEN=your_bearer_token

# External APIs
OPENWEATHER_API_KEY=your_openweather_key
\`\`\`

## API Endpoints

### Core Endpoints
- `POST /api/reports` - Submit hazard report
- `GET /api/reports` - Retrieve reports with filtering
- `POST /api/social` - Ingest social media post
- `GET /api/hotspots` - Get current hazard zones
- `POST /api/alerts/issue` - Issue emergency alert
- `WS /api/ws/realtime` - Real-time updates

### Admin Endpoints
- `POST /api/admin/teams` - Create rescue team
- `POST /api/admin/zones` - Create manual hazard zone
- `GET /api/admin/analytics` - System analytics
- `PUT /api/reports/{id}/verify` - Verify report

## ML Pipeline

### Text Classification
- Hazard type detection (oil spill, tsunami, storm surge, etc.)
- Urgency scoring based on keywords and context
- Credibility assessment of reporters

### Image Analysis
- Visual hazard detection in uploaded media
- Oil spill identification from satellite/drone imagery
- Damage assessment from photos

### Threat Scoring
Combined confidence score from:
- Text analysis (40%)
- Image analysis (30%)
- Reporter credibility (15%)
- Location density (10%)
- Social corroboration (5%)

## Deployment

### Production Deployment
1. Set up PostgreSQL with PostGIS on cloud provider
2. Deploy backend to Railway/Render/AWS
3. Deploy frontend to Vercel
4. Configure environment variables
5. Set up Celery workers for background processing

### Docker Deployment
\`\`\`bash
docker-compose up -d
\`\`\`

## Integration with Authorities

### Supported Agencies
- **Indian Coast Guard**: Oil spill and maritime emergencies
- **NDMA**: Tsunami and major disaster coordination
- **IMD**: Weather-related hazard verification
- **State Pollution Boards**: Environmental incidents

### Alert Channels
- SMS to emergency contacts
- Email notifications
- REST API webhooks
- Cell tower broadcast (via telecom integration)

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For technical support or questions:
- Email: support@atlas-alert.org
- Documentation: [docs.atlas-alert.org](https://docs.atlas-alert.org)
- Issues: [GitHub Issues](https://github.com/atlas-alert/issues)

---

**Atlas-Alert**: Protecting coastal communities through technology and collaboration.
\`\`\`







```python file="" isHidden
