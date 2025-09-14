"""
SQLAlchemy ORM models with PostGIS support
Atlas-Alert database schema
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography, Geometry
import uuid
from sqlalchemy.dialects.postgresql import UUID

from ..database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    phone_hash = Column(String(255))  # Hashed phone number for privacy
    role = Column(String(50), default="citizen")  # citizen, admin, analyst
    credibility_score = Column(Float, default=0.5)
    last_known_lat = Column(Float)
    last_known_lon = Column(Float)
    last_known_geom = Column(Geography('POINT', srid=4326))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    reports = relationship("Report", back_populates="user")

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    source = Column(String(50))  # 'app', 'sms', 'social'
    hazard_type = Column(String(100))
    description = Column(Text)
    media_url = Column(String(500))
    lat = Column(Float)
    lon = Column(Float)
    geom = Column(Geography('POINT', srid=4326))
    severity = Column(String(20), default="medium")  # low, medium, high
    confidence = Column(Float, default=0.0)  # 0..1 from ML scoring
    verified = Column(Boolean, default=False)
    status = Column(String(50), default="pending")  # pending, verified, rejected
    report_scores = Column(JSON)  # ML model outputs for audit
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="reports")
    alerts = relationship("Alert", back_populates="report")

class SocialPost(Base):
    __tablename__ = "social_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50))  # twitter, facebook, instagram
    post_id = Column(String(255))  # Platform-specific post ID
    author_handle = Column(String(255))
    text = Column(Text)
    posted_at = Column(DateTime(timezone=True))
    lat = Column(Float)
    lon = Column(Float)
    geom = Column(Geography('POINT', srid=4326))
    relevance = Column(Float, default=0.0)  # 0..1 relevance to hazards
    urgency = Column(Float, default=0.0)  # 0..1 urgency score
    credibility = Column(Float, default=0.5)  # Author credibility
    hazard_type = Column(String(100))
    keywords = Column(ARRAY(String))
    processed = Column(Boolean, default=False)
    outreach_sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Zone(Base):
    __tablename__ = "zones"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20))  # 'red', 'green'
    name = Column(String(255))
    geom = Column(Geography('POLYGON', srid=4326))
    metadata = Column(JSON)  # Additional zone information
    avg_confidence = Column(Float)
    report_count = Column(Integer, default=0)
    radius_km = Column(Float)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    alerts = relationship("Alert", back_populates="zone")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=True)
    message = Column(Text)
    channels = Column(ARRAY(String))  # ['sms', 'push', 'email']
    status = Column(String(50), default="pending")  # pending, sent, acknowledged
    authority_notified = Column(Boolean, default=False)
    sms_count = Column(Integer, default=0)
    issued_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    zone = relationship("Zone", back_populates="alerts")
    report = relationship("Report", back_populates="alerts")

class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    phone = Column(String(20))
    assigned_zone_id = Column(Integer, ForeignKey("zones.id"), nullable=True)
    status = Column(String(50), default="available")  # available, deployed, offline
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    live_locations = relationship("LiveLocation", back_populates="team")

class LiveLocation(Base):
    __tablename__ = "live_locations"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    lat = Column(Float)
    lon = Column(Float)
    geom = Column(Geography('POINT', srid=4326))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    team = relationship("Team", back_populates="live_locations")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    action = Column(String(255))
    resource_type = Column(String(100))  # report, zone, alert
    resource_id = Column(String(100))
    details = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class SocialOutreach(Base):
    __tablename__ = "social_outreach"
    
    id = Column(Integer, primary_key=True, index=True)
    social_post_id = Column(Integer, ForeignKey("social_posts.id"))
    outreach_type = Column(String(50))  # 'dm', 'reply', 'webform'
    status = Column(String(50), default="pending")  # pending, sent, responded
    message_sent = Column(Text)
    response_received = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    responded_at = Column(DateTime(timezone=True))
