"""
Literature Integration - ArXiv and PubMed
Provides citation validation, paper search, and enrichment
"""

import arxiv
from Bio import Entrez
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

# Configure Entrez (PubMed)
Entrez.email = "garywelz@gmail.com"  # Required by NCBI
Entrez.tool = "GLMP_Service"


class ArxivSearch:
    """Search and retrieve papers from ArXiv"""
    
    def __init__(self):
        logger.info("✓ Initialized ArXiv search")
    
    def search_papers(self, query, max_results=10, category=None):
        """
        Search ArXiv for papers
        
        Args:
            query: Search query string
            max_results: Maximum number of results (default: 10)
            category: ArXiv category (e.g., 'q-bio', 'cs.AI')
        
        Returns:
            List of paper dicts
        """
        try:
            # Add category to query if specified
            if category:
                query = f"{query} AND cat:{category}"
            
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            papers = []
            for result in search.results():
                papers.append({
                    'title': result.title,
                    'authors': [author.name for author in result.authors],
                    'published': result.published.isoformat(),
                    'updated': result.updated.isoformat(),
                    'abstract': result.summary,
                    'url': result.entry_id,
                    'pdf_url': result.pdf_url,
                    'categories': result.categories,
                    'primary_category': result.primary_category
                })
            
            logger.info(f"✓ Found {len(papers)} papers on ArXiv for: {query}")
            return papers
            
        except Exception as e:
            logger.error(f"ArXiv search failed: {e}")
            return []
    
    
    def find_papers_for_process(self, process_name, organism, max_results=5):
        """
        Find recent ArXiv papers relevant to a biological process
        
        Args:
            process_name: Name of the process
            organism: Organism name
            max_results: Max papers to return
        
        Returns:
            List of relevant papers
        """
        query = f"{process_name} {organism} regulation gene expression"
        return self.search_papers(query, max_results=max_results, category='q-bio')


class PubMedSearch:
    """Search and validate citations using PubMed"""
    
    def __init__(self):
        logger.info("✓ Initialized PubMed search")
    
    
    def search_pubmed(self, query, max_results=10):
        """
        Search PubMed for papers
        
        Args:
            query: Search query
            max_results: Maximum results
        
        Returns:
            List of PubMed IDs
        """
        try:
            handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
            record = Entrez.read(handle)
            handle.close()
            
            pmids = record.get("IdList", [])
            logger.info(f"✓ Found {len(pmids)} papers in PubMed for: {query}")
            return pmids
            
        except Exception as e:
            logger.error(f"PubMed search failed: {e}")
            return []
    
    
    def fetch_paper_details(self, pmid):
        """
        Fetch detailed information for a PubMed ID
        
        Args:
            pmid: PubMed ID
        
        Returns:
            Paper details dict
        """
        try:
            handle = Entrez.efetch(db="pubmed", id=pmid, rettype="medline", retmode="text")
            record = handle.read()
            handle.close()
            
            # Parse the MEDLINE format
            details = self._parse_medline(record)
            details['pmid'] = pmid
            
            logger.info(f"✓ Fetched details for PMID: {pmid}")
            return details
            
        except Exception as e:
            logger.error(f"Failed to fetch PMID {pmid}: {e}")
            return None
    
    
    def _parse_medline(self, medline_text):
        """Parse MEDLINE format text"""
        details = {}
        
        # Extract title
        title_match = re.search(r'TI  - (.+?)(?:\n[A-Z]{2}  -|\Z)', medline_text, re.DOTALL)
        if title_match:
            details['title'] = title_match.group(1).replace('\n      ', ' ').strip()
        
        # Extract authors
        author_match = re.search(r'AU  - (.+?)(?:\n[A-Z]{2}  -|\Z)', medline_text, re.DOTALL)
        if author_match:
            details['authors'] = author_match.group(1).replace('\n      ', ' ').strip()
        
        # Extract journal
        journal_match = re.search(r'TA  - (.+)', medline_text)
        if journal_match:
            details['journal'] = journal_match.group(1).strip()
        
        # Extract year
        year_match = re.search(r'DP  - (\d{4})', medline_text)
        if year_match:
            details['year'] = int(year_match.group(1))
        
        # Extract abstract
        abstract_match = re.search(r'AB  - (.+?)(?:\n[A-Z]{2}  -|\Z)', medline_text, re.DOTALL)
        if abstract_match:
            details['abstract'] = abstract_match.group(1).replace('\n      ', ' ').strip()
        
        # Extract DOI
        doi_match = re.search(r'LID - (.+?) \[doi\]', medline_text)
        if doi_match:
            details['doi'] = doi_match.group(1).strip()
        
        return details
    
    
    def validate_citation(self, citation):
        """
        Validate a citation against PubMed
        
        Args:
            citation: Citation dict with title, authors, year, pmid
        
        Returns:
            Validation result dict
        """
        try:
            # If PMID provided, fetch and compare
            if 'pmid' in citation and citation['pmid']:
                details = self.fetch_paper_details(citation['pmid'])
                if details:
                    # Check if title matches
                    title_match = citation.get('title', '').lower() in details.get('title', '').lower()
                    
                    return {
                        'valid': True,
                        'pmid': citation['pmid'],
                        'title_match': title_match,
                        'details': details
                    }
            
            # Otherwise search by title and year
            query = f"{citation.get('title', '')} {citation.get('year', '')}"
            pmids = self.search_pubmed(query, max_results=1)
            
            if pmids:
                return {
                    'valid': True,
                    'pmid': pmids[0],
                    'found_by_search': True
                }
            
            return {
                'valid': False,
                'reason': 'Citation not found in PubMed'
            }
            
        except Exception as e:
            logger.error(f"Citation validation failed: {e}")
            return {
                'valid': False,
                'reason': str(e)
            }
    
    
    def validate_all_citations(self, process_data):
        """
        Validate all citations in a process
        
        Args:
            process_data: Process JSON dict
        
        Returns:
            Validation summary dict
        """
        sources = process_data.get('sources', [])
        results = []
        
        for source in sources:
            validation = self.validate_citation(source)
            results.append({
                'citation': source,
                'validation': validation
            })
        
        valid_count = sum(1 for r in results if r['validation'].get('valid', False))
        
        return {
            'total_citations': len(sources),
            'valid_citations': valid_count,
            'invalid_citations': len(sources) - valid_count,
            'validation_rate': valid_count / len(sources) if sources else 0,
            'results': results
        }
    
    
    def find_papers_for_process(self, process_name, organism, max_results=10):
        """
        Find PubMed papers for a biological process
        
        Args:
            process_name: Process name
            organism: Organism name
            max_results: Max results
        
        Returns:
            List of papers with details
        """
        query = f"{process_name} {organism} regulation molecular mechanism"
        pmids = self.search_pubmed(query, max_results=max_results)
        
        papers = []
        for pmid in pmids[:5]:  # Fetch details for top 5
            details = self.fetch_paper_details(pmid)
            if details:
                papers.append(details)
        
        return papers


class LiteratureEnricher:
    """Combine ArXiv and PubMed for comprehensive literature enrichment"""
    
    def __init__(self):
        self.arxiv = ArxivSearch()
        self.pubmed = PubMedSearch()
        logger.info("✓ Initialized Literature Enricher")
    
    
    def enrich_process(self, process_data, include_arxiv=True, include_pubmed=True):
        """
        Enrich a process with recent literature
        
        Args:
            process_data: Process JSON dict
            include_arxiv: Include ArXiv papers
            include_pubmed: Include PubMed papers
        
        Returns:
            Enrichment results dict
        """
        results = {
            'process_id': process_data.get('id'),
            'process_name': process_data.get('name'),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # ArXiv papers
        if include_arxiv:
            arxiv_papers = self.arxiv.find_papers_for_process(
                process_data.get('name'),
                process_data.get('organism'),
                max_results=5
            )
            results['arxiv_papers'] = arxiv_papers
            results['arxiv_count'] = len(arxiv_papers)
        
        # PubMed papers
        if include_pubmed:
            pubmed_papers = self.pubmed.find_papers_for_process(
                process_data.get('name'),
                process_data.get('organism'),
                max_results=10
            )
            results['pubmed_papers'] = pubmed_papers
            results['pubmed_count'] = len(pubmed_papers)
        
        # Validate existing citations
        citation_validation = self.pubmed.validate_all_citations(process_data)
        results['citation_validation'] = citation_validation
        
        logger.info(f"✓ Enriched {process_data.get('name')}: {results.get('arxiv_count', 0)} ArXiv + {results.get('pubmed_count', 0)} PubMed papers")
        
        return results


# Global instances
arxiv_search = None
pubmed_search = None
enricher = None

def get_arxiv():
    """Get or create ArxivSearch instance"""
    global arxiv_search
    if arxiv_search is None:
        arxiv_search = ArxivSearch()
    return arxiv_search

def get_pubmed():
    """Get or create PubMedSearch instance"""
    global pubmed_search
    if pubmed_search is None:
        pubmed_search = PubMedSearch()
    return pubmed_search

def get_literature_enricher():
    """Get or create LiteratureEnricher instance"""
    global enricher
    if enricher is None:
        enricher = LiteratureEnricher()
    return enricher
