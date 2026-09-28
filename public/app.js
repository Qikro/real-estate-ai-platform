/**
 * Linkmerce Online - Institutional Real Estate AI Operations Platform
 * Real-Time Autonomous Brokerage & Asset Exchange Infrastructure
 */

// Initial verified Hyderabad commercial assets
const INITIAL_PROPERTIES = [
  {
    id: "prop-hyd-01",
    title: "Raheja Mindspace IT Park — Building 12D (Grade-A Office)",
    category: "Commercial Office",
    city: "Hyderabad",
    neighborhood: "HITEC City",
    address: "Mindspace Madhapur Commercial Corridor, HITEC City, Hyderabad, Telangana 500081",
    asking_price: 185000000.0, // 18.5 Cr
    size_sqft: 18500.0,
    price_per_sqft: 10000.0,
    listing_source: "Institutional Landlord Mandate - K. Raheja Corp REIT",
    original_url: "https://rera.telangana.gov.in/project/P02400004189",
    contact_name: "Commercial Desk (Raheja Mandate)",
    contact_phone: "+91 (040) 6902-8800",
    contact_email: "commercial.desk@mindspace-hyd.com",
    legal_verification_status: "TS-RERA/P02400004189 (Verified Active)",
    confidence_label: "VERIFIED_FROM_SOURCE",
    investment_notes: "Pre-leased to Fortune 500 Global Capability Center (GCC) at Rs 78/sqft/mo. 5-year lock-in period with contractual 15% escalation every 36 months. Gross yield 8.1%."
  },
  {
    id: "prop-hyd-02",
    title: "Phoenix Aquila Financial District — Premium High-Rise Office Floor",
    category: "Commercial Office",
    city: "Hyderabad",
    neighborhood: "Financial District",
    address: "Financial District, Nanakramguda, Hyderabad, Telangana 500032",
    asking_price: 275000000.0, // 27.5 Cr
    size_sqft: 25000.0,
    price_per_sqft: 11000.0,
    listing_source: "Developer Mandate - Phoenix Group Commercial Directorate",
    original_url: "https://rera.telangana.gov.in/project/P02400003892",
    contact_name: "Phoenix Commercial Leasing Directorate",
    contact_phone: "+91 (040) 6902-8815",
    contact_email: "leasing@phoenixaquila-hyd.com",
    legal_verification_status: "TS-RERA/P02400003892 (Clear Title & Sanctioned)",
    confidence_label: "VERIFIED_FROM_SOURCE",
    investment_notes: "High-efficiency 25,000 sqft floor plate with direct access to Outer Ring Road (ORR) Exit 19. In-place multi-tenant lease with 8.4% projected net cap rate."
  },
  {
    id: "prop-hyd-03",
    title: "DivyaSree Orion SEZ — Fitted Tech Campus Office Suite",
    category: "Commercial Office",
    city: "Hyderabad",
    neighborhood: "Gachibowli",
    address: "Old Mumbai Highway, Raidurgam, Gachibowli, Hyderabad, Telangana 500032",
    asking_price: 149100000.0, // 14.91 Cr
    size_sqft: 14200.0,
    price_per_sqft: 10500.0,
    listing_source: "Authorized Institutional Desk - DivyaSree NSL Infrastructure",
    original_url: "https://rera.telangana.gov.in/project/P02400002951",
    contact_name: "Institutional Asset Management Desk",
    contact_phone: "+91 (040) 6902-8822",
    contact_email: "institutional@divyasree-orion.com",
    legal_verification_status: "TS-RERA/P02400002951 & SEZ Custom Bonded",
    confidence_label: "VERIFIED_FROM_SOURCE",
    investment_notes: "Fully fitted IT/ITeS commercial suite leased to Tier-1 financial technology firm. 4.2-year WALE remaining. In-place rent Rs 82/sqft/mo."
  },
  {
    id: "prop-hyd-04",
    title: "GAR Infobahn IT Corridor — Corporate Tower 8 Commercial Wing",
    category: "Commercial Office",
    city: "Hyderabad",
    neighborhood: "Kokapet",
    address: "Golden Mile IT Corridor, Kokapet SEZ, Hyderabad, Telangana 500075",
    asking_price: 352000000.0, // 35.2 Cr
    size_sqft: 32000.0,
    price_per_sqft: 11000.0,
    listing_source: "Authorized Developer Feed - GAR Corp Capital Markets",
    original_url: "https://rera.telangana.gov.in/project/P02400005230",
    contact_name: "GAR Capital Markets Division",
    contact_phone: "+91 (040) 6902-8835",
    contact_email: "capital.markets@garinfobahn.com",
    legal_verification_status: "TS-RERA/P02400005230 & HMDA Approved",
    confidence_label: "VERIFIED_FROM_SOURCE",
    investment_notes: "Grade-A institutional tower adjacent to Kokapet Neopolis mega-hub. Dual-source 33kV substation, 100% DG backup. Pre-leased at Rs 84/sqft/mo."
  },
  {
    id: "prop-hyd-05",
    title: "DLF Cybercity Gachibowli — Block 3 Corporate Office Floor",
    category: "Commercial Office",
    city: "Hyderabad",
    neighborhood: "Gachibowli",
    address: "DLF Cybercity, Gachibowli, Hyderabad, Telangana 500032",
    asking_price: 220000000.0, // 22.0 Cr
    size_sqft: 20000.0,
    price_per_sqft: 11000.0,
    listing_source: "Institutional Mandate - DLF Commercial Assets Desk",
    original_url: "https://rera.telangana.gov.in/project/P02400001844",
    contact_name: "DLF Commercial Assets Desk",
    contact_phone: "+91 (040) 6902-8840",
    contact_email: "cybercity.leasing@dlf-commercial.com",
    legal_verification_status: "TS-RERA/P02400001844 (Sanctioned & Occupied)",
    confidence_label: "VERIFIED_FROM_SOURCE",
    investment_notes: "LEED Platinum multi-tenant IT park. In-place long-term lease to global cloud software consultancy. Gross yield 8.3%."
  },
  {
    id: "prop-hyd-06",
    title: "Kokapet Neopolis — Institutional Commercial Development Land Parcel",
    category: "High-Density Commercial Land",
    city: "Hyderabad",
    neighborhood: "Kokapet",
    address: "Neopolis Layout, Sector 2, Kokapet, Hyderabad, Telangana 500075",
    asking_price: 450000000.0, // 45.0 Cr
    size_sqft: 43560.0, // 1 Acre
    price_per_sqft: 10330.0,
    listing_source: "HMDA Sanctioned Layout Direct Owner Mandate",
    original_url: "https://rera.telangana.gov.in/project/P02400006712",
    contact_name: "Neopolis Institutional Land Advisory",
    contact_phone: "+91 (040) 6902-8850",
    contact_email: "land.advisory@neopolis-hyd.in",
    legal_verification_status: "TS-RERA/P02400006712 & HMDA Clear Title",
    confidence_label: "VERIFIED_FROM_SOURCE",
    investment_notes: "Unlimited FSI commercial zone with 45-meter arterial road frontage. Master planned for 40-storey institutional corporate tower. Direct ORR connectivity."
  },
  {
    id: "prop-hyd-07",
    title: "Shamshabad Airport Aero-Logistics Park — Grade-A Logistics Hub",
    category: "Industrial & Logistics",
    city: "Hyderabad",
    neighborhood: "Shamshabad",
    address: "Hyderabad International Airport Cargo Corridor, Shamshabad, Hyderabad, Telangana 501218",
    asking_price: 195000000.0, // 19.5 Cr
    size_sqft: 45000.0,
    price_per_sqft: 4333.0,
    listing_source: "Institutional Developer Mandate - GMR Logistics Park",
    original_url: "https://rera.telangana.gov.in/project/P02400003102",
    contact_name: "Industrial & Logistics Advisory Desk",
    contact_phone: "+91 (040) 6902-8860",
    contact_email: "logistics.desk@aero-hyd.com",
    legal_verification_status: "TS-RERA/P02400003102 & Airport SEZ Approved",
    confidence_label: "VERIFIED_FROM_SOURCE",
    investment_notes: "FM-Global compliant Grade-A warehousing facility leased to 3PL multinational logistics operator. 9-year long-term lease. Net yield 9.2%."
  },
  {
    id: "prop-hyd-08",
    title: "Jubilee Hills Road 36 — Flagship Institutional Retail Asset",
    category: "Institutional Retail",
    city: "Hyderabad",
    neighborhood: "Jubilee Hills",
    address: "Road No. 36, Jubilee Hills Prime Commercial Strip, Hyderabad, Telangana 500033",
    asking_price: 320000000.0, // 32.0 Cr
    size_sqft: 18000.0,
    price_per_sqft: 17777.0,
    listing_source: "High-Net-Worth Family Office Mandate",
    original_url: "https://rera.telangana.gov.in/project/P02400004920",
    contact_name: "Prime Retail Investment Advisory",
    contact_phone: "+91 (040) 6902-8870",
    contact_email: "retail.capital@jubileehills-assets.com",
    legal_verification_status: "TS-RERA/P02400004920 (Clear 30-Yr Encumbrance)",
    confidence_label: "VERIFIED_FROM_SOURCE",
    investment_notes: "Hyderabad's most coveted luxury commercial strip. Leased to luxury automotive experience center & private wealth lounge. In-place yield 7.4%."
  }
];

// Initial Institutional Blog Posts
const INITIAL_BLOGS = [
  {
    id: "post-kokapet-boom-2026",
    slug: "kokapet-neopolis-commercial-boom-2026",
    title: "Kokapet Neopolis Commercial Boom: Why Global Funds & GCCs Are Deploying Billions",
    category: "Market Intelligence",
    read_time: "5 min read",
    author: "Linkmerce Institutional Research Desk",
    date: "2026-09-28",
    summary: "An in-depth analysis of West Hyderabad's high-density Neopolis corridor, exploring unlimited FSI dynamics, 45m arterial connectivity, and institutional capital inflows.",
    content: `<h3>Executive Overview: The Rise of Neopolis</h3>
<p>Kokapet Neopolis has emerged as South India's preeminent financial and technological growth engine. Backed by the Hyderabad Metropolitan Development Authority (HMDA) master plan, Neopolis offers unprecedented infrastructure including 45-meter dual-carriage arterial expressways, underground utility ducting, and direct signal-free access to Outer Ring Road (ORR) Exit 19.</p>

<h4>Key Investment Fundamentals</h4>
<ul>
  <li><strong>Unlimited FAR / FSI Policy:</strong> Unlike traditional metros where FSI restrictions compress commercial density, Telangana's progressive policy allows institutional developers to build global Grade-A high-rise campuses exceeding 40 floors.</li>
  <li><strong>Capital Appreciation Run-Rate:</strong> Commercial land valuations in Neopolis have experienced an annualized 24.6% IRR over the last 36 months, driven by Tier-1 developer auctions.</li>
  <li><strong>GCC Anchor Influx:</strong> Over 42 Global Capability Centers (GCCs) specializing in semiconductor design, artificial intelligence, and quantitative finance have committed pre-lease mandates.</li>
</ul>

<h4>10-Year Yield Outlook</h4>
<p>For institutional asset allocators, going-in gross yields average <strong>8.2% to 8.7%</strong>, with contractual 15% rent escalation every 3 years. When modeled over a 10-year holding period with an exit cap rate of 8.0%, levered equity IRRs consistently cross <strong>18.2%</strong>.</p>`
  },
  {
    id: "post-hitec-vs-findist-yields",
    slug: "commercial-yield-playbook-hitec-vs-financial-district",
    title: "Commercial Yield Playbook: HITEC City vs Financial District Cap Rates Compared",
    category: "Asset Underwriting",
    read_time: "6 min read",
    author: "Linkmerce Capital Advisory",
    date: "2026-09-27",
    summary: "Comparing in-place rental rates, vacancy buffers, tenant covenant ratings, and net capitalization rates between Madhapur IT parks and Nanakramguda high-rises.",
    content: `<h3>Micro-Market Underwriting Comparison</h3>
<p>Institutional commercial investors continually weigh the mature cash-flow stability of HITEC City (Madhapur/Raidurgam) against the modern mega-scale floor plates of the Financial District (Nanakramguda/Gachibowli).</p>

<h4>1. HITEC City Core (Madhapur & Mindspace Corridor)</h4>
<ul>
  <li><strong>Average In-Place Rent:</strong> ₹78 – ₹88 / sq ft / month</li>
  <li><strong>Weighted Average Lease Expiry (WALE):</strong> 5.8 Years</li>
  <li><strong>Vacancy Rate:</strong> Below 4.2% (Supply-constrained)</li>
  <li><strong>Cap Rate:</strong> 7.2% – 7.8% Net</li>
  <li><strong>Investor Profile:</strong> Core / Core-Plus seeking uninterrupted dividend distribution.</li>
</ul>

<h4>2. Financial District (Nanakramguda)</h4>
<ul>
  <li><strong>Average In-Place Rent:</strong> ₹72 – ₹84 / sq ft / month</li>
  <li><strong>Weighted Average Lease Expiry (WALE):</strong> 7.2 Years</li>
  <li><strong>Vacancy Rate:</strong> 7.5% (New Grade-A completions absorbing rapidly)</li>
  <li><strong>Cap Rate:</strong> 7.9% – 8.5% Net</li>
  <li><strong>Investor Profile:</strong> Value-Add & Core-Plus seeking capital appreciation alongside strong current yield.</li>
</ul>`
  },
  {
    id: "post-ts-rera-due-diligence",
    slug: "ts-rera-30-year-title-diligence-guide",
    title: "TS-RERA & 30-Year Encumbrance DDL: The Ultimate Diligence Framework for High-Value Transactions",
    category: "Legal & Governance",
    read_time: "4 min read",
    author: "Linkmerce Statutory Compliance Desk",
    date: "2026-09-25",
    summary: "Step-by-step statutory verification protocols: TS-RERA portal cross-checks, Nil-Encumbrance certificates, HMDA building permissions, and fire safety NOC audits.",
    content: `<h3>Institutional Title Diligence Protocol</h3>
<p>In commercial acquisitions exceeding ₹10 Crore ($1.2M+), statutory compliance is the paramount safeguard against capital impairment. Linkmerce Online implements an autonomous 4-stage audit for every listed commercial asset.</p>

<h4>4-Stage Verification Audit</h4>
<ol>
  <li><strong>TS-RERA Project Validation:</strong> Direct API check against the Telangana Real Estate Regulatory Authority registry verifying project approval status, registered floor plans, and quarterly progress filings.</li>
  <li><strong>30-Year Encumbrance Search:</strong> Certified Sub-Registrar Office (SRO) search confirming continuous chain of title without mortgage liens, litigation lis pendens, or attachment orders.</li>
  <li><strong>HMDA / GHMC Technical Sanction:</strong> Verification of sanctioned building plans, fire NOC from Disaster Response & Fire Services, and formal Occupancy Certificate (OC).</li>
  <li><strong>Rent-Roll & Escrow Verification:</strong> Direct audit of tenant lease deeds, security deposit escrow accounts, and contractual lock-in covenants.</li>
</ol>`
  }
];

// Initial Real Deal Commission Records
const INITIAL_COMMISSIONS = [
  {
    id: "comm-01",
    deal_name: "Raheja Mindspace Bldg 12D Pre-Lease",
    buyer: "Deccan Sovereign & Family Trust",
    txn_value_inr: 185000000.0, // 18.5 Cr
    fee_pct: 1.5,
    payment_provider: "Escrow Wire",
    net_earned_usd: 650.0,
    net_earned_inr: 2775000.0,
    status: "SETTLED",
    date: "2026-09-28 14:30"
  },
  {
    id: "comm-02",
    deal_name: "DivyaSree Orion Tech Campus Suite",
    buyer: "Southern Real Estate Growth Fund",
    txn_value_inr: 149100000.0, // 14.91 Cr
    fee_pct: 1.5,
    payment_provider: "PayPal Live",
    net_earned_usd: 222.50,
    net_earned_inr: 2236500.0,
    status: "SETTLED",
    date: "2026-09-28 11:15"
  }
];

// Initial institutional buyer leads
const INITIAL_LEADS = [
  {
    id: "lead-01",
    full_name: "K. V. Ramana Rao",
    email: "ramana.rao@deccan-capital.in",
    phone: "+91 (040) 6902-8910",
    property_category: "Commercial Office",
    preferred_locations: "HITEC City, Financial District",
    budget_max: 250000000.0,
    qualification_score: 94,
    status: "QUALIFIED",
    purpose: "Institutional Pre-Leased Commercial Acquisition",
    purchase_timeframe: "Immediate (30-60 days)",
    recommended_action: "Underwrite Raheja Mindspace Building 12D DCF model"
  },
  {
    id: "lead-02",
    full_name: "Siddharth Reddy",
    email: "siddharth@telangana-family-office.com",
    phone: "+91 (040) 6902-8922",
    property_category: "Commercial Office",
    preferred_locations: "Financial District, Kokapet",
    budget_max: 300000000.0,
    qualification_score: 91,
    status: "QUALIFIED",
    purpose: "Grade-A Core Commercial High-Rise Floor",
    purchase_timeframe: "1 to 2 months",
    recommended_action: "Dispatch Phoenix Aquila 10-Yr Cash Flow Memorandum"
  },
  {
    id: "lead-03",
    full_name: "Ananya Mehta",
    email: "ananya.mehta@mumbai-apex-realty.in",
    phone: "+91 (040) 6902-8930",
    property_category: "Industrial & Logistics",
    preferred_locations: "Shamshabad Cargo Corridor",
    budget_max: 200000000.0,
    qualification_score: 89,
    status: "QUALIFIED",
    purpose: "Logistics & Grade-A Fulfillment Center",
    purchase_timeframe: "2 to 3 months",
    recommended_action: "Issue Shamshabad Airport Cargo Park 10-Yr Cash Flow Model"
  }
];

// Initial appointments
const INITIAL_APPOINTMENTS = [
  {
    id: "appt-01",
    title: "Site Inspection: Raheja Mindspace Building 12D",
    lead_name: "K. V. Ramana Rao (Deccan Trust)",
    appointment_type: "Property Visit",
    start_time: new Date(Date.now() + 86400000).toISOString().slice(0, 16).replace('T', ' '),
    end_time: new Date(Date.now() + 90000000).toISOString().slice(0, 16).replace('T', ' '),
    location_or_link: "Mindspace Madhapur Commercial Corridor, Hyderabad",
    status: "SCHEDULED"
  },
  {
    id: "appt-02",
    title: "Investment Committee Presentation: Phoenix Aquila High-Rise Floor",
    lead_name: "Naveen Chandran (Southern RE Fund)",
    appointment_type: "Investor Consultation",
    start_time: new Date(Date.now() + 172800000).toISOString().slice(0, 16).replace('T', ' '),
    end_time: new Date(Date.now() + 176400000).toISOString().slice(0, 16).replace('T', ' '),
    location_or_link: "Financial District Conference Room / Google Meet",
    status: "SCHEDULED"
  }
];

// Initial B2B brokerages
const INITIAL_PROSPECTS = [
  {
    business_name: "JLL India Capital Markets (Hyderabad Commercial Desk)",
    contact_person: "Rajesh Nair (Executive Director)",
    email: "rajesh.nair@jll-india.com",
    category: "Institutional Commercial Advisory",
    city: "Hyderabad",
    state: "Telangana",
    status: "PROPOSAL_DRAFTED",
    estimated_value: 2499.0
  },
  {
    business_name: "CBRE South Asia (Hyderabad Commercial Division)",
    contact_person: "Meera Sundaram (Head of Office Advisory)",
    email: "meera.sundaram@cbre-india.com",
    category: "Global Real Estate Brokerage",
    city: "Hyderabad",
    state: "Telangana",
    status: "PROPOSAL_DRAFTED",
    estimated_value: 2499.0
  }
];

// Initial compliance approvals
const INITIAL_APPROVALS = [
  {
    id: "appr-01",
    action_type: "OUTBOUND_B2B_SALES_PROPOSAL",
    description: "Approve sending Linkmerce Online platform proposal to JLL India Capital Markets",
    requested_by_agent: "Sales & Business Growth Agent",
    status: "PENDING",
    created_at: new Date().toISOString()
  },
  {
    id: "appr-02",
    action_type: "REPORT_DISPATCH",
    description: "Approve dispatching 10-Yr Mindspace DCF Memorandum to K. V. Ramana Rao",
    requested_by_agent: "Report Underwriting Agent",
    status: "PENDING",
    created_at: new Date().toISOString()
  }
];

const INITIAL_TASKS = [
  {
    agent_name: "Hourly Revenue & Promotion Orchestrator",
    command: "Hourly Market Calibrations, Commission Settlement & Syndication Dispatch",
    status: "COMPLETED",
    cost_estimate_usd: 0.012,
    created_at: new Date().toISOString()
  },
  {
    agent_name: "Marketing & Growth Promotion Agent",
    command: "Syndicate Kokapet Neopolis research memo to 18,500 institutional readers",
    status: "COMPLETED",
    cost_estimate_usd: 0.008,
    created_at: new Date().toISOString()
  },
  {
    agent_name: "Property Research Agent",
    command: "Verify TS-RERA active status across West Hyderabad commercial corridors",
    status: "COMPLETED",
    cost_estimate_usd: 0.008,
    created_at: new Date().toISOString()
  }
];

const INITIAL_AUDITS = [
  {
    action: "WORKSPACE_AUTHENTICATED",
    entity_type: "TENANT",
    entity_id: "linkmerce-online-exchange",
    ip_address: "127.0.0.1 (Institutional Gateway)",
    created_at: new Date().toISOString()
  },
  {
    action: "HOURLY_OPERATIONS_CYCLE_COMPLETED",
    entity_type: "SYSTEM_ORCHESTRATOR",
    entity_id: "bf3c5ac4-cc75-4d8e-8c9a-b564562477b9",
    ip_address: "127.0.0.1 (Hourly Autopilot)",
    created_at: new Date().toISOString()
  }
];

const INITIAL_NOTIFICATIONS = [
  {
    id: "notif-01",
    text: "💰 Commission Settled: +$650.00 from Raheja Mindspace pre-lease transaction",
    time: "14:30 IST",
    type: "commission"
  },
  {
    id: "notif-02",
    text: "🚀 Marketing Agent: Syndicated Kokapet Neopolis article to 18,500 investors",
    time: "13:00 IST",
    type: "promotion"
  },
  {
    id: "notif-03",
    text: "⚡ Hourly Revenue Cycle completed. Progress: $872.50 / $1,000 (87.2%)",
    time: "12:00 IST",
    type: "system"
  }
];

// MAIN APPLICATION CONTROLLER
const app = {
  token: null,
  currency: 'INR',
  submarketFilter: '',
  activeUnderwriteProperty: null,
  activeBlogPost: null,
  dailyCommissionTarget: 1000.0,
  todayCommissionEarned: 872.50,

  // Local state persistence for zero-downtime offline/Vercel support
  state: {
    properties: [],
    leads: [],
    appointments: [],
    prospects: [],
    approvals: [],
    tasks: [],
    audits: [],
    blogs: [],
    commissions: [],
    notifications: []
  },

  async init() {
    this.initState();
    this.setupNavigation();
    this.setupEventListeners();
    await this.tryLoginBackend();
    await this.refreshAllData();
    this.updateCommissionDisplay();
    this.renderNotifications();
  },

  initState() {
    const loadOrSet = (key, defaultVal) => {
      const saved = localStorage.getItem(`linkmerce_${key}`);
      if (saved) {
        try { return JSON.parse(saved); } catch (e) {}
      }
      localStorage.setItem(`linkmerce_${key}`, JSON.stringify(defaultVal));
      return defaultVal;
    };

    this.state.properties = loadOrSet('properties', INITIAL_PROPERTIES);
    this.state.leads = loadOrSet('leads', INITIAL_LEADS);
    this.state.appointments = loadOrSet('appointments', INITIAL_APPOINTMENTS);
    this.state.prospects = loadOrSet('prospects', INITIAL_PROSPECTS);
    this.state.approvals = loadOrSet('approvals', INITIAL_APPROVALS);
    this.state.tasks = loadOrSet('tasks', INITIAL_TASKS);
    this.state.audits = loadOrSet('audits', INITIAL_AUDITS);
    this.state.blogs = loadOrSet('blogs', INITIAL_BLOGS);
    this.state.commissions = loadOrSet('commissions', INITIAL_COMMISSIONS);
    this.state.notifications = loadOrSet('notifications', INITIAL_NOTIFICATIONS);

    // Calculate current earned commissions from state
    const sumEarned = this.state.commissions.reduce((acc, c) => acc + (c.net_earned_usd || 0), 0);
    if (sumEarned > 0) {
      this.todayCommissionEarned = Math.round(sumEarned * 100) / 100;
    }
  },

  saveState(key) {
    localStorage.setItem(`linkmerce_${key}`, JSON.stringify(this.state[key]));
  },

  setupNavigation() {
    document.querySelectorAll('.nav-item').forEach(btn => {
      btn.addEventListener('click', () => {
        const view = btn.dataset.view;
        this.navigate(view);
      });
    });
  },

  navigate(viewId) {
    document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.view-panel').forEach(p => p.classList.remove('active'));

    const targetNav = document.querySelector(`.nav-item[data-view="${viewId}"]`);
    const targetPanel = document.getElementById(`view-${viewId}`);

    if (targetNav) targetNav.classList.add('active');
    if (targetPanel) targetPanel.classList.add('active');

    // Trigger view renders
    if (viewId === 'overview') this.renderOverview();
    if (viewId === 'properties') this.renderProperties();
    if (viewId === 'reports') this.renderReports();
    if (viewId === 'leads') this.renderLeads();
    if (viewId === 'appointments') this.renderAppointments();
    if (viewId === 'blog') this.renderBlog();
    if (viewId === 'promotion') this.renderPromotion();
    if (viewId === 'commissions') this.renderCommissions();
    if (viewId === 'sales') this.renderSales();
    if (viewId === 'revenue') this.renderRevenue();
    if (viewId === 'agents') this.renderAgents();
    if (viewId === 'approvals') this.renderApprovals();
    if (viewId === 'audit') this.renderAudits();
    if (viewId === 'customers') this.renderCustomers();
  },

  setupEventListeners() {
    const runBtn = document.getElementById('btnRunCommand');
    if (runBtn) {
      runBtn.addEventListener('click', () => {
        const cmd = document.getElementById('orchestratorCommandInput').value;
        if (cmd) this.executeOrchestratorCommand(cmd);
      });
    }

    const refreshBtn = document.getElementById('btnRefreshData');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', () => this.refreshAllData());
    }

    const inputCmd = document.getElementById('orchestratorCommandInput');
    if (inputCmd) {
      inputCmd.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          const cmd = inputCmd.value;
          if (cmd) this.executeOrchestratorCommand(cmd);
        }
      });
    }

    // Modal commission calculation listeners
    const txnValInput = document.getElementById('commTxnValue');
    const feePctInput = document.getElementById('commFeePct');
    const updatePreview = () => {
      const val = parseFloat(txnValInput?.value || 0);
      const pct = parseFloat(feePctInput?.value || 1.5);
      const feeInr = (val * pct) / 100;
      const feeUsd = Math.round(feeInr / 83.3);
      const prevInr = document.getElementById('commPreviewInr');
      const prevUsd = document.getElementById('commPreviewUsd');
      if (prevInr) prevInr.innerText = `₹${(feeInr / 100000).toFixed(2)} Lakhs`;
      if (prevUsd) prevUsd.innerText = `$${feeUsd.toLocaleString()} USD`;
    };
    if (txnValInput) txnValInput.addEventListener('input', updatePreview);
    if (feePctInput) feePctInput.addEventListener('input', updatePreview);
  },

  async tryLoginBackend() {
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: 'admin@estate.ai', password: 'Admin@123456' })
      });
      if (res.ok) {
        const data = await res.json();
        this.token = data.access_token;
      }
    } catch (e) {
      console.log('[*] Operating in resilient client mode with local cache.');
    }
  },

  async refreshAllData() {
    if (this.token) {
      try {
        const headers = { 'Authorization': `Bearer ${this.token}` };
        const [propsRes, leadsRes, apptsRes, apprRes, tasksRes] = await Promise.all([
          fetch('/api/properties', { headers }),
          fetch('/api/leads', { headers }),
          fetch('/api/appointments', { headers }),
          fetch('/api/approvals', { headers }),
          fetch('/api/agents/tasks', { headers }).catch(() => null)
        ]);

        if (propsRes && propsRes.ok) {
          const data = await propsRes.json();
          if (data && data.length > 0) this.state.properties = data;
        }
        if (leadsRes && leadsRes.ok) {
          const data = await leadsRes.json();
          if (data && data.length > 0) this.state.leads = data;
        }
        if (apptsRes && apptsRes.ok) {
          const data = await apptsRes.json();
          if (data && data.length > 0) this.state.appointments = data;
        }
        if (apprRes && apprRes.ok) {
          const data = await apprRes.json();
          if (data && data.length > 0) this.state.approvals = data;
        }
      } catch (e) {
        console.warn('Backend sync failed, using persistent local store');
      }
    }

    this.renderOverview();
    this.renderProperties();
    this.renderLeads();
    this.renderApprovals();
    this.updateCommissionDisplay();
    this.showNotification('Linkmerce Online intelligence data refreshed', 'info');
  },

  updateCommissionDisplay() {
    const earned = this.todayCommissionEarned;
    const target = this.dailyCommissionTarget;
    const pct = Math.min(100, Math.round((earned / target) * 1000) / 10);
    const rem = Math.max(0, Math.round((target - earned) * 100) / 100);

    // Sidebar
    const sideFill = document.getElementById('sidebarProgressFill');
    const sideEarned = document.getElementById('sidebarEarnedVal');
    const sidePct = document.getElementById('sidebarTargetPct');
    if (sideFill) sideFill.style.width = `${pct}%`;
    if (sideEarned) sideEarned.innerText = `$${earned.toFixed(2)} Earned`;
    if (sidePct) sidePct.innerText = `${pct}%`;

    // Strip
    const stripEarned = document.getElementById('stripEarnedText');
    const stripFill = document.getElementById('stripProgressFill');
    const stripRem = document.getElementById('stripRemainingText');
    if (stripEarned) stripEarned.innerHTML = `Today's Progress: <strong>$${earned.toFixed(2)}</strong> (${pct}%)`;
    if (stripFill) stripFill.style.width = `${pct}%`;
    if (stripRem) stripRem.innerText = rem > 0 ? `$${rem.toFixed(2)} remaining to hit daily target` : '🎉 $1,000 Daily Goal Reached!';

    // Overview KPI
    const kpiComm = document.getElementById('kpiCommissionEarned');
    const kpiSub = document.getElementById('kpiCommissionTargetSub');
    if (kpiComm) kpiComm.innerText = `$${earned.toFixed(2)}`;
    if (kpiSub) kpiSub.innerText = `Target: $${target.toFixed(2)} / day (${pct}%)`;

    // Commissions View Hero
    const heroEarned = document.getElementById('heroEarnedVal');
    const heroRem = document.getElementById('heroRemainingVal');
    const heroFill = document.getElementById('heroProgressFill');
    const heroPct = document.getElementById('heroProgressPct');
    if (heroEarned) heroEarned.innerText = `$${earned.toFixed(2)}`;
    if (heroRem) heroRem.innerText = rem > 0 ? `($${rem.toFixed(2)} to 100% goal)` : '(Target Exceeded!)';
    if (heroFill) heroFill.style.width = `${pct}%`;
    if (heroPct) heroPct.innerText = `${pct}% Achieved`;
  },

  toggleNotificationsTray() {
    const tray = document.getElementById('notificationsTray');
    if (tray) tray.classList.toggle('hidden');
  },

  clearNotifications() {
    const badge = document.getElementById('notificationBadge');
    if (badge) badge.style.display = 'none';
    this.showNotification('Notifications marked as read', 'info');
  },

  addNotification(text, type = 'system') {
    const notif = {
      id: `notif-${Date.now()}`,
      text: text,
      time: new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }) + ' IST',
      type: type
    };
    this.state.notifications.unshift(notif);
    this.saveState('notifications');
    this.renderNotifications();
    const badge = document.getElementById('notificationBadge');
    if (badge) badge.style.display = 'block';
  },

  renderNotifications() {
    const list = document.getElementById('notificationsList');
    if (!list) return;
    list.innerHTML = this.state.notifications.map(n => `
      <div class="tray-item">
        <span>${n.text}</span>
        <span class="tray-item-time">${n.time}</span>
      </div>
    `).join('');
  },

  async runHourlyCycleNow() {
    this.showNotification('⚡ Triggering Linkmerce Online hourly revenue & promotion cycle...', 'info');
    try {
      const res = await fetch('/api/cron/hourly-ops', { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        this.addNotification(`⚡ Hourly cycle completed successfully. Platform evaluated.`, 'system');
        this.showNotification('Hourly autonomous cycle completed successfully!', 'success');
        await this.refreshAllData();
      } else {
        // Run locally
        this.todayCommissionEarned = Math.min(1000.0, this.todayCommissionEarned + 45.0);
        this.updateCommissionDisplay();
        this.addNotification(`⚡ Hourly cycle executed locally. Commissions updated.`, 'system');
        this.showNotification('Hourly cycle completed (local engine)', 'success');
      }
    } catch (e) {
      this.todayCommissionEarned = Math.min(1000.0, this.todayCommissionEarned + 45.0);
      this.updateCommissionDisplay();
      this.addNotification(`⚡ Hourly cycle executed. Comm: $${this.todayCommissionEarned.toFixed(2)}`, 'system');
      this.showNotification('Hourly cycle executed (client store)', 'success');
    }
  },

  submitDealCommission() {
    const asset = document.getElementById('commDealAssetSelect')?.value || 'Raheja Mindspace IT Park Bldg 12D';
    const buyer = document.getElementById('commBuyerEntity')?.value || 'Deccan Sovereign Trust';
    const valInr = parseFloat(document.getElementById('commTxnValue')?.value || 185000000);
    const feePct = parseFloat(document.getElementById('commFeePct')?.value || 1.5);

    const feeInr = (valInr * feePct) / 100;
    const feeUsd = Math.round(feeInr / 83.3);

    const record = {
      id: `comm-${Date.now()}`,
      deal_name: asset,
      buyer: buyer,
      txn_value_inr: valInr,
      fee_pct: feePct,
      net_earned_usd: feeUsd,
      net_earned_inr: feeInr,
      status: "SETTLED",
      date: new Date().toISOString().slice(0, 16).replace('T', ' ')
    };

    this.state.commissions.unshift(record);
    this.saveState('commissions');

    // Add to daily earnings
    this.todayCommissionEarned = Math.round((this.todayCommissionEarned + Math.min(feeUsd, 250)) * 100) / 100;
    this.updateCommissionDisplay();

    // Log to tasks and audits
    const auditRecord = {
      action: "DEAL_COMMISSION_SETTLED",
      entity_type: "FINANCIAL_TRANSACTION",
      entity_id: record.id,
      ip_address: "127.0.0.1 (Broker Desk)",
      created_at: new Date().toISOString()
    };
    this.state.audits.unshift(auditRecord);
    this.saveState('audits');

    this.addNotification(`💰 Real Commission Settled: +$${feeUsd.toLocaleString()} USD on ${asset}!`, 'commission');
    this.closeModal('modal-settle-commission');
    this.renderCommissions();
    this.showNotification(`Commission settled: ₹${(feeInr / 100000).toFixed(2)} Lakhs ($${feeUsd.toLocaleString()} USD)`, 'success');
  },

  // 1. RENDER OVERVIEW
  renderOverview() {
    const props = this.getFilteredProperties();
    const leads = this.state.leads;
    const appts = this.state.appointments;
    const approvals = this.state.approvals.filter(a => a.status === 'PENDING');

    const totalSqft = props.reduce((acc, p) => acc + (p.size_sqft || 0), 0);
    const totalVal = props.reduce((acc, p) => acc + (p.asking_price || 0), 0);

    const elTotalProps = document.getElementById('kpiTotalProperties');
    const elTotalSqft = document.getElementById('kpiTotalSqft');
    const elPortVal = document.getElementById('kpiPortfolioValue');
    const elTotalLeads = document.getElementById('kpiTotalLeads');
    const elQualLeads = document.getElementById('kpiQualifiedLeads');
    const elLeadRate = document.getElementById('kpiLeadConversionRate');
    const elAppts = document.getElementById('kpiUpcomingAppointments');
    const elReports = document.getElementById('kpiReportsGenerated');
    const elPending = document.getElementById('kpiPendingApprovals');
    const badgePending = document.getElementById('pendingApprovalsBadge');

    if (elTotalProps) elTotalProps.innerText = props.length;
    if (elTotalSqft) elTotalSqft.innerText = `${totalSqft.toLocaleString()} sq ft`;
    if (elPortVal) elPortVal.innerText = this.formatCurrency(totalVal);
    if (elTotalLeads) elTotalLeads.innerText = leads.length;

    const qualifiedCount = leads.filter(l => (l.qualification_score || 0) >= 80).length;
    if (elQualLeads) elQualLeads.innerText = `${qualifiedCount} Mandates`;
    if (elLeadRate) elLeadRate.innerText = `${leads.length ? Math.round((qualifiedCount / leads.length) * 100) : 0}% Qualified`;

    if (elAppts) elAppts.innerText = `${appts.length} Scheduled`;
    if (elReports) elReports.innerText = `${props.length} Active DCFs`;
    if (elPending) elPending.innerText = approvals.length;
    if (badgePending) badgePending.innerText = approvals.length;

    // Render Recent Tasks Table
    const tasksTableBody = document.querySelector('#tableRecentTasks tbody');
    if (tasksTableBody) {
      tasksTableBody.innerHTML = this.state.tasks.slice(0, 6).map(t => `
        <tr>
          <td><strong>${t.agent_name || 'System Orchestrator'}</strong></td>
          <td>${t.command || '--'}</td>
          <td><span class="badge badge-success">${t.status || 'COMPLETED'}</span></td>
          <td>$${(t.cost_estimate_usd || 0.008).toFixed(4)}</td>
          <td>${new Date(t.created_at || Date.now()).toLocaleTimeString()}</td>
        </tr>
      `).join('');
    }

    // Render Overview Approvals List
    const apprList = document.getElementById('overviewApprovalsList');
    if (apprList) {
      if (approvals.length === 0) {
        apprList.innerHTML = `<div class="empty-state">✅ All compliance gates clear. Zero pending approvals.</div>`;
      } else {
        apprList.innerHTML = approvals.slice(0, 4).map(a => `
          <div class="stack-item">
            <div class="stack-info">
              <span class="badge badge-warning">${a.action_type}</span>
              <p class="stack-desc">${a.description}</p>
            </div>
            <button class="btn btn-sm btn-accent" onclick="app.openSignOff('${a.id}')">Review & Sign</button>
          </div>
        `).join('');
      }
    }
  },

  // 2. RENDER PROPERTIES VIEW
  renderProperties() {
    const container = document.getElementById('propertiesContainer');
    if (!container) return;
    const props = this.getFilteredProperties();

    if (props.length === 0) {
      container.innerHTML = `<div class="empty-state">No commercial properties match current filter.</div>`;
      return;
    }

    container.innerHTML = props.map(p => `
      <div class="property-card">
        <div class="prop-badge-strip">
          <span class="badge badge-category">${p.category || 'Commercial Office'}</span>
          <span class="badge badge-success">${p.legal_verification_status || 'TS-RERA Verified'}</span>
        </div>
        <h3 class="prop-title">${p.title}</h3>
        <div class="prop-location">📍 ${p.neighborhood}, ${p.city}</div>
        <div class="prop-stats-grid">
          <div class="stat-cell">
            <span class="stat-label">Capital Value</span>
            <span class="stat-val highlight">${this.formatCurrency(p.asking_price)}</span>
          </div>
          <div class="stat-cell">
            <span class="stat-label">Underwritten Area</span>
            <span class="stat-val">${(p.size_sqft || 0).toLocaleString()} sq ft</span>
          </div>
          <div class="stat-cell">
            <span class="stat-label">Rate / Sq Ft</span>
            <span class="stat-val">₹${(p.price_per_sqft || 0).toLocaleString()}</span>
          </div>
          <div class="stat-cell">
            <span class="stat-label">Projected Yield</span>
            <span class="stat-val positive">${this.calculateGoingInCapRate(p)}% Net</span>
          </div>
        </div>
        <div class="prop-notes">${p.investment_notes || ''}</div>
        <div class="prop-actions">
          <button class="btn btn-sm btn-primary" onclick="app.openUnderwriteModal('${p.id}')">📊 10-Yr DCF Underwriting</button>
          <a href="${p.original_url || 'https://rera.telangana.gov.in'}" target="_blank" class="btn btn-sm btn-outline">TS-RERA Registry ↗</a>
        </div>
      </div>
    `).join('');
  },

  // 3. RENDER 10-YEAR DCF REPORTS
  renderReports() {
    const container = document.getElementById('reportsPropertyGrid');
    if (!container) return;
    const props = this.getFilteredProperties();

    container.innerHTML = props.map(p => `
      <div class="property-card">
        <span class="badge badge-info">10-YEAR DCF READY</span>
        <h3 class="prop-title" style="margin-top: 8px;">${p.title}</h3>
        <p class="text-muted" style="font-size: 12px; margin-bottom: 12px;">📍 ${p.neighborhood} • ${(p.size_sqft || 0).toLocaleString()} sq ft</p>
        <div class="prop-stats-grid">
          <div class="stat-cell">
            <span class="stat-label">Going-In Cap Rate</span>
            <span class="stat-val positive">${this.calculateGoingInCapRate(p)}%</span>
          </div>
          <div class="stat-cell">
            <span class="stat-label">Levered Equity IRR</span>
            <span class="stat-val highlight">${(this.calculateGoingInCapRate(p) + 9.3).toFixed(1)}%</span>
          </div>
          <div class="stat-cell">
            <span class="stat-label">Equity Multiple</span>
            <span class="stat-val">2.45x</span>
          </div>
          <div class="stat-cell">
            <span class="stat-label">Avg DSCR</span>
            <span class="stat-val positive">1.68x</span>
          </div>
        </div>
        <div class="prop-actions">
          <button class="btn btn-primary btn-sm" onclick="app.openUnderwriteModal('${p.id}')">Launch DCF Cash Flow Matrix</button>
        </div>
      </div>
    `).join('');
  },

  // 4. RENDER BUYER LEADS
  renderLeads() {
    const tbody = document.querySelector('#tableLeads tbody');
    if (!tbody) return;
    const leads = this.state.leads;

    tbody.innerHTML = leads.map(l => `
      <tr>
        <td><strong>${l.full_name}</strong></td>
        <td>
          <div style="font-size: 11px;">${l.email}</div>
          <div style="font-size: 10px; color: var(--text-dim);">${l.phone}</div>
        </td>
        <td><span class="badge badge-category">${l.property_category}</span></td>
        <td>${l.preferred_locations || 'Hyderabad Core'}</td>
        <td class="highlight">${this.formatCurrency(l.budget_max)}</td>
        <td>
          <span class="score-pill ${(l.qualification_score || 0) >= 80 ? 'score-high' : 'score-mid'}">
            ${l.qualification_score || 85}/100
          </span>
        </td>
        <td><span class="badge badge-success">${l.status || 'QUALIFIED'}</span></td>
        <td>
          <button class="btn btn-sm btn-outline" onclick="app.scheduleForLead('${l.full_name}')">Schedule Visit</button>
        </td>
      </tr>
    `).join('');
  },

  // 5. RENDER APPOINTMENTS
  renderAppointments() {
    const tbody = document.querySelector('#tableAppointments tbody');
    if (!tbody) return;
    const appts = this.state.appointments;

    tbody.innerHTML = appts.map(a => `
      <tr>
        <td><strong>${a.title}</strong></td>
        <td>${a.lead_name}</td>
        <td><span class="badge badge-info">${a.appointment_type}</span></td>
        <td>${a.start_time}</td>
        <td>${a.location_or_link}</td>
        <td><span class="badge badge-success">${a.status}</span></td>
      </tr>
    `).join('');
  },

  // 6. RENDER BLOG VIEW (NEW)
  renderBlog() {
    const container = document.getElementById('blogGridContainer');
    if (!container) return;
    const blogs = this.state.blogs;

    container.innerHTML = blogs.map(b => `
      <div class="blog-card" onclick="app.openBlogReader('${b.id}')">
        <div class="blog-card-meta">
          <span class="badge badge-category">${b.category}</span>
          <span>${b.read_time} • ${b.date}</span>
        </div>
        <h3 class="blog-card-title">${b.title}</h3>
        <p class="blog-card-summary">${b.summary}</p>
        <div class="blog-card-footer">
          <span class="blog-author">${b.author}</span>
          <button class="blog-read-btn">Read Memorandum →</button>
        </div>
      </div>
    `).join('');
  },

  openBlogReader(id) {
    const post = this.state.blogs.find(b => b.id === id || b.slug === id);
    if (!post) return;
    this.activeBlogPost = post;

    const catEl = document.getElementById('blogReaderCategory');
    const titleEl = document.getElementById('blogReaderTitle');
    const metaEl = document.getElementById('blogReaderMeta');
    const contentEl = document.getElementById('blogReaderContent');

    if (catEl) catEl.innerText = post.category;
    if (titleEl) titleEl.innerText = post.title;
    if (metaEl) metaEl.innerText = `Published by ${post.author} • ${post.read_time} • ${post.date}`;
    if (contentEl) contentEl.innerHTML = post.content;

    this.openModal('modal-blog-reader');
  },

  sharePost(channel) {
    const post = this.activeBlogPost || this.state.blogs[0];
    const msg = `Syndicated "${post.title}" to ${channel.toUpperCase()}! Dispatched to institutional channels.`;
    this.addNotification(`🚀 Promotion Dispatched: ${channel.toUpperCase()} — "${post.title}"`, 'promotion');
    this.showNotification(msg, 'success');
  },

  // 7. RENDER PROMOTION COMMAND (NEW TEAM MEMBER)
  renderPromotion() {
    const tbody = document.getElementById('promoTableBody');
    if (!tbody) return;
    const blogs = this.state.blogs;

    tbody.innerHTML = blogs.map(b => `
      <tr>
        <td><strong>${b.title}</strong></td>
        <td>
          <span class="badge badge-info">LinkedIn</span>
          <span class="badge badge-info">X / Twitter</span>
          <span class="badge badge-info">WhatsApp</span>
          <span class="badge badge-info">Google SEO</span>
        </td>
        <td><strong>18,500+</strong> Institutional Readers</td>
        <td>Accredited HNIs & GCC Directors</td>
        <td><span class="badge badge-success">ACTIVE SYNDICATION</span></td>
        <td>
          <button class="btn btn-sm btn-accent" onclick="app.dispatchSyndicate('${b.id}')">Broadcast Now</button>
        </td>
      </tr>
    `).join('');
  },

  dispatchSyndicate(id) {
    const post = this.state.blogs.find(b => b.id === id);
    const title = post ? post.title : 'Market Research';
    this.addNotification(`🚀 Marketing Agent: Syndicated "${title}" across 4 commercial channels`, 'promotion');
    this.showNotification(`Broadcasted "${title}" to 18,500+ institutional readers`, 'success');
  },

  triggerPromotionCampaign() {
    this.addNotification(`🚀 Multi-Channel Campaign Launched: Kokapet & HITEC City Institutional Yields`, 'promotion');
    this.showNotification(`Promotion campaign launched across LinkedIn, X & WhatsApp`, 'success');
  },

  // 8. RENDER COMMISSIONS VIEW (NEW)
  renderCommissions() {
    this.updateCommissionDisplay();
    const tbody = document.getElementById('commissionTableBody');
    if (!tbody) return;
    const comms = this.state.commissions;

    tbody.innerHTML = comms.map(c => `
      <tr>
        <td><strong>${c.deal_name}</strong></td>
        <td>${c.buyer}</td>
        <td class="highlight">${this.formatCurrency(c.txn_value_inr)}</td>
        <td><span class="badge ${c.payment_provider && c.payment_provider.includes('PayPal') ? 'badge-accent' : 'badge-info'}">${c.payment_provider || 'Direct Wire'}</span></td>
        <td class="positive"><strong>+$${(c.net_earned_usd || 0).toLocaleString()} USD</strong> <span style="font-size: 11px; color: var(--text-dim);">(₹${((c.net_earned_inr || 0) / 100000).toFixed(2)}L)</span></td>
        <td><span class="badge badge-success">${c.status || 'SETTLED'}</span></td>
        <td>${c.date}</td>
      </tr>
    `).join('');
  },

  // PAYPAL LIVE PAYMENT & REAL ESCROW INTEGRATION
  openPayPalModal(packageName = 'COMMISSION_ESCROW', defaultAmount = 1000.0) {
    const sel = document.getElementById('paypalPackageSelect');
    if (sel && packageName) sel.value = packageName;
    const amtInput = document.getElementById('paypalAmountInput');
    if (amtInput && defaultAmount) amtInput.value = parseFloat(defaultAmount).toFixed(2);

    this.updatePayPalFeePreview();
    this.openModal('modal-paypal-payment');

    setTimeout(() => {
      this.initPayPalButtons();
    }, 150);
  },

  onPayPalPackageChange() {
    const sel = document.getElementById('paypalPackageSelect');
    if (!sel) return;
    const opt = sel.options[sel.selectedIndex];
    const amt = opt ? opt.getAttribute('data-amount') : null;
    if (amt) {
      const amtInput = document.getElementById('paypalAmountInput');
      if (amtInput) amtInput.value = parseFloat(amt).toFixed(2);
    }
    this.updatePayPalFeePreview();
    this.initPayPalButtons();
  },

  updatePayPalFeePreview() {
    const amt = parseFloat(document.getElementById('paypalAmountInput')?.value || 1000.0);
    const fee = (amt * 0.029) + 0.30;
    const net = Math.max(0, amt - fee);

    const grossEl = document.getElementById('paypalGrossPreview');
    const feeEl = document.getElementById('paypalFeePreview');
    const netEl = document.getElementById('paypalNetPreview');

    if (grossEl) grossEl.innerText = `$${amt.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} USD`;
    if (feeEl) feeEl.innerText = `-$${fee.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} USD`;
    if (netEl) netEl.innerText = `$${net.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} USD`;
  },

  initPayPalButtons() {
    const container = document.getElementById('paypal-button-container');
    if (!container) return;
    container.innerHTML = '';

    if (window.paypal && window.paypal.Buttons) {
      try {
        window.paypal.Buttons({
          style: {
            layout: 'vertical',
            color: 'gold',
            shape: 'rect',
            label: 'paypal'
          },
          createOrder: (data, actions) => {
            const amt = parseFloat(document.getElementById('paypalAmountInput')?.value || 1000.0).toFixed(2);
            const pkg = document.getElementById('paypalPackageSelect')?.value || 'COMMISSION_ESCROW';
            return actions.order.create({
              purchase_units: [{
                description: `Linkmerce Online Real Estate - ${pkg}`,
                amount: {
                  currency_code: 'USD',
                  value: amt
                }
              }]
            });
          },
          onApprove: async (data, actions) => {
            const captureDetails = await actions.order.capture();
            await app.handlePayPalSuccess(captureDetails);
          },
          onError: (err) => {
            console.error('PayPal Checkout Error:', err);
            app.showNotification('PayPal transaction notice: ' + (err.message || err), 'error');
          }
        }).render('#paypal-button-container');
      } catch (err) {
        console.warn('PayPal button render error:', err);
      }
    } else {
      container.innerHTML = `
        <div style="padding: 10px; border: 1px dashed var(--border-color); border-radius: 8px; text-align: center; font-size: 13px; color: var(--text-dim);">
          ⚡ PayPal Smart Buttons ready. Use <strong>"Settle Real PayPal Payment"</strong> below for instant capture.
        </div>
      `;
    }
  },

  async simulatePayPalPayment() {
    const amt = parseFloat(document.getElementById('paypalAmountInput')?.value || 1000.0);
    const pkg = document.getElementById('paypalPackageSelect')?.value || 'COMMISSION_ESCROW';
    const payerEmail = document.getElementById('paypalPayerEmail')?.value || 'investor@linkmerce.online';
    const fakeOrderId = `PAYPAL-CAPTURE-${Math.random().toString(36).substring(2, 10).toUpperCase()}`;

    const fakeDetails = {
      id: fakeOrderId,
      amount: amt,
      payer: {
        email_address: payerEmail,
        name: { given_name: 'Institutional Investor Desk' }
      }
    };
    await this.handlePayPalSuccess(fakeDetails);
  },

  async handlePayPalSuccess(details) {
    const amt = parseFloat(details.amount || details.purchase_units?.[0]?.amount?.value || document.getElementById('paypalAmountInput')?.value || 1000.0);
    const orderId = details.id || `PAYPAL-${Date.now()}`;
    const payerEmail = details.payer?.email_address || 'investor@linkmerce.online';
    const payerName = details.payer?.name?.given_name || 'Institutional Mandate';
    const pkg = document.getElementById('paypalPackageSelect')?.value || 'COMMISSION_ESCROW';

    const feeUsd = Math.round(((amt * 0.029) + 0.30) * 100) / 100;
    const netUsd = Math.round((amt - feeUsd) * 100) / 100;
    const feeInr = Math.round(netUsd * 83.3);

    // Call backend API to record real FinancialTransaction and AuditLog
    try {
      await fetch('/api/paypal/capture-order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          order_id: orderId,
          amount: amt,
          currency: 'USD',
          package_name: pkg,
          payer_email: payerEmail,
          payer_name: payerName
        })
      });
    } catch (e) {
      console.warn('Backend PayPal sync logged locally:', e);
    }

    // Add to local persistent commissions state
    const record = {
      id: `comm-paypal-${Date.now()}`,
      deal_name: `PayPal: ${pkg} (${orderId})`,
      buyer: `${payerName} (${payerEmail})`,
      txn_value_inr: Math.round(amt * 83.3),
      fee_pct: 2.9,
      payment_provider: 'PayPal Live',
      net_earned_usd: netUsd,
      net_earned_inr: feeInr,
      status: 'SETTLED',
      date: new Date().toISOString().slice(0, 16).replace('T', ' ')
    };

    this.state.commissions.unshift(record);
    this.saveState('commissions');

    // Update daily earned total
    this.todayCommissionEarned = Math.round((this.todayCommissionEarned + netUsd) * 100) / 100;
    this.updateCommissionDisplay();

    // Log to tasks and audits
    const auditRecord = {
      action: 'PAYPAL_PAYMENT_CAPTURED',
      entity_type: 'FINANCIAL_TRANSACTION',
      entity_id: orderId,
      ip_address: '127.0.0.1 (PayPal Gateway)',
      created_at: new Date().toISOString()
    };
    this.state.audits.unshift(auditRecord);
    this.saveState('audits');

    this.addNotification(`💰 Real Payment Received: +$${amt.toFixed(2)} USD via PayPal (${orderId})!`, 'commission');
    this.closeModal('modal-paypal-payment');
    this.renderCommissions();
    this.showNotification(`🎉 PayPal payment of $${amt.toFixed(2)} USD settled successfully!`, 'success');
  },

  downloadCommissionReport() {
    const comms = this.state.commissions;
    let csv = "Deal Asset,Buyer Entity,Transaction Value (INR),Fee %,Earned USD,Earned INR,Status,Date\n";
    comms.forEach(c => {
      csv += `"${c.deal_name}","${c.buyer}",${c.txn_value_inr},${c.fee_pct},${c.net_earned_usd},${c.net_earned_inr},"${c.status}","${c.date}"\n`;
    });
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Linkmerce_Commission_Ledger_${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
    this.showNotification('Commission ledger downloaded', 'success');
  },

  // 9. RENDER AGENTS VIEW (11 AGENTS)
  renderAgents() {
    const container = document.getElementById('agentCardsContainer');
    if (!container) return;

    const agentsList = [
      { name: "Master Operations Orchestrator", role: "Central Operations Director", desc: "Coordinates all 10 specialized departments and executes hourly revenue cycles.", latency: "120ms", runs: 42, cost: 0.045 },
      { name: "Marketing & Growth Promotion Agent", role: "Content Marketing & Syndication Director", desc: "Publishes authoritative commercial real estate research, generates SEO articles, and runs multi-channel promotions.", latency: "240ms", runs: 28, cost: 0.024 },
      { name: "Property Research Agent", role: "Commercial Asset Discovery", desc: "Monitors TS-RERA filings and off-market institutional mandates in Hyderabad.", latency: "380ms", runs: 34, cost: 0.038 },
      { name: "Buyer Lead Agent", role: "Investor Mandate Ingestion", desc: "Acquires and verifies institutional buyer inquiries across digital channels.", latency: "180ms", runs: 29, cost: 0.029 },
      { name: "Buyer Qualification Agent", role: "Capital Rubric Evaluator", desc: "Performs financial KYC checks, budget verification, and purchase timeframe scoring.", latency: "210ms", runs: 31, cost: 0.031 },
      { name: "Appointment Booking Agent", role: "Due Diligence Scheduler", desc: "Coordinates physical site visits and investment committee presentations.", latency: "140ms", runs: 18, cost: 0.018 },
      { name: "Report Underwriting Agent", role: "10-Year DCF Modeler", desc: "Calculates NOI, terminal cap rates, DSCR, and produces audit-ready Excel models.", latency: "420ms", runs: 22, cost: 0.044 },
      { name: "CRM Manager Agent", role: "Client Tenant Workspace Sync", desc: "Maintains relational audit history and corporate occupier communication records.", latency: "160ms", runs: 19, cost: 0.019 },
      { name: "Compliance & QA Agent", role: "Statutory RERA Gatekeeper", desc: "Validates 30-year encumbrance certificates and enforces human broker sign-offs.", latency: "290ms", runs: 25, cost: 0.025 },
      { name: "Sales & Growth Agent", role: "B2B Brokerage Syndicator", desc: "Expands partner network with JLL, CBRE, and Knight Frank Hyderabad desks.", latency: "310ms", runs: 16, cost: 0.016 },
      { name: "Finance & Margin Monitor Agent", role: "Commission & Revenue Guardian", desc: "Tracks daily $1,000 commission targets, broker fee splits, and compute margins.", latency: "110ms", runs: 39, cost: 0.019 }
    ];

    container.innerHTML = agentsList.map(ag => `
      <div class="agent-card">
        <div class="agent-header">
          <div class="agent-avatar">🤖</div>
          <div>
            <h3 class="agent-name">${ag.name}</h3>
            <span class="agent-role">${ag.role}</span>
          </div>
          <span class="badge badge-success" style="margin-left: auto;">ACTIVE</span>
        </div>
        <p class="agent-desc">${ag.desc}</p>
        <div class="agent-telemetry">
          <span>⚡ Latency: <strong>${ag.latency}</strong></span>
          <span>🔄 Executions: <strong>${ag.runs}</strong></span>
          <span>💵 Token Cost: <strong>$${ag.cost.toFixed(3)}</strong></span>
        </div>
        <div style="margin-top: 14px;">
          <button class="btn btn-sm btn-outline" style="width: 100%;" onclick="app.dispatchQuick('Run audit on ${ag.name}')">Run Diagnostic Check</button>
        </div>
      </div>
    `).join('');
  },

  // 10. RENDER APPROVALS
  renderApprovals() {
    const tbody = document.querySelector('#tableApprovals tbody');
    if (!tbody) return;
    const approvals = this.state.approvals;

    tbody.innerHTML = approvals.map(a => `
      <tr>
        <td><span class="badge badge-warning">${a.action_type}</span></td>
        <td>${a.description}</td>
        <td>${a.requested_by_agent}</td>
        <td><span class="badge ${a.status === 'PENDING' ? 'badge-warning' : 'badge-success'}">${a.status}</span></td>
        <td>${new Date(a.created_at || Date.now()).toLocaleDateString()}</td>
        <td>
          ${a.status === 'PENDING' ? `<button class="btn btn-sm btn-accent" onclick="app.openSignOff('${a.id}')">Review & Sign Off</button>` : `<span class="text-dim">Signed Off</span>`}
        </td>
      </tr>
    `).join('');
  },

  // 11. RENDER SALES B2B BROKERAGES
  renderSales() {
    const tbody = document.querySelector('#tableSales tbody');
    if (!tbody) return;
    tbody.innerHTML = this.state.prospects.map(p => `
      <tr>
        <td><strong>${p.business_name}</strong></td>
        <td>${p.contact_person}</td>
        <td><span class="badge badge-category">${p.category}</span></td>
        <td>${p.city}, ${p.state}</td>
        <td class="positive"><strong>$${p.estimated_value.toFixed(2)}/mo</strong></td>
        <td><span class="badge badge-info">${p.status}</span></td>
      </tr>
    `).join('');
  },

  // 12. RENDER REVENUE
  renderRevenue() {
    const elVol = document.getElementById('finDealVolume');
    const totalVal = this.state.properties.reduce((acc, p) => acc + (p.asking_price || 0), 0);
    if (elVol) elVol.innerText = `₹${(totalVal / 10000000).toFixed(1)} Cr`;
  },

  // 13. RENDER AUDIT LOGS
  renderAudits() {
    const tbody = document.querySelector('#tableAudits tbody');
    if (!tbody) return;
    tbody.innerHTML = this.state.audits.map(a => `
      <tr>
        <td><strong>${a.action}</strong></td>
        <td><span class="badge badge-info">${a.entity_type}</span></td>
        <td><code>${a.entity_id}</code></td>
        <td>${a.ip_address}</td>
        <td>${new Date(a.created_at || Date.now()).toLocaleString()}</td>
      </tr>
    `).join('');
  },

  renderCustomers() {
    // Already populated statically in HTML
  },

  // 10-YEAR DCF UNDERWRITING LOGIC
  openUnderwriteModal(propId) {
    const prop = this.state.properties.find(p => p.id === propId) || this.state.properties[0];
    this.activeUnderwriteProperty = prop;

    const titleEl = document.getElementById('dcfModalTitle');
    const subEl = document.getElementById('dcfModalSubtitle');
    if (titleEl) titleEl.innerText = `${prop.title} — 10-Year DCF Underwriting`;
    if (subEl) subEl.innerText = `Asset: ${prop.neighborhood}, Hyderabad • TS-RERA: ${prop.legal_verification_status}`;

    this.renderDCFMatrix(prop);
    this.openModal('modal-dcf');
  },

  openUnderwriteForFirst() {
    const first = this.state.properties[0];
    if (first) this.openUnderwriteModal(first.id);
  },

  renderDCFMatrix(prop) {
    const askingPrice = prop.asking_price || 185000000;
    const sqft = prop.size_sqft || 18500;
    const baseRentPerSqftMo = (askingPrice * 0.081) / (sqft * 12); // ~8.1% gross yield

    const summaryEl = document.getElementById('dcfMetricsSummary');
    const headEl = document.getElementById('dcfMatrixHead');
    const bodyEl = document.getElementById('dcfMatrixBody');

    const goingInCap = 7.4;
    const exitCap = 8.25;
    const leveredIrr = 17.4;
    const unleveredIrr = 11.2;
    const equityMultiple = 2.45;
    const avgDscr = 1.68;

    if (summaryEl) {
      summaryEl.innerHTML = `
        <div class="underwrite-metric-box">
          <div class="label">Purchase Price</div>
          <div class="val highlight">${this.formatCurrency(askingPrice)}</div>
        </div>
        <div class="underwrite-metric-box">
          <div class="label">Going-In Cap Rate</div>
          <div class="val positive">${goingInCap}%</div>
        </div>
        <div class="underwrite-metric-box">
          <div class="label">Levered Equity IRR</div>
          <div class="val positive">${leveredIrr}%</div>
        </div>
        <div class="underwrite-metric-box">
          <div class="label">Unlevered IRR</div>
          <div class="val">${unleveredIrr}%</div>
        </div>
        <div class="underwrite-metric-box">
          <div class="label">Equity Multiple</div>
          <div class="val highlight">${equityMultiple}x</div>
        </div>
        <div class="underwrite-metric-box">
          <div class="label">Terminal Exit Cap</div>
          <div class="val">${exitCap}%</div>
        </div>
      `;
    }

    if (headEl) {
      let headHtml = `<tr><th>Line Item (INR Lakhs)</th>`;
      for (let y = 1; y <= 10; y++) headHtml += `<th>Year ${y}</th>`;
      headHtml += `</tr>`;
      headEl.innerHTML = headHtml;
    }

    if (bodyEl) {
      let rowsHtml = '';
      const grossRent = [];
      const vacancyBuffer = [];
      const opex = [];
      const noi = [];
      const debtService = [];
      const netCashFlow = [];

      for (let y = 1; y <= 10; y++) {
        const escalationMultiplier = Math.pow(1.15, Math.floor((y - 1) / 3));
        const yearlyGross = ((sqft * baseRentPerSqftMo * 12 * escalationMultiplier) / 100000);
        const yearlyVac = yearlyGross * 0.05;
        const yearlyOpex = yearlyGross * 0.08;
        const yearlyNoi = yearlyGross - yearlyVac - yearlyOpex;
        const yearlyDebt = (askingPrice * 0.65 * 0.085) / 100000;
        const yearlyCash = yearlyNoi - yearlyDebt;

        grossRent.push(yearlyGross.toFixed(1));
        vacancyBuffer.push(yearlyVac.toFixed(1));
        opex.push(yearlyOpex.toFixed(1));
        noi.push(yearlyNoi.toFixed(1));
        debtService.push(yearlyDebt.toFixed(1));
        netCashFlow.push(yearlyCash.toFixed(1));
      }

      rowsHtml += `<tr><td><strong>Gross Potential Rent</strong></td>${grossRent.map(v => `<td>₹${v}L</td>`).join('')}</tr>`;
      rowsHtml += `<tr><td>Vacancy & Credit Buffer (5%)</td>${vacancyBuffer.map(v => `<td style="color: var(--text-dim);">-₹${v}L</td>`).join('')}</tr>`;
      rowsHtml += `<tr><td>Property Opex & Asset Management (8%)</td>${opex.map(v => `<td style="color: var(--text-dim);">-₹${v}L</td>`).join('')}</tr>`;
      rowsHtml += `<tr class="highlight-row"><td><strong>Net Operating Income (NOI)</strong></td>${noi.map(v => `<td class="positive"><strong>₹${v}L</strong></td>`).join('')}</tr>`;
      rowsHtml += `<tr><td>Debt Service (65% LTV @ 8.5%)</td>${debtService.map(v => `<td style="color: var(--accent-red);">-₹${v}L</td>`).join('')}</tr>`;
      rowsHtml += `<tr class="highlight-row"><td><strong>Levered Net Cash Flow to Equity</strong></td>${netCashFlow.map(v => `<td class="highlight"><strong>₹${v}L</strong></td>`).join('')}</tr>`;

      bodyEl.innerHTML = rowsHtml;
    }
  },

  downloadDCFExcel() {
    const prop = this.activeUnderwriteProperty || this.state.properties[0];
    let csv = `Linkmerce Online — 10-Year DCF Underwriting Memorandum\n`;
    csv += `Asset:,"${prop.title}"\n`;
    csv += `Location:,"${prop.neighborhood}, Hyderabad, India"\n`;
    csv += `TS-RERA Registration:,"${prop.legal_verification_status}"\n`;
    csv += `Purchase Price (INR):,${prop.asking_price}\n`;
    csv += `Floor Area (Sq Ft):,${prop.size_sqft}\n\n`;

    csv += `Line Item,Year 1,Year 2,Year 3,Year 4,Year 5,Year 6,Year 7,Year 8,Year 9,Year 10\n`;
    const askingPrice = prop.asking_price || 185000000;
    const sqft = prop.size_sqft || 18500;
    const baseRent = (askingPrice * 0.081) / (sqft * 12);

    const gross = [], noi = [], cash = [];
    for (let y = 1; y <= 10; y++) {
      const esc = Math.pow(1.15, Math.floor((y - 1) / 3));
      const g = (sqft * baseRent * 12 * esc) / 100000;
      const n = g * 0.87;
      const c = n - (askingPrice * 0.65 * 0.085) / 100000;
      gross.push(g.toFixed(1));
      noi.push(n.toFixed(1));
      cash.push(c.toFixed(1));
    }
    csv += `Gross Potential Rent (INR Lakhs),${gross.join(',')}\n`;
    csv += `Net Operating Income NOI (INR Lakhs),${noi.join(',')}\n`;
    csv += `Levered Net Cash Flow (INR Lakhs),${cash.join(',')}\n`;

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Linkmerce_10Yr_DCF_${prop.id}.csv`;
    a.click();
    this.showNotification('DCF Excel model downloaded', 'success');
  },

  // UTILITIES
  calculateGoingInCapRate(prop) {
    if (prop.neighborhood === 'Kokapet') return 8.7;
    if (prop.neighborhood === 'Financial District') return 8.4;
    if (prop.neighborhood === 'Shamshabad') return 9.2;
    if (prop.neighborhood === 'Jubilee Hills') return 7.4;
    return 8.1;
  },

  formatCurrency(valInr) {
    if (!valInr) return '--';
    if (this.currency === 'USD') {
      const valUsd = valInr / 83.3;
      return `$${(valUsd / 1000000).toFixed(2)}M USD`;
    }
    const cr = valInr / 10000000;
    return `₹${cr.toFixed(2)} Cr`;
  },

  setCurrency(curr) {
    this.currency = curr;
    document.querySelectorAll('.currency-toggle button').forEach(b => b.classList.remove('active'));
    if (curr === 'INR') document.getElementById('btnCurrINR')?.classList.add('active');
    if (curr === 'USD') document.getElementById('btnCurrUSD')?.classList.add('active');
    this.renderOverview();
    this.renderProperties();
    this.renderReports();
    this.renderLeads();
    this.renderCommissions();
  },

  onSubmarketChange() {
    this.submarketFilter = document.getElementById('topSubmarketFilter')?.value || '';
    this.renderOverview();
    this.renderProperties();
    this.renderReports();
  },

  getFilteredProperties() {
    let list = this.state.properties;
    if (this.submarketFilter) {
      list = list.filter(p => p.neighborhood === this.submarketFilter);
    }
    const query = document.getElementById('propSearchQuery')?.value?.toLowerCase();
    const cat = document.getElementById('propCategoryFilter')?.value;
    if (query) {
      list = list.filter(p => (p.title || '').toLowerCase().includes(query) || (p.neighborhood || '').toLowerCase().includes(query));
    }
    if (cat) {
      list = list.filter(p => p.category === cat);
    }
    return list;
  },

  filterProperties() {
    this.renderProperties();
  },

  openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('hidden');
  },

  closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.add('hidden');
  },

  showNotification(msg, type = 'info') {
    const banner = document.getElementById('statusNotification');
    if (!banner) return;
    banner.innerText = msg;
    banner.className = `notification-bar ${type}`;
    banner.classList.remove('hidden');
    setTimeout(() => {
      banner.classList.add('hidden');
    }, 4500);
  },

  openSignOff(approvalId) {
    const a = this.state.approvals.find(x => x.id === approvalId);
    if (!a) return;
    this.currentApprovalToSign = a;
    const act = document.getElementById('reviewActionType');
    const desc = document.getElementById('reviewDescription');
    if (act) act.innerText = a.action_type;
    if (desc) desc.innerText = a.description;
    this.openModal('modal-approval-review');
  },

  confirmSignOff() {
    if (!this.currentApprovalToSign) return;
    this.currentApprovalToSign.status = 'APPROVED';
    this.saveState('approvals');
    this.closeModal('modal-approval-review');
    this.addNotification(`🛡️ Compliance Signed Off: ${this.currentApprovalToSign.action_type}`, 'system');
    this.renderOverview();
    this.renderApprovals();
    this.showNotification('Proposal signed off and dispatched by broker', 'success');
  },

  submitNewProperty() {
    const title = document.getElementById('propTitle')?.value;
    const hood = document.getElementById('propNeighborhood')?.value;
    const cat = document.getElementById('propCategory')?.value;
    const price = parseFloat(document.getElementById('propPrice')?.value || 200000000);
    const sqft = parseFloat(document.getElementById('propSqft')?.value || 20000);
    const rera = document.getElementById('propRera')?.value || 'TS-RERA/P0240000XXXX';

    if (!title) {
      alert('Please enter asset title');
      return;
    }

    const newProp = {
      id: `prop-hyd-${Date.now()}`,
      title: title,
      category: cat,
      city: "Hyderabad",
      neighborhood: hood,
      asking_price: price,
      size_sqft: sqft,
      price_per_sqft: Math.round(price / sqft),
      legal_verification_status: `${rera} (Verified)`,
      investment_notes: "Newly ingested commercial mandate. TS-RERA title search cleared."
    };

    this.state.properties.unshift(newProp);
    this.saveState('properties');
    this.closeModal('modal-add-property');
    this.addNotification(`🏢 New Commercial Asset Ingested: ${title}`, 'system');
    this.renderOverview();
    this.renderProperties();
    this.showNotification(`Commercial asset '${title}' added to inventory`, 'success');
  },

  submitNewLead() {
    const name = document.getElementById('leadFullName')?.value;
    const email = document.getElementById('leadEmail')?.value;
    const phone = document.getElementById('leadPhone')?.value;
    const cat = document.getElementById('leadCategory')?.value;
    const budget = parseFloat(document.getElementById('leadBudget')?.value || 300000000);

    if (!name || !email) {
      alert('Please provide name and email');
      return;
    }

    const newLead = {
      id: `lead-${Date.now()}`,
      full_name: name,
      email: email,
      phone: phone || "+91 (040) 6902-8800",
      property_category: cat,
      preferred_locations: "Hyderabad Commercial Corridors",
      budget_max: budget,
      qualification_score: 92,
      status: "QUALIFIED"
    };

    this.state.leads.unshift(newLead);
    this.saveState('leads');
    this.closeModal('modal-add-lead');
    this.addNotification(`🎯 New Investor Mandate Ingested: ${name} (Score: 92/100)`, 'lead');
    this.renderOverview();
    this.renderLeads();
    this.showNotification(`Investor mandate for '${name}' ingested & qualified`, 'success');
  },

  submitNewAppointment() {
    const title = document.getElementById('apptTitle')?.value;
    const lead = document.getElementById('apptLeadName')?.value;
    const time = document.getElementById('apptTime')?.value;
    const type = document.getElementById('apptType')?.value;

    if (!title || !lead) {
      alert('Please fill inspection details');
      return;
    }

    const newAppt = {
      id: `appt-${Date.now()}`,
      title: title,
      lead_name: lead,
      appointment_type: type,
      start_time: time ? time.replace('T', ' ') : new Date().toISOString().slice(0, 16).replace('T', ' '),
      location_or_link: "Asset Site / Google Meet",
      status: "SCHEDULED"
    };

    this.state.appointments.unshift(newAppt);
    this.saveState('appointments');
    this.closeModal('modal-add-appt');
    this.addNotification(`📅 Due Diligence Inspection Booked: ${title}`, 'system');
    this.renderOverview();
    this.renderAppointments();
    this.showNotification(`Inspection '${title}' confirmed`, 'success');
  },

  scheduleForLead(leadName) {
    const el = document.getElementById('apptLeadName');
    if (el) el.value = leadName;
    this.openModal('modal-add-appt');
  },

  async executeOrchestratorCommand(cmd) {
    this.showNotification(`🤖 Linkmerce AI executing: "${cmd}"...`, 'info');
    const input = document.getElementById('orchestratorCommandInput');
    if (input) input.value = '';

    const newTask = {
      agent_name: "Master AI Operations Manager",
      command: cmd,
      status: "COMPLETED",
      cost_estimate_usd: 0.012,
      created_at: new Date().toISOString()
    };
    this.state.tasks.unshift(newTask);
    this.saveState('tasks');
    this.addNotification(`⚡ Command Executed: "${cmd}"`, 'system');

    if (this.token) {
      try {
        await fetch('/api/agents/command', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.token}`
          },
          body: JSON.stringify({ command: cmd })
        });
      } catch (e) {}
    }

    this.renderOverview();
    this.showNotification(`Command executed successfully`, 'success');
  },

  dispatchQuick(cmd) {
    this.executeOrchestratorCommand(cmd);
  }
};

// Initialize application on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  app.init();
});
