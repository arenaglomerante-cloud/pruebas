# Roadmap - GEX Quant Analysis Platform

## Visión General

GammaDesk Terminal es una plataforma de análisis cuantitativo de microestructura de derivados que combina:
- **IP Cuantitativa**: Cálculo de gamma exposure (Black-Scholes) con Python
- **UI Institucional**: Terminal moderna con Next.js + Tailwind (tema dark trading)
- **LLM Táctico**: Motor de análisis con razonamiento integrado (z-ai SDK)
- **Datos Reales**: Integración Alpaca Markets con fallbacks automáticos

---

## Timeline & Fases

### 🟢 **FASE 1: MVP Completo** (v0.2.0) ✅ COMPLETADO
**Estado**: Producción-ready | Lint: 0 errores | E2E verificado

#### ✅ Hitos Alcanzados
- [x] GEX Calculator Python (Black-Scholes gamma/vega)
- [x] Options Chain fetcher (yfinance integration)
- [x] Alpaca data adapter con fallbacks
- [x] GammaMap SVG interactiva
- [x] ScenarioMatrix IF/THEN
- [x] LLM Quant Analyst engine
- [x] Session persistence (Prisma SQLite)
- [x] UI Terminal oscura (institutional theme)
- [x] E2E testing con VLM
- [x] SKILL.md documentation

#### 📊 Métricas
| Métrica | Target | Actual |
|---------|--------|--------|
| Lint errors | 0 | ✅ 0 |
| Type coverage | 100% | ✅ 100% |
| E2E pass rate | 100% | ✅ 100% (6/6) |
| Response time | <45s | ✅ ~40s |
| Mobile responsive | Yes | ✅ Verified |

---

### 🟡 **FASE 2: Robustness & Stability** (v0.2.1) ⏳ EN PROGRESO
**Duración estimada**: 2 semanas | **Prioridad**: CRÍTICA

#### 🎯 Objetivos
- [ ] **Error Handling Robusto**
  - [ ] Timeouts en child_process (30s max)
  - [ ] Retry logic con backoff exponencial
  - [ ] Graceful degradation en fallos de datos
  - [ ] Error boundaries en componentes críticos

- [ ] **Input Validation**
  - [ ] Schema validation con Zod en `/api/analyze`
  - [ ] Sanitización de inputs del usuario
  - [ ] Type guards en Python service
  - [ ] Boundary testing (valores extremos)

- [ ] **Database Hardening**
  - [ ] Índices en tabla AnalysisSession
  - [ ] Backup automático de SQLite
  - [ ] Migration scripts robustos
  - [ ] Query optimization

- [ ] **Logging & Monitoring**
  - [ ] Structured logging (pino o winston)
  - [ ] Error tracking (Sentry integration)
  - [ ] Performance metrics (analytics)
  - [ ] Audit trail de sesiones

#### 📋 Tareas Específicas
```
[ ] src/app/api/scan/route.ts
    - [ ] Add timeout handling
    - [ ] Retry logic on Python failure
    - [ ] Detailed error responses

[ ] src/app/api/analyze/route.ts
    - [ ] Zod schema validation
    - [ ] Input bounds checking
    - [ ] Rate limiting

[ ] mini-services/quant-engine/
    - [ ] Try-catch en scan_cli.py
    - [ ] Health check endpoint
    - [ ] Graceful shutdown

[ ] src/lib/
    - [ ] createZodSchemas() for all domain types
    - [ ] Input sanitizer utility

[ ] Testing
    - [ ] Unit tests for gex_calculator.py
    - [ ] Integration tests for adapters
    - [ ] Load testing (scan + analyze concurrent)
```

#### 📅 Sprint Breakdown
**Sprint 2.1** (Week 1-2):
- Child process timeout + error handling
- Zod validation schemas
- Python exception handling

**Sprint 2.2** (Week 3-4):
- Database hardening
- Logging infrastructure
- Performance benchmarks

---

### 🔵 **FASE 3: Feature Richness** (v0.3.0) ⏳ PLANIFICADO
**Duración estimada**: 4 semanas | **Prioridad**: ALTA

#### 🎯 Objetivos
- [ ] **Análisis Comparativo**
  - [ ] Modo "Compare DTEs" (7DTE vs 30DTE vs 60DTE)
  - [ ] Side-by-side GammaMaps
  - [ ] LLM divergence analysis
  - [ ] Historical comparison (archivo sesiones previas)

- [ ] **Export & Reporting**
  - [ ] CSV export de ScenarioMatrix
  - [ ] PDF reports generados (puppeteer)
  - [ ] Email delivery de reportes
  - [ ] Scheduled reports (cron jobs)

- [ ] **Data Persistence 2.0**
  - [ ] Persistir GexCurve en sesión (Prisma)
  - [ ] Re-hydrate análisis históricos
  - [ ] Snapshot de market conditions
  - [ ] Price action replay

- [ ] **Enhanced UI/UX**
  - [ ] Tabla de detalles ampliable (Magnet Zones, Air Pockets)
  - [ ] Hovercard con estadísticas de strikes
  - [ ] Histograma de probabilidades escenarios
  - [ ] Dark mode refinamiento

#### 📋 Tareas Específicas
```
[ ] Comparative Analysis
    - [ ] src/components/quant/ComparisonView.tsx
    - [ ] Dual GammaMap layout
    - [ ] src/lib/compareAnalysis.ts utility
    - [ ] Update LLM prompt para divergences

[ ] Export Functionality
    - [ ] CSV exporter (src/lib/exporters/csv.ts)
    - [ ] PDF generator (src/lib/exporters/pdf.ts)
    - [ ] Email sender (src/lib/email.ts)
    - [ ] Background job queue (Bull/BullMQ)

[ ] Data Persistence
    - [ ] Update Prisma schema (gexCurve JSON field)
    - [ ] GexCurvePoint[] serialization
    - [ ] Replay UI component
    - [ ] Historical query optimization

[ ] UI Enhancements
    - [ ] AnalysisDetails collapsible sections
    - [ ] Strike detail cards con hover
    - [ ] Probability distribution chart
    - [ ] Theme refinements (colors, spacing)

[ ] Testing
    - [ ] E2E comparison flow
    - [ ] Export file integrity
    - [ ] Email delivery verification
```

#### 📅 Sprint Breakdown
**Sprint 3.1** (Weeks 1-2):
- Comparative analysis UI + backend
- CSV export

**Sprint 3.2** (Weeks 3-4):
- PDF generation + email
- GexCurve persistence
- UI enhancements

---

### 🔷 **FASE 4: Real-Time & Advanced** (v0.4.0) ⏳ BACKLOG
**Duración estimada**: 6 semanas | **Prioridad**: MEDIA

#### 🎯 Objetivos
- [ ] **Real-Time Updates**
  - [ ] WebSocket server (ws o Socket.io)
  - [ ] Live spot price updates
  - [ ] Auto re-scan en threshold breach
  - [ ] Push notifications

- [ ] **Advanced Analysis**
  - [ ] Multi-leg detection (spreads, condors, calendars)
  - [ ] Order flow heuristics
  - [ ] Volatility term structure analysis
  - [ ] Greeks greeks (delta, theta decay patterns)

- [ ] **Risk Metrics**
  - [ ] Vega exposure aggregación
  - [ ] Theta decay forecast
  - [ ] Rho (rates) sensitivity
  - [ ] Value at Risk (VaR) estimation

- [ ] **Backtesting Framework**
  - [ ] Historical data ingestion
  - [ ] Scenario replay (price paths)
  - [ ] Win rate statistics
  - [ ] Drawdown analysis

#### 📋 Tareas Específicas
```
[ ] WebSocket Infrastructure
    - [ ] nextjs-websocket or ws integration
    - [ ] Client connection manager
    - [ ] Message queue (price updates, scan results)
    - [ ] Reconnection logic

[ ] Live Updates
    - [ ] Alpaca stream integration
    - [ ] GammaMap real-time curve updates
    - [ ] Regime change detection
    - [ ] Alert triggers

[ ] Advanced Analysis
    - [ ] Multi-leg detection algorithm
    - [ ] Order flow inference (volume profile)
    - [ ] Term structure analyzer
    - [ ] Greeks aggregation

[ ] Risk Metrics
    - [ ] Vega aggregator (src/lib/greeks/vega.ts)
    - [ ] Theta decay projector
    - [ ] Rho sensitivity
    - [ ] VaR calculator (scipy.stats)

[ ] Backtesting
    - [ ] Historical data store (daily snapshots)
    - [ ] Price path generator
    - [ ] Scenario evaluator
    - [ ] Statistics aggregator

[ ] Testing
    - [ ] WebSocket connection tests
    - [ ] Live update latency benchmarks
    - [ ] Backtest accuracy validation
```

#### 📅 Sprint Breakdown
**Sprint 4.1** (Weeks 1-2):
- WebSocket infrastructure
- Live spot updates

**Sprint 4.2** (Weeks 3-4):
- Advanced analysis (multi-leg, order flow)
- Greeks aggregation

**Sprint 4.3** (Weeks 5-6):
- Risk metrics
- Backtesting framework

---

### 🟣 **FASE 5: Enterprise & Scaling** (v1.0.0) ⏳ FUTURE
**Duración estimada**: 8+ semanas | **Prioridad**: BAJA (cuando PMF establecido)

#### 🎯 Objetivos
- [ ] **Multi-User SaaS**
  - [ ] Authentication (Auth0 o Clerk)
  - [ ] Role-based access (RBAC)
  - [ ] Team workspaces
  - [ ] API key management

- [ ] **Scaling Infrastructure**
  - [ ] Database sharding (PostgreSQL)
  - [ ] Redis caching layer
  - [ ] Python service microservices
  - [ ] Docker/Kubernetes deployment

- [ ] **Advanced Integrations**
  - [ ] Interactive Brokers API
  - [ ] ThinkorSwim datafeed
  - [ ] Bloomberg Terminal data (enterprise)
  - [ ] Webhook alerts (Discord, Telegram, Email)

- [ ] **ML/AI Enhancements**
  - [ ] Predictive regime classifier
  - [ ] Anomaly detection (unusual GEX patterns)
  - [ ] Natural language search
  - [ ] Smart scenario generation (ML-augmented)

- [ ] **Analytics & Business Intelligence**
  - [ ] Performance tracking dashboard
  - [ ] Win/loss analytics
  - [ ] Portfolio attribution
  - [ ] Custom reporting engine

#### 📋 High-Level Tasks
```
[ ] Multi-User Architecture
    - [ ] Auth provider setup
    - [ ] User/Team schema (Prisma)
    - [ ] API key hashing + rotation
    - [ ] Session isolation

[ ] Infrastructure Scaling
    - [ ] Migrate to PostgreSQL
    - [ ] Redis integration
    - [ ] Python service containerization
    - [ ] K8s manifests

[ ] Integrations
    - [ ] IB API client
    - [ ] ThinkorSwim connector
    - [ ] Notification service (multi-channel)
    - [ ] Webhook dispatcher

[ ] ML Pipeline
    - [ ] Data collection + labeling
    - [ ] Regime predictor training
    - [ ] Anomaly detector (Isolation Forest)
    - [ ] LLM fine-tuning

[ ] Analytics
    - [ ] MetaBase or Looker setup
    - [ ] Performance queries
    - [ ] Custom metric aggregators
```

---

## Dependencias & Bloqueadores

### Actuales (v0.2.1)
| Dependencia | Estado | Impacto | ETA Fix |
|-------------|--------|--------|---------|
| z-ai SDK stability | ✅ Estable | Alto | - |
| Alpaca API rate limits | ⚠️ 100 req/min | Medio | 2 semanas |
| React 19 + Sonner | ✅ Resuelto | Alto | - |
| Python scipy builds | ⚠️ Platform-specific | Bajo | Docker needed |

### Futuras (v0.3.0+)
| Dependencia | Estado | Impacto | Workaround |
|-------------|--------|--------|-----------|
| WebSocket library choice | 📋 TODO | Alto | ws + Socket.io comparison |
| PostgreSQL migration | 📋 TODO | Alto | SQLite → Prisma migrate |
| ML training data | 📋 TODO | Medio | Synthetic data generator |
| Bloomberg/IB APIs | 📋 TODO | Bajo | Manual integration spec |

---

## Success Metrics

### Fase 2 (v0.2.1)
- [ ] 99.5% uptime (no crashes)
- [ ] 0 unhandled errors en production
- [ ] < 100ms response time (P95) para /api/sessions
- [ ] 100% input validation coverage

### Fase 3 (v0.3.0)
- [ ] 50% reduction en support tickets (better UX)
- [ ] 10+ exported reports por semana (usage signal)
- [ ] 95% user retention (reopen análisis históricos)
- [ ] < 2 min time-to-analysis (end-to-end)

### Fase 4 (v0.4.0)
- [ ] 100+ concurrent WebSocket connections
- [ ] < 500ms latency para live price updates
- [ ] 85%+ backtest accuracy vs real performance
- [ ] 4+ integrations completadas (IB, ThinkorSwim, etc)

### Fase 5 (v1.0.0)
- [ ] 1000+ paying users
- [ ] 99.99% SLA uptime
- [ ] $10k+ MRR
- [ ] < 2% churn rate

---

## Recursos & Presupuesto

### Infraestructura
- **Dev**: Vercel + Railway (Free tiers) ✅
- **Prod**: Vercel Pro ($20/mo) + Railway DB ($50+/mo)
- **Monitoring**: Sentry Free ($0) → Pro ($50/mo)
- **CDN**: Vercel included ✅

### Herramientas
- **LLM API**: z-ai ($TBD/mo based on usage)
- **Data APIs**: 
  - Alpaca ($0 paper trading, $0 for basic data)
  - yfinance ($0)
  - Bloomberg/IB (TBD when needed)

### Equipo (Estimado)
- 1x Full-stack dev (lead)
- 1x Quant researcher (part-time)
- 1x DevOps (v1.0 onwards)

---

## Decision Log

### ✅ Decisiones Tomadas
1. **Python mini-service** vs monolith
   - ✅ Preserva IP cuantitativa, separación limpia
2. **Child process** vs persistent server
   - ✅ Robusto en sandbox ephemeral
3. **SQLite** vs PostgreSQL para MVP
   - ✅ Suficiente, fácil migración después
4. **z-ai SDK** vs OpenAI API
   - ✅ Thinking habilitado, mejor razonamiento cuant
5. **Dark theme** vs light
   - ✅ Institucional, reduce eye strain

### ⏳ Por Decidir
1. Hosting postgres: Railway vs Supabase vs AWS RDS?
2. WebSocket library: ws vs Socket.io vs Hono?
3. ML framework: scikit-learn vs PyTorch?
4. Backtesting: backtrader vs custom engine?

---

## Comunicación & Feedback

### Canales
- **GitHub Issues**: Bugs, feature requests
- **Discussions**: Ideas, preguntas
- **Email**: arenaglomerante@gmail.com
- **Discord** (próximamente): Community

### Review Cadence
- Weekly standup (sync sprint progress)
- Bi-weekly demo (stakeholder updates)
- Monthly planning (next sprint planning)

---

**Última actualización**: 2026-06-26
**Versión actual**: v0.2.0 (MVP Complete)
**Siguiente hito**: v0.2.1 (Robustness) - In Progress
