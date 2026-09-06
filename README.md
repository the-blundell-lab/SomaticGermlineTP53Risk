# README

Packages and versions:

matplotlib 3.8.2
pandas 2.6.3
numpy 1.26.2
networkx 3.4.2
statsmodels 0.14.0
lifelines 0.28.0

Required software: GERMLINE2 \url{https://github.com/gusevlab/germline2} and qctool. 

The notebooks contain code used for the analysis in MacGregor et al. _Shared inheritance reveals landscape of germline and somatic cancer risk in TP53_ (AJHG, 2026). To reproduce the results exactly, data files containing TP53 variants are required -- UK Biobank forbids the publication of this data on GitHub, so the code here cannot be run as is. The full UKB data needed to run this code will be made available to registered researchers via the UKB returns system in due course. 

Notebooks:

### 1. Haplotype calling with GERMLINE2 (requires UKB data)

Identification of IBD segments using GERMLINE2 and classifying UKB TP53 variants

### 2. TP53 variant distribution and analysis

Generates Figures 1 and 2 from the manuscript (except Fig. 1e)

### 3. Random haplotypes

Analysis of uncertainty in IBD calling by identifying the rate of haplotype sharing among randomly chosen individuals. 

### 4. Logistic regression analysis

Investigates the relationship between TP53 carrier status and a range of covariates (Fig. 1e)

### 5. Survival analysis

Investigates the relationship between TP53 carrier status and cancer-free survival using a Cox proportional hazards model (Fig. 3)
