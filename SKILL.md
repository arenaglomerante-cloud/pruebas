name: GEX Gamma Exposure Calculator & Analysis Engine
description: |
  Comprehensive quantitative analysis system for derivatives microstructure (NDX/NQ markets).
  Combines Black-Scholes gamma calculations with real-time options chain data and LLM-powered
  tactical reporting. Features dual architecture: Python backend (GEX computation, data adapters)
  and Next.js terminal UI with institutional-grade visualizations.

tags:
  - quantitative-analysis
  - gamma-exposure
  - options-microstructure
  - derivatives-trading
  - ndx
  - nq
  - fintech

version: "0.2.0"
author: "Arena Glomerante Cloud"
repository: "https://github.com/arenaglomerante-cloud/pruebas"

features:
  - name: "Gamma Exposure Calculator"
    description: "Black-Scholes based gamma/vega computation at multiple price levels"
    language: "Python"
    module: "src/core/gex_calculator.py"
    
  - name: "Options Chain Data Management"
    description: "Real-time options data fetching from yfinance with cleaning and analysis"
    language: "Python"
    module: "src/core/options_chain.py"
    
  - name: "Alpaca Paper Trading Integration"
    description: "Real-time spot price and options data from Alpaca Markets API with fallback adapters"
    language: "Python"
    module: "src/core/adapters.py"
    
  - name: "GEX Curve Visualization"
    description: "Interactive SVG gamma map showing flip points, call/put walls, and support/resistance"
    language: "TypeScript/React"
    component: "src/components/quant/GammaMap.tsx"
    
  - name: "Scenario Matrix Builder"
    description: "IF/THEN tactical scenarios with probability weighting and invalidation conditions"
    language: "TypeScript/React"
    component: "src/components/quant/ScenarioMatrix.tsx"
    
  - name: "LLM-Powered Tactical Reports"
    description: "Senior Quant Analyst prompts generate structured JSON + markdown reports"
    language: "TypeScript"
    service: "src/lib/quant-engine.ts"
    integration: "z-ai-web-dev-sdk with extended thinking"
    
  - name: "Session Persistence & History"
    description: "SQLite-backed session management with full analysis replay capability"
    language: "TypeScript/Prisma"
    database: "src/prisma/schema.prisma"

capabilities:
  analysis:
    - "Multi-strike gamma exposure calculation"
    - "Gamma flip point detection"
    - "Support/resistance level identification via GEX"
    - "Call/Put wall analysis"
    - "Dealer hedging flow inference"
    - "Delta bias detection"
    
  data_sources:
    - "Alpaca Markets (real-time spot + paper trading)"
    - "Yahoo Finance (options chain backup)"
    - "Synthetic deterministic data (fallback)"
    
  visualizations:
    - "Interactive gamma heatmap (SVG)"
    - "Regime badges (LONG/SHORT/FLIP)"
    - "Confidence meter (gradient scale)"
    - "Tactical matrix (BASE/BREAKOUT/INVALIDATION)"
    - "Real-time data source indicator"
    
  reporting:
    - "Institutional markdown reports"
    - "Session history with full audit trail"
    - "Scenario comparison & probability weighting"
    - "Risk analysis & convergence/divergence notes"

technical_stack:
  frontend:
    - "Next.js 16 (App Router)"
    - "React 19"
    - "TypeScript 5"
    - "Tailwind CSS 4"
    - "shadcn/ui components"
    - "Framer Motion animations"
    - "React Markdown"
    
  backend:
    - "Node.js (API routes)"
    - "Prisma ORM (SQLite)"
    - "z-ai-web-dev-sdk (LLM integration)"
    - "Python FastAPI (quant-engine mini-service)"
    
  python_stack:
    - "scipy/numpy (numerical)"
    - "pandas (data)"
    - "yfinance (market data)"
    - "alpaca-trade-api (broker)"
    - "FastAPI/uvicorn (REST service)"
    
  infrastructure:
    - "SQLite (local database)"
    - "Child process spawning (Python CLI)"
    - "Error boundaries (React error handling)"

usage_examples:
  basic_analysis: |
    ```typescript
    // Next.js API endpoint
    POST /api/analyze
    {
      "price": 600.50,
      "gammaExposure": 2500,
      "flipPoint": 598.00,
      "callWalls": [{ price: 605, magnitude: 8500 }],
      "putWalls": [{ price: 595, magnitude: 7200 }],
      "volatilityRegime": "elevated"
    }
    // Response: JSON with scenarios + markdown report
    ```
    
  market_scan: |
    ```typescript
    // Scan real market data
    POST /api/scan
    // Returns: spot price, GEX curve, flip points, data source
    // Automatically fills form with market context
    ```
    
  python_gex: |
    ```python
    from src.core import GEXCalculator, OptionsChain
    
    # Fetch live options
    chain = OptionsChain(symbol='QQQ')
    data = chain.fetch()
    
    # Calculate GEX
    calc = GEXCalculator(spot_price=chain.spot_price)
    gex_results = calc.compute_gex(data)
    
    # Find critical levels
    flips = calc.find_gamma_flip_points(gex_results)
    levels = calc.find_support_resistance(gex_results)
    ```

integration_points:
  - name: "Market Data Ingestion"
    endpoint: "/api/scan"
    inputs: ["symbol", "expiration_dte", "data_source"]
    outputs: ["MarketDataInput", "GexCurvePoint[]", "ScanStatusBadge"]
    
  - name: "Quantitative Analysis"
    endpoint: "/api/analyze"
    inputs: ["MarketDataInput"]
    outputs: ["QuantAnalysis (JSON)", "TacticalReport (Markdown)", "Scenarios[]"]
    llm_integration: "z-ai-web-dev-sdk with thinking enabled"
    
  - name: "Session Management"
    endpoint: "/api/sessions"
    crud: ["POST (create)", "GET (list)", "GET/:id", "DELETE/:id"]
    persistence: "Prisma + SQLite"

deployment:
  development: |
    ```bash
    npm run dev              # Next.js on :3000
    # Python service spawned on-demand via child_process
    ```
    
  production: |
    ```bash
    npm run build
    npm start                # NODE_ENV=production
    # Standalone output with Python service in PATH
    ```
    
  requirements:
    - "Node.js 18+"
    - "Python 3.9+"
    - "Alpaca API keys (optional, for real data)"
    - "z-ai API key (for LLM analysis)"

environment_variables:
  - name: "DATABASE_URL"
    description: "SQLite connection string"
    example: "file:/home/user/db/custom.db"
    
  - name: "ALPACA_API_KEY"
    description: "Alpaca Markets paper/live trading API key"
    required: false
    
  - name: "ALPACA_SECRET_KEY"
    description: "Alpaca Markets secret key"
    required: false
    
  - name: "Z_AI_API_KEY"
    description: "Z.ai API key for LLM integration"
    required: true

performance_metrics:
  scan_time: "~2-5 seconds (Alpaca) | ~10-15 seconds (yfinance)"
  analyze_time: "~30-40 seconds (LLM thinking enabled)"
  memory_footprint: "~200MB Node.js + ~150MB Python venv"
  concurrent_sessions: "10+ simultaneous analyses"
  database_queries: "Sub-100ms for session operations"

reliability:
  error_handling:
    - "React Error Boundaries on critical components"
    - "Python exception handling with graceful fallbacks"
    - "Alpaca → yfinance → synthetic adapter chain"
    - "Child process timeout management (30s)"
    
  testing:
    - "E2E verification with Agent Browser + VLM (glm-4.6v)"
    - "Unit tests for GEX calculations (scipy validation)"
    - "Lint: 0 errors (ESLint + TypeScript strict mode)"
    - "6+ consecutive scan+analyze cycles without errors"

roadmap:
  v0.2.1:
    - "Add timeout + error handling in child_process"
    - "Input validation with zod schemas"
    - "Persist GexCurve in session database"
    
  v0.3.0:
    - "Comparative analysis (2 DTE side-by-side)"
    - "CSV export for scenarios"
    - "Backtesting framework (replay historical)"
    
  v0.4.0:
    - "WebSocket real-time updates"
    - "Multi-leg detection (spreads, condors)"
    - "Risk metrics (vega, theta, rho)"
    - "Advanced order flow analysis"

license: "MIT"
contact: "arenaglomerante@gmail.com"
documentation: |
  - README.md: Project overview & quick start
  - notebooks/01_gex_introduction.ipynb: Educational GEX tutorial
  - worklog.md: Development history & architecture decisions
  - CONTRIBUTING.md: Contributing guidelines (planned)
  - ROADMAP.md: Feature roadmap (planned)

support:
  issues: "https://github.com/arenaglomerante-cloud/pruebas/issues"
  discussions: "https://github.com/arenaglomerante-cloud/pruebas/discussions"
