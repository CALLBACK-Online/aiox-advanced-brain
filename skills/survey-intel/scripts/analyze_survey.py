#!/usr/bin/env python3
"""
Survey Intel · script de análise inicial em camadas

Uso:
    python analyze_survey.py <caminho_do_csv> [opções]

Executa L1-L5 automaticamente e imprime relatório.
L6-L8 requerem decisão humana e são gerados depois.

Adapte as configurações no topo conforme o dataset.
"""

import pandas as pd
import sys
from collections import Counter
from pathlib import Path


# ============ CONFIGURAÇÃO (adapte por dataset) ============

# Renomeação de colunas (de nome real → nome padrão)
COLUMN_MAP = {
    # 'Qual seu melhor e-mail?': 'email',
    # 'Qual dessas frases mais te descreve?': 'perfil',
    # ...
}

# Campos categóricos chave para análise univariada e cruzamentos
CATEGORICAL_FIELDS = ['perfil', 'problema_ia', 'tempo_semana', 'ferramentas', 'setor']

# Campos abertos para análise temática
OPEN_FIELDS = ['resultado_desejado', 'maior_dificuldade']

# Pares para cruzamentos 2D
CROSSTABS = [
    ('perfil', 'problema_ia'),
    ('setor', 'problema_ia'),
    ('tempo_semana', 'problema_ia'),
    ('ferramentas', 'problema_ia'),
]

# Temas para análise temática (adaptar ao domínio)
TEMAS_DEFAULT = {
    'Vendas / prospecção / clientes': ['vend', 'prospec', 'cliente', 'lead', 'capt', 'comercial'],
    'Automação / processos repetitivos': ['automa', 'processo', 'repetitiv', 'manual', 'fluxo'],
    'Criação de conteúdo / criativos': ['conteúd', 'conteud', 'post', 'criativ', 'design'],
    'Tempo / produtividade': ['tempo', 'produtividade', 'rápid', 'demora'],
    'Criar sites/apps/sistemas': ['site', 'app ', 'aplicat', 'sistema'],
    'Conhecimento / aprender': ['conhecimento', 'aprender', 'entender', 'saber', 'começar'],
    'Escala': ['escala', 'escalar', 'replicar'],
    'Marketing / tráfego': ['marketing', 'tráfego', 'trafego', 'anúncio'],
    'Recursos / dinheiro': ['dinheiro', 'recurso', 'capital', 'investim'],
    'Foco / organização': ['foco', 'organiz', 'gestão', 'gestao'],
}


# ============ L1: DIAGNÓSTICO ============

def L1_diagnostico(df):
    print("="*80)
    print("L1 · DIAGNÓSTICO DO DATASET")
    print("="*80)
    print(f"Total de respostas: {len(df)}")
    print(f"\nPreenchimento por campo:")
    for col in df.columns:
        n = df[col].notna().sum()
        pct = 100 * n / len(df)
        flag = " ⚠️" if pct < 50 else ""
        print(f"  {col}: {n} ({pct:.1f}%){flag}")
    
    print(f"\nTipos detectados:")
    for col in df.columns:
        n_unique = df[col].nunique()
        if n_unique <= 10:
            print(f"  {col} → categórico ({n_unique} níveis)")
        elif df[col].dtype == object:
            avg_len = df[col].dropna().astype(str).str.len().mean()
            if avg_len > 30:
                print(f"  {col} → texto aberto (avg {avg_len:.0f} chars)")
    print()


# ============ L2: UNIVARIADAS ============

def L2_univariadas(df, fields):
    print("="*80)
    print("L2 · DISTRIBUIÇÕES UNIVARIADAS")
    print("="*80)
    
    for field in fields:
        if field not in df.columns:
            continue
        print(f"\n>>> {field}")
        counts = df[field].value_counts()
        for cat, n in counts.items():
            pct = 100 * n / df[field].notna().sum()
            print(f"  {cat}: {n} ({pct:.1f}%)")
    print()


# ============ L3: CRUZAMENTOS ============

def L3_cruzamentos(df, pairs):
    print("="*80)
    print("L3 · CRUZAMENTOS 2D · procurando célula quente")
    print("="*80)
    
    hot_cells = []
    
    for f1, f2 in pairs:
        if f1 not in df.columns or f2 not in df.columns:
            continue
        
        print(f"\n>>> {f1} × {f2}")
        ct = pd.crosstab(df[f1], df[f2])
        ct_pct = pd.crosstab(df[f1], df[f2], normalize='index') * 100
        
        print(ct.to_string())
        print(f"\n(% por linha)")
        print(ct_pct.round(1).to_string())
        
        # Detectar célula quente (>50% em uma linha)
        for idx in ct_pct.index:
            for col in ct_pct.columns:
                pct = ct_pct.loc[idx, col]
                n_abs = ct.loc[idx, col]
                if pct >= 50 and n_abs >= 50:
                    hot_cells.append({
                        'cross': f"{f1} × {f2}",
                        'cell': f"{idx} → {col}",
                        'n': n_abs,
                        'pct': round(pct, 1)
                    })
    
    if hot_cells:
        print("\n" + "="*80)
        print("🔥 CÉLULAS QUENTES DETECTADAS (>50% em linha + n≥50)")
        print("="*80)
        for hc in hot_cells:
            print(f"  {hc['cross']} → {hc['cell']}: n={hc['n']} ({hc['pct']}%)")
        print("\n  → CANDIDATA(S) PARA AVATAR PRIMÁRIO (L6)")
    else:
        print("\nℹ️  Nenhuma célula quente clara. Pular L6, focar em segmentos diversos.")
    print()
    
    return hot_cells


# ============ L4: ANÁLISE TEMÁTICA ============

def L4_tematica(df, open_fields, temas):
    print("="*80)
    print("L4 · ANÁLISE TEMÁTICA · respostas abertas")
    print("="*80)
    
    for field in open_fields:
        if field not in df.columns:
            continue
        
        substantivas = df[field].dropna().astype(str)
        substantivas = substantivas[substantivas.str.len() > 40]
        
        if len(substantivas) < 50:
            print(f"\n>>> {field}: apenas {len(substantivas)} substantivas, pulando")
            continue
        
        print(f"\n>>> {field}")
        print(f"  N substantivas: {len(substantivas)}")
        
        # Contar tema dominante
        dominante = Counter()
        for resp in substantivas:
            resp_lower = resp.lower()
            for tema, kws in temas.items():
                if any(kw in resp_lower for kw in kws):
                    dominante[tema] += 1
                    break  # primeiro match = dominante
        
        # Cobertura
        cobertura = sum(dominante.values())
        pct_cobertura = 100 * cobertura / len(substantivas)
        print(f"  Cobertura: {pct_cobertura:.1f}%")
        
        # Ranking
        print(f"  Ranking de temas:")
        for tema, n in dominante.most_common():
            pct = 100 * n / len(substantivas)
            print(f"    {tema}: {n} ({pct:.1f}%)")
        
        # Citações canônicas (top 3 por tema)
        print(f"\n  Citações canônicas top temas:")
        for tema in [t for t, _ in dominante.most_common(5)]:
            matches = [r for r in substantivas 
                      if any(kw in r.lower() for kw in temas[tema])]
            matches = [m for m in matches if 60 <= len(m) <= 220]
            matches.sort(key=lambda x: abs(len(x) - 120))
            print(f"\n    {tema}:")
            for c in matches[:3]:
                print(f"      • {c.strip()}")
    print()


# ============ L5: SEGMENTOS ============

def L5_segmentos(df):
    print("="*80)
    print("L5 · SEGMENTOS ACIONÁVEIS")
    print("="*80)
    print("\nNota: Adapte os critérios abaixo ao seu dataset")
    
    # Templates de segmentos canônicos
    segments = {}
    
    # Avatar primário (precisa célula quente)
    # Adapte os valores específicos
    
    # Premium high-ticket
    if all(c in df.columns for c in ['perfil', 'ferramentas', 'tempo_semana']):
        # ...
        pass
    
    print("\nSegmentos canônicos a sempre considerar:")
    print("  - AV_PRIMARIO (célula quente de L3)")
    print("  - AV_PREMIUM (já tem negócio + alta capacidade técnica + alto tempo)")
    print("  - AV_INICIANTE_ABSOLUTO (sem ferramenta + baixo tempo)")
    print("  - AV_DESCOMPASSO (quer X mas não tem capacidade pra X)")
    print("  - AV_ICP_OPERACIONAL (dor + capacidade)")
    print()


# ============ MAIN ============

def main():
    if len(sys.argv) < 2:
        print("Uso: python analyze_survey.py <caminho_csv>")
        sys.exit(1)
    
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Arquivo não encontrado: {path}")
        sys.exit(1)
    
    # Carregar
    if path.suffix == '.csv':
        df = pd.read_csv(path)
    elif path.suffix in ['.xlsx', '.xls']:
        df = pd.read_excel(path)
    else:
        print(f"Formato não suportado: {path.suffix}")
        sys.exit(1)
    
    # Renomear se necessário
    if COLUMN_MAP:
        df = df.rename(columns=COLUMN_MAP)
    
    # Executar camadas
    L1_diagnostico(df)
    L2_univariadas(df, CATEGORICAL_FIELDS)
    hot_cells = L3_cruzamentos(df, CROSSTABS)
    L4_tematica(df, OPEN_FIELDS, TEMAS_DEFAULT)
    L5_segmentos(df)
    
    print("="*80)
    print("ANÁLISE INICIAL COMPLETA")
    print("="*80)
    print("\nPróximos passos:")
    if hot_cells:
        print(f"  → L6: Aprofundar avatar primário ({hot_cells[0]['cell']})")
        print(f"  → L7: Inteligência aplicada (linguagem, citações, frase abertura)")
        print(f"  → L8: Materializar (markdown + dashboard)")
    else:
        print(f"  → Pular L6 (sem célula quente)")
        print(f"  → L5 refinado: explorar combinações de segmentos")
        print(f"  → L8: Materializar com foco em distribuições e segmentos")


if __name__ == "__main__":
    main()
