if outreach_count < len(recent_applications) * 0.5:
            recommendations.append(
                f"📧 Increase outreach: You sent {outreach_count} messages for {len(recent_applications)} applications. "
                f"Direct outreach increases interview rates by 3x."
            )
        
        return recommendations
```

**Deliverables:**
- ✅ Success pattern recognition
- ✅ Weekly performance reports (emailed)
- ✅ Personalized recommendations
- ✅ Continuous optimization suggestions

---

## 🚀 Phase 4: Polish & Launch (Weeks 13-16)

### Week 13: Mobile App (React Native)

#### Day 85-87: Core Mobile Features

**Tasks:**
- [ ] Setup React Native project (Expo)
- [ ] Build authentication screens
- [ ] Create dashboard view
- [ ] Add application tracker
- [ ] Implement push notifications

**Code:**
```typescript
// mobile/app/(tabs)/dashboard.tsx
import { View, Text, ScrollView, RefreshControl } from 'react-native';
import { useQuery } from '@tanstack/react-query';

export default function DashboardScreen() {
  const { data: applications, refetch, isRefetching } = useQuery({
    queryKey: ['applications'],
    queryFn: fetchApplications,
  });
  
  const stats = {
    pending: applications?.filter(a => a.status === 'pending').length || 0,
    interviewing: applications?.filter(a => a.status === 'interviewing').length || 0,
  };
  
  return (
    <ScrollView
      className="flex-1 bg-white p-4"
      refreshControl={
        <RefreshControl refreshing={isRefetching} onRefresh={refetch} />
      }
    >
      {/* Stats */}
      <View className="mb-6 border-4 border-black bg-neon-yellow p-6">
        <Text className="text-3xl font-black">YOUR APPLICATIONS</Text>
        <Text className="mt-2 text-lg font-bold">
          {applications?.length || 0} total
        </Text>
      </View>
      
      <View className="mb-6 flex-row gap-4">
        <View className="flex-1 border-4 border-black bg-white p-4">
          <Text className="text-4xl font-black">{stats.pending}</Text>
          <Text className="text-sm font-bold">PENDING</Text>
        </View>
        
        <View className="flex-1 border-4 border-black bg-neon-green p-4">
          <Text className="text-4xl font-black">{stats.interviewing}</Text>
          <Text className="text-sm font-bold">INTERVIEWS</Text>
        </View>
      </View>
      
      {/* Recent Applications */}
      <Text className="mb-4 text-xl font-black">RECENT APPLICATIONS</Text>
      {applications?.slice(0, 10).map(app => (
        <ApplicationCard key={app.id} application={app} />
      ))}
    </ScrollView>
  );
}
```

**Push Notifications:**
```typescript
// mobile/services/notifications.ts
import * as Notifications from 'expo-notifications';

export async function setupPushNotifications() {
  // Request permissions
  const { status } = await Notifications.requestPermissionsAsync();
  if (status !== 'granted') return;
  
  // Get push token
  const token = await Notifications.getExpoPushTokenAsync();
  
  // Send to backend
  await fetch(`${API_URL}/api/users/push-token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ token: token.data }),
  });
}

// Configure notification handler
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

// Notification types
export const sendNotification = {
  applicationResponse: (jobTitle: string, company: string) => ({
    title: '🎉 Response Received!',
    body: `${company} responded to your ${jobTitle} application`,
    data: { type: 'response' },
  }),
  
  interviewScheduled: (company: string, time: string) => ({
    title: '📅 Interview Scheduled',
    body: `${company} interview on ${time}`,
    data: { type: 'interview' },
  }),
  
  weeklyReport: (applicationsCount: number, interviewRate: number) => ({
    title: '📊 Weekly Report',
    body: `${applicationsCount} applications, ${interviewRate}% interview rate`,
    data: { type: 'report' },
  }),
};
```

**Deliverables:**
- ✅ iOS and Android apps
- ✅ Core features (dashboard, tracker)
- ✅ Push notifications (responses, interviews)
- ✅ Offline support with sync

---

#### Day 88-91: Quick Actions & Widgets

**Tasks:**
- [ ] Add quick apply from mobile
- [ ] Build resume upload from phone
- [ ] Create home screen widgets
- [ ] Add Siri shortcuts
- [ ] Implement share extension

**Deliverables:**
- ✅ One-tap apply from mobile browser
- ✅ Home screen widget showing stats
- ✅ Siri shortcuts ("Apply to jobs")
- ✅ Share job links directly to app

---

### Week 14: Enterprise Features

#### Day 92-94: Team Accounts

**Tasks:**
- [ ] Build organization/team structure
- [ ] Add role-based access control (RBAC)
- [ ] Create team analytics dashboard
- [ ] Implement shared template library
- [ ] Add team collaboration features

**Code:**
```python
# backend/models/organization.py
class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    plan = Column(String(50))  # starter, professional, enterprise
    settings = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    members = relationship("OrganizationMember", back_populates="organization")
    templates = relationship("SharedTemplate", back_populates="organization")

class OrganizationMember(Base):
    __tablename__ = "organization_members"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID, ForeignKey("organizations.id"))
    user_id = Column(UUID, ForeignKey("users.id"))
    role = Column(String(50))  # admin, member, viewer
    permissions = Column(JSONB)
    joined_at = Column(DateTime, default=datetime.utcnow)

# RBAC implementation
class PermissionChecker:
    PERMISSIONS = {
        'admin': ['*'],  # All permissions
        'member': [
            'applications.read',
            'applications.write',
            'resumes.read',
            'resumes.write',
            'analytics.read',
        ],
        'viewer': [
            'applications.read',
            'analytics.read',
        ],
    }
    
    def can(self, user: User, permission: str, organization_id: str) -> bool:
        """Check if user has permission in organization"""
        
        member = db.query(OrganizationMember).filter(
            OrganizationMember.organization_id == organization_id,
            OrganizationMember.user_id == user.id
        ).first()
        
        if not member:
            return False
        
        user_permissions = self.PERMISSIONS.get(member.role, [])
        
        # Check wildcard
        if '*' in user_permissions:
            return True
        
        # Check exact permission
        if permission in user_permissions:
            return True
        
        # Check wildcard permission (e.g., 'applications.*')
        permission_parts = permission.split('.')
        wildcard = f"{permission_parts[0]}.*"
        
        return wildcard in user_permissions
```

**Team Analytics:**
```typescript
// components/TeamAnalytics.tsx
export const TeamAnalytics: React.FC<{ orgId: string }> = ({ orgId }) => {
  const { data: analytics } = useQuery({
    queryKey: ['team-analytics', orgId],
    queryFn: () => fetchTeamAnalytics(orgId),
  });
  
  return (
    <div className="p-8">
      <div className="mb-8 border-4 border-black bg-white p-6 shadow-brutal">
        <h1 className="text-3xl font-black">TEAM PERFORMANCE</h1>
      </div>
      
      {/* Team Stats */}
      <div className="mb-8 grid grid-cols-5 gap-4">
        <StatCard label="Total Members" value={analytics?.memberCount} />
        <StatCard label="Total Applications" value={analytics?.totalApplications} />
        <StatCard label="Team Response Rate" value={`${analytics?.responseRate}%`} />
        <StatCard label="Active This Week" value={analytics?.activeMembers} />
        <StatCard label="Offers This Month" value={analytics?.offersThisMonth} />
      </div>
      
      {/* Member Leaderboard */}
      <div className="mb-8 border-4 border-black bg-white p-6 shadow-brutal">
        <h2 className="mb-4 text-2xl font-black">MEMBER LEADERBOARD</h2>
        <table className="w-full">
          <thead>
            <tr className="border-b-2 border-black">
              <th className="py-2 text-left font-black">MEMBER</th>
              <th className="py-2 text-right font-black">APPLICATIONS</th>
              <th className="py-2 text-right font-black">INTERVIEWS</th>
              <th className="py-2 text-right font-black">OFFERS</th>
            </tr>
          </thead>
          <tbody>
            {analytics?.memberStats.map(member => (
              <tr key={member.id} className="border-b border-gray-200">
                <td className="py-3 font-bold">{member.name}</td>
                <td className="py-3 text-right">{member.applications}</td>
                <td className="py-3 text-right">{member.interviews}</td>
                <td className="py-3 text-right font-black text-neon-green">
                  {member.offers}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
```

**Deliverables:**
- ✅ Multi-user team accounts
- ✅ Role-based permissions (admin/member/viewer)
- ✅ Team analytics and leaderboard
- ✅ Shared resume/template library

---

#### Day 95-98: API for Recruitment Agencies

**Tasks:**
- [ ] Build public REST API
- [ ] Create API documentation (OpenAPI)
- [ ] Add API key authentication
- [ ] Implement rate limiting
- [ ] Build API dashboard

**Code:**
```python
# backend/api/public_api.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer

router = APIRouter(prefix="/api/v1", tags=["public"])
security = HTTPBearer()

async def verify_api_key(credentials = Depends(security)) -> Organization:
    """Verify API key and return organization"""
    
    api_key = credentials.credentials
    
    org = db.query(Organization).filter(
        Organization.api_key == api_key
    ).first()
    
    if not org:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Check rate limits
    if not await check_rate_limit(org.id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    return org

@router.post("/applications")
async def create_application(
    data: ApplicationCreateRequest,
    org: Organization = Depends(verify_api_key)
):
    """
    Create a new job application
    
    This endpoint allows recruitment agencies to submit applications
    on behalf of candidates.
    """
    
    # Create application
    application = Application(
        organization_id=org.id,
        job_title=data.job_title,
        company=data.company,
        candidate_email=data.candidate_email,
        resume_url=data.resume_url,
    )
    
    db.add(application)
    db.commit()
    
    return {
        "success": True,
        "application_id": application.id,
    }

@router.get("/applications/{application_id}")
async def get_application(
    application_id: str,
    org: Organization = Depends(verify_api_key)
):
    """Get application status and details"""
    
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.organization_id == org.id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return {
        "id": application.id,
        "status": application.status,
        "applied_at": application.applied_at,
        "response_at": application.response_at,
        "ats_score": application.ats_score,
    }

# Rate limiting
async def check_rate_limit(org_id: str) -> bool:
    """Check if organization is within rate limits"""
    
    key = f"api:rate_limit:{org_id}:{datetime.utcnow().strftime('%Y-%m-%d-%H')}"
    
    current_count = await redis.get(key)
    
    if current_count and int(current_count) >= 1000:  # 1000 requests per hour
        return False
    
    await redis.incr(key)
    await redis.expire(key, 3600)
    
    return True
```

**API Documentation (OpenAPI):**
```yaml
openapi: 3.0.0
info:
  title: JobHack API
  version: 1.0.0
  description: Programmatic access to JobHack features

servers:
  - url: https://api.jobhack.io/v1

security:
  - BearerAuth: []

paths:
  /applications:
    post:
      summary: Create application
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                job_title:
                  type: string
                company:
                  type: string
                candidate_email:
                  type: string
                resume_url:
                  type: string
      responses:
        '201':
          description: Application created
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                  application_id:
                    type: string

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
```

**Deliverables:**
- ✅ REST API with 10+ endpoints
- ✅ OpenAPI documentation
- ✅ API key authentication
- ✅ Rate limiting (1000 req/hour)
- ✅ API usage dashboard

---

### Week 15: Performance & Security

#### Day 99-101: Performance Optimization

**Tasks:**
- [ ] Implement database query optimization
- [ ] Add Redis caching layer
- [ ] Setup CDN for static assets
- [ ] Optimize bundle size (code splitting)
- [ ] Add image optimization
- [ ] Implement lazy loading

**Code:**
```typescript
// Database query optimization
// Before: N+1 query problem
const applications = await db.query(Application).all();
for (const app of applications) {
  const resume = await db.query(Resume).filter(Resume.id == app.resume_id).first();
}

// After: Single query with joins
const applications = await db.query(Application)
  .join(Resume)
  .options(joinedload(Application.resume))
  .all();

// Redis caching
async function getCachedOrFetch<T>(
  key: string,
  fetchFn: () => Promise<T>,
  ttl: number = 3600
): Promise<T> {
  // Try cache first
  const cached = await redis.get(key);
  if (cached) {
    return JSON.parse(cached);
  }
  
  // Fetch from source
  const data = await fetchFn();
  
  // Store in cache
  await redis.setex(key, ttl, JSON.stringify(data));
  
  return data;
}

// Usage
const applications = await getCachedOrFetch(
  `user:${userId}:applications`,
  () => fetchApplicationsFromDB(userId),
  1800  // 30 minutes
);
```

**Bundle Optimization:**
```typescript
// next.config.js
module.exports = {
  // Enable SWC minification
  swcMinify: true,
  
  // Image optimization
  images: {
    domains: ['storage.jobhack.io'],
    formats: ['image/avif', 'image/webp'],
  },
  
  // Bundle analyzer
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.optimization.splitChunks = {
        chunks: 'all',
        cacheGroups: {
          default: false,
          vendors: false,
          commons: {
            name: 'commons',
            chunks: 'all',
            minChunks: 2,
          },
          lib: {
            test: /node_modules/,
            name: 'lib',
            priority: 10,
          },
        },
      };
    }
    return config;
  },
};
```

**Deliverables:**
- ✅ 50%+ reduction in API response times
- ✅ 40%+ reduction in bundle size
- ✅ 90+ Lighthouse score
- ✅ < 2s initial page load

---

#### Day 102-105: Security Hardening

**Tasks:**
- [ ] Implement rate limiting on all endpoints
- [ ] Add CSRF protection
- [ ] Setup WAF (Web Application Firewall)
- [ ] Implement SQL injection prevention
- [ ] Add XSS protection
- [ ] Setup security headers
- [ ] Perform penetration testing

**Code:**
```python
# Security middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://jobhack.io"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["jobhack.io", "*.jobhack.io"]
)

# Security headers
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

# Input validation
from pydantic import BaseModel, validator

class ApplicationCreate(BaseModel):
    job_title: str
    company: str
    
    @validator('job_title', 'company')
    def sanitize_input(cls, v):
        # Remove potential XSS
        return v.replace('<', '&lt;').replace('>', '&gt;')

# SQL injection prevention (always use parameterized queries)
# ✅ Good
result = db.execute(
    "SELECT * FROM applications WHERE user_id = :user_id",
    {"user_id": user_id}
)

# ❌ Bad (vulnerable to SQL injection)
# result = db.execute(f"SELECT * FROM applications WHERE user_id = {user_id}")
```

**Security Checklist:**
```markdown
- [x] All endpoints rate-limited
- [x] HTTPS only (HSTS enabled)
- [x] API keys encrypted at rest
- [x] User passwords hashed with bcrypt
- [x] CSRF tokens on all forms
- [x] Input validation on all endpoints
- [x] SQL injection prevention
- [x] XSS protection
- [x] Security headers configured
- [x] Regular dependency updates
- [x] Secrets in environment variables (not code)
- [x] Database backups encrypted
- [x] Audit logging for sensitive actions
```

**Deliverables:**
- ✅ Pass OWASP Top 10 security tests
- ✅ A+ rating on securityheaders.com
- ✅ Zero critical vulnerabilities
- ✅ Security audit documentation

---

### Week 16: Launch Preparation

#### Day 106-108: Beta Testing

**Tasks:**
- [ ] Recruit 50 beta testers
- [ ] Setup feedback collection system
- [ ] Monitor error rates and performance
- [ ] Fix critical bugs
- [ ] Collect testimonials

**Beta Program:**
```typescript
// components/BetaSignup.tsx
export const BetaSignupForm: React.FC = () => {
  const [submitted, setSubmitted] = useState(false);
  
  const handleSubmit = async (data: BetaSignupData) => {
    await fetch('/api/beta/signup', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    
    setSubmitted(true);
  };
  
  return (
    <div className="mx-auto max-w-2xl border-4 border-black bg-neon-yellow p-8 shadow-brutal">
      <h2 className="mb-4 text-3xl font-black">JOIN BETA</h2>
      <p className="mb-6 font-bold">
        Get early access. Shape the product. Land your dream job.
      </p>
      
      {submitted ? (
        <div className="border-4 border-black bg-neon-green p-6">
          <p className="text-2xl font-black">✓ YOU'RE IN!</p>
          <p className="mt-2">Check your email for beta access.</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="email"
            placeholder="YOUR EMAIL"
            className="w-full border-4 border-black p-4 font-bold"
            required
          />
          
          <select className="w-full border-4 border-black p-4 font-bold" required>
            <option>HOW MANY JOBS ARE YOU APPLYING TO?</option>
            <option>0-10 per week</option>
            <option>10-25 per week</option>
            <option>25+ per week</option>
          </select>
          
          <button
            type="submit"
            className="w-full border-4 border-black bg-black py-4 font-black text-white text-xl hover:bg-gray-900"
          >
            GET EARLY ACCESS
          </button>
        </form>
      )}
    </div>
  );
};
```

**Deliverables:**
- ✅ 50+ beta users testing
- ✅ < 0.1% error rate
- ✅ 10+ testimonials collected
- ✅ All critical bugs fixed

---

#### Day 109-112: Launch Marketing & Go-Live

**Tasks:**
- [ ] Create launch landing page
- [ ] Prepare Product Hunt launch
- [ ] Write launch blog post
- [ ] Setup social media accounts
- [ ] Create demo video
- [ ] Prepare press kit
- [ ] Launch on Product Hunt
- [ ] Post on HackerNews, Reddit
- [ ] Email beta users

**Launch Checklist:**
```markdown
## Pre-Launch (T-7 days)
- [x] Landing page live
- [x] Demo video created (2-3 min)
- [x] Product Hunt page drafted
- [x] Twitter/LinkedIn accounts created
- [x] Press kit ready (screenshots, logo, description)
- [x] Beta users notified of launch date
- [x] Monitoring/analytics setup
- [x] Support email/chat ready

## Launch Day
- [ ] 12:01 AM PT: Submit to Product Hunt
- [ ] 6:00 AM: Post on HackerNews
- [ ] 8:00 AM: Post on r/entrepreneur, r/jobs, r/cscareerquestions
- [ ] 9:00 AM: LinkedIn post (personal + company page)
- [ ] 10:00 AM: Twitter thread
- [ ] 11:00 AM: Email newsletter to beta users
- [ ] Throughout day: Respond to ALL comments
- [ ] 5:00 PM: Send to press contacts
- [ ] Monitor: Server load, error rates, sign-ups

## Post-Launch (T+1 week)
- [ ] Daily: Post updates/wins on Twitter
- [ ] Write case studies from early users
- [ ] Reach out to rejected Product Hunt users
- [ ] Guest post on relevant blogs
- [ ] SEO optimization based on traffic data
- [ ] Feature improvements based on feedback
```

**Product Hunt Copy:**
```markdown
# JobHack - AI-Powered Job Application Automation

## Tagline
Land interviews 3x faster with AI-optimized resumes and automated outreach

## Description
Job hunting sucks. JobHack makes it brutally efficient.

🎯 Upload resume → AI optimizes for every job (ATS score 80+)
⚡ One-click apply to 50+ jobs/day with tailored resumes
🕵️ Find hiring managers → Send personalized DMs automatically
📊 Track everything → Learn what works, improve continuously

Built for job seekers who are tired of sending 100 applications into the void.

## First Comment (Maker)
Hey Product Hunt! 👋

I built JobHack because I was TIRED of the modern job search being so broken.

After applying to 200+ jobs with a 2% response rate, I realized:
- Generic resumes get auto-rejected by ATS
- You never reach the actual decision-maker
- There's zero feedback on what works

So I built the tool I wish I had:
✅ AI that rewrites your resume for EVERY job
✅ Auto-applies while you sleep
✅ Finds hiring managers + sends personalized messages
✅ Tracks what works so you improve every week

Beta users are getting 30%+ response rates (vs 5% before).

Happy to answer any questions! 🚀
```

**Deliverables:**
- ✅ Successful Product Hunt launch (>500 upvotes)
- ✅ 1000+ sign-ups in first week
- ✅ Featured on 3+ tech blogs
- ✅ Positive reception (< 5% negative feedback)

---

## 📈 Post-Launch Roadmap (Week 17+)

### Month 2-3: Growth & Iteration
- Implement user feedback
- A/B test landing page (conversion optimization)
- Build referral program
- Add more job board integrations
- Expand LinkedIn automation features
- Create video tutorials

### Month 4-6: Scale
- Hire first employee (customer success)
- Build affiliate program
- Expand to international markets
- Add more languages
- Build integrations (Zapier, Make)
- Launch white-label version for agencies

### Month 7-12: Monetization & Expansion
- Refine pricing tiers
- Build enterprise sales team
- Add advanced analytics
- Build Chrome extension premium features
- Partnerships with career coaches
- Series A fundraising

---

## 🎯 Success Metrics

### Week 4 (MVP)
- [x] Core features working
- [x] Can upload resume → optimize → apply
- [x] ATS scoring functional
- [x] 10 beta users testing

### Week 8 (Core Features)
- [x] Chrome extension published
- [x] LinkedIn integration live
- [x] Outreach automation working
- [x] 50 beta users

### Week 12 (Advanced Features)
- [x] Mobile app published
- [x] All major features complete
- [x] 100 beta users
- [x] < 1% error rate

### Week 16 (Launch)
- [x] Public launch on Product Hunt
- [x] 1000+ users
- [x] Payment system live
- [x] First paying customers

---

## 💰 Monetization Strategy

### Pricing Tiers

**Free (Forever)**
- 5 applications/month
- 1 resume
- Basic ATS scoring
- Community support

**Pro ($29/month)**
- Unlimited applications
- Unlimited resumes
- Advanced ATS optimization
- Chrome extension
- LinkedIn automation (50 DMs/day)
- Email support

**Enterprise ($99/month)**
- Everything in Pro
- Team accounts (5+ users)
- API access
- Priority support
- Custom integrations
- Dedicated account manager

**Agency ($299/month)**
- Everything in Enterprise
- Unlimited team members
- White-label option
- Advanced API limits
- Custom features

---

## 🚨 Critical Path Items

These MUST be done for launch:

1. **Week 1-2**: Authentication + Basic UI working
2. **Week 3**: Resume parsing + ATS scoring
3. **Week 4**: LaTeX generation + optimization
4. **Week 5-6**: Chrome extension + auto-apply
5. **Week 7-8**: LinkedIn integration + outreach
6. **Week 9-12**: Polish + advanced features
7. **Week 13-14**: Mobile app + enterprise features
8. **Week 15**: Security + performance
9. **Week 16**: Beta test + launch

**If running behind schedule, CUT these first:**
- Mobile app (can launch web-only)
- Enterprise features (can add post-launch)
- Some advanced analytics
- Interview prep features

**NEVER cut these:**
- Core resume optimization
- ATS scoring
- Application tracking
- Chrome extension
- Basic outreach

---

## 🛠️ Development Resources Needed

### Tools & Services

**Required:**
- OpenAI/Anthropic API ($200/mo during dev)
- Supabase (free tier OK)
- Vercel (free tier OK)
- SendGrid (free 100 emails/day)
- GitHub (free)

**Optional but Recommended:**
- Figma Pro ($12/mo)
- Linear for project management ($8/mo)
- Sentry for error tracking (free tier)
- PostHog for analytics (free tier)

**Total Monthly Cost During Development:** ~$220/mo

---

## ✅ Daily Development Workflow

### Morning (9 AM - 12 PM)
1. Check GitHub issues/bugs
2. Code 3-4 hours (focus time, no distractions)
3. Push commits, update project board

### Afternoon (1 PM - 5 PM)
4. Test features built in morning
5. Code 2-3 more hours
6. Review day's progress
7. Plan tomorrow's tasks

### Evening (Optional)
8. Learn new tech if needed
9. Research competitors
10. Engage with beta users

### Weekly Review (Friday EOD)
- Review milestone completion
- Adjust next week's plan if behind
- Deploy weekly beta release
- Collect user feedback

---

## 🎓 Learning Resources

If you need to learn any of these technologies:

**Next.js 14:** nextjs.org/learn
**FastAPI:** fastapi.tiangolo.com/tutorial
**React Native:** reactnative.dev/docs/getting-started
**PostgreSQL:** postgresqltutorial.com
****Deliverables:**
- ✅ Multi-offer comparison tool
- ✅ Total compensation calculator
- ✅ Equity valuation estimates
- ✅ AI-powered recommendation with reasoning

---

### Week 11: A/B Testing & Optimization

#### Day 71-73: Resume A/B Testing Framework

**Tasks:**
- [ ] Build A/B test creation flow
- [ ] Implement automatic variant generation
- [ ] Add statistical significance calculator
- [ ] Create results dashboard
- [ ] Automate winner selection

**Code:**
```python
# backend/services/ab_testing.py
class ResumeABTester:
    def create_ab_test(
        self, 
        base_resume: Dict,
        variants: List[Dict],
        target_metric: str = 'response_rate'
    ) -> str:
        """Create A/B test for resume variants"""
        
        test = ABTest(
            user_id=base_resume['user_id'],
            base_resume_id=base_resume['id'],
            variants=variants,
            target_metric=target_metric,
            status='active',
            start_date=datetime.utcnow(),
        )
        
        db.add(test)
        db.commit()
        
        return test.id
    
    async def generate_variants(
        self, 
        base_resume: Dict,
        num_variants: int = 3
    ) -> List[Dict]:
        """Generate resume variants to test"""
        
        variants = []
        
        for i in range(num_variants):
            prompt = f"""
            Create a variant of this resume with these changes:
            
            Variant {i+1} focus:
            - Variant 1: More technical/quantitative focus
            - Variant 2: More leadership/impact focus  
            - Variant 3: More concise/scannable format
            
            Base resume: {json.dumps(base_resume)}
            
            Maintain truthfulness. Only rephrase and reorganize.
            Return modified resume as JSON.
            """
            
            response = await self.llm.generate(prompt)
            variant = json.loads(response)
            variant['variant_type'] = f'variant_{i+1}'
            
            variants.append(variant)
        
        return variants
    
    def calculate_significance(
        self, 
        control_data: Dict,
        variant_data: Dict
    ) -> Dict:
        """Calculate statistical significance of results"""
        
        from scipy import stats
        
        # Extract metrics
        control_responses = control_data['responses']
        control_total = control_data['total']
        variant_responses = variant_data['responses']
        variant_total = variant_data['total']
        
        # Perform chi-square test
        contingency_table = [
            [control_responses, control_total - control_responses],
            [variant_responses, variant_total - variant_responses]
        ]
        
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        # Calculate effect size
        control_rate = control_responses / control_total if control_total > 0 else 0
        variant_rate = variant_responses / variant_total if variant_total > 0 else 0
        lift = ((variant_rate - control_rate) / control_rate * 100) if control_rate > 0 else 0
        
        return {
            'p_value': p_value,
            'is_significant': p_value < 0.05,
            'confidence': (1 - p_value) * 100,
            'lift': lift,
            'control_rate': control_rate,
            'variant_rate': variant_rate,
        }
    
    def auto_select_winner(self, test_id: str) -> str:
        """Automatically select winning variant"""
        
        test = db.query(ABTest).filter(ABTest.id == test_id).first()
        
        # Must have minimum 50 applications per variant
        if test.applications_count < 50 * len(test.variants):
            return None
        
        # Calculate results for each variant
        results = []
        
        for variant in test.variants:
            apps = db.query(Application).filter(
                Application.resume_id == variant['id']
            ).all()
            
            responses = len([a for a in apps if a.response_at is not None])
            total = len(apps)
            
            results.append({
                'variant_id': variant['id'],
                'responses': responses,
                'total': total,
                'rate': responses / total if total > 0 else 0,
            })
        
        # Find best performer
        best_variant = max(results, key=lambda x: x['rate'])
        
        # Check significance vs control (base)
        control = results[0]  # Assuming first is control
        significance = self.calculate_significance(control, best_variant)
        
        if significance['is_significant'] and significance['lift'] > 10:
            test.winner_variant_id = best_variant['variant_id']
            test.status = 'completed'
            db.commit()
            
            return best_variant['variant_id']
        
        return None
```

**Frontend Dashboard:**
```typescript
// components/ABTestDashboard.tsx
export const ABTestDashboard: React.FC<{ testId: string }> = ({ testId }) => {
  const { data: test } = useQuery({
    queryKey: ['ab-test', testId],
    queryFn: () => fetchABTest(testId),
  });
  
  return (
    <div className="p-8">
      <div className="mb-8 border-4 border-black bg-white p-6 shadow-brutal">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-black">A/B TEST: {test?.name}</h2>
            <p className="text-sm">Started {formatDate(test?.startDate)}</p>
          </div>
          
          <div className={`border-2 border-black px-4 py-2 font-black ${
            test?.status === 'active' ? 'bg-neon-yellow' : 'bg-neon-green'
          }`}>
            {test?.status.toUpperCase()}
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-4 gap-4">
        {test?.variants.map((variant, idx) => (
          <div
            key={variant.id}
            className={`border-4 border-black bg-white p-6 shadow-brutal ${
              variant.id === test.winnerVariantId ? 'border-neon-green' : ''
            }`}
          >
            <div className="mb-4 flex items-start justify-between">
              <h3 className="text-lg font-black">
                {idx === 0 ? 'CONTROL' : `VARIANT ${idx}`}
              </h3>
              {variant.id === test.winnerVariantId && (
                <span className="bg-neon-green px-2 py-1 text-xs font-black">
                  WINNER
                </span>
              )}
            </div>
            
            <div className="space-y-4">
              <MetricRow
                label="Applications"
                value={variant.stats.applications}
              />
              <MetricRow
                label="Responses"
                value={variant.stats.responses}
              />
              <MetricRow
                label="Response Rate"
                value={`${variant.stats.responseRate}%`}
                highlight
              />
              <MetricRow
                label="Interviews"
                value={variant.stats.interviews}
              />
            </div>
            
            {idx > 0 && variant.significance && (
              <div className="mt-4 border-t-2 border-black pt-4">
                <div className="text-sm">
                  <div className="font-bold">vs Control:</div>
                  <div className={variant.significance.isSignificant ? 'text-green-600' : 'text-gray-600'}>
                    {variant.significance.lift > 0 ? '+' : ''}{variant.significance.lift.toFixed(1)}% lift
                  </div>
                  <div className="text-xs">
                    {variant.significance.confidence.toFixed(1)}% confidence
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
      
      {!test?.winnerVariantId && test?.status === 'active' && (
        <div className="mt-8 border-4 border-black bg-neon-yellow p-6 shadow-brutal">
          <p className="font-bold">
            ⏳ Test in progress... Need {test.remainingApplications} more applications for statistical significance
          </p>
        </div>
      )}
    </div>
  );
};
```

**Deliverables:**
- ✅ Automatic variant generation (3+ versions)
- ✅ Statistical significance calculation
- ✅ Real-time results dashboard
- ✅ Auto-winner selection at p < 0.05

---

#### Day 74-77: Message Template Optimization

**Tasks:**
- [ ] Build template testing system
- [ ] Track email/DM performance
- [ ] A/B test subject lines
- [ ] Optimize message length
- [ ] Create winning template library

**Code:**
```python
# backend/services/message_optimizer.py
class MessageTemplateOptimizer:
    def create_template_test(
        self,
        template_type: str,  # email, linkedin_dm
        variants: List[str],
        target_metric: str = 'reply_rate'
    ) -> str:
        """Create A/B test for message templates"""
        
        test = MessageABTest(
            template_type=template_type,
            variants=variants,
            target_metric=target_metric,
            status='active',
        )
        
        db.add(test)
        db.commit()
        
        return test.id
    
    def get_next_template(self, test_id: str) -> Dict:
        """Get next template variant to use (round-robin)"""
        
        test = db.query(MessageABTest).filter(MessageABTest.id == test_id).first()
        
        # Count usage of each variant
        usage_counts = {}
        for variant in test.variants:
            count = db.query(OutreachMessage).filter(
                OutreachMessage.template_variant_id == variant['id']
            ).count()
            usage_counts[variant['id']] = count
        
        # Return least-used variant
        least_used = min(usage_counts, key=usage_counts.get)
        
        return next(v for v in test.variants if v['id'] == least_used)
    
    async def optimize_subject_lines(
        self,
        base_subject: str,
        context: Dict
    ) -> List[str]:
        """Generate optimized subject line variants"""
        
        prompt = f"""
        Generate 5 email subject line variants for a cold outreach email.
        
        Base subject: {base_subject}
        Context: Applying for {context['job_title']} at {context['company']}
        
        Create variants that:
        1. Are under 60 characters
        2. Create curiosity without clickbait
        3. Personalize to recipient or company
        4. Stand out in inbox
        5. Avoid spam triggers
        
        Return as JSON array: ["subject 1", "subject 2", ...]
        """
        
        response = await self.llm.generate(prompt)
        variants = json.loads(response)
        
        return variants
    
    def analyze_winning_patterns(self, template_type: str) -> Dict:
        """Analyze patterns in high-performing templates"""
        
        # Get all completed tests
        completed_tests = db.query(MessageABTest).filter(
            MessageABTest.template_type == template_type,
            MessageABTest.status == 'completed',
        ).all()
        
        winners = []
        for test in completed_tests:
            winner = next(
                v for v in test.variants 
                if v['id'] == test.winner_variant_id
            )
            winners.append(winner['content'])
        
        # Analyze patterns
        patterns = {
            'avg_length': sum(len(w) for w in winners) / len(winners),
            'common_phrases': self.extract_common_phrases(winners),
            'avg_questions': sum(w.count('?') for w in winners) / len(winners),
            'personalization_rate': sum(
                1 for w in winners if '{' in w  # Template variables
            ) / len(winners),
        }
        
        return patterns
```

**Template Library:**
```typescript
// components/TemplateLibrary.tsx
export const TemplateLibrary: React.FC = () => {
  const { data: templates } = useQuery({
    queryKey: ['winning-templates'],
    queryFn: fetchWinningTemplates,
  });
  
  return (
    <div className="p-8">
      <div className="mb-8 border-4 border-black bg-neon-yellow p-6 shadow-brutal">
        <h1 className="text-3xl font-black">WINNING TEMPLATES</h1>
        <p>Proven templates with 30%+ reply rates</p>
      </div>
      
      <div className="grid grid-cols-2 gap-6">
        {templates?.map(template => (
          <div
            key={template.id}
            className="border-4 border-black bg-white p-6 shadow-brutal"
          >
            <div className="mb-4 flex items-start justify-between">
              <div>
                <h3 className="text-xl font-black">{template.name}</h3>
                <p className="text-sm text-gray-600">{template.type}</p>
              </div>
              
              <div className="text-right">
                <div className="text-2xl font-black text-neon-green">
                  {template.replyRate}%
                </div>
                <div className="text-xs">Reply Rate</div>
              </div>
            </div>
            
            <div className="mb-4 rounded-none border-2 border-gray-300 bg-gray-50 p-4 font-mono text-sm">
              {template.content}
            </div>
            
            <div className="grid grid-cols-3 gap-2 text-center text-xs">
              <div>
                <div className="font-black">{template.stats.sent}</div>
                <div className="text-gray-600">Sent</div>
              </div>
              <div>
                <div className="font-black">{template.stats.opened}</div>
                <div className="text-gray-600">Opened</div>
              </div>
              <div>
                <div className="font-black">{template.stats.replied}</div>
                <div className="text-gray-600">Replied</div>
              </div>
            </div>
            
            <button className="mt-4 w-full border-2 border-black bg-neon-yellow py-2 font-black hover:bg-yellow-300">
              USE TEMPLATE
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};
```

**Deliverables:**
- ✅ Template A/B testing system
- ✅ Subject line optimizer
- ✅ Winning template library (30%+ reply rate)
- ✅ Pattern analysis (length, tone, personalization)

---

### Week 12: Rejection Analytics & Learning

#### Day 78-80: Rejection Tracking System

**Tasks:**
- [ ] Add rejection reason categorization
- [ ] Build feedback collection system
- [ ] Create rejection pattern analysis
- [ ] Generate improvement recommendations
- [ ] Track common rejection reasons

**Code:**
```python
# backend/services/rejection_analyzer.py
class RejectionAnalyzer:
    REJECTION_CATEGORIES = [
        'underqualified',
        'overqualified',
        'cultural_fit',
        'technical_skills',
        'experience_mismatch',
        'location',
        'compensation',
        'timing',
        'other'
    ]
    
    async def analyze_rejection(
        self,
        application_id: str,
        rejection_email: str = None
    ) -> Dict:
        """Analyze rejection and categorize reason"""
        
        app = db.query(Application).filter(Application.id == application_id).first()
        
        if rejection_email:
            # Use AI to categorize
            category = await self.categorize_rejection(rejection_email)
            extracted_reason = await self.extract_reason(rejection_email)
        else:
            # User manually selects
            category = 'other'
            extracted_reason = None
        
        # Store rejection data
        rejection = Rejection(
            application_id=application_id,
            category=category,
            reason=extracted_reason,
            rejection_email=rejection_email,
            created_at=datetime.utcnow(),
        )
        
        db.add(rejection)
        db.commit()
        
        # Generate insights
        insights = await self.generate_rejection_insights(app, rejection)
        
        return {
            'category': category,
            'reason': extracted_reason,
            'insights': insights,
        }
    
    async def categorize_rejection(self, email_text: str) -> str:
        """Use AI to categorize rejection reason"""
        
        prompt = f"""
        Categorize this rejection email into one of these categories:
        {', '.join(self.REJECTION_CATEGORIES)}
        
        Email: {email_text}
        
        Return only the category name, nothing else.
        """
        
        response = await self.llm.generate(prompt)
        category = response.strip().lower()
        
        if category not in self.REJECTION_CATEGORIES:
            category = 'other'
        
        return category
    
    async def generate_rejection_insights(
        self,
        application: Application,
        rejection: Rejection
    ) -> List[str]:
        """Generate actionable insights from rejection"""
        
        insights = []
        
        # Get user's rejection history
        user_rejections = db.query(Rejection).join(Application).filter(
            Application.user_id == application.user_id
        ).all()
        
        # Find patterns
        category_counts = {}
        for r in user_rejections:
            category_counts[r.category] = category_counts.get(r.category, 0) + 1
        
        # Most common rejection reason
        if category_counts:
            most_common = max(category_counts, key=category_counts.get)
            if category_counts[most_common] >= 3:
                insights.append(
                    f"You've been rejected {category_counts[most_common]} times for '{most_common}'. "
                    f"This is a pattern to address."
                )
        
        # Category-specific insights
        if rejection.category == 'technical_skills':
            # Find which skills are missing
            jd = application.job_description
            resume = application.resume
            
            missing_skills = set(jd.required_skills) - set(resume.skills)
            if missing_skills:
                insights.append(
                    f"Missing technical skills: {', '.join(list(missing_skills)[:3])}. "
                    f"Consider upskilling or highlighting equivalent experience."
                )
        
        elif rejection.category == 'experience_mismatch':
            insights.append(
                "Experience level mismatch. Consider targeting more senior/junior roles, "
                "or emphasize transferable skills more strongly."
            )
        
        elif rejection.category == 'underqualified':
            insights.append(
                "You may be applying to roles above your current level. "
                "Focus on roles matching your experience, or gain skills/certifications."
            )
        
        return insights
    
    def generate_improvement_plan(self, user_id: str) -> Dict:
        """Generate personalized improvement plan based on rejections"""
        
        rejections = db.query(Rejection).join(Application).filter(
            Application.user_id == user_id
        ).all()
        
        if len(rejections) < 5:
            return {
                'message': 'Not enough data yet. Apply to more jobs!',
                'actions': [],
            }
        
        # Analyze patterns
        top_rejection_reason = self.get_top_rejection_category(rejections)
        
        # Generate plan
        plan = {
            'top_issue': top_rejection_reason,
            'actions': self.get_category_actions(top_rejection_reason),
            'metrics_to_track': [
                'Applications per week',
                'Response rate',
                'Interview conversion rate',
            ],
            'timeline': '4-6 weeks',
        }
        
        return plan
```

**Frontend - Rejection Dashboard:**
```typescript
// components/RejectionDashboard.tsx
export const RejectionDashboard: React.FC = () => {
  const { data: rejections } = useQuery({
    queryKey: ['rejections'],
    queryFn: fetchRejections,
  });
  
  const { data: insights } = useQuery({
    queryKey: ['rejection-insights'],
    queryFn: fetchRejectionInsights,
  });
  
  const categoryData = rejections?.reduce((acc, r) => {
    acc[r.category] = (acc[r.category] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
  
  return (
    <div className="p-8">
      <div className="mb-8 border-4 border-black bg-red-500 p-6 text-white shadow-brutal">
        <h1 className="text-3xl font-black">REJECTION ANALYTICS</h1>
        <p className="mt-2">Learn from failures. Get better.</p>
      </div>
      
      {/* Overview Stats */}
      <div className="mb-8 grid grid-cols-4 gap-4">
        <StatCard
          label="Total Rejections"
          value={rejections?.length || 0}
          color="red"
        />
        <StatCard
          label="Response Rate"
          value={`${insights?.responseRate || 0}%`}
          color="yellow"
        />
        <StatCard
          label="Top Issue"
          value={insights?.topIssue || 'N/A'}
          color="black"
        />
        <StatCard
          label="Improvement"
          value={`${insights?.improvement || 0}%`}
          color="green"
          trend="up"
        />
      </div>
      
      {/* Rejection Breakdown */}
      <div className="mb-8 border-4 border-black bg-white p-6 shadow-brutal">
        <h2 className="mb-4 text-2xl font-black">REJECTION REASONS</h2>
        <div className="space-y-2">
          {Object.entries(categoryData || {})
            .sort((a, b) => b[1] - a[1])
            .map(([category, count]) => (
              <div key={category} className="flex items-center gap-4">
                <div className="w-48 font-bold uppercase">{category}</div>
                <div className="flex-1">
                  <div className="h-8 border-2 border-black bg-gray-100">
                    <div
                      className="h-full bg-red-500"
                      style={{
                        width: `${(count / rejections.length) * 100}%`,
                      }}
                    />
                  </div>
                </div>
                <div className="w-16 text-right font-black">{count}</div>
              </div>
            ))}
        </div>
      </div>
      
      {/* Insights */}
      <div className="mb-8 border-4 border-black bg-neon-yellow p-6 shadow-brutal">
        <h2 className="mb-4 text-2xl font-black">💡 INSIGHTS</h2>
        <ul className="space-y-3">
          {insights?.insights.map((insight, idx) => (
            <li key={idx} className="flex gap-3">
              <span className="font-black">•</span>
              <span className="font-bold">{insight}</span>
            </li>
          ))}
        </ul>
      </div>
      
      {/* Improvement Plan */}
      {insights?.improvementPlan && (
        <div className="border-4 border-black bg-white p-6 shadow-brutal">
          <h2 className="mb-4 text-2xl font-black">🎯 IMPROVEMENT PLAN</h2>
          <div className="space-y-4">
            <div>
              <div className="text-sm font-bold text-gray-600">TOP ISSUE</div>
              <div className="text-xl font-black">
                {insights.improvementPlan.top_issue}
              </div>
            </div>
            
            <div>
              <div className="text-sm font-bold text-gray-600">ACTION ITEMS</div>
              <ol className="mt-2 space-y-2">
                {insights.improvementPlan.actions.map((action, idx) => (
                  <li key={idx} className="flex gap-2">
                    <span className="font-black">{idx + 1}.</span>
                    <span className="font-bold">{action}</span>
                  </li>
                ))}
              </ol>
            </div>
            
            <div>
              <div className="text-sm font-bold text-gray-600">TIMELINE</div>
              <div className="font-bold">{insights.improvementPlan.timeline}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
```

**Deliverables:**
- ✅ Rejection categorization (9 categories)
- ✅ Pattern analysis (identify recurring issues)
- ✅ Personalized insights and recommendations
- ✅ Improvement plan generator

---

#### Day 81-84: Learning Loop & Continuous Optimization

**Tasks:**
- [ ] Build feedback collection after each application
- [ ] Implement success pattern recognition
- [ ] Create automatic resume updates based on learnings
- [ ] Add weekly performance reports
- [ ] Build recommendation engine

**Code:**
```python
# backend/services/learning_engine.py
class LearningEngine:
    async def analyze_success_patterns(self, user_id: str) -> Dict:
        """Analyze what works for this user"""
        
        # Get all applications
        applications = db.query(Application).filter(
            Application.user_id == user_id
        ).all()
        
        # Separate successful vs unsuccessful
        successful = [a for a in applications if a.status in ['interviewing', 'offer']]
        unsuccessful = [a for a in applications if a.status in ['rejected', 'no_response']]
        
        patterns = {
            'successful_resume_features': self.analyze_resume_patterns(successful),
            'successful_companies': self.analyze_company_patterns(successful),
            'successful_roles': self.analyze_role_patterns(successful),
            'optimal_timing': self.analyze_timing_patterns(successful),
            'effective_outreach': self.analyze_outreach_patterns(successful),
        }
        
        return patterns
    
    def analyze_resume_patterns(self, successful_apps: List[Application]) -> Dict:
        """Find common resume features in successful applications"""
        
        features = {
            'avg_ats_score': 0,
            'common_keywords': [],
            'optimal_length': 0,
            'effective_format': None,
        }
        
        if not successful_apps:
            return features
        
        # Average ATS score of successful resumes
        ats_scores = [a.resume.ats_score for a in successful_apps if a.resume.ats_score]
        features['avg_ats_score'] = sum(ats_scores) / len(ats_scores) if ats_scores else 0
        
        # Common keywords
        all_keywords = []
        for app in successful_apps:
            if app.job_description:
                all_keywords.extend(app.job_description.keywords)
        
        keyword_counts = {}
        for kw in all_keywords:
            keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
        
        features['common_keywords'] = sorted(
            keyword_counts.keys(),
            key=keyword_counts.get,
            reverse=True
        )[:10]
        
        return features
    
    async def generate_weekly_report(self, user_id: str) -> Dict:
        """Generate weekly performance report"""
        
        # Get last week's data
        last_week = datetime.utcnow() - timedelta(days=7)
        applications = db.query(Application).filter(
            Application.user_id == user_id,
            Application.created_at >= last_week
        ).all()
        
        report = {
            'week_ending': datetime.utcnow().strftime('%Y-%m-%d'),
            'applications_submitted': len(applications),
            'responses_received': len([a for a in applications if a.response_at]),
            'interviews_scheduled': len([a for a in applications if a.status == 'interviewing']),
            'offers_received': len([a for a in applications if a.status == 'offer']),
            'rejections': len([a for a in applications if a.status == 'rejected']),
            'avg_ats_score': self.calculate_avg_ats_score(applications),
            'top_performing_resume': self.find_top_resume(user_id, last_week),
            'recommendations': await self.generate_recommendations(user_id, applications),
            'next_week_goals': self.generate_goals(applications),
        }
        
        return report
    
    async def generate_recommendations(
        self,
        user_id: str,
        recent_applications: List[Application]
    ) -> List[str]:
        """Generate personalized recommendations"""
        
        recommendations = []
        
        # Application volume
        if len(recent_applications) < 10:
            recommendations.append(
                f"🎯 Increase volume: You applied to {len(recent_applications)} jobs this week. "
                f"Target 15-20 for better results."
            )
        
        # Response rate
        responses = len([a for a in recent_applications if a.response_at])
        response_rate = (responses / len(recent_applications) * 100) if recent_applications else 0
        
        if response_rate < 20:
            recommendations.append(
                f"📝 Improve quality: {response_rate:.1f}% response rate is below average. "
                f"Focus on better resume-JD matching and higher ATS scores."
            )
        
        # ATS scores
        avg_ats = self.calculate_avg_ats_score(recent_applications)
        if avg_ats < 70:
            recommendations.append(
                f"⚡ Boost ATS scores: Average ATS score is {avg_ats:.1f}. "
                f"Aim for 80+ by adding more relevant keywords."
            )
        
        # Outreach
        outreach_count = db.query(OutreachMessage).join(Application).filter(
            Application.user_id == user_id,
            OutreachMessage.created_at >= datetime.utcnow() - timedelta(days=7)
        ).count()
        
        if outreach_count < len(recent_applications) * 0.5:
            recommendations.append(
                f"📧 Increase outreach: You sent {outreach_count} messages for {# JobHack Development Milestones

**Complete step-by-step guide to building JobHack from Day 1 to Launch**

This document breaks down the entire project into actionable daily/weekly milestones with specific tasks, code examples, and completion criteria.

---

## 📅 Timeline Overview

- **Phase 1**: Foundation & MVP (Weeks 1-4)
- **Phase 2**: Core Features (Weeks 5-8)
- **Phase 3**: Advanced Features (Weeks 9-12)
- **Phase 4**: Polish & Launch (Weeks 13-16)

**Total Duration**: 16 weeks (4 months)  
**Recommended Team**: 1-2 developers (full-stack)

---

## 🎯 Phase 1: Foundation & MVP (Weeks 1-4)

### Week 1: Project Setup & Infrastructure

#### Day 1-2: Repository & Development Environment

**Tasks:**
- [ ] Create GitHub repository
- [ ] Setup monorepo structure (Turborepo or npm workspaces)
- [ ] Initialize Next.js 14 frontend
- [ ] Initialize FastAPI backend
- [ ] Setup PostgreSQL database (local + Supabase)
- [ ] Setup Redis (local Docker)
- [ ] Configure ESLint, Prettier, Husky

**Code:**
```bash
# Initialize project
npx create-turbo@latest jobhack
cd jobhack

# Frontend
npx create-next-app@latest frontend --typescript --tailwind --app
cd frontend
npm install zustand @tanstack/react-query axios zod react-hook-form

# Backend
cd ../backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary redis pydantic python-multipart

# Database
docker-compose up -d postgres redis
```

**Deliverables:**
- ✅ Running Next.js dev server at `localhost:3000`
- ✅ Running FastAPI at `localhost:8000`
- ✅ Database accessible
- ✅ Git hooks working (pre-commit linting)

---

#### Day 3-4: Authentication & User Management

**Tasks:**
- [ ] Setup Clerk/NextAuth for authentication
- [ ] Create User model in database
- [ ] Build signup/login pages (neo-brutal design)
- [ ] Implement protected routes
- [ ] Setup session management

**Code:**
```typescript
// app/api/auth/[...nextauth]/route.ts
import NextAuth from "next-auth";
import GoogleProvider from "next-auth/providers/google";

export const authOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  callbacks: {
    async session({ session, token }) {
      session.user.id = token.sub;
      return session;
    },
  },
};

export const GET = NextAuth(authOptions);
export const POST = NextAuth(authOptions);
```

```python
# backend/models/user.py
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    linkedin_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
```

**Deliverables:**
- ✅ User can sign up with email/Google
- ✅ Protected dashboard route
- ✅ User profile stored in DB

---

#### Day 5-7: Neo-Brutalism Design System

**Tasks:**
- [ ] Create Tailwind config with brutal theme
- [ ] Build base UI components (Button, Card, Input, Modal)
- [ ] Create layout components (Header, Sidebar, Footer)
- [ ] Build landing page (with aggressive CTA)
- [ ] Setup typography system

**Code:**
```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        'brutal-black': '#000000',
        'brutal-white': '#FFFFFF',
        'neon-yellow': '#F4FF61',
        'neon-green': '#39FF14',
        'neon-pink': '#FF10F0',
      },
      fontFamily: {
        sans: ['Space Grotesk', 'sans-serif'],
        mono: ['Space Mono', 'monospace'],
      },
      boxShadow: {
        'brutal': '8px 8px 0px 0px rgba(0,0,0,1)',
        'brutal-hover': '12px 12px 0px 0px rgba(0,0,0,1)',
      },
    },
  },
};
```

```typescript
// components/ui/Button.tsx
export const Button: React.FC<ButtonProps> = ({ 
  children, 
  variant = 'primary',
  size = 'md',
  ...props 
}) => {
  return (
    <button
      className={cn(
        "border-4 border-black font-black uppercase transition-all",
        "hover:translate-x-1 hover:translate-y-1",
        "shadow-brutal hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]",
        variant === 'primary' && "bg-neon-yellow text-black",
        variant === 'secondary' && "bg-white text-black",
        size === 'sm' && "px-4 py-2 text-sm",
        size === 'md' && "px-6 py-3 text-base",
        size === 'lg' && "px-8 py-4 text-xl"
      )}
      {...props}
    >
      {children}
    </button>
  );
};
```

**Deliverables:**
- ✅ 10+ reusable brutal UI components
- ✅ Landing page with clear value prop
- ✅ Consistent design system

---

### Week 2: Resume Upload & Parsing

#### Day 8-10: File Upload System

**Tasks:**
- [ ] Build file upload component (drag & drop)
- [ ] Setup S3/Supabase storage
- [ ] Create upload API endpoint
- [ ] Validate file types (PDF, DOCX, LaTeX)
- [ ] Show upload progress

**Code:**
```typescript
// app/api/resume/upload/route.ts
export async function POST(req: Request) {
  const formData = await req.formData();
  const file = formData.get('file') as File;
  
  // Validate file
  if (!file) {
    return NextResponse.json({ error: 'No file provided' }, { status: 400 });
  }
  
  const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
  if (!validTypes.includes(file.type)) {
    return NextResponse.json({ error: 'Invalid file type' }, { status: 400 });
  }
  
  // Upload to S3
  const buffer = Buffer.from(await file.arrayBuffer());
  const fileName = `${userId}/${Date.now()}-${file.name}`;
  
  const { data, error } = await supabase.storage
    .from('resumes')
    .upload(fileName, buffer, {
      contentType: file.type,
    });
  
  // Trigger parsing job
  await queue.add('parse-resume', {
    userId,
    filePath: data.path,
    fileType: file.type,
  });
  
  return NextResponse.json({ 
    success: true, 
    fileId: data.path 
  });
}
```

**Deliverables:**
- ✅ Working file upload with progress bar
- ✅ Files stored in cloud storage
- ✅ Database record created

---

#### Day 11-14: Resume Parsing Engine

**Tasks:**
- [ ] Install PyMuPDF, python-docx
- [ ] Build PDF text extraction
- [ ] Build section detection (regex + NLP)
- [ ] Extract contact info (email, phone, LinkedIn)
- [ ] Parse experience and education
- [ ] Extract skills

**Code:**
```python
# backend/services/resume_parser.py
import fitz  # PyMuPDF
import re
from typing import Dict, List
import spacy

nlp = spacy.load("en_core_web_sm")

class ResumeParser:
    def parse_pdf(self, file_path: str) -> Dict:
        """Extract and parse resume from PDF"""
        
        # Extract text
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        
        # Parse sections
        sections = self._identify_sections(text)
        
        # Extract entities
        contact_info = self._extract_contact_info(text)
        
        # Parse experience
        experience = self._parse_experience(sections.get('experience', ''))
        
        # Parse education
        education = self._parse_education(sections.get('education', ''))
        
        # Extract skills
        skills = self._extract_skills(sections.get('skills', ''))
        
        return {
            "contact": contact_info,
            "experience": experience,
            "education": education,
            "skills": skills,
            "raw_text": text,
        }
    
    def _identify_sections(self, text: str) -> Dict[str, str]:
        """Identify major resume sections"""
        sections = {}
        
        # Define section headers
        patterns = {
            'experience': r'(?i)(work experience|experience|employment history)',
            'education': r'(?i)(education|academic background)',
            'skills': r'(?i)(skills|technical skills|competencies)',
            'summary': r'(?i)(summary|profile|objective)',
        }
        
        # Find section boundaries
        for section_name, pattern in patterns.items():
            matches = list(re.finditer(pattern, text))
            if matches:
                start_idx = matches[0].end()
                # Find next section or end of text
                next_match = None
                for other_pattern in patterns.values():
                    if other_pattern != pattern:
                        next_matches = list(re.finditer(other_pattern, text[start_idx:]))
                        if next_matches:
                            if next_match is None or next_matches[0].start() < next_match:
                                next_match = next_matches[0].start()
                
                end_idx = start_idx + next_match if next_match else len(text)
                sections[section_name] = text[start_idx:end_idx].strip()
        
        return sections
    
    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract name, email, phone, LinkedIn"""
        contact = {}
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact['email'] = email_match.group(0)
        
        # Phone
        phone_pattern = r'\b(\+\d{1,3}[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            contact['phone'] = phone_match.group(0)
        
        # LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_match = re.search(linkedin_pattern, text)
        if linkedin_match:
            contact['linkedin'] = 'https://' + linkedin_match.group(0)
        
        # Name (assume first line or use NLP)
        doc = nlp(text[:500])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                contact['name'] = ent.text
                break
        
        return contact
    
    def _parse_experience(self, experience_text: str) -> List[Dict]:
        """Parse work experience entries"""
        experiences = []
        
        # Split by common patterns (dates, company names)
        # This is simplified - in production, use more robust parsing
        entries = re.split(r'\n\n+', experience_text)
        
        for entry in entries:
            if len(entry.strip()) < 20:
                continue
                
            exp = {
                'raw_text': entry,
                'title': self._extract_job_title(entry),
                'company': self._extract_company(entry),
                'dates': self._extract_dates(entry),
                'description': entry,
            }
            experiences.append(exp)
        
        return experiences
    
    def _extract_skills(self, skills_text: str) -> List[str]:
        """Extract skills from skills section"""
        # Common tech skills database
        known_skills = [
            'Python', 'JavaScript', 'React', 'Node.js', 'AWS',
            'Docker', 'Kubernetes', 'SQL', 'MongoDB', 'Git',
            # ... add more
        ]
        
        skills = []
        text_lower = skills_text.lower()
        
        for skill in known_skills:
            if skill.lower() in text_lower:
                skills.append(skill)
        
        # Also extract from bullet points
        bullets = re.findall(r'[•\-\*]\s*(.+)', skills_text)
        for bullet in bullets:
            cleaned = bullet.strip()
            if cleaned and len(cleaned) < 50:
                skills.append(cleaned)
        
        return list(set(skills))  # Remove duplicates
```

**API Endpoint:**
```python
# backend/api/resume.py
@router.post("/parse")
async def parse_resume(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks,
):
    # Save file temporarily
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Parse resume
    parser = ResumeParser()
    parsed_data = parser.parse_pdf(temp_path)
    
    # Save to database
    resume = Resume(
        user_id=current_user.id,
        content=parsed_data,
        filename=file.filename,
    )
    db.add(resume)
    db.commit()
    
    # Clean up
    os.remove(temp_path)
    
    return {
        "success": True,
        "resume_id": resume.id,
        "parsed_data": parsed_data,
    }
```

**Deliverables:**
- ✅ Accurate parsing of 90%+ of resumes
- ✅ Extracted contact, experience, education, skills
- ✅ Data stored in structured format

---

### Week 3: Job Description Analysis & ATS Scoring

#### Day 15-17: JD Parser

**Tasks:**
- [ ] Build JD input component (paste URL or text)
- [ ] Create JD parsing API
- [ ] Extract required skills from JD
- [ ] Identify experience level requirements
- [ ] Extract keywords for ATS matching

**Code:**
```python
# backend/services/jd_parser.py
class JobDescriptionParser:
    def parse(self, jd_text: str, jd_url: Optional[str] = None) -> Dict:
        """Parse job description and extract key information"""
        
        # Clean text
        jd_text = self._clean_text(jd_text)
        
        # Extract basic info
        job_title = self._extract_title(jd_text)
        company = self._extract_company(jd_text)
        location = self._extract_location(jd_text)
        
        # Extract requirements
        requirements = self._extract_requirements(jd_text)
        responsibilities = self._extract_responsibilities(jd_text)
        
        # Extract skills
        required_skills = self._extract_skills(requirements)
        
        # Determine experience level
        experience_level = self._determine_experience_level(jd_text)
        
        # Extract keywords for ATS
        keywords = self._extract_keywords(jd_text, top_n=50)
        
        # Generate embedding for semantic matching
        embedding = self._generate_embedding(jd_text)
        
        return {
            "title": job_title,
            "company": company,
            "location": location,
            "requirements": requirements,
            "responsibilities": responsibilities,
            "required_skills": required_skills,
            "experience_level": experience_level,
            "keywords": keywords,
            "embedding": embedding,
            "raw_text": jd_text,
            "url": jd_url,
        }
    
    def _extract_keywords(self, text: str, top_n: int = 50) -> List[str]:
        """Extract most important keywords using TF-IDF"""
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            max_features=top_n,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Fit and transform
        tfidf_matrix = vectorizer.fit_transform([text])
        feature_names = vectorizer.get_feature_names_out()
        
        # Get scores
        scores = tfidf_matrix.toarray()[0]
        
        # Sort by score
        keyword_scores = list(zip(feature_names, scores))
        keyword_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [kw for kw, score in keyword_scores[:top_n]]
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from requirements"""
        skill_database = load_skill_database()  # Load from file/DB
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in skill_database:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def _determine_experience_level(self, text: str) -> str:
        """Determine required experience level"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['senior', '5+ years', '7+ years', 'lead']):
            return 'senior'
        elif any(word in text_lower for word in ['mid-level', '3+ years', '2-4 years']):
            return 'mid'
        elif any(word in text_lower for word in ['entry', 'junior', '0-2 years', 'recent graduate']):
            return 'entry'
        else:
            return 'mid'  # default
```

**Deliverables:**
- ✅ JD parsing with 85%+ accuracy
- ✅ Extracted skills, keywords, requirements
- ✅ Experience level detection

---

#### Day 18-21: ATS Scoring Algorithm

**Tasks:**
- [ ] Build ATS scoring engine
- [ ] Implement keyword matching algorithm
- [ ] Score format quality (sections, bullet points)
- [ ] Calculate skills alignment
- [ ] Generate improvement suggestions

**Code:**
```python
# backend/services/ats_scorer.py
class ATSScorer:
    def calculate_score(
        self, 
        resume: Dict, 
        job_description: Dict
    ) -> Dict:
        """Calculate comprehensive ATS score"""
        
        scores = {
            'keyword_match': self._score_keyword_match(resume, job_description),
            'format_quality': self._score_format(resume),
            'section_completeness': self._score_sections(resume),
            'skills_alignment': self._score_skills(resume, job_description),
            'experience_relevance': self._score_experience(resume, job_description),
        }
        
        # Weighted total
        weights = {
            'keyword_match': 0.40,
            'format_quality': 0.20,
            'section_completeness': 0.15,
            'skills_alignment': 0.15,
            'experience_relevance': 0.10,
        }
        
        total_score = sum(
            scores[key] * weights[key] 
            for key in scores.keys()
        )
        
        # Generate suggestions
        suggestions = self._generate_suggestions(scores, resume, job_description)
        
        return {
            'total_score': round(total_score, 1),
            'breakdown': scores,
            'suggestions': suggestions,
            'weights': weights,
        }
    
    def _score_keyword_match(self, resume: Dict, jd: Dict) -> float:
        """Score based on keyword overlap"""
        resume_text = resume.get('raw_text', '').lower()
        jd_keywords = jd.get('keywords', [])
        
        if not jd_keywords:
            return 50.0  # neutral score if no keywords
        
        # Count matches
        matches = sum(1 for kw in jd_keywords if kw.lower() in resume_text)
        match_percentage = (matches / len(jd_keywords)) * 100
        
        return min(match_percentage, 100.0)
    
    def _score_format(self, resume: Dict) -> float:
        """Score resume format quality"""
        score = 100.0
        
        # Check for required sections
        required_sections = ['contact', 'experience', 'education']
        missing_sections = [s for s in required_sections if not resume.get(s)]
        score -= len(missing_sections) * 20
        
        # Check contact completeness
        contact = resume.get('contact', {})
        if not contact.get('email'):
            score -= 10
        if not contact.get('phone'):
            score -= 5
        
        # Check experience formatting
        experiences = resume.get('experience', [])
        if experiences:
            for exp in experiences:
                if not exp.get('title'):
                    score -= 5
                if not exp.get('company'):
                    score -= 5
        
        return max(score, 0.0)
    
    def _score_skills(self, resume: Dict, jd: Dict) -> float:
        """Score skills alignment"""
        resume_skills = set(s.lower() for s in resume.get('skills', []))
        required_skills = set(s.lower() for s in jd.get('required_skills', []))
        
        if not required_skills:
            return 50.0
        
        # Calculate overlap
        matching_skills = resume_skills.intersection(required_skills)
        match_percentage = (len(matching_skills) / len(required_skills)) * 100
        
        return min(match_percentage, 100.0)
    
    def _generate_suggestions(
        self, 
        scores: Dict, 
        resume: Dict, 
        jd: Dict
    ) -> List[str]:
        """Generate actionable improvement suggestions"""
        suggestions = []
        
        # Keyword suggestions
        if scores['keyword_match'] < 70:
            missing_keywords = self._find_missing_keywords(resume, jd)
            suggestions.append(
                f"Add these keywords to your resume: {', '.join(missing_keywords[:5])}"
            )
        
        # Format suggestions
        if scores['format_quality'] < 80:
            if not resume.get('contact', {}).get('email'):
                suggestions.append("Add your email address")
            if not resume.get('experience'):
                suggestions.append("Add work experience section")
        
        # Skills suggestions
        if scores['skills_alignment'] < 70:
            missing_skills = self._find_missing_skills(resume, jd)
            suggestions.append(
                f"Highlight these skills: {', '.join(missing_skills[:3])}"
            )
        
        return suggestions
```

**API Endpoint:**
```python
@router.post("/ats-score")
async def calculate_ats_score(
    resume_id: str,
    jd_id: str,
    current_user: User = Depends(get_current_user)
):
    # Fetch resume and JD from database
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    
    # Calculate score
    scorer = ATSScorer()
    score_data = scorer.calculate_score(resume.content, jd.parsed_data)
    
    # Cache result
    await redis.setex(
        f"ats_score:{resume_id}:{jd_id}",
        3600,  # 1 hour TTL
        json.dumps(score_data)
    )
    
    return score_data
```

**Deliverables:**
- ✅ Working ATS scorer with 0-100 scale
- ✅ Detailed breakdown by category
- ✅ Actionable improvement suggestions

---

### Week 4: LaTeX Resume Generation

#### Day 22-25: LaTeX Template Engine

**Tasks:**
- [ ] Create 3-5 LaTeX templates (modern, classic, minimal)
- [ ] Build template renderer with Jinja2
- [ ] Implement variable replacement (name, experience, skills)
- [ ] Add LaTeX → PDF compilation
- [ ] Create preview system

**Code:**
```python
# backend/services/latex_generator.py
from jinja2 import Template
import subprocess
import tempfile
import os

class LaTeXGenerator:
    def __init__(self):
        self.templates = {
            'modern': self._load_template('modern.tex'),
            'classic': self._load_template('classic.tex'),
            'minimal': self._load_template('minimal.tex'),
        }
    
    def generate_resume(
        self, 
        resume_data: Dict, 
        template_name: str = 'modern'
    ) -> str:
        """Generate LaTeX resume from data"""
        
        # Get template
        template = self.templates.get(template_name)
        if not template:
            raise ValueError(f"Template {template_name} not found")
        
        # Prepare data for template
        context = self._prepare_context(resume_data)
        
        # Render template
        latex_content = template.render(**context)
        
        return latex_content
    
    def compile_to_pdf(self, latex_content: str) -> bytes:
        """Compile LaTeX to PDF"""
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            # Write LaTeX file
            tex_path = os.path.join(tmpdir, 'resume.tex')
            with open(tex_path, 'w') as f:
                f.write(latex_content)
            
            # Compile with pdflatex
            try:
                subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', 'resume.tex'],
                    cwd=tmpdir,
                    check=True,
                    capture_output=True
                )
                
                # Read PDF
                pdf_path = os.path.join(tmpdir, 'resume.pdf')
                with open(pdf_path, 'rb') as f:
                    pdf_content = f.read()
                
                return pdf_content
                
            except subprocess.CalledProcessError as e:
                raise Exception(f"LaTeX compilation failed: {e.stderr.decode()}")
    
    def _prepare_context(self, resume_data: Dict) -> Dict:
        """Prepare data for LaTeX template"""
        
        # Format experience section
        experience_items = []
        for exp in resume_data.get('experience', []):
            experience_items.append({
                'title': self._escape_latex(exp.get('title', '')),
                'company': self._escape_latex(exp.get('company', '')),
                'dates': self._escape_latex(exp.get('dates', '')),
                'description': self._format_bullets(exp.get('description', '')),
            })
        
        # Format education
        education_items = []
        for edu in resume_data.get('education', []):
            education_items.append({
                'degree': self._escape_latex(edu.get('degree', '')),
                'school': self._escape_latex(edu.get('school', '')),
                'dates': self._escape_latex(edu.get('dates', '')),
            })
        
        # Format skills
        skills = [self._escape_latex(s) for s in resume_data.get('skills', [])]
        
        return {
            'name': self._escape_latex(resume_data['contact'].get('name', '')),
            'email': resume_data['contact'].get('email', ''),
            'phone': resume_data['contact'].get('phone', ''),
            'linkedin': resume_data['contact'].get('linkedin', ''),
            'experience': experience_items,
            'education': education_items,
            'skills': skills,
        }
    
    def _escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters"""
        replacements = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\^{}',
            '\\': r'\textbackslash{}',
        }
        
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        return text
    
    def _format_bullets(self, text: str) -> List[str]:
        """Convert text to bullet points for LaTeX"""
        # Split by newlines or bullet points
        bullets = re.split(r'\n+|[•\-\*]\s+', text)
        bullets = [b.strip() for b in bullets if b.strip()]
        return [self._escape_latex(b) for b in bullets]
```

**LaTeX Template Example:**
```latex
% modern.tex
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\geometry{margin=0.75in}
\usepackage{enumitem}
\usepackage{hyperref}

\begin{document}

% Header
\begin{center}
    {\Huge \textbf{{ name }}}\\
    \vspace{0.2cm}
    {{ email }} | {{ phone }} | \href{{ linkedin }}{{ linkedin }}
\end{center}

% Experience
\section*{Experience}
{% for exp in experience %}
    \textbf{{ exp.title }} \hfill {{ exp.dates }}\\
    \textit{{ exp.company }}
    \begin{itemize}[leftmargin=*]
    {% for bullet in exp.description %}
        \item {{ bullet }}
    {% endfor %}
    \end{itemize}
{% endfor %}

% Education
\section*{Education}
{% for edu in education %}
    \textbf{{ edu.degree }} \hfill {{ edu.dates }}\\
    {{ edu.school }}
{% endfor %}

% Skills
\section*{Skills}
{{ skills|join(', ') }}

\end{document}
```

**Deliverables:**
- ✅ 3 LaTeX templates functional
- ✅ LaTeX → PDF compilation working
- ✅ Generated resumes look professional
- ✅ Preview system shows real-time changes

---

#### Day 26-28: Resume Optimization Engine

**Tasks:**
- [ ] Build AI-powered resume rewriter
- [ ] Integrate OpenAI/Anthropic API
- [ ] Implement JD-to-resume matching
- [ ] Create bullet point optimizer
- [ ] Add skill highlighting system

**Code:**
```python
# backend/services/resume_optimizer.py
from anthropic import Anthropic

class ResumeOptimizer:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    async def optimize_for_jd(
        self, 
        resume: Dict, 
        job_description: Dict
    ) -> Dict:
        """Optimize resume content for specific job description"""
        
        # Extract key info
        jd_keywords = job_description.get('keywords', [])
        required_skills = job_description.get('required_skills', [])
        jd_text = job_description.get('raw_text', '')
        
        # Optimize each section
        optimized_resume = resume.copy()
        
        # Optimize experience bullets
        optimized_experience = []
        for exp in resume.get('experience', []):
            optimized_bullets = await self._optimize_bullets(
                exp.get('description', ''),
                jd_keywords,
                required_skills
            )
            optimized_experience.append({
                **exp,
                'description': optimized_bullets,
                'original_description': exp.get('description'),
            })
        
        optimized_resume['experience'] = optimized_experience
        
        # Optimize skills section
        optimized_resume['skills'] = self._optimize_skills(
            resume.get('skills', []),
            required_skills
        )
        
        # Generate optimized summary
        optimized_resume['summary'] = await self._generate_summary(
            resume,
            job_description
        )
        
        return optimized_resume
    
    async def _optimize_bullets(
        self, 
        original_bullets: str, 
        keywords: List[str],
        skills: List[str]
    ) -> List[str]:
        """Optimize bullet points using AI"""
        
        prompt = f"""
        Rewrite these resume bullet points to include relevant keywords and skills 
        while maintaining truthfulness and impact.
        
        Original bullets:
        {original_bullets}
        
        Target keywords: {', '.join(keywords[:10])}
        Target skills: {', '.join(skills[:5])}
        
        Requirements:
        - Keep the same meaning and achievements
        - Naturally incorporate 3-5 keywords
        - Start with strong action verbs
        - Quantify results where possible
        - Keep each bullet under 150 characters
        - Return as a JSON array of strings
        
        Return only the JSON array, no explanation.
        """
        
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse response
        optimized_bullets = json.loads(response.content[0].text)
        return optimized_bullets
    
    def _optimize_skills(
        self, 
        current_skills: List[str], 
        required_skills: List[str]
    ) -> List[str]:
        """Reorder and highlight relevant skills"""
        
        # Prioritize required skills
        prioritized = []
        
        # Add matching required skills first
        for skill in required_skills:
            for current_skill in current_skills:
                if skill.lower() in current_skill.lower():
                    if current_skill not in prioritized:
                        prioritized.append(current_skill)
        
        # Add remaining skills
        for skill in current_skills:
            if skill not in prioritized:
                prioritized.append(skill)
        
        return prioritized
    
    async def _generate_summary(
        self, 
        resume: Dict, 
        job_description: Dict
    ) -> str:
        """Generate tailored professional summary"""
        
        prompt = f"""
        Write a compelling 2-3 sentence professional summary for this candidate 
        applying to: {job_description.get('title', 'this position')}
        
        Candidate background:
        - Skills: {', '.join(resume.get('skills', [])[:10])}
        - Experience highlights: {resume.get('experience', [{}])[0].get('title', 'N/A')} 
        
        Job requirements:
        {job_description.get('requirements', '')[:500]}
        
        Make it impactful, specific, and keyword-rich. No fluff.
        """
        
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text.strip()
```

**API Endpoint:**
```python
@router.post("/optimize")
async def optimize_resume(
    resume_id: str,
    jd_id: str,
    current_user: User = Depends(get_current_user)
):
    # Fetch data
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    
    # Optimize
    optimizer = ResumeOptimizer()
    optimized = await optimizer.optimize_for_jd(
        resume.content, 
        jd.parsed_data
    )
    
    # Save optimized version
    new_resume = Resume(
        user_id=current_user.id,
        title=f"{resume.title} - Optimized for {jd.company}",
        content=optimized,
        parent_resume_id=resume_id,
    )
    db.add(new_resume)
    db.commit()
    
    return {
        "success": True,
        "optimized_resume_id": new_resume.id,
        "changes": calculate_diff(resume.content, optimized),
    }
```

**Deliverables:**
- ✅ AI-powered resume optimization
- ✅ JD-specific keyword injection
- ✅ Before/after comparison view
- ✅ Track which changes improve ATS score

---

## 🚀 Phase 2: Core Features (Weeks 5-8)

### Week 5: Chrome Extension

#### Day 29-31: Extension Setup & Job Board Integration

**Tasks:**
- [ ] Create Manifest V3 extension structure
- [ ] Build popup UI (neo-brutal design)
- [ ] Implement content scripts for job boards
- [ ] Add LinkedIn job extraction
- [ ] Add Indeed job extraction

**Code:**
```json
// manifest.json
{
  "manifest_version": 3,
  "name": "JobHack - Auto-Apply Assistant",
  "version": "1.0.0",
  "description": "Auto-apply to jobs with optimized resumes",
  "permissions": [
    "storage",
    "tabs",
    "activeTab"
  ],
  "host_permissions": [
    "https://www.linkedin.com/*",
    "https://www.indeed.com/*",
    "https://jobhack.io/*"
  ],
  "action": {
    "default_popup": "popup.html",
    "default_icon": "icon.png"
  },
  "content_scripts": [
    {
      "matches": ["https://www.linkedin.com/jobs/*"],
      "js": ["linkedin-scraper.js"]
    },
    {
      "matches": ["https://www.indeed.com/viewjob*"],
      "js": ["indeed-scraper.js"]
    }
  ],
  "background": {
    "service_worker": "background.js"
  }
}
```

```typescript
// linkedin-scraper.ts
class LinkedInJobScraper {
  extractJobData(): JobData {
    // Extract from LinkedIn's job posting page
    const title = document.querySelector('.job-details-jobs-unified-top-card__job-title')?.textContent;
    const company = document.querySelector('.job-details-jobs-unified-top-card__company-name')?.textContent;
    const location = document.querySelector('.job-details-jobs-unified-top-card__bullet')?.textContent;
    const description = document.querySelector('.jobs-description__content')?.textContent;
    
    return {
      title: title?.trim() || '',
      company: company?.trim() || '',
      location: location?.trim() || '',
      description: description?.trim() || '',
      url: window.location.href,
      source: 'linkedin',
      extractedAt: new Date().toISOString(),
    };
  }
  
  injectApplyButton() {
    // Find LinkedIn's apply button
    const applySection = document.querySelector('.jobs-apply-button--top-card');
    
    if (!applySection) return;
    
    // Create JobHack button
    const jobhackBtn = document.createElement('button');
    jobhackBtn.className = 'jobhack-apply-btn';
    jobhackBtn.textContent = '⚡ JOBHACK APPLY';
    jobhackBtn.style.cssText = `
      background: #F4FF61;
      border: 4px solid black;
      padding: 12px 24px;
      font-weight: 900;
      text-transform: uppercase;
      cursor: pointer;
      box-shadow: 4px 4px 0px 0px rgba(0,0,0,1);
      margin-left: 12px;
    `;
    
    jobhackBtn.addEventListener('click', () => this.handleJobHackApply());
    
    applySection.appendChild(jobhackBtn);
  }
  
  async handleJobHackApply() {
    // Extract job data
    const jobData = this.extractJobData();
    
    // Send to backend
    const response = await fetch('https://api.jobhack.io/api/extension/apply', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${await this.getAuthToken()}`,
      },
      body: JSON.stringify(jobData),
    });
    
    if (response.ok) {
      this.showSuccessNotification();
    }
  }
}

// Initialize when page loads
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    const scraper = new LinkedInJobScraper();
    scraper.injectApplyButton();
  });
} else {
  const scraper = new LinkedInJobScraper();
  scraper.injectApplyButton();
}
```

**Deliverables:**
- ✅ Working Chrome extension
- ✅ Extract jobs from LinkedIn & Indeed
- ✅ One-click apply button injection
- ✅ Communication with backend API

---

#### Day 32-35: Auto-Fill & Application Submission

**Tasks:**
- [ ] Build form detection system
- [ ] Implement field mapping (resume → form)
- [ ] Add auto-fill functionality
- [ ] Handle file uploads (resume PDF)
- [ ] Add submission verification

**Code:**
```typescript
// auto-filler.ts
class ApplicationAutoFiller {
  private formMapping = {
    firstName: ['first_name', 'firstname', 'fname', 'given_name'],
    lastName: ['last_name', 'lastname', 'lname', 'surname'],
    email: ['email', 'email_address', 'e-mail'],
    phone: ['phone', 'phone_number', 'mobile', 'telephone'],
    linkedin: ['linkedin', 'linkedin_url', 'linkedin_profile'],
  };
  
  async fillApplication(resumeData: ResumeData) {
    // Find all form fields
    const forms = document.querySelectorAll('form');
    
    for (const form of forms) {
      await this.fillForm(form, resumeData);
    }
  }
  
  async fillForm(form: HTMLFormElement, data: ResumeData) {
    const inputs = form.querySelectorAll('input, textarea, select');
    
    for (const input of inputs) {
      const element = input as HTMLInputElement;
      const fieldName = this.identifyField(element);
      
      if (fieldName && data[fieldName]) {
        await this.fillField(element, data[fieldName]);
      }
    }
    
    // Handle file uploads
    await this.uploadResume(form, data.resumePdfUrl);
  }
  
  identifyField(element: HTMLInputElement): string | null {
    // Check name, id, placeholder, label
    const indicators = [
      element.name,
      element.id,
      element.placeholder,
      element.getAttribute('aria-label'),
    ].map(s => s?.toLowerCase().replace(/[_\s-]/g, ''));
    
    // Match against known patterns
    for (const [field, patterns] of Object.entries(this.formMapping)) {
      for (const pattern of patterns) {
        if (indicators.some(ind => ind?.includes(pattern))) {
          return field;
        }
      }
    }
    
    return null;
  }
  
  async fillField(element: HTMLInputElement, value: string) {
    // Simulate human typing
    element.focus();
    
    // Set value
    element.value = value;
    
    // Trigger events that frameworks expect
    element.dispatchEvent(new Event('input', { bubbles: true }));
    element.dispatchEvent(new Event('change', { bubbles: true }));
    
    // Small delay to appear human
    await this.sleep(100 + Math.random() * 200);
  }
  
  async uploadResume(form: HTMLFormElement, pdfUrl: string) {
    const fileInputs = form.querySelectorAll('input[type="file"]');
    
    for (const input of fileInputs) {
      const fileInput = input as HTMLInputElement;
      
      // Check if it's for resume
      const label = this.getFieldLabel(fileInput);
      if (!label?.toLowerCase().includes('resume')) continue;
      
      // Download PDF and create File object
      const blob = await fetch(pdfUrl).then(r => r.blob());
      const file = new File([blob], 'resume.pdf', { type: 'application/pdf' });
      
      // Create DataTransfer to set files
      const dataTransfer = new DataTransfer();
      dataTransfer.items.add(file);
      fileInput.files = dataTransfer.files;
      
      // Trigger change event
      fileInput.dispatchEvent(new Event('change', { bubbles: true }));
    }
  }
  
  sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

**Deliverables:**
- ✅ Auto-fill 80%+ of common form fields
- ✅ Resume PDF auto-upload
- ✅ Human-like typing simulation
- ✅ Success/failure tracking

---

### Week 6: LinkedIn Integration & Org Graphing

#### Day 36-38: LinkedIn OAuth & Profile Scraping

**Tasks:**
- [ ] Setup LinkedIn OAuth app
- [ ] Implement OAuth flow
- [ ] Build profile import functionality
- [ ] Extract work history from LinkedIn
- [ ] Import skills and endorsements

**Code:**
```typescript
// pages/api/auth/linkedin/callback.ts
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const code = searchParams.get('code');
  
  if (!code) {
    return NextResponse.json({ error: 'No code provided' }, { status: 400 });
  }
  
  // Exchange code for access token
  const tokenResponse = await fetch('https://www.linkedin.com/oauth/v2/accessToken', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      client_id: process.env.LINKEDIN_CLIENT_ID!,
      client_secret: process.env.LINKEDIN_CLIENT_SECRET!,
      redirect_uri: `${process.env.NEXT_PUBLIC_URL}/api/auth/linkedin/callback`,
    }),
  });
  
  const { access_token } = await tokenResponse.json();
  
  // Fetch profile data
  const profileResponse = await fetch('https://api.linkedin.com/v2/me', {
    headers: { 'Authorization': `Bearer ${access_token}` },
  });
  
  const profile = await profileResponse.json();
  
  // Store in database
  await saveLinkedInProfile(profile, access_token);
  
  return NextResponse.redirect('/dashboard');
}
```

```python
# backend/services/linkedin_scraper.py
class LinkedInProfileScraper:
    async def scrape_profile(self, profile_url: str) -> Dict:
        """Scrape LinkedIn profile (fallback when API unavailable)"""
        
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Login with session cookie
        await page.context.add_cookies(self.get_session_cookies())
        
        # Navigate to profile
        await page.goto(profile_url)
        await page.wait_for_selector('.pv-top-card')
        
        # Extract data
        data = await page.evaluate("""
        () => {
          return {
            name: document.querySelector('.pv-top-card--list li')?.textContent,
            headline: document.querySelector('.pv-top-card-section__headline')?.textContent,
            location: document.querySelector('.pv-top-card--list.pv-top-card--list-bullet li')?.textContent,
            experience: Array.from(document.querySelectorAll('.pv-entity__position-group-pager')).map(exp => ({
              title: exp.querySelector('.t-16')?.textContent,
              company: exp.querySelector('.t-14')?.textContent,
              dates: exp.querySelector('.t-14.t-black--light span:nth-child(2)')?.textContent,
            })),
            skills: Array.from(document.querySelectorAll('.pv-skill-category-entity__name')).map(s => s.textContent),
          };
        }
        """)
        
        await browser.close()
        return data
```

**Deliverables:**
- ✅ LinkedIn OAuth login
- ✅ Import profile to resume
- ✅ Extract full work history
- ✅ Scraping fallback when API limited

---

#### Day 39-42: Organization Graph Builder

**Tasks:**
- [ ] Build company employee scraper
- [ ] Create org chart visualization
- [ ] Identify hiring managers by department
- [ ] Score decision-maker relevance
- [ ] Build visual org graph UI

**Code:**
```python
# backend/services/org_graph_builder.py
class OrgGraphBuilder:
    async def build_company_graph(
        self, 
        company_name: str,
        target_department: str = None
    ) -> OrgGraph:
        """Build organizational graph for a company"""
        
        # 1. Find company LinkedIn page
        company_url = await self.find_company_page(company_name)
        
        # 2. Scrape employee list
        employees = await self.scrape_employees(company_url, limit=500)
        
        # 3. Filter by relevant departments
        if target_department:
            employees = self.filter_by_department(employees, target_department)
        
        # 4. Identify decision makers
        decision_makers = self.identify_decision_makers(employees)
        
        # 5. Build hierarchy
        org_graph = self.build_hierarchy(employees)
        
        # 6. Calculate relevance scores
        for person in org_graph.nodes:
            person.relevance_score = self.calculate_relevance(person, target_department)
        
        return org_graph
    
    async def scrape_employees(
        self, 
        company_url: str, 
        limit: int = 500
    ) -> List[Employee]:
        """Scrape employees from company LinkedIn page"""
        
        employees = []
        page = 1
        
        while len(employees) < limit:
            url = f"{company_url}/people/?page={page}"
            
            # Scrape page
            page_employees = await self.scrape_employee_page(url)
            employees.extend(page_employees)
            
            if not page_employees:
                break  # No more pages
            
            page += 1
            await asyncio.sleep(2)  # Rate limiting
        
        return employees[:limit]
    
    def identify_decision_makers(self, employees: List[Employee]) -> List[Employee]:
        """Identify likely decision makers"""
        
        decision_keywords = [
            'director', 'vp', 'vice president', 'head of', 
            'chief', 'ceo', 'cto', 'manager', 'lead', 'principal'
        ]
        
        decision_makers = []
        
        for emp in employees:
            title_lower = emp.title.lower()
            if any(keyword in title_lower for keyword in decision_keywords):
                emp.is_decision_maker = True
                decision_makers.append(emp)
        
        return decision_makers
    
    def calculate_relevance(
        self, 
        person: Employee, 
        target_role: str
    ) -> float:
        """Calculate how relevant this person is for outreach"""
        
        score = 0.0
        
        # Title relevance
        if target_role.lower() in person.title.lower():
            score += 40
        
        # Seniority
        seniority_keywords = {
            'director': 30,
            'vp': 35,
            'head': 30,
            'chief': 40,
            'manager': 25,
            'lead': 20,
        }
        
        for keyword, points in seniority_keywords.items():
            if keyword in person.title.lower():
                score += points
                break
        
        # Department match
        if person.department and target_role:
            dept_match = self.calculate_dept_similarity(person.department, target_role)
            score += dept_match * 30
        
        return min(score, 100.0)
```

**Frontend - Org Graph Visualization:**
```typescript
// components/OrgGraphVisualization.tsx
import React from 'react';
import ReactFlow, { Node, Edge } from 'reactflow';

export const OrgGraphVisualization: React.FC<{ orgData: OrgGraph }> = ({ orgData }) => {
  const nodes: Node[] = orgData.employees.map((emp, idx) => ({
    id: emp.id,
    data: {
      label: (
        <div className="border-2 border-black bg-white p-3">
          <div className="font-black text-sm">{emp.name}</div>
          <div className="text-xs">{emp.title}</div>
          <div className="text-xs text-gray-600">{emp.department}</div>
          {emp.relevance_score > 70 && (
            <div className="mt-1 bg-neon-green px-2 py-1 text-xs font-black">
              TARGET ({emp.relevance_score})
            </div>
          )}
        </div>
      ),
    },
    position: { x: idx * 200, y: emp.level * 150 },
    className: emp.is_decision_maker ? 'border-4 border-neon-yellow' : '',
  }));
  
  const edges: Edge[] = orgData.relationships.map(rel => ({
    id: `${rel.from}-${rel.to}`,
    source: rel.from,
    target: rel.to,
    animated: rel.type === 'reports_to',
  }));
  
  return (
    <div className="h-screen w-full border-4 border-black">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
      />
    </div>
  );
};
```

**Deliverables:**
- ✅ Scrape 200+ employees per company
- ✅ Identify top 10 decision makers
- ✅ Visual org chart with relevance scores
- ✅ Export decision-maker contact list

---

### Week 7: Outreach Automation

#### Day 43-45: Email Generation & Sending

**Tasks:**
- [ ] Build AI message generator
- [ ] Create email templates (cold, follow-up, thank you)
- [ ] Integrate SendGrid/Resend
- [ ] Add email tracking (opens, clicks)
- [ ] Implement sending queue

**Code:**
```typescript
// backend/services/outreach_generator.ts
class OutreachGenerator {
  async generateColdEmail(
    recipient: Employee,
    resume: Resume,
    jobDescription: JobDescription
  ): Promise<EmailMessage> {
    const prompt = `
    Generate a cold email to ${recipient.name} (${recipient.title} at ${recipient.company}).
    
    Context:
    - Job applying for: ${jobDescription.title}
    - My background: ${this.summarizeResume(resume)}
    - Recipient's background: ${recipient.title}, ${recipient.department}
    
    Requirements:
    - Subject line: Under 60 characters, intriguing
    - Body: 100-150 words max
    - Reference something specific from their profile/company
    - Clear call-to-action (15-min chat)
    - Professional but authentic tone
    - NO generic phrases like "I hope this email finds you well"
    
    Format as JSON: { "subject": "...", "body": "..." }
    `;
    
    const response = await this.llm.generate(prompt);
    const { subject, body } = JSON.parse(response);
    
    // Add tracking pixel
    const trackingPixel = `<img src="https://api.jobhack.io/track/${messageId}" width="1" height="1" />`;
    const bodyWithTracking = body + trackingPixel;
    
    return {
      to: recipient.email,
      subject,
      body: bodyWithTracking,
      attachments: [
        {
          filename: 'resume.pdf',
          path: resume.pdfUrl,
        },
      ],
    };
  }
}
```

```python
# backend/services/email_sender.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class EmailSender:
    def __init__(self):
        self.client = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
    
    async def send_email(self, message: EmailMessage) -> str:
        """Send email via SendGrid"""
        
        mail = Mail(
            from_email=('noreply@jobhack.io', 'JobHack'),
            to_emails=message.to,
            subject=message.subject,
            html_content=message.body
        )
        
        # Add attachments
        for attachment in message.attachments:
            with open(attachment.path, 'rb') as f:
                data = f.read()
                encoded = base64.b64encode(data).decode()
                
                mail.add_attachment(
                    FileContent(encoded),
                    FileName(attachment.filename),
                    FileType('application/pdf'),
                    Disposition('attachment')
                )
        
        # Send
        response = self.client.send(mail)
        
        # Store in database
        await self.store_outreach_record(message, response.headers.get('X-Message-Id'))
        
        return response.headers.get('X-Message-Id')
```

**Deliverables:**
- ✅ AI-generated personalized emails
- ✅ Email sending with attachments
- ✅ Open/click tracking
- ✅ Queue system for bulk sending

---

#### Day 46-49: LinkedIn DM Automation

**Tasks:**
- [ ] Implement LinkedIn messaging API
- [ ] Build DM template generator
- [ ] Add connection request handling
- [ ] Create sending scheduler (avoid spam flags)
- [ ] Track DM engagement

**Code:**
```typescript
// backend/services/linkedin_messenger.ts
class LinkedInMessenger {
  async sendMessage(
    recipientId: string,
    message: string,
    sendAfter: Date = new Date()
  ): Promise<void> {
    // Check if connected
    const isConnected = await this.checkConnection(recipientId);
    
    if (!isConnected) {
      // Send connection request first
      await this.sendConnectionRequest(recipientId, message);
      return;
    }
    
    // Schedule message
    await this.scheduleMessage(recipientId, message, sendAfter);
  }
  
  async sendConnectionRequest(
    recipientId: string,
    note: string
  ): Promise<void> {
    const response = await fetch(
      'https://api.linkedin.com/v2/invitations',
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          invitee: {
            'com.linkedin.voyager.growth.invitation.InviteeProfile': {
              profileId: recipientId,
            },
          },
          message: note.substring(0, 300), // LinkedIn limit
        }),
      }
    );
    
    if (!response.ok) {
      throw new Error('Failed to send connection request');
    }
  }
  
  async scheduleMessage(
    recipientId: string,
    message: string,
    sendAfter: Date
  ): Promise<void> {
    // Add to queue with delay
    await queue.add(
      'send-linkedin-dm',
      {
        recipientId,
        message,
        userId: this.userId,
      },
      {
        delay: sendAfter.getTime() - Date.now(),
      }
    );
  }
}
```

**Rate Limiting Strategy:**
```typescript
class LinkedInRateLimiter {
  private limits = {
    connectionsPerDay: 50,
    messagesPerDay: 100,
    messagesPerHour: 20,
  };
  
  async canSendMessage(userId: string): Promise<boolean> {
    const today = new Date().toISOString().split('T')[0];
    const thisHour = new Date().toISOString().substring(0, 13);
    
    // Increment daily counter
    await redis.incr(`linkedin:messages:${userId}:${today}`);
    await redis.expire(`linkedin:messages:${userId}:${today}`, 86400);
    
    // Increment hourly counter
    await redis.incr(`linkedin:messages:${userId}:${thisHour}`);
    await redis.expire(`linkedin:messages:${userId}:${thisHour}`, 3600);
  }
}
```

**Deliverables:**
- ✅ LinkedIn DM automation
- ✅ Connection request with custom note
- ✅ Rate limiting (50 connections/day, 100 DMs/day)
- ✅ Scheduled sending to appear human

---

### Week 8: Application Tracking Dashboard

#### Day 50-52: Dashboard UI

**Tasks:**
- [ ] Design dashboard layout (neo-brutal)
- [ ] Build application status cards
- [ ] Create kanban board view
- [ ] Add filtering and sorting
- [ ] Implement search functionality

**Code:**
```typescript
// app/dashboard/page.tsx
export default function DashboardPage() {
  const { data: applications } = useQuery({
    queryKey: ['applications'],
    queryFn: fetchApplications,
  });
  
  const stats = {
    total: applications?.length || 0,
    pending: applications?.filter(a => a.status === 'pending').length || 0,
    interviewing: applications?.filter(a => a.status === 'interviewing').length || 0,
    rejected: applications?.filter(a => a.status === 'rejected').length || 0,
    offers: applications?.filter(a => a.status === 'offer').length || 0,
  };
  
  return (
    <div className="min-h-screen bg-white p-8">
      {/* Stats Bar */}
      <div className="mb-8 grid grid-cols-5 gap-4">
        <StatCard label="Total Applied" value={stats.total} color="black" />
        <StatCard label="Pending" value={stats.pending} color="yellow" />
        <StatCard label="Interviewing" value={stats.interviewing} color="green" />
        <StatCard label="Rejected" value={stats.rejected} color="red" />
        <StatCard label="Offers" value={stats.offers} color="green" />
      </div>
      
      {/* Brutal Header */}
      <div className="mb-8 border-4 border-black bg-neon-yellow p-6 shadow-brutal">
        <h1 className="text-4xl font-black uppercase">Your Applications</h1>
        <p className="mt-2 text-lg">Brutally tracking every application. No excuses.</p>
      </div>
      
      {/* Kanban Board */}
      <ApplicationKanban applications={applications} />
    </div>
  );
}

const StatCard: React.FC<{ label: string; value: number; color: string }> = ({ 
  label, 
  value, 
  color 
}) => {
  const bgColor = {
    black: 'bg-black text-white',
    yellow: 'bg-neon-yellow text-black',
    green: 'bg-neon-green text-black',
    red: 'bg-red-500 text-white',
  }[color];
  
  return (
    <div className={`border-4 border-black p-6 shadow-brutal ${bgColor}`}>
      <div className="text-5xl font-black">{value}</div>
      <div className="mt-2 text-sm font-bold uppercase">{label}</div>
    </div>
  );
};
```

**Kanban Board Component:**
```typescript
// components/ApplicationKanban.tsx
const columns = [
  { id: 'pending', title: 'PENDING', color: 'bg-gray-100' },
  { id: 'submitted', title: 'SUBMITTED', color: 'bg-blue-100' },
  { id: 'interviewing', title: 'INTERVIEWING', color: 'bg-green-100' },
  { id: 'rejected', title: 'REJECTED', color: 'bg-red-100' },
  { id: 'offer', title: 'OFFER', color: 'bg-neon-green' },
];

export const ApplicationKanban: React.FC<{ applications: Application[] }> = ({ 
  applications 
}) => {
  const [localApps, setLocalApps] = useState(applications);
  
  const handleDragEnd = async (result: DropResult) => {
    if (!result.destination) return;
    
    const app = localApps.find(a => a.id === result.draggableId);
    if (!app) return;
    
    // Update status
    const newStatus = result.destination.droppableId;
    await updateApplicationStatus(app.id, newStatus);
    
    // Update local state
    setLocalApps(prev => 
      prev.map(a => 
        a.id === app.id ? { ...a, status: newStatus } : a
      )
    );
  };
  
  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <div className="grid grid-cols-5 gap-4">
        {columns.map(column => (
          <Droppable droppableId={column.id} key={column.id}>
            {(provided) => (
              <div
                ref={provided.innerRef}
                {...provided.droppableProps}
                className="min-h-screen"
              >
                <div className={`mb-4 border-4 border-black p-4 ${column.color}`}>
                  <h3 className="text-xl font-black">{column.title}</h3>
                  <span className="text-sm">
                    {localApps.filter(a => a.status === column.id).length}
                  </span>
                </div>
                
                {localApps
                  .filter(app => app.status === column.id)
                  .map((app, index) => (
                    <Draggable key={app.id} draggableId={app.id} index={index}>
                      {(provided) => (
                        <div
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                        >
                          <ApplicationCard application={app} />
                        </div>
                      )}
                    </Draggable>
                  ))}
                
                {provided.placeholder}
              </div>
            )}
          </Droppable>
        ))}
      </div>
    </DragDropContext>
  );
};
```

**Application Card:**
```typescript
const ApplicationCard: React.FC<{ application: Application }> = ({ application }) => {
  return (
    <div className="mb-4 border-4 border-black bg-white p-4 shadow-brutal hover:shadow-brutal-hover">
      <div className="mb-2 flex items-start justify-between">
        <h4 className="text-lg font-black">{application.jobTitle}</h4>
        <span className="rounded-none border-2 border-black bg-neon-yellow px-2 py-1 text-xs font-bold">
          {application.atsScore}
        </span>
      </div>
      
      <p className="text-sm font-bold">{application.company}</p>
      <p className="text-xs text-gray-600">{application.location}</p>
      
      <div className="mt-3 flex gap-2">
        <button className="border-2 border-black bg-white px-3 py-1 text-xs font-bold hover:bg-gray-100">
          VIEW
        </button>
        <button className="border-2 border-black bg-white px-3 py-1 text-xs font-bold hover:bg-gray-100">
          NOTES
        </button>
      </div>
      
      <div className="mt-3 text-xs text-gray-500">
        Applied {formatDistanceToNow(new Date(application.appliedAt))} ago
      </div>
    </div>
  );
};
```

**Deliverables:**
- ✅ Kanban board with drag-and-drop
- ✅ Real-time status updates
- ✅ Search and filter functionality
- ✅ Application detail modal

---

#### Day 53-56: Analytics & Insights

**Tasks:**
- [ ] Build analytics engine
- [ ] Create charts (response rate, time-to-interview)
- [ ] Add resume performance tracking
- [ ] Show A/B test results
- [ ] Generate weekly reports

**Code:**
```typescript
// components/AnalyticsDashboard.tsx
export const AnalyticsDashboard: React.FC = () => {
  const { data: analytics } = useQuery({
    queryKey: ['analytics'],
    queryFn: fetchAnalytics,
  });
  
  return (
    <div className="space-y-8">
      {/* Key Metrics */}
      <div className="grid grid-cols-4 gap-4">
        <MetricCard
          title="Response Rate"
          value={`${analytics?.responseRate || 0}%`}
          change="+5.2%"
          trend="up"
        />
        <MetricCard
          title="Avg. Time to Response"
          value={`${analytics?.avgResponseTime || 0}d`}
          change="-2d"
          trend="down"
        />
        <MetricCard
          title="Interview Rate"
          value={`${analytics?.interviewRate || 0}%`}
          change="+12%"
          trend="up"
        />
        <MetricCard
          title="Offer Rate"
          value={`${analytics?.offerRate || 0}%`}
          change="+3%"
          trend="up"
        />
      </div>
      
      {/* Charts */}
      <div className="border-4 border-black bg-white p-6 shadow-brutal">
        <h3 className="mb-4 text-2xl font-black">APPLICATION FUNNEL</h3>
        <ApplicationFunnelChart data={analytics?.funnelData} />
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        <div className="border-4 border-black bg-white p-6 shadow-brutal">
          <h3 className="mb-4 text-xl font-black">RESUME PERFORMANCE</h3>
          <ResumePerformanceChart data={analytics?.resumePerformance} />
        </div>
        
        <div className="border-4 border-black bg-white p-6 shadow-brutal">
          <h3 className="mb-4 text-xl font-black">OUTREACH EFFECTIVENESS</h3>
          <OutreachChart data={analytics?.outreachData} />
        </div>
      </div>
      
      {/* Insights */}
      <div className="border-4 border-black bg-neon-yellow p-6 shadow-brutal">
        <h3 className="mb-4 text-2xl font-black">🔥 INSIGHTS</h3>
        <ul className="space-y-2">
          {analytics?.insights.map((insight, idx) => (
            <li key={idx} className="flex items-start gap-2">
              <span className="font-black">•</span>
              <span className="font-bold">{insight}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
```

**Analytics Backend:**
```python
# backend/services/analytics.py
class AnalyticsEngine:
    def calculate_user_analytics(self, user_id: str) -> Dict:
        """Calculate comprehensive analytics for user"""
        
        applications = self.get_user_applications(user_id)
        
        # Response rate
        total_apps = len(applications)
        responded = len([a for a in applications if a.response_at])
        response_rate = (responded / total_apps * 100) if total_apps > 0 else 0
        
        # Average time to response
        response_times = [
            (a.response_at - a.applied_at).days 
            for a in applications if a.response_at
        ]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        # Interview rate
        interviews = len([a for a in applications if a.status == 'interviewing'])
        interview_rate = (interviews / total_apps * 100) if total_apps > 0 else 0
        
        # Offer rate
        offers = len([a for a in applications if a.status == 'offer'])
        offer_rate = (offers / total_apps * 100) if total_apps > 0 else 0
        
        # Resume performance
        resume_performance = self.calculate_resume_performance(user_id)
        
        # Outreach effectiveness
        outreach_data = self.calculate_outreach_effectiveness(user_id)
        
        # Generate insights
        insights = self.generate_insights(applications, resume_performance, outreach_data)
        
        return {
            'responseRate': round(response_rate, 1),
            'avgResponseTime': round(avg_response_time, 1),
            'interviewRate': round(interview_rate, 1),
            'offerRate': round(offer_rate, 1),
            'funnelData': self.calculate_funnel(applications),
            'resumePerformance': resume_performance,
            'outreachData': outreach_data,
            'insights': insights,
        }
    
    def generate_insights(self, applications, resume_perf, outreach_data) -> List[str]:
        """Generate actionable insights"""
        
        insights = []
        
        # Resume insights
        if resume_perf['best_performing']:
            best = resume_perf['best_performing']
            insights.append(
                f"Your '{best['title']}' resume has a {best['response_rate']}% response rate. Use it more!"
            )
        
        # Outreach insights
        if outreach_data['email_open_rate'] < 30:
            insights.append(
                f"Your email open rate is {outreach_data['email_open_rate']}%. Try more compelling subject lines."
            )
        
        # Timing insights
        best_days = self.find_best_application_days(applications)
        if best_days:
            insights.append(
                f"You get the most responses when applying on {', '.join(best_days)}."
            )
        
        # Application volume
        apps_this_week = len([a for a in applications if self.is_this_week(a.applied_at)])
        if apps_this_week < 5:
            insights.append(
                f"You only applied to {apps_this_week} jobs this week. Increase volume to 10+ for better results."
            )
        
        return insights
```

**Deliverables:**
- ✅ Comprehensive analytics dashboard
- ✅ Interactive charts (Recharts)
- ✅ Resume A/B test results
- ✅ AI-generated insights and recommendations

---

## 🎨 Phase 3: Advanced Features (Weeks 9-12)

### Week 9: AI Interview Prep

#### Day 57-59: Interview Question Generator

**Tasks:**
- [ ] Build question database by role
- [ ] Create JD-specific question generator
- [ ] Add behavioral question templates
- [ ] Implement technical question generation
- [ ] Build company research integration

**Code:**
```python
# backend/services/interview_prep.py
class InterviewPrepGenerator:
    def generate_interview_prep(
        self, 
        job_description: Dict,
        resume: Dict,
        company_name: str
    ) -> Dict:
        """Generate comprehensive interview prep materials"""
        
        # 1. Generate likely questions
        technical_questions = self.generate_technical_questions(job_description)
        behavioral_questions = self.generate_behavioral_questions(job_description, resume)
        company_questions = self.generate_company_questions(company_name)
        
        # 2. Generate suggested answers
        answer_frameworks = self.generate_answer_frameworks(resume, job_description)
        
        # 3. Research company
        company_research = self.research_company(company_name)
        
        # 4. Prepare questions to ask interviewer
        questions_to_ask = self.generate_questions_to_ask(job_description, company_name)
        
        return {
            'technical_questions': technical_questions,
            'behavioral_questions': behavioral_questions,
            'company_questions': company_questions,
            'answer_frameworks': answer_frameworks,
            'company_research': company_research,
            'questions_to_ask': questions_to_ask,
        }
    
    async def generate_technical_questions(self, jd: Dict) -> List[Dict]:
        """Generate role-specific technical questions"""
        
        required_skills = jd.get('required_skills', [])
        experience_level = jd.get('experience_level', 'mid')
        
        prompt = f"""
        Generate 10 technical interview questions for a {jd.get('title')} position.
        
        Required skills: {', '.join(required_skills[:10])}
        Experience level: {experience_level}
        
        Questions should:
        - Test practical knowledge of the required skills
        - Match the seniority level
        - Include both conceptual and practical questions
        - Range from basic to advanced
        
        Return as JSON array: [{{ "question": "...", "difficulty": "easy|medium|hard", "topic": "..." }}]
        """
        
        response = await self.llm.generate(prompt)
        questions = json.loads(response)
        
        return questions
    
    async def generate_answer_frameworks(
        self, 
        resume: Dict, 
        jd: Dict
    ) -> List[Dict]:
        """Generate STAR method answer frameworks based on resume"""
        
        experiences = resume.get('experience', [])
        
        frameworks = []
        
        for exp in experiences[:3]:  # Top 3 experiences
            prompt = f"""
            Create a STAR method answer framework for this experience:
            
            Role: {exp.get('title')} at {exp.get('company')}
            Description: {exp.get('description')}
            
            Target role: {jd.get('title')}
            
            Generate a STAR framework that highlights relevant achievements:
            - Situation: Set the context
            - Task: Explain the challenge
            - Action: Describe what you did
            - Result: Quantify the impact
            
            Return as JSON: {{ "situation": "...", "task": "...", "action": "...", "result": "..." }}
            """
            
            response = await self.llm.generate(prompt)
            framework = json.loads(response)
            framework['experience_title'] = exp.get('title')
            
            frameworks.append(framework)
        
        return frameworks
```

**Deliverables:**
- ✅ 20+ likely interview questions per JD
- ✅ STAR method answer frameworks
- ✅ Company research summary
- ✅ Questions to ask interviewer

---

#### Day 60-63: Mock Interview Simulator

**Tasks:**
- [ ] Build voice-based mock interview
- [ ] Implement speech-to-text
- [ ] Add AI interviewer responses
- [ ] Create answer evaluation system
- [ ] Record and playback interviews

**Code:**
```typescript
// components/MockInterview.tsx
export const MockInterview: React.FC<{ jobId: string }> = ({ jobId }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<string[]>([]);
  const [transcript, setTranscript] = useState('');
  
  const { data: questions } = useQuery({
    queryKey: ['interview-questions', jobId],
    queryFn: () => fetchInterviewQuestions(jobId),
  });
  
  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    
    const audioChunks: Blob[] = [];
    
    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };
    
    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
      
      // Transcribe using Web Speech API or backend
      const transcription = await transcribeAudio(audioBlob);
      setTranscript(transcription);
      
      // Evaluate answer
      const evaluation = await evaluateAnswer(
        questions[currentQuestion].question,
        transcription
      );
      
      setAnswers(prev => [...prev, transcription]);
      
      // Move to next question
      if (currentQuestion < questions.length - 1) {
        setCurrentQuestion(prev => prev + 1);
      }
    };
    
    mediaRecorder.start();
    setIsRecording(true);
    
    // Auto-stop after 2 minutes
    setTimeout(() => {
      mediaRecorder.stop();
      setIsRecording(false);
    }, 120000);
  };
  
  return (
    <div className="min-h-screen bg-white p-8">
      <div className="mx-auto max-w-4xl">
        <div className="mb-8 border-4 border-black bg-neon-yellow p-6 shadow-brutal">
          <h1 className="text-3xl font-black">MOCK INTERVIEW</h1>
          <p className="mt-2">Question {currentQuestion + 1} of {questions?.length}</p>
        </div>
        
        {/* Current Question */}
        <div className="mb-8 border-4 border-black bg-white p-8 shadow-brutal">
          <p className="text-2xl font-bold">{questions?.[currentQuestion]?.question}</p>
          <span className="mt-4 inline-block border-2 border-black bg-gray-100 px-3 py-1 text-sm font-bold">
            {questions?.[currentQuestion]?.topic}
          </span>
        </div>
        
        {/* Recording Controls */}
        <div className="mb-8 text-center">
          <button
            onClick={startRecording}
            disabled={isRecording}
            className={`border-4 border-black px-12 py-6 text-2xl font-black uppercase shadow-brutal transition-all hover:translate-x-1 hover:translate-y-1 ${
              isRecording ? 'bg-red-500 text-white' : 'bg-neon-green text-black'
            }`}
          >
            {isRecording ? '🔴 RECORDING...' : '🎤 START ANSWER'}
          </button>
          
          {isRecording && (
            <p className="mt-4 text-sm font-bold">Recording... Speak clearly!</p>
          )}
        </div>
        
        {/* Live Transcript */}
        {transcript && (
          <div className="mb-8 border-4 border-black bg-gray-50 p-6 shadow-brutal">
            <h3 className="mb-2 text-lg font-black">YOUR ANSWER:</h3>
            <p className="font-mono">{transcript}</p>
          </div>
        )}
        
        {/* Progress */}
        <div className="border-4 border-black bg-white p-4">
          <div className="flex gap-2">
            {questions?.map((_, idx) => (
              <div
                key={idx}
                className={`h-4 flex-1 border-2 border-black ${
                  idx < currentQuestion ? 'bg-neon-green' :
                  idx === currentQuestion ? 'bg-neon-yellow' :
                  'bg-white'
                }`}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
```

**Answer Evaluation:**
```python
# backend/services/interview_evaluator.py
class InterviewAnswerEvaluator:
    async def evaluate_answer(
        self, 
        question: str,
        answer: str,
        resume: Dict
    ) -> Dict:
        """Evaluate interview answer quality"""
        
        prompt = f"""
        Evaluate this interview answer on a scale of 1-10:
        
        Question: {question}
        Answer: {answer}
        
        Candidate background: {self.summarize_resume(resume)}
        
        Evaluate on:
        1. Relevance (does it answer the question?)
        2. Structure (STAR method, clear logic)
        3. Specificity (concrete examples, quantified results)
        4. Confidence (assertive language, no hedging)
        5. Length (appropriate, not too long/short)
        
        Provide:
        - Overall score (1-10)
        - Scores for each criterion
        - Specific feedback
        - Improved version of the answer
        
        Return as JSON.
        """
        
        response = await self.llm.generate(prompt)
        evaluation = json.loads(response)
        
        return evaluation
```

**Deliverables:**
- ✅ Voice-based mock interview
- ✅ Real-time transcription
- ✅ AI answer evaluation (1-10 score)
- ✅ Detailed feedback and improvements

---

### Week 10: Salary Negotiation Intelligence

#### Day 64-66: Salary Data Aggregator

**Tasks:**
- [ ] Scrape Glassdoor/Levels.fyi/PayScale
- [ ] Build salary database by role/location
- [ ] Create salary calculator
- [ ] Add compensation package analyzer
- [ ] Generate negotiation talking points

**Code:**
```python
# backend/services/salary_intelligence.py
class SalaryIntelligence:
    async def get_salary_insights(
        self, 
        job_title: str,
        company: str,
        location: str,
        experience_years: int
    ) -> Dict:
        """Get comprehensive salary insights"""
        
        # 1. Scrape salary data
        glassdoor_data = await self.scrape_glassdoor(job_title, company)
        levels_data = await self.scrape_levels_fyi(job_title, company)
        
        # 2. Calculate statistics
        base_salary_range = self.calculate_salary_range(glassdoor_data, levels_data)
        total_comp_range = self.calculate_total_comp_range(levels_data)
        
        # 3. Adjust for location
        adjusted_range = self.adjust_for_location(base_salary_range, location)
        
        # 4. Adjust for experience
        adjusted_range = self.adjust_for_experience(adjusted_range, experience_years)
        
        # 5. Generate negotiation strategy
        negotiation_strategy = await self.generate_negotiation_strategy(
            adjusted_range,
            company,
            job_title
        )
        
        return {
            'base_salary': {
                'min': adjusted_range['min'],
                'median': adjusted_range['median'],
                'max': adjusted_range['max'],
            },
            'total_compensation': total_comp_range,
            'breakdown': {
                'base': adjusted_range['median'],
                'bonus': total_comp_range['median'] * 0.15,  # Estimate
                'equity': total_comp_range['median'] - adjusted_range['median'] - (total_comp_range['median'] * 0.15),
            },
            'market_percentile': self.calculate_percentile(adjusted_range['median'], glassdoor_data),
            'negotiation_strategy': negotiation_strategy,
        }
    
    async def generate_negotiation_strategy(
        self,
        salary_range: Dict,
        company: str,
        role: str
    ) -> Dict:
        """Generate personalized negotiation strategy"""
        
        prompt = f"""
        Create a salary negotiation strategy for:
        
        Role: {role} at {company}
        Market range: ${salary_range['min']:,} - ${salary_range['max']:,}
        Target: ${salary_range['median']:,}
        
        Provide:
        1. Opening anchor (what to ask for first)
        2. Minimum acceptable (walk-away point)
        3. Key talking points (market data, skills, impact)
        4. Non-salary benefits to negotiate
        5. Phrases to use
        6. Phrases to avoid
        
        Be specific and actionable. Return as JSON.
        """
        
        response = await self.llm.generate(prompt)
        strategy = json.loads(response)
        
        return strategy
```

**Deliverables:**
- ✅ Real-time salary data for any role
- ✅ Total compensation breakdown
- ✅ Location/experience adjustments
- ✅ Negotiation script generator

---

#### Day 67-70: Offer Comparison Tool

**Tasks:**
- [ ] Build offer input form
- [ ] Create TCO (total comp) calculator
- [ ] Add equity valuation
- [ ] Build side-by-side comparison view
- [ ] Generate recommendation

**Code:**
```typescript
// components/OfferComparison.tsx
export const OfferComparison: React.FC = () => {
  const [offers, setOffers] = useState<Offer[]>([]);
  
  const addOffer = () => {
    setOffers(prev => [...prev, emptyOffer()]);
  };
  
  const calculateTotalComp = (offer: Offer): number => {
    const base = offer.baseSalary;
    const bonus = offer.bonus || 0;
    const equity = estimateEquityValue(offer.equity, offer.company);
    const benefits = estimateBenefitsValue(offer.benefits);
    
    return base + bonus + equity + benefits;
  };
  
  return (
    <div className="p-8">
      <div className="mb-8 border-4 border-black bg-neon-yellow p-6 shadow-brutal">
        <h1 className="text-3xl font-black">OFFER COMPARISON</h1>
        <p>Compare offers brutally honest. Numbers don't lie.</p>
      </div>
      
      <div className="grid grid-cols-3 gap-4">
        {offers.map((offer, idx) => (
          <OfferCard
            key={idx}
            offer={offer}
            totalComp={calculateTotalComp(offer)}
            onChange={(updated) => updateOffer(idx, updated)}
          />
        ))}
        
        <button
          onClick={addOffer}
          className="border-4 border-dashed border-black bg-white p-8 text-center font-black hover:bg-gray-50"
        >
          + ADD OFFER
        </button>
      </div>
      
      {offers.length >= 2 && (
        <div className="mt-8 border-4 border-black bg-white p-6 shadow-brutal">
          <h2 className="mb-4 text-2xl font-black">RECOMMENDATION</h2>
          <OfferRecommendation offers={offers} />
        </div>
      )}
    </div>
  );
};
```

**Deliverables:**
    
    // Check daily limit
    const dailyCount = await redis.get(`linkedin:messages:${userId}:${today}`);
    if (parseInt(dailyCount || '0') >= this.limits.messagesPerDay) {
      return false;
    }
    
    // Check hourly limit
    const hourlyCount = await redis.get(`linkedin:messages:${userId}:${thisHour}`);
    if (parseInt(hourlyCount || '0') >= this.limits.messagesPerHour) {
      return false;
    }
    
    return true;
  }
  
  async incrementMessageCount(userId: string): Promise<void> {
    const today = new Date().toISOString().split('T')[0];
    const thisHour = new Date().toISOString().substring(0, 13);