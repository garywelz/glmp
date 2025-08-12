---
language:
- en
license:
- other
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- text-classification
- text-generation
- other
task_ids:
- other-other
paperswithcode_id: null
configs:
- config_name: default
  data_files:
  - split: train
    path: welz_1995_genome_programming.html
  - split: train
    path: beta_galactosidase_flowchart.png
  - split: train
    path: welz.genome0.shtml
  default: true
---

# Dataset Card for Gary Welz's "Is a Genome Like a Computer Program?" (1995)

## Dataset Description

- **Repository:** [Add repository URL]
- **Paper:** [Add paper URL if applicable]
- **Point of Contact:** [Add contact information]
- **Huggingface.co Editor:** [Add editor username]

### Dataset Summary

This dataset contains Gary Welz's groundbreaking 1995 article "Is a Genome Like a Computer Program?" originally published in *The X Advisor* (July 1995, Vol 1 No 2). This work represents one of the earliest attempts to bridge computer science and molecular biology, proposing that genomes could be understood and modeled as computer programs.

The dataset includes:
- A clean, modern HTML version of the original article
- The original archived HTML from the Wayback Machine
- A high-resolution version of the beta-galactosidase flowchart
- Comprehensive documentation of the article's historical significance

### Supported Tasks and Leaderboards

This dataset is primarily intended for:
- **Historical Research**: Understanding the evolution of computational biology
- **Educational Use**: Teaching the intersection of computer science and biology
- **Literature Review**: Providing context for modern systems biology research

### Languages

The dataset is in English.

## Dataset Structure

### Data Instances

The dataset contains three main files:

1. **welz_1995_genome_programming.html**: Clean, modern HTML version of the article with improved formatting and styling
2. **beta_galactosidase_flowchart.png**: High-resolution image of the original flowchart showing the lac operon regulation
3. **welz.genome0.shtml**: Original archived HTML from the Wayback Machine (March 10, 1997)

### Data Fields

The HTML files contain the following key sections:
- Introduction to the genome-as-program metaphor
- Historical context of the 1995 online discussion
- Beta-galactosidase flowchart and explanation
- The challenge for interdisciplinary collaboration
- Scientific context and references

### Data Splits

All files are included in the training split as this is a historical document dataset.

## Dataset Creation

### Curation Rationale

This dataset was created to preserve and make accessible an important piece of scientific history that demonstrates early interdisciplinary thinking between computer science and molecular biology. The work foreshadowed modern approaches in systems biology and computational biology.

### Source Data

#### Initial Data Collection and Normalization

The original article was published in *The X Advisor* in July 1995 and was archived by the Wayback Machine on March 10, 1997. The dataset includes both the original archived version and a modernized version for better readability.

#### Who are the source language producers?

Gary Welz, a New York City-based journalist, consultant, and WWW designer, wrote the original article.

### Annotations

#### Annotation process

No additional annotations were added. The dataset preserves the original content with only formatting improvements for the modern HTML version.

#### Who are the annotators?

No annotators were involved in this dataset creation.

### Personal and Sensitive Information

The dataset contains no personal or sensitive information beyond the author's professional contact information, which was publicly available in the original publication.

## Additional Information

### Dataset Curators

[Add curator information]

### Licensing Information

The original article is © 1995-96 Gary Welz, All Rights Reserved. Used With Permission.

### Citation Information

When using this dataset, please cite:

```
Welz, G. (1995). Is a Genome Like a Computer Program? The X Advisor, 1(2), July 1995.
```

### Contributions

[Add contribution information]

---

*This dataset preserves an important piece of scientific history and demonstrates how early interdisciplinary thinking can lead to significant advances in multiple fields.*
