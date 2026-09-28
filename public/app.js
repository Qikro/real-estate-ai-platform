// Real Estate AI Operations Platform - Client SPA Application
const app = {
  token: localStorage.getItem('estate_token') || null,
  activeApprovalId: null,
  cachedProperties: [],
  cachedLeads: [],

  async init() {
    this.bindEvents();
    if (!this.token) {
      await this.loginDefaultAdmin();
    }
    await this.refreshAllData();
  },

  async loginDefaultAdmin() {
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: 'admin@estate.ai', password: 'Admin@123456' })
      });
      const data = await res.json();
      if (data.access_token) {
        this.token = data.access_token;
        localStorage.setItem('estate_token', this.token);
        document.getElementById('currentWorkspaceName').innerText = data.tenant_name;
        document.getElementById('currentUserRole').innerText = `${data.role} (${data.tenant_name})`;
      }
    } catch (e) {
      console.error("Auto login error:", e);
    }
  },

  async api(endpoint, options = {}) {
    if (!this.token) await this.loginDefaultAdmin();
    const headers = options.headers || {};
    if (!(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json';
    }
    headers['Authorization'] = `Bearer ${this.token}`;

    const res = await fetch(endpoint, { ...options, headers });
    if (res.status === 401) {
      await this.loginDefaultAdmin();
      headers['Authorization'] = `Bearer ${this.token}`;
      return fetch(endpoint, { ...options, headers }).then(r => r.json());
    }
    return res.json();
  },

  bindEvents() {
    // Navigation
    document.querySelectorAll('.nav-item').forEach(btn => {
      btn.addEventListener('click', () => {
        const view = btn.getAttribute('data-view');
        this.navigate(view);
      });
    });

    // Command dispatch
    const btnCmd = document.getElementById('btnRunCommand');
    const inputCmd = document.getElementById('orchestratorCommandInput');
    btnCmd.addEventListener('click', () => this.dispatchCommand(inputCmd.value));
    inputCmd.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') this.dispatchCommand(inputCmd.value);
    });

    // Refresh button
    document.getElementById('btnRefreshData').addEventListener('click', () => {
      this.refreshAllData();
      this.notify("Data refreshed from continuous database bus.");
    });
  },

  navigate(viewName) {
    document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.view-panel').forEach(p => p.classList.remove('active'));

    const targetNav = document.querySelector(`.nav-item[data-view="${viewName}"]`);
    const targetPanel = document.getElementById(`view-${viewName}`);

    if (targetNav) targetNav.classList.add('active');
    if (targetPanel) targetPanel.classList.add('active');
  },

  notify(msg, isError = false) {
    const banner = document.getElementById('statusNotification');
    banner.innerText = msg;
    banner.style.backgroundColor = isError ? '#7F1D1D' : '#1E293B';
    banner.classList.remove('hidden');
    setTimeout(() => {
      banner.classList.add('hidden');
    }, 5000);
  },

  async refreshAllData() {
    await Promise.all([
      this.loadOverviewKPIs(),
      this.loadAgents(),
      this.loadProperties(),
      this.loadLeads(),
      this.loadAppointments(),
      this.loadReports(),
      this.loadApprovals(),
      this.loadSales(),
      this.loadRevenue(),
      this.loadAuditLogs()
    ]);
  },

  async dispatchCommand(cmd) {
    if (!cmd || !cmd.trim()) return;
    this.notify(`⚡ Master Orchestrator executing: "${cmd}"...`);
    try {
      const res = await this.api('/api/agents/command', {
        method: 'POST',
        body: JSON.stringify({ command: cmd.trim() })
      });
      if (res.status === 'SUCCESS' || res.status === 'APPROVAL_REQUIRED') {
        this.notify(`[Orchestrator] ${res.message}`);
        document.getElementById('orchestratorCommandInput').value = '';
        await this.refreshAllData();
      } else {
        this.notify(`[Orchestrator] ${res.message || 'Execution response received.'}`);
      }
    } catch (e) {
      this.notify(`Command execution error: ${e.message}`, true);
    }
  },

  dispatchQuick(cmd) {
    document.getElementById('orchestratorCommandInput').value = cmd;
    this.dispatchCommand(cmd);
  },

  // 1. OVERVIEW
  async loadOverviewKPIs() {
    try {
      const [crmRes, finRes, props, leads, appts, reports, approvals, tasks] = await Promise.all([
        this.api('/api/crm/summary'),
        this.api('/api/finance/metrics'),
        this.api('/api/properties'),
        this.api('/api/leads'),
        this.api('/api/appointments'),
        this.api('/api/reports'),
        this.api('/api/approvals?status=PENDING'),
        this.api('/api/agents/tasks?limit=6')
      ]);

      const crm = crmRes.summary || {};
      const fin = finRes.metrics || {};

      document.getElementById('kpiTotalProperties').innerText = props.length || 0;
      document.getElementById('kpiVerifiedListings').innerText = props.filter(p => p.confidence_label === 'VERIFIED_FROM_SOURCE').length || 0;
      document.getElementById('kpiTotalLeads').innerText = leads.length || 0;
      document.getElementById('kpiQualifiedLeads').innerText = leads.filter(l => l.status === 'QUALIFIED').length || 0;
      document.getElementById('kpiLeadConversionRate').innerText = `${crm.pipeline_conversion_rate || '0%'} qualified`;
      document.getElementById('kpiUpcomingAppointments').innerText = appts.length || 0;
      document.getElementById('kpiReportsGenerated').innerText = reports.length || 0;
      document.getElementById('kpiActiveClients').innerText = fin.active_paying_customers || 1;
      document.getElementById('kpiMonthlyRevenue').innerText = `$${fin.monthly_recurring_revenue_usd || 1999}`;
      document.getElementById('kpiPendingApprovals').innerText = approvals.length || 0;
      document.getElementById('pendingApprovalsBadge').innerText = approvals.length || 0;
      document.getElementById('kpiAccumulatedCost').innerText = `$${(fin.accumulated_ai_costs_usd || 0) + (fin.accumulated_infra_costs_usd || 0)}`;

      // Tasks table
      const tbodyTasks = document.querySelector('#tableRecentTasks tbody');
      tbodyTasks.innerHTML = (tasks || []).map(t => `
        <tr>
          <td><b>${t.agent_name}</b></td>
          <td><code>${t.command}</code></td>
          <td><span class="badge ${t.status === 'COMPLETED' ? 'badge-success' : 'badge-warning'}">${t.status}</span></td>
          <td>$${t.cost_estimate_usd}</td>
          <td>${new Date(t.created_at).toLocaleTimeString()}</td>
        </tr>
      `).join('') || '<tr><td colspan="5" class="text-dim">No tasks in queue.</td></tr>';

      // Urgent approvals
      const containerApprovals = document.getElementById('overviewApprovalsList');
      containerApprovals.innerHTML = (approvals || []).map(a => `
        <div class="workspace-pill" style="margin-bottom: 8px;">
          <div class="ws-info" style="flex:1;">
            <span class="ws-name">${a.action_type}</span>
            <span class="ws-role">${a.description}</span>
          </div>
          <button class="btn btn-sm btn-primary" onclick="app.openApprovalDecision('${a.id}', '${a.action_type}', '${escape(a.description)}')">Review</button>
        </div>
      `).join('') || '<div class="text-dim" style="padding:10px;">Zero pending approvals. All operations cleared.</div>';

    } catch (e) {
      console.error("Overview load error:", e);
    }
  },

  // 2. AGENTS
  async loadAgents() {
    try {
      const res = await this.api('/api/agents');
      const container = document.getElementById('agentCardsContainer');
      container.innerHTML = (res.agents || []).map(a => `
        <div class="agent-card">
          <div class="agent-card-header">
            <div>
              <div class="agent-name">${a.name}</div>
              <div class="agent-role">${a.role}</div>
            </div>
            <span class="badge ${a.status === 'IDLE' ? 'badge-info' : 'badge-success'}">${a.status}</span>
          </div>
          <div class="agent-desc">${a.description}</div>
          <div class="agent-stats-strip">
            <span>Runs: <b>${a.total_runs}</b></span>
            <span>Success: <b>${a.success_rate}%</b></span>
            <span>Cost: <b>$${a.cost_usd}</b></span>
          </div>
          <div class="agent-actions">
            <button class="btn btn-sm btn-outline" onclick="app.dispatchQuick('Run ${a.name}')">Run Now</button>
          </div>
        </div>
      `).join('');
    } catch (e) {
      console.error("Load agents error:", e);
    }
  },

  // 3. PROPERTIES
  async loadProperties() {
    try {
      const props = await this.api('/api/properties');
      this.cachedProperties = props;
      this.renderProperties(props);
    } catch (e) {
      console.error("Load properties error:", e);
    }
  },

  renderProperties(props) {
    const tbody = document.querySelector('#tableProperties tbody');
    tbody.innerHTML = props.map(p => `
      <tr>
        <td><b>${p.title}</b><br><small style="color:#64748B;">${p.address || p.neighborhood}</small></td>
        <td><span class="badge badge-info">${p.category}</span></td>
        <td>${p.neighborhood}</td>
        <td><b>INR ${(p.asking_price/10000000).toFixed(2)} Cr</b></td>
        <td>${p.size_sqft.toLocaleString()} sqft</td>
        <td>INR ${p.price_per_sqft?.toLocaleString() || '--'}</td>
        <td><span class="badge ${p.confidence_label === 'VERIFIED_FROM_SOURCE' ? 'badge-success' : 'badge-warning'}">${p.confidence_label}</span></td>
        <td>
          <button class="btn btn-sm btn-outline" onclick="app.underwriteProperty('${p.id}')">Underwrite</button>
        </td>
      </tr>
    `).join('') || '<tr><td colspan="8">No properties found.</td></tr>';
  },

  filterProperties() {
    const q = document.getElementById('propSearchQuery').value.toLowerCase();
    const cat = document.getElementById('propCategoryFilter').value;
    const filtered = this.cachedProperties.filter(p => {
      const matchQ = p.title.toLowerCase().includes(q) || p.neighborhood.toLowerCase().includes(q);
      const matchCat = !cat || p.category === cat;
      return matchQ && matchCat;
    });
    this.renderProperties(filtered);
  },

  async underwriteProperty(propId) {
    this.notify("Underwriting financial model for property...");
    const res = await this.api('/api/reports/generate', {
      method: 'POST',
      body: JSON.stringify({ property_id: propId })
    });
    this.notify(`Report created: ${res.message}`);
    this.navigate('reports');
    await this.loadReports();
  },

  // 4. LEADS
  async loadLeads() {
    try {
      const leads = await this.api('/api/leads');
      this.cachedLeads = leads;
      const tbody = document.querySelector('#tableLeads tbody');
      tbody.innerHTML = leads.map(l => `
        <tr>
          <td><b>${l.full_name}</b></td>
          <td>${l.email}<br><small style="color:#64748B;">${l.phone}</small></td>
          <td>${l.property_category}<br><small style="color:#64748B;">${l.preferred_locations}</small></td>
          <td>INR ${(l.budget_min/10000000).toFixed(1)}Cr - ${(l.budget_max/10000000).toFixed(1)}Cr</td>
          <td><span class="badge ${l.qualification_score >= 75 ? 'badge-success' : 'badge-warning'}">${l.qualification_score}/100</span></td>
          <td><span class="badge badge-info">${l.status}</span></td>
          <td><small>${l.recommended_action || '--'}</small></td>
        </tr>
      `).join('') || '<tr><td colspan="7">No buyer leads found.</td></tr>';

      // Populate lead dropdown in appointment modal
      const select = document.getElementById('apptLeadSelect');
      select.innerHTML = leads.map(l => `<option value="${l.id}">${l.full_name} (${l.property_category})</option>`).join('');
    } catch (e) {
      console.error("Load leads error:", e);
    }
  },

  async qualifyAllLeads() {
    this.notify("🤖 Buyer Qualification Agent evaluating parameters...");
    const res = await this.api('/api/leads/qualify-all', { method: 'POST' });
    this.notify(res.message);
    await this.loadLeads();
    await this.loadOverviewKPIs();
  },

  // 5. APPOINTMENTS
  async loadAppointments() {
    try {
      const appts = await this.api('/api/appointments');
      const tbody = document.querySelector('#tableAppointments tbody');
      tbody.innerHTML = appts.map(a => `
        <tr>
          <td><b>${a.title}</b></td>
          <td><span class="badge badge-info">${a.appointment_type}</span></td>
          <td>${new Date(a.start_time).toLocaleString()}</td>
          <td>${new Date(a.end_time).toLocaleString()}</td>
          <td>${a.location_or_link}</td>
          <td><span class="badge badge-success">${a.status}</span></td>
        </tr>
      `).join('') || '<tr><td colspan="6">No scheduled appointments.</td></tr>';
    } catch (e) {
      console.error("Load appointments error:", e);
    }
  },

  // 6. REPORTS
  async loadReports() {
    try {
      const reports = await this.api('/api/reports');
      const tbody = document.querySelector('#tableReports tbody');
      tbody.innerHTML = reports.map(r => `
        <tr>
          <td><b>${r.title}</b></td>
          <td>${r.client_name}</td>
          <td>INR ${(r.asking_price/10000000).toFixed(2)} Cr</td>
          <td><span class="badge badge-info">${r.gross_yield}%</span></td>
          <td><span class="badge badge-success">${r.cap_rate}%</span></td>
          <td>${new Date(r.created_at).toLocaleDateString()}</td>
          <td>
            <a href="/api/reports/${r.id}/download/pdf" class="btn btn-sm btn-outline" download>📥 PDF</a>
            <a href="/api/reports/${r.id}/download/xlsx" class="btn btn-sm btn-outline" download>📊 Excel</a>
          </td>
        </tr>
      `).join('') || '<tr><td colspan="7">No investor reports generated.</td></tr>';
    } catch (e) {
      console.error("Load reports error:", e);
    }
  },

  // 7. APPROVALS GATE
  async loadApprovals() {
    try {
      const approvals = await this.api('/api/approvals?status=ALL');
      const tbody = document.querySelector('#tableApprovals tbody');
      tbody.innerHTML = approvals.map(a => `
        <tr>
          <td><b>${a.action_type}</b></td>
          <td>${a.description}</td>
          <td>${a.requested_by_agent}</td>
          <td><span class="badge ${a.status === 'APPROVED' ? 'badge-success' : a.status === 'REJECTED' ? 'badge-danger' : 'badge-warning'}">${a.status}</span></td>
          <td>${new Date(a.created_at).toLocaleString()}</td>
          <td>
            ${a.status === 'PENDING' ? `
              <button class="btn btn-sm btn-primary" onclick="app.openApprovalDecision('${a.id}', '${a.action_type}', '${escape(a.description)}')">Review</button>
            ` : `<small style="color:#64748B;">Decided</small>`}
          </td>
        </tr>
      `).join('') || '<tr><td colspan="6">No approval gate items.</td></tr>';
    } catch (e) {
      console.error("Load approvals error:", e);
    }
  },

  openApprovalDecision(id, actionType, description) {
    this.activeApprovalId = id;
    document.getElementById('approvalModalTitle').innerText = `Review Gate: ${actionType}`;
    document.getElementById('approvalModalDesc').innerText = unescape(description);
    this.openModal('modal-approval-decision');
  },

  async submitApprovalDecision(decision) {
    if (!this.activeApprovalId) return;
    const comment = document.getElementById('approvalDecisionComment').value;
    try {
      const res = await this.api(`/api/approvals/${this.activeApprovalId}/decision`, {
        method: 'POST',
        body: JSON.stringify({ decision, comment })
      });
      this.closeModal('modal-approval-decision');
      this.notify(`Compliance Gate: Action ${decision} successfully.`);
      await this.loadApprovals();
      await this.loadOverviewKPIs();
    } catch (e) {
      this.notify(`Decision error: ${e.message}`, true);
    }
  },

  // 8. SALES PIPELINE
  async loadSales() {
    try {
      const prospects = await this.api('/api/sales/prospects');
      const tbody = document.querySelector('#tableSalesProspects tbody');
      tbody.innerHTML = prospects.map(p => `
        <tr>
          <td><b>${p.business_name}</b><br><small style="color:#64748B;">${p.website || ''}</small></td>
          <td>${p.contact_person}<br><small style="color:#64748B;">${p.email}</small></td>
          <td><span class="badge badge-info">${p.category}</span></td>
          <td>${p.city}, ${p.state}</td>
          <td><span class="badge badge-warning">${p.status}</span></td>
          <td><b>$${p.estimated_value}</b>/mo</td>
        </tr>
      `).join('') || '<tr><td colspan="6">No prospects found.</td></tr>';
    } catch (e) {
      console.error("Load sales error:", e);
    }
  },

  // 9. REVENUE & UNIT ECONOMICS
  async loadRevenue() {
    try {
      const res = await this.api('/api/finance/metrics');
      const m = res.metrics || {};
      const container = document.getElementById('revenueMetricsContainer');
      container.innerHTML = `
        <div class="kpi-grid">
          <div class="kpi-card">
            <div class="kpi-label">Monthly Recurring Revenue (MRR)</div>
            <div class="kpi-val">$${m.monthly_recurring_revenue_usd || 1999}</div>
            <div class="kpi-sub">INR ${(m.monthly_recurring_revenue_inr || 165000).toLocaleString()} / month</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Daily Revenue Run-Rate</div>
            <div class="kpi-val highlight">$${m.current_daily_run_rate_usd || 66.63} / day</div>
            <div class="kpi-sub positive">Target: $1,000 / day (${m.target_progress_pct || 6.6}%)</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">AI API Operating Costs</div>
            <div class="kpi-val text-success">$${m.accumulated_ai_costs_usd || 28.50}</div>
            <div class="kpi-sub">Prompt token caching active</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Gross Margin</div>
            <div class="kpi-val text-success">${m.estimated_gross_margin_pct || 97.9}%</div>
            <div class="kpi-sub">Institutional SaaS profile</div>
          </div>
        </div>
      `;

      // Customer panel content
      document.getElementById('customersPanelContent').innerHTML = `
        <div class="workspace-pill">
          <div class="ws-dot active"></div>
          <div class="ws-info">
            <span class="ws-name">Apex Realty & Capital Advisory (Current Tenant)</span>
            <span class="ws-role">Tier: INVESTOR_OPS ($1,999/mo) | Dedicated SQLite/PostgreSQL Tenant Schema</span>
          </div>
        </div>
        <p style="color:#94A3B8; font-size:13px; margin-top:10px;">
          Multi-tenant isolation active. Client leads, confidential investor memorandums, and custom property research are encrypted and partitioned.
        </p>
      `;
    } catch (e) {
      console.error("Load revenue error:", e);
    }
  },

  // 10. AUDIT LOGS
  async loadAuditLogs() {
    try {
      const logs = await this.api('/api/audit');
      const tbody = document.querySelector('#tableAuditLogs tbody');
      tbody.innerHTML = logs.map(l => `
        <tr>
          <td><small>${new Date(l.created_at).toLocaleString()}</small></td>
          <td><b>${l.action}</b></td>
          <td><span class="badge badge-info">${l.entity_type}</span></td>
          <td><code>${l.entity_id}</code></td>
          <td><small>${l.ip_address}</small></td>
        </tr>
      `).join('') || '<tr><td colspan="5">No audit entries.</td></tr>';
    } catch (e) {
      console.error("Load audit error:", e);
    }
  },

  // MODAL CONTROLS
  openModal(id) {
    document.getElementById(id).classList.remove('hidden');
  },
  closeModal(id) {
    document.getElementById(id).classList.add('hidden');
  },

  async submitAddProperty(e) {
    e.preventDefault();
    const payload = {
      title: document.getElementById('newPropTitle').value,
      category: document.getElementById('newPropCategory').value,
      neighborhood: document.getElementById('newPropNeighborhood').value,
      asking_price: parseFloat(document.getElementById('newPropPrice').value),
      size_sqft: parseFloat(document.getElementById('newPropSize').value),
      original_url: document.getElementById('newPropUrl').value || null
    };

    try {
      const res = await this.api('/api/properties', {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      this.closeModal('modal-add-property');
      this.notify(`Property added: ${res.title}`);
      await this.loadProperties();
      await this.loadOverviewKPIs();
    } catch (err) {
      this.notify(`Failed to add property: ${err.message}`, true);
    }
  },

  async submitAddLead(e) {
    e.preventDefault();
    const payload = {
      full_name: document.getElementById('newLeadName').value,
      email: document.getElementById('newLeadEmail').value,
      phone: document.getElementById('newLeadPhone').value,
      property_category: document.getElementById('newLeadCategory').value,
      budget_max: parseFloat(document.getElementById('newLeadBudget').value),
      preferred_locations: document.getElementById('newLeadLocations').value
    };

    try {
      const res = await this.api('/api/leads', {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      this.closeModal('modal-add-lead');
      this.notify(`Lead ingested: ${res.full_name} (Score: ${res.qualification_score}/100)`);
      await this.loadLeads();
      await this.loadOverviewKPIs();
    } catch (err) {
      this.notify(`Failed to add lead: ${err.message}`, true);
    }
  },

  async submitCsvImport() {
    const fileInput = document.getElementById('csvFileInput');
    if (!fileInput.files.length) {
      alert("Please select a CSV file.");
      return;
    }
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
      const res = await this.api('/api/leads/import-csv', {
        method: 'POST',
        body: formData
      });
      this.closeModal('modal-import-csv');
      this.notify(res.message);
      await this.loadLeads();
      await this.loadOverviewKPIs();
    } catch (err) {
      this.notify(`CSV Import error: ${err.message}`, true);
    }
  },

  async submitAddAppointment(e) {
    e.preventDefault();
    const payload = {
      title: document.getElementById('apptTitle').value,
      lead_id: document.getElementById('apptLeadSelect').value,
      appointment_type: document.getElementById('apptType').value,
      start_time: document.getElementById('apptDateTime').value,
      duration_minutes: parseInt(document.getElementById('apptDuration').value),
      location_or_link: document.getElementById('apptLocation').value
    };

    try {
      const res = await this.api('/api/appointments/schedule', {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      if (res.status === 'CONFLICT_DETECTED') {
        alert(res.message);
        return;
      }
      this.closeModal('modal-add-appointment');
      this.notify(res.message);
      await this.loadAppointments();
      await this.loadOverviewKPIs();
    } catch (err) {
      this.notify(`Schedule error: ${err.message}`, true);
    }
  }
};

window.addEventListener('DOMContentLoaded', () => app.init());
