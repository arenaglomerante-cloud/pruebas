# GEX Quant Analysis Platform

**Análisis cuantitativo de Gamma Exposure (GEX) para mercados $NQ (Nasdaq-100) y $NDX (Nasdaq-100 Index)**

> ⚠️ **Estado actual del proyecto**: este repositorio contiene hoy la base cuantitativa en Python
> (`src/core/gex_calculator.py`, `src/core/options_chain.py`, `config/config.py`) más su suite de
> tests (`tests/`) y CI. El resto de las secciones de este README y de `ROADMAP.md`/`SKILL.md`
> (UI Next.js, motor LLM, adaptador Alpaca, persistencia Prisma/SQLite, backtesting, dashboards)
> describen la **visión objetivo** del proyecto y **aún no están implementadas**. Úsalas como guía
> de diseño, no como documentación de funcionalidad existente.

## 🎯 Objetivo

Construir una plataforma escalable para:
- Identificar niveles críticos de gamma exposure en mercados de opciones
- Detectar gamma flip points y puntos de cobertura
- Analizar flujos de cobertura de dealers
- Generar señales de trading basadas en microestructura del mercado

## 📦 Características Principales

Implementado hoy:
- ✅ Cálculo de GEX (Black-Scholes) e identificación de gamma flip points/soporte-resistencia
- ✅ Fetch de cadenas de opciones vía yfinance con limpieza y resumen de datos
- ✅ Tests unitarios (`pytest`) y CI (GitHub Actions)

Planeado (ver `ROADMAP.md`):
- ⏳ Extracción en tiempo real multi-fuente (Alpha Vantage, Alpaca)
- ⏳ Cálculo de Vanna/Charm
- ⏳ Dashboards interactivos
- ⏳ Backtesting de estrategias
- ⏳ API backend para integración

## 🗂️ Estructura del Proyecto

```
pruebas/
├── data/                      # Datos y datasources
│   ├── raw/                   # Datos sin procesar
│   ├── processed/             # Datos procesados
│   └── cache/                 # Cache local
├── src/
│   ├── core/                  # Módulos core
│   │   ├── gex_calculator.py  # Cálculos GEX
│   │   ├── options_chain.py   # Gestión de cadenas
│   │   └── market_data.py     # Fuentes de datos
│   ├── analysis/              # Análisis e indicadores
│   │   ├── gamma_analysis.py
│   │   ├── technical.py
│   │   └── signals.py
│   ├── strategies/            # Estrategias de trading
│   ├── visualization/         # Dashboards y gráficos
│   └── utils/                 # Utilidades
├── notebooks/                 # Jupyter notebooks de análisis
├── tests/                     # Tests unitarios
├── config/                    # Configuración
├── requirements.txt
├── setup.py
└── README.md
```

## 🚀 Quick Start

### Instalación

```bash
git clone https://github.com/arenaglomerante-cloud/pruebas.git
cd pruebas
pip install -r requirements.txt
```

### Uso Básico

```python
from src.core import GEXCalculator, OptionsChain

# Obtener cadena de opciones para un símbolo (p.ej. QQQ)
chain = OptionsChain(symbol='QQQ', data_source='yfinance')
data = chain.fetch()
cleaned = chain.clean_data()

# Calcular GEX
calculator = GEXCalculator(spot_price=chain.spot_price)
gex_levels = calculator.compute_gex(cleaned)

# Identificar flip points y niveles de soporte/resistencia
flip_points = calculator.find_gamma_flip_points(gex_levels)
levels = calculator.find_support_resistance(gex_levels)
```

### Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

Un workflow de CI (`.github/workflows/ci.yml`) ejecuta automáticamente `pytest`, `black --check`
y `pylint` en cada push/PR.

## 📊 Fuentes de Datos

- **Opciones**: Alpha Vantage, Alpaca Markets, QuantConnect
- **Spot Price**: Yahoo Finance, IB
- **Volatilidad**: IV Index, OptionChain APIs

## 📈 Análisis Soportados

1. **Gamma Exposure por Strike** - Identificar áreas de cobertura
2. **Gamma Flip Points** - Transiciones en dinámicas de hedging
3. **Dealer Net Exposure** - Flujos de cobertura institucionales
4. **Technical + GEX** - Confluence analysis
5. **Backtesting** - Validación de estrategias

## 🔗 Referencias y Inspiración

- [pikki622/gex-analytics](https://github.com/pikki622/gex-analytics)
- [FlashAlpha-lab/gex-explained](https://github.com/FlashAlpha-lab/gex-explained)
- [alexjust-data/gex-options-realtime](https://github.com/alexjust-data/gex-options-realtime)
- [mfish324/GEX](https://github.com/mfish324/GEX)

## 📚 Documentación

Ver `/docs` para documentación técnica detallada.

## ⚖️ Disclaimer

Este proyecto es para propósitos educativos y de investigación. No constituye asesoramiento financiero.

## 👨‍💻 Contribuciones

Las contribuciones son bienvenidas. Por favor abre un PR.

---

**Last Updated**: 2026-06-25
