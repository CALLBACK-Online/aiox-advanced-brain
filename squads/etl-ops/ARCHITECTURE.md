# ETL-Ops Squad — Architecture

## Overview

O squad `etl-ops` é operacional para execução de pipelines ETL usando infraestrutura existente em `services/etl/`. Três agentes funcionais cobrem Extract, Transform e Load, com orquestração centralizada pelo etl-chief.

## Agent Hierarchy

```
etl-chief (Orchestrator)
├── etl-extractor       # Extração de fontes (vídeo, áudio, web, APIs)
└── etl-transformer     # Transformação, diarização, normalização
```

Squad funcional e enxuto — 3 agentes cobrem o pipeline ETL end-to-end.

## Pipeline Flow

```
Source (URL, file, YouTube, podcast)
        ↓
[etl-extractor]
  ├── Download & validate
  ├── Whisper.cpp transcription (local)
  ├── YouTube transcript fallback
  └── Metadata extraction
        ↓
  Raw artifact (.txt, .mp3, .json)
        ↓
[etl-transformer]
  ├── Diarization (speaker attribution)
  ├── Normalization (formatting, encoding)
  ├── Enrichment (timestamps, chapters)
  └── JSON + Markdown output generation
        ↓
  Processed artifact (-diarized.md, -diarized.json, index.json)
        ↓
[etl-chief]
  └── Routing + handoff to consumer squad (copy, spy, books)
```

## Infrastructure

| Component | Location |
|-----------|----------|
| Services core | `services/etl/` |
| Whisper.cpp runtime | Local binary (via `WHISPER_CPP_CLI` env var) |
| Models | `$WHISPER_CPP_MODEL` (base, small, medium, large) |
| YouTube transcript fallback | services/etl/youtube-transcript |
| Output registry | `outputs/etl-ops/etl-{YYYYMMDD-{hash}}/` |

## Output Structure

Each ETL run produces a versioned directory:

```
outputs/etl-ops/etl-20260311-qj04/
├── {videoId}.json              # Raw metadata
├── {videoId}.txt               # Raw transcript
├── {videoId}-diarized.md       # Human-readable diarized
├── {videoId}-diarized.json     # Machine-readable diarized
├── stderr.log                  # Execution log
└── index.json                  # Run manifest
```

## Supported Sources

| Type | Primary Method | Fallback |
|------|---------------|----------|
| YouTube video | Whisper transcription of audio | YouTube transcript API |
| Podcast RSS | Download + Whisper | — |
| Local audio/video | Whisper direct | — |
| Articles (web) | HTML → text extraction | — |

## Integration Points

| Downstream consumer | How outputs are used |
|---------------------|---------------------|
| `copy` | Source material for offer stacks, briefings, workshops |
| `spy` | Research material for competitive intelligence |
| `books` pipeline | Extract from book/audiobook sources |
| `visual-knowledge-squad` | Source material for slide generation |

## Boundary

- **In scope:** ETL pipelines (extract, transform, load), transcription, diarization, content normalization
- **Out of scope:** Content generation (that's copy/spy), publishing (that's devops), AI summarization beyond diarization

## Tasks Canônicas (8 total)

ETL pipeline execution, transcription setup, diarization tuning, batch processing, source validation, output indexing.
