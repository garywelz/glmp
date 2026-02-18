#!/bin/bash
# Test all GLMP Cloud Service endpoints

SERVICE_URL="https://glmp-service-204731194849.us-central1.run.app"

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║          Testing GLMP Cloud Service - Phase 2 Features              ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Test 1: Health Check
echo "1. Health Check..."
curl -s $SERVICE_URL/health | python3 -m json.tool
echo ""

# Test 2: List Processes
echo "2. List Processes..."
curl -s $SERVICE_URL/api/processes | python3 -m json.tool | head -20
echo ""

# Test 3: Validate Citations
echo "3. Validate Citations (Lac Operon)..."
curl -s -X POST $SERVICE_URL/api/validate-citations \
  -H "Content-Type: application/json" \
  -d '{"process_id": "ecoli_lac_operon"}' | python3 -m json.tool
echo ""

# Test 4: Search ArXiv
echo "4. Search ArXiv (lac operon)..."
curl -s -X POST $SERVICE_URL/api/search-arxiv \
  -H "Content-Type: application/json" \
  -d '{"query": "lac operon regulation", "max_results": 3, "category": "q-bio"}' | python3 -m json.tool | head -30
echo ""

# Test 5: Search PubMed
echo "5. Search PubMed (trp operon)..."
curl -s -X POST $SERVICE_URL/api/search-pubmed \
  -H "Content-Type: application/json" \
  -d '{"query": "trp operon attenuation", "max_results": 5}' | python3 -m json.tool | head -30
echo ""

# Test 6: AI Validation
echo "6. AI Validation (Lac Operon) - May take 10-30 seconds..."
curl -s -X POST $SERVICE_URL/api/ai-validate \
  -H "Content-Type: application/json" \
  -d '{"process_id": "ecoli_lac_operon"}' | python3 -m json.tool
echo ""

# Test 7: Literature Enrichment
echo "7. Literature Enrichment (DNA Replication) - May take 30-60 seconds..."
curl -s -X POST $SERVICE_URL/api/enrich \
  -H "Content-Type: application/json" \
  -d '{"process_id": "ecoli_dna_replication_initiation", "include_arxiv": true, "include_pubmed": true}' | python3 -m json.tool | head -50
echo ""

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                     All Tests Complete!                              ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
