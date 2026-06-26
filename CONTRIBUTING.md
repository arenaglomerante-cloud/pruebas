# Guía de Contribución - GEX Quant Analysis Platform

## Bienvenida 👋

¡Gracias por tu interés en contribuir a GammaDesk Terminal! Este documento guía el proceso de contribución.

## Código de Conducta

- Sé respetuoso con otros contribuidores
- Enfócate en lo mejor para la comunidad
- Reporta comportamientos inapropiados a: arenaglomerante@gmail.com

## ¿Cómo Contribuir?

### 1. Reportar Bugs 🐛

**Antes de reportar:**
- Verifica que el bug no esté ya reportado
- Reproduce el problema en la última versión

**Al reportar incluye:**
```markdown
**Descripción del bug:**
[Descripción clara y concisa]

**Pasos para reproducir:**
1. Ir a '...'
2. Hacer clic en '...'
3. Ver error '...'

**Comportamiento esperado:**
[Qué debería ocurrir]

**Comportamiento actual:**
[Qué sucede realmente]

**Entorno:**
- OS: [e.g. Windows, macOS, Linux]
- Node: [e.g. 18.0.0]
- Python: [e.g. 3.11.0]
- Rama: [main, develop, etc]

**Logs/Screenshots:**
[Adjunta si es relevante]
```

### 2. Sugerir Mejoras 💡

Abre una discusión en GitHub con:
- Caso de uso específico
- Ventajas de la mejora
- Posible implementación
- Impacto en la compatibilidad

### 3. Crear Pull Requests 🚀

#### Antes de empezar:

```bash
# Fork el repositorio
git clone https://github.com/TU_USUARIO/pruebas.git
cd pruebas

# Instala dependencias
npm install

# Crea rama feature
git checkout -b feature/tu-feature
# o bugfix
git checkout -b bugfix/tu-bug-fix
```

#### Durante el desarrollo:

```bash
# Verifica linting
npm run lint

# Actualiza base de datos si modificas schema.prisma
npm run db:push

# Ejecuta dev server
npm run dev
```

#### Antes de hacer commit:

```bash
# Sigue conventional commits:
# feat: añade nueva funcionalidad
# fix: corrige un bug
# docs: cambios en documentación
# style: cambios de formato (sin lógica)
# refactor: refactoriza código
# perf: mejoras de rendimiento
# test: añade/actualiza tests
# chore: cambios en build/dependencies

git add .
git commit -m "feat: descripción clara del cambio"
```

#### Envía el PR:

```bash
git push origin feature/tu-feature
```

**Tu PR debe incluir:**
- ✅ Título descriptivo
- ✅ Descripción clara del cambio
- ✅ Referencia a issue (si existe): `Closes #123`
- ✅ Capturas/videos si es UI
- ✅ Tests si es lógica crítica
- ✅ Actualización de docs si aplica

## Estándares de Código

### TypeScript

```typescript
// ✅ BIEN
interface UserProfile {
  id: string;
  email: string;
  createdAt: Date;
}

const getUserProfile = async (id: string): Promise<UserProfile> => {
  const user = await db.query(id);
  return user;
};

// ❌ MAL
const getUser = async (id) => {
  return await db.query(id);
};
```

### Python

```python
# ✅ BIEN
def calculate_gamma_exposure(
    strikes: List[float],
    spot_price: float,
    time_to_expiry: float,
    volatility: float
) -> pd.DataFrame:
    """
    Calculate gamma exposure at multiple price levels.
    
    Args:
        strikes: Array of strike prices
        spot_price: Current spot price
        time_to_expiry: Time to expiration in years
        volatility: Implied volatility (decimal)
    
    Returns:
        DataFrame with price levels and GEX values
    """
    results = []
    # Implementation...
    return pd.DataFrame(results)

# ❌ MAL
def calc_gex(strikes, spot, tte, vol):
    # no docstring, unclear parameter names
    pass
```

### React Components

```typescript
// ✅ BIEN
interface GammaMapProps {
  gexCurve: GexCurvePoint[];
  spotPrice: number;
  flipPoints: FlipPoint[];
  isLoading?: boolean;
}

export const GammaMap: React.FC<GammaMapProps> = ({
  gexCurve,
  spotPrice,
  flipPoints,
  isLoading = false
}) => {
  if (isLoading) return <GammaMapSkeleton />;
  
  return (
    <svg className="w-full h-full">
      {/* Implementation */}
    </svg>
  );
};

// ❌ MAL
export const GammaMap = (props) => {
  // no TypeScript, unclear prop structure
  return <svg>{/*...*/}</svg>;
};
```

## Estructura de Carpetas

```
pruebas/
├── src/
│   ├── app/              # Next.js App Router
│   │   ├── api/         # API routes
│   │   ├── page.tsx     # Home page
│   │   └── layout.tsx   # Root layout
│   ├── components/      # React components
│   │   ├── quant/       # Quantitative analysis components
│   │   ├── ui/          # shadcn/ui components
│   │   └── ...
│   ├── core/            # Python quant logic
│   │   ├── gex_calculator.py
│   │   ├── options_chain.py
│   │   └── adapters.py
│   ├── lib/             # Utilities & helpers
│   ├── prisma/          # Prisma schema
│   └── ...
├── mini-services/       # External services
│   ├── quant-engine/    # Python FastAPI service
│   └── ...
├── notebooks/           # Jupyter notebooks
├── tests/               # Test files
└── ...
```

## Áreas Prioritarias para Contribuir

### 🔴 Crítica
- [ ] Error handling robusto en Python service
- [ ] Validación de input con zod
- [ ] Timeouts en child_process
- [ ] Tests unitarios para GEX calculator

### 🟡 Importante
- [ ] Persistencia de GexCurve en DB
- [ ] Modo comparativo multi-DTE
- [ ] CSV export de escenarios
- [ ] Documentación API OpenAPI/Swagger

### 🟢 Nice-to-have
- [ ] WebSocket real-time updates
- [ ] Backtesting framework
- [ ] Multi-leg detection
- [ ] Dashboard de métricas de risk

## Process de Review

1. **Automated Checks**
   - Lint (ESLint + TypeScript)
   - Type safety
   - Database schema validation

2. **Manual Review**
   - Code clarity
   - Test coverage
   - Performance impact
   - Documentation

3. **Testing**
   - Browser testing (Chromium)
   - API integration tests
   - Python unit tests

4. **Merge**
   - Squash commits si es necesario
   - Update CHANGELOG.md
   - Merge a main branch

## Recursos Útiles

### Documentación
- [Next.js Docs](https://nextjs.org/docs)
- [React Docs](https://react.dev)
- [Prisma Docs](https://www.prisma.io/docs/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui](https://ui.shadcn.com/)

### Tools
- [z-ai SDK Docs](https://z-ai-web-dev.com)
- [Alpaca API Reference](https://alpaca.markets/docs/api-references/)
- [Black-Scholes Python](https://scipy.org/)

### Community
- GitHub Issues: [Discussions](https://github.com/arenaglomerante-cloud/pruebas/discussions)
- Email: arenaglomerante@gmail.com

## Development Setup

```bash
# Clonar repositorio
git clone https://github.com/arenaglomerante-cloud/pruebas.git
cd pruebas

# Instalar dependencias Node
npm install

# Instalar dependencias Python
cd mini-services/quant-engine
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Edita .env con tus credenciales

# Database setup
npm run db:generate
npm run db:push

# Iniciar desarrollo
npm run dev
# En otra terminal:
cd mini-services/quant-engine
source venv/bin/activate
python main.py
```

## Ayuda & Soporte

- 📖 Ver [README.md](./README.md) para visión general
- 📚 Revisar [SKILL.md](./SKILL.md) para capacidades detalladas
- 📋 Revisar [worklog.md](./worklog.md) para decisiones arquitectónicas
- 💬 Abrir discusión en GitHub

---

**¡Gracias por contribuir a hacer GammaDesk Terminal más increíble!** 🚀
