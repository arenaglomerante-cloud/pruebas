# GEX Quant Analysis Platform

**Análisis cuantitativo de Gamma Exposure (GEX) para mercados $NQ (Nasdaq-100) y $NDX (Nasdaq-100 Index)**

## 🎯 Objetivo

Construir una plataforma escalable para:
- Identificar niveles críticos de gamma exposure en mercados de opciones
- Detectar gamma flip points y puntos de cobertura
- Analizar flujos de cobertura de dealers
- Generar señales de trading basadas en microestructura del mercado

## 📦 Características Principales

- ✅ Extracción en tiempo real de cadenas de opciones
- ✅ Cálculo de GEX, Vanna, Charm por strike
- ✅ Identificación de niveles de soporte/resistencia
- ✅ Dashboards interactivos
- ✅ Backtesting de estrategias
- ✅ API backend para integración

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

# Obtener cadena de opciones para NQ
chain = OptionsChain(symbol='NQ', expiration='2026-07-15')
data = chain.fetch()

# Calcular GEX
calculator = GEXCalculator(chain_data=data)
gex_levels = calculator.compute_gex()

# Identificar flip points
flip_points = calculator.find_gamma_flips()
```

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
